# Architecture

## 1. Three layers, never conflate them

| Layer | What it owns | What it does not own |
|---|---|---|
| Model / Provider | endpoint, model ID, real context/output limits, modality, billing | sessions, tools, system prompts |
| Agent framework | session, system prompt, tool loop, permissions, reasoning display | model weights or provider quota |
| Bridge | protocol, auth injection, session lifecycle, file/image conversion, SSE, usage, cleanup | agent policy, tool execution, model substitution |

A bridge is infrastructure, not a third agent. If the Source only exposes its model through an agent session, the bridge is necessarily an **agent-to-agent** adapter and inherits the Source agent's system prompt, tools, and reasoning behavior. Say so explicitly in the delivery notes.

Source classification (S1–S4) and role duality are detailed in `source-modes.md`; one-click/persistence is detailed in `one-click.md`.

## 2. Five patterns

### P0 — Direct provider (no bridge)

Use when the Target supports the provider's native protocol and you hold a legitimate key.

```
Target ──native API──> Provider
```

Lowest latency, fewest failure domains, no extra process. Always check this first; a bridge is justified only by a capability the Target cannot reach directly.

### P1 — Credential-injecting reverse proxy

Use when the Source has a standard API but the Target cannot send the required auth/signature, or you want one local endpoint for several Targets.

```
Target ──OpenAI Chat──> Bridge ──signed/native request──> Provider
```

The bridge owns secrets, signing, retries, and error translation. It must not change the model or prompt. If signing requires a device/owner identity that you cannot legitimately obtain, stop; do not brute-force the scheme.

### P2 — Agent-session bridge

Use when the model is only usable inside the Source agent (free tier, local session API, proprietary routing).

```
Target ──OpenAI Chat──> Bridge ──session API──> Source Agent ──> Provider
```

The bridge creates a Source session, submits the prompt and attachments, polls or streams messages, extracts the final assistant text, and deletes the session. This is the highest-fidelity way to reuse a logged-in agent, and the highest-complexity one: you inherit the Source agent's system prompt, tool policy, context overhead, and reasoning/tool intermediate states.

### P3 — Protocol translation

Use when Target and Source speak different protocols (Responses↔Chat, Anthropic↔Chat, Gemini↔Chat).

Translate only the subset in use. Do not claim full compatibility. Tool schemas and reasoning blocks are the usual lossy points.

### P4 — Capture/replay (diagnostic only)

A temporary relay that records one real request to learn headers or payload shape. It is not a product: tokens are sensitive, signatures may be bound to host/time, and replay usually fails. Require explicit operator authorization, keep captures in memory, redact, and delete configuration afterwards.

## 3. Reference data flow (P2)

```text
Target Agent
  │  POST /v1/chat/completions  (model, messages, stream)
  ▼
Bridge
  │  1. validate local caller, normalize messages
  │  2. map model ID and capabilities
  │  3. create/reuse Source session (agent, model, variant)
  │  4. submit prompt + files
  │  5. poll messages or consume stream
  │  6. select final assistant text (not reasoning/tool intermediates)
  │  7. normalize usage
  │  8. delete session / expire files
  ▼
Source Agent ──> Provider
  │
  └── messages/usage ──> Bridge ──> Target (JSON or synthesized SSE)
```

The downstream contract is stateless HTTP; the upstream is stateful. The bridge absorbs that mismatch. Every retry can create a new upstream session, so cleanup and idempotency matter.

## 4. Adapter contract

### 4.1 Minimum endpoints

| Method | Path | Purpose |
|---|---|---|
| GET | `/v1/models` | list exactly the model IDs the bridge can serve |
| POST | `/v1/chat/completions` | text, optional image, optional stream |
| GET | `/health` | process liveness for the start script and operator |
| GET | `/ready` | upstream auth/model readiness, without a generation call |

Optional: `/v1/models/{id}`, `/metrics`, `/version`. Do not implement endpoints you cannot honor.

### 4.2 Request normalization

- Accept both string content and OpenAI content-part arrays.
- Keep `system`/`developer` messages only if the upstream supports them; otherwise fold them into the prompt deliberately and document the change.
- For image requests, prefer the latest user message plus the last image-bearing user message. Sending the entire history to an agent upstream multiplies system/tool overhead and can trigger tool loops.
- For agent-session upstreams, apply the direct-answer/no-tools instruction to text and image requests; the bridge does not forward the Source's tool calls to the Target.
- Preserve `max_tokens`, `temperature`, `top_p`, `stop` only when the upstream supports them. Do not silently drop a parameter the caller depends on; log it as unsupported.
- Reject unknown model IDs with `404` rather than silently substituting a default.

### 4.3 Response and streaming

- Non-stream response: `choices[0].message.content`, `finish_reason`, `usage`.
- Stream response: valid SSE frames, a role delta first, content deltas, a final `finish_reason`, usage on the final chunk, then `data: [DONE]`.
- If the upstream is non-streaming, synthesize SSE. Never emit raw upstream events that the Target cannot parse.
- If the upstream streams, relay but normalize event names and ensure usage is present.
- Agent-session upstream: wait for an assistant message with `finish=stop` and a non-empty text part; never return text from a `tool-calls` message.
- Do not synthesize content from reasoning. Default to `502 reasoning_only` / `tool_calls_only` when no final text exists; only a clearly labeled, opt-in fallback may return cleaned reasoning.
- Keep the downstream assistant message to `role` + `content`; do not add `reasoning_content` unless the Target explicitly supports it.
- On client disconnect, abort the upstream request and clean up the session/files.

### 4.4 Error mapping

| Upstream condition | Downstream status | Body |
|---|---|---|
| invalid local caller | 401 | `invalid_api_key` |
| upstream auth/token expired | 401 | `upstream_auth_failed` + redacted detail |
| free tier / policy / region | 403 | `upstream_forbidden` |
| unknown model | 404 | `model_not_found` |
| context overflow | 400 | `context_length_exceeded` |
| rate limit/quota | 429 | `rate_limited` |
| upstream timeout | 504 | `upstream_timeout` |
| upstream 5xx / malformed | 502 | `upstream_error` |
| final turn has tool calls but no final text | 502 | `tool_calls_only` |
| only reasoning, no final text | 502 | `reasoning_only` |
| empty final text | 502 | `empty_response` |

Never turn an upstream failure into `200 OK` with a fake assistant message. A stub that returns `pong` is worse than an error because it poisons validation.

### 4.5 Session lifecycle

- One session per request by default: simple, isolated, easy to delete.
- Reuse only with an explicit key and a bounded cache; concurrent requests must not share a session unless the upstream supports it.
- Always delete in `finally`, including on timeout and client abort. Keep sessions on failure only when a debug flag is set, and say so.
- Log session ID, not prompt text.

### 4.6 Images and files

OpenAI image parts arrive as `image_url.url`:

- `data:` URL → decode, validate MIME and size, write to a private temp directory with a random name.
- `http(s):` URL → fetch with a size limit and an allowlist/deny-private-address policy if the bridge is exposed beyond localhost.
- `file:` URL → only allow a configured directory; never accept arbitrary local paths from a remote caller.

Then convert to what the Source expects (path, `file://` URI, upload ID). Tell the model the images are attached in the prompt. Some agent upstreams will still try to read files or verify; an explicit instruction to answer directly from the rendered images is part of the bridge contract, not a hack.

Cleanup: TTL (e.g., 1 hour) plus a periodic sweep; delete on request completion when the upstream no longer needs the file. Never log base64 or full local paths.

### 4.7 Usage

Report the real upstream usage when available:

```text
prompt_tokens     = uncached_input + cache_read + cache_write
completion_tokens = output
total_tokens      = prompt_tokens + completion_tokens
```

If the upstream only reports output, mark usage as estimated; do not report zero. Include `prompt_tokens_details.cached_tokens` when known.

### 4.8 Readiness and auth expiry

- `/health` proves only that the process is alive. It must not be used as evidence that the Source credential works.
- `/ready` performs a non-generating upstream check: list models, validate the session, or call the Source’s cheapest authenticated endpoint.
- If the credential/session is expired or revoked, return `401`/`403` with a machine-readable `reauth_required` code and a human-readable next step. Do not return `200` with a stale session, a cached answer, or the Target’s default model.
- The start script should wait for `/ready` when provided; the one-click flow must preflight auth before editing the Target.
- Record the auth source and expiry behavior in the delivery notes. Persistence of the Target config does not imply persistence of the Source credential.

## 5. Trust boundaries

- Bind `127.0.0.1` by default. Binding `0.0.0.0` turns a local credential proxy into a network service.
- The Target's `apiKey` is a local placeholder; the real credential stays in the bridge or Source credential store.
- Optionally require a local bearer token so other local processes cannot use the bridge.
- Credentials: environment variable or ACL-restricted file, never in Git, logs, crash dumps, or error bodies.
- Do not log prompts, images, tokens, or full upstream responses by default. Opt-in debug logs must redact.
- No bypass of anti-debug, DRM, safeStorage, signature checks, or free-tier enforcement. If the only path forward is bypassing a control, the correct deliverable is "not feasible; use a standard provider or request official access."

## 6. Deployment and operations

- One process, one port, one log file, one PID file.
- Start/stop scripts are manual unless the operator explicitly asks for autostart. A hidden background process that survives reboot without the operator knowing is an incident waiting to happen.
- Start script: check Node, check port, refuse to kill an unknown listener, start hidden, wait for `/health`, write PID/metadata.
- Stop script: verify the PID belongs to the bridge before killing; fall back to the listener PID only with explicit force.
- Log rotation or size cap; request IDs and latency; never secrets.
- Version the config and keep a backup before editing a Target profile.

## 7. Failure domains

| Domain | Typical symptom | First check |
|---|---|---|
| Source auth | 401/403 before any model work | token expiry, owner/device binding, signature headers |
| Source agent | tool loops, reasoning-only output, first text part is a plan, long latency | agent choice, prompt, session messages, `finish` |
| Bridge normalization | Target parses nothing / empty content | SSE framing, content-part shape, final message selection |
| Target config | model not in picker, request goes to default | live profile path, provider row merge semantics, restart |
| Network/runtime | connection refused, port conflict | listener PID, firewall, IPv6 vs IPv4 |
| Context | 400 overflow or truncated history | real limits, system/tool overhead, cache tokens |

## 8. Anti-patterns

- Returning reasoning text as `content`.
- Returning the first text part from a `tool-calls` message as if it were the final answer.
- Falling back to reasoning by default, or without a marker in logs/delivery notes.
- Treating a reasoning-token count as proof that the bridge returned reasoning.
- Reusing one Source session for all requests.
- Hardcoding `contextWindow` to the provider maximum while the Source agent injects tens of thousands of tokens.
- Editing the Target's default-model row when the requirement is "add a provider".
- Writing the bridge config into a profile the running app does not read.
- Hardcoding drive letters, usernames, install directories, ports, or process names instead of discovering them.
- Treating a `200` with `pong` as end-to-end success.
- Treating `/health` as proof that upstream auth works.
- Keeping image temp files forever.
- Brute-forcing a signature scheme or replaying a captured signature.
- Calling a free-tier workaround "reverse engineering success" when the provider explicitly forbids it.
