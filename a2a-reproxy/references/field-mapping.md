# Field Mapping

File names, paths, and ports below are **examples of target formats**, not hardcoded contracts. Discover the live profile with `source-modes.md` / `scripts/discover-app.ps1`, then map fields for that version.

## 1. Procedure

1. **Classify the Source** with `source-modes.md` (S1/S2a/S2b/S3/S4). Do not map fields until the mode is known: S1 maps provider→provider; S2b maps a session request/response, not provider fields; S3 may have no public mappable contract; S4 has only evidence.
2. **Inventory the Source**: endpoint, auth type, model ID, real limits, modality, whether it is a pure API or an agent session.
3. **Inventory the Target**: config file and live profile path, provider schema, protocol, header support, merge semantics, restart requirement.
4. **Write the contract** before editing: model ID, base URL seen by Target, base URL seen by Bridge, auth owner, image path, stream behavior, usage source, session cleanup.
5. **Map one field at a time**; validate after each change.
6. **Keep the Target's existing providers and default model untouched** unless the operator explicitly asks to switch defaults.

## 2. Target configuration shapes

These are common shapes, not a guarantee for every version. Verify against the installed version's schema or UI before writing.

### DeepSeek Harness (DSH) — `cordis.patch.yml`

```yaml
- id: llm-pi-ai
  config:
    providers:
      local-bridge:
        displayName: Local Bridge
        api: openai-completions
        baseURL: http://127.0.0.1:8787/v1
        headers:
          Authorization: Bearer local-placeholder
        defaultContextWindow: 180000
        defaultMaxTokens: 32000
        models:
          - id: exact-upstream-model-id
            name: Display Name
            contextWindow: 180000
            maxTokens: 32000
            input: [ text, image ]
            reasoningEfforts:
              low: low
              high: high
```

Rules:

- The patch row replaces the `config` of the targeted `id`; preserve existing rows/providers.
- Do not add or edit `agent-default-model` for an add-only request. That row changes the default model.
- The live desktop profile may be under the install directory, not the user home. Confirm with the running process or its logs.
- A provider often will not appear until it has a model row and any required header/key placeholder; restart the Target after editing.

### OpenCode — `opencode.json`

```json
{
  "$schema": "https://opencode.ai/config.json",
  "provider": {
    "local-bridge": {
      "npm": "@ai-sdk/openai-compatible",
      "name": "Local Bridge",
      "options": {
        "baseURL": "http://127.0.0.1:8787/v1",
        "apiKey": "local-placeholder"
      },
      "models": {
        "exact-upstream-model-id": { "name": "Display Name" }
      }
    }
  }
}
```

Keep existing provider keys. Some versions expect the API key in `options.apiKey`, others via env; confirm the schema.

### Codex — `~/.codex/config.toml`

```toml
[model_providers.local_bridge]
name = "Local Bridge"
base_url = "http://127.0.0.1:8787/v1"
env_key = "LOCAL_BRIDGE_API_KEY"
wire_api = "chat"

[profiles.bridge]
model = "exact-upstream-model-id"
model_provider = "local_bridge"
```

If the installed Codex prefers the Responses API, either use `wire_api = "responses"` with a Responses-capable bridge or translate Chat↔Responses. Verify; do not assume both wires are interchangeable.

### GUI targets (Trae, Qoder, Kimi Code, Pi, etc.)

Most expose "custom / OpenAI-compatible provider": base URL, API key, model ID. The usual failure is a doubled or missing `/v1`. Test:

```text
http://127.0.0.1:8787/v1   + /chat/completions  → /v1/chat/completions
http://127.0.0.1:8787     + /v1/chat/completions
```

Pick the form the UI expects; expose both only if the bridge routes them explicitly.

## 3. Worked case: OpenCode free model → DSH

### Source

- OpenCode local service on `127.0.0.1:45278`, Basic auth from the local service descriptor.
- Built-in `general` agent.
- Upstream model: `deepseek-v4.1-flash-free` (free tier usable through the OpenCode client, not as a direct cloud API key).
- Session API: create session → submit prompt (optional `files`) → poll messages.

### Bridge

- `127.0.0.1:8787/v1`, OpenAI Chat Completions + SSE + `/health`.
- One OpenCode session per request; delete afterwards.
- Image parts → temp files → `files[].uri`; latest user message only for image requests.
- Bridge instruction: answer directly from attached images, do not read files, call tools, or verify.
- Final assistant text preferred; reasoning used only as a cleaned fallback.
- Usage includes cache read/write.

### Target (verified add-only shape)

```yaml
- id: llm-pi-ai
  config:
    providers:
      opencode-local:
        displayName: OpenCode Local
        api: openai-completions
        baseURL: http://127.0.0.1:8787/v1
        headers:
          Authorization: Bearer local-adapter
        defaultContextWindow: 180000
        defaultMaxTokens: 32000
        models:
          - id: deepseek-v4.1-flash-free
            name: DeepSeek V4.1 Flash Free
            contextWindow: 180000
            maxTokens: 32000
            input: [ text, image ]
            reasoningEfforts:
              low: low
              high: high
              max: max
```

No `agent-default-model` row. The Target's original DeepSeek default remains. The new provider appears alongside it.

### Why these values

- `180000`, not the model's theoretical 200K: the Source agent injects a large system/tool prompt; the Target's budget must leave headroom.
- `32000` output: match the upstream cap; a larger value can produce upstream errors or silent truncation.
- `input: [text, image]`: only claim image support after a real image test through the bridge.
- `reasoningEfforts`: only variants the upstream actually accepts. A Target field that names a variant the Source ignores is a lie, not a feature.
- **Observed result**: a small prompt reported ~19.3K prompt tokens because cache-read and agent context were included; before the usage fix it showed 271. This is expected for an agent-session bridge, and is the main reason not to set the context budget to the raw model maximum.

## 4. Case: TeleAgent default relay (S3/S4 — signed, not portable as-is)

### Observed shape

- Base: `https://agent.teleai.com.cn/superCowork/sapi/api/v1`
- Protocol: OpenAI Chat Completions; default model `chat-pro`, background tasks `chat-lite`.
- The app uses `useSuperAgentAuth` and signs each request.
- Headers observed: `X-Token`, `X-App-Version`, `X-SuperAgent-Nonce`, `X-SuperAgent-Timestamp`, `X-SuperAgent-Device-Id`, `X-SuperAgent-Install-Id`, `X-SuperAgent-Signature`, `X-SuperAgent-Sign-Version: v1`, `X-Route-Target: ops-gateway`.
- Signing: HMAC-SHA256, lowercase hex; key derived from the JWT's third segment; timestamp in seconds.
- Owner token lives in the app's `app-auth/token.json`, protected by Electron safeStorage. A web-login `operationToken` can authenticate web calls but does not reproduce the desktop signature.

### What failed, and why it matters

Static reconstruction of the canonical string (version + token + install ID + timestamp + nonce, in various orders) did not pass the live relay. Capturing one real desktop request and replaying/transforming its signature also failed, which points to host/context binding (method, path, body hash, device identity, or a server-side session). Error codes seen: missing security headers, invalid token, client version too low, unsupported sign version/invalid signature, time sync, risk control.

**Conclusion:** do not productize this path without a legitimate owner token and an official signing contract. Combinatorial guessing is not a strategy. Use a standard provider the app already configures (for example an OpenAI-compatible SiliconFlow endpoint with a real key) or request official API access. This case is **S3/S4**, not S1: the extracted URL and model IDs are evidence, not a usable credential.

### General lesson

If a relay needs a per-request signature, first answer:

1. Is there an official API key or documented signing scheme?
2. Is the signature bound to a device, install, host, path, or body hash?
3. Can the owner token be obtained legitimately, and does it survive restart?

If any answer is "unknown" and there is no official path, stop and choose another route.

## 5. Context and usage math

```text
prompt_tokens = uncached_input + cache_read + cache_write
context_used ≈ system_prompt + tool_schemas + history + images + current_turn
```

- `contextWindow` is a **budget**, not a deployment limit; it cannot exceed the real provider limit.
- `maxTokens` is an **output** cap, not context.
- Agent-session bridges add hidden overhead. A 200K model may have only ~180K usable through the Source agent.
- If the Target reports 271 tokens for a 19K-token request, cache-read tokens are missing, not the context.
- Long histories should be trimmed by the Target or the bridge deliberately; do not rely on the upstream to silently truncate.

## 6. Reasoning and channels

- **content**: the final answer; this is what an OpenAI-compatible Target should display.
- **reasoning**: internal deliberation; may be exposed by the Source as a separate field/part.
- **tool calls**: intermediate actions; `finish_reason: tool_calls` means the turn is not final.

Mapping rules:

- Never concatenate reasoning into `content`.
- Prefer the final assistant message; if only reasoning exists, return an explicit error or a clearly labeled fallback, not a silent guess.
- If the Source agent tends to call tools, choose a general/no-tool agent and state "answer directly" in the prompt. Do not disable security controls; choose the supported agent mode.
- `reasoningEfforts` maps only to real upstream variants. If the Source ignores variants, omit the mapping.
- A Target may render reasoning differently from the Source; that is a UI/framework difference, not evidence that the bridge is broken.

## 7. Capability matrix (fill per case)

| Capability | Source | Bridge | Target | Verified |
|---|---|---|---|---|
| text | yes | yes | yes | yes/no |
| streaming | yes/no | relay/synthesize | yes/no | yes/no |
| image input | yes/no | convert | yes/no | yes/no |
| tools | yes/no | pass/deny | yes/no | yes/no |
| reasoning variants | list | map/ignore | list | yes/no |
| usage | exact/estimated | normalize | display | yes/no |
| session reuse | yes/no | per-request/cache | n/a | yes/no |

Unverified cells are limitations, not features.
