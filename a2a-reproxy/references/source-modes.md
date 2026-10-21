# Source Modes and Roles

## 1. Why classify first

The same request URL can mean very different things:

- A public provider endpoint with a key you own.
- A local service that only accepts its own logged-in client.
- A signed relay bound to an owner/device/install.
- A static URL extracted from an app, with no usable credential at all.

The route, the deliverable, and the stop condition all depend on which one it is. Do not choose “build a bridge” just because the URL looks OpenAI-compatible.

## 2. S1 — Standard API + key

**Evidence**

- Official docs/console describe the endpoint and auth.
- A key is issued to you (or your organization) and is not tied to a specific desktop install.
- A neutral client can call `/models` and a minimal chat completion.

**Route**

- Target supports the protocol → direct provider config. No bridge.
- Target speaks a different protocol → protocol bridge only.
- You need one local endpoint for several targets or auth injection → thin proxy; keep it stateless.

**Do not**

- Add a session/orchestration layer “just in case”.
- Copy a key into a target config file, logs, or screenshots.
- Assume a model ID from a UI label is the API ID.

**Deliverable**

Target’s add-only provider/model config, a probe record, and a note on limits/billing. No bridge required.

## 3. S2a — Local standard API

**Evidence**

- Source exposes a local HTTP API (OpenAI-compatible or similar).
- The main differences are auth, base path, or model naming, not agent semantics.

**Route**

Thin bridge: inject auth, rewrite paths/model IDs, normalize errors/usage. Prefer passing streaming through rather than reimplementing it.

**Risks**

- Local API may be undocumented and version-specific.
- Auth may be a cookie/session rather than a stable key.
- The service may bind only to `127.0.0.1` and start with the app.

## 4. S2b — Agent session / login

**Evidence**

- The model is usable inside the Source app but not with a standalone key.
- Direct cloud calls return `FreeTierError`, `403`, or a client/version error.
- A local session API exists (create session, submit prompt, read messages).

**What the bridge inherits**

The Source agent’s system prompt, tool policy, context overhead, free-tier restrictions, and reasoning/tool intermediate states. The bridge is an embedded client of that agent, not a pure model proxy.

**Route**

1. Validate the Source is logged in and the model works in its own UI.
2. Create one Source session per request.
3. Submit the prompt and any attachments in the Source’s format.
4. Poll or stream messages until a final assistant message.
5. Prefer final `content`; do not return reasoning or tool intermediates as the answer.
6. Normalize usage, including cache read/write.
7. Delete the session and expire attachments in `finally`.

**Image requests**

- Convert OpenAI `image_url` parts to the Source’s file/attachment format.
- Prefer the latest user message (plus the last image-bearing user message) rather than replaying the whole history into an agent.
- State that the images are attached and visible; tell the agent to answer directly and not to read files or call tools.
- Verify with an image containing known text.

**Free tier**

Free access may be tied to specific built-in agents/clients. Do not impersonate a client or bypass the restriction. If the supported path is not usable for a persistent bridge, report that and stop.

**Context**

The Source agent can add tens of thousands of tokens of system/tool prompt. Set the Target budget below the raw model maximum and measure the real usage.

**Deliverable**

A stateful bridge with session lifecycle, plus explicit limitations: agent choice, tools, reasoning, free-tier policy, context overhead, latency.

## 5. S3 — Signed / private relay

**Evidence**

- URL + bearer token fails with missing-security-header, invalid-signature, client-version, time-sync, or risk-control errors.
- The app signs each request (nonce/timestamp/device/install/signature headers).
- The owner token lives in protected storage (OS keychain, Electron safeStorage, etc.).

**What is required to productize**

1. A legitimate owner credential that survives restart.
2. A documented or officially supported canonical string, including method/path/body binding.
3. Knowledge of replay window, clock unit, device/install binding, and host/URL binding.
4. Permission to build the integration.

If any of these is missing, the route is not viable. A captured signature is not a reusable credential.

**Do not**

- Brute-force field orders, key encodings, or token shapes.
- Replay a captured signature and call it a bridge.
- Bypass anti-debug, safeStorage, integrity checks, or risk control.
- Extract protected tokens without explicit authorization.

**Deliverable when blocked**

A clear feasibility report with error evidence and the recommended alternative (standard provider, official API, vendor request). That is a successful outcome, not a failure to “try harder”.

## 6. S4 — Static extraction only

**Evidence**

- You found a base URL, model IDs, header names, or feature flags in an asar/config/log.
- You do not have a usable credential or session.

**What it proves**

Architecture and intent: where the app sends requests, which models exist, which auth scheme it expects.

**What it does not prove**

That you can legally or technically call the endpoint. A model ID is not authorization. A header name is not a signature.

**Deliverable**

An evidence note: endpoint, model IDs, auth requirements, observed errors, open questions. Do not label it “working reverse proxy”.

## 7. Role duality

### Source role

- The app’s own agent loop runs: system prompt, tools, permissions, session, free-tier policy.
- The bridge sees agent semantics, not just a model.
- The Source’s agent selection and prompt are part of the bridge contract.

### Target role

- The app’s own agent loop still runs: its tools, permissions, UI, reasoning display.
- The bridge only supplies a model endpoint; it must not replicate or override the Target’s agent behavior.
- The Target’s default model must remain untouched for an add-only request.

### Same program, different behavior

| Program (example) | As Source | As Target |
|---|---|---|
| OpenCode | Local session/agent; free tier may be client-bound; model is reached through its loop | Provider config; its own loop/tools continue; model requests go to the bridge |
| DSH | If the version exposes a local session/API, it exposes its profile/agent loop | Add a provider in its profile; its own loop/UI continue |
| TeleAgent | Signed relay/owner token; default model is not a public API | Only if the version supports a custom OpenAI provider |
| Codex | Only if the version exposes a local session/API | `config.toml` provider/profile; its own loop continues |

Rules:

- Do not take the Source agent’s prompt/tool policy and inject it into the Target; the Target already has its own.
- Only add the minimum bridge instruction needed for the Source’s attachment/tool behavior.
- Confirm capabilities per version; “can be a Target” does not imply “can be a Source”.

## 8. Windows discovery (no hardcoded paths)

**Process and command line**

```powershell
$p = Get-CimInstance Win32_Process |
  Where-Object { $_.Name -like '*<app>*' -or $_.CommandLine -like '*<app>*' }
$p | Select-Object ProcessId, Name, ExecutablePath, CommandLine
```

**Listening ports**

```powershell
$pids = $p.ProcessId
Get-NetTCPConnection -State Listen |
  Where-Object { $pids -contains $_.OwningProcess } |
  Select-Object LocalAddress, LocalPort, OwningProcess
```

**Config roots**

- `$env:APPDATA`, `$env:LOCALAPPDATA`, `$env:ProgramData`
- `$env:ProgramFiles`, `${env:ProgramFiles(x86)}`
- The executable directory from the process record
- User profile, but bounded depth

Use `scripts/discover-app.ps1` for a read-only first pass; it lists process, ports, and candidate config files without reading contents.

Command lines and logs may contain secrets (tokens, keys, URLs with credentials). Redact before sharing. The discovery script lists paths/metadata only; it does not parse `.env` or token files.

**Target live profile**

- Read process arguments for `--config`, `--profile`, `--user-data-dir`.
- Check the app’s logs for the loaded profile path.
- Search the install/user config roots, then confirm with a live request.
- Do not assume the home-directory profile is the one the desktop app reads.

**Source config**

- Use the official config directory/CLI/UI.
- Do not read or export protected token stores.
- Logs/DB can reveal model IDs and endpoint, but not grant authorization.

## 9. Auth lifecycle and persistence

| Auth type | Persistence | Preflight | Expiry behavior |
|---|---|---|---|
| API key (S1) | User env var/credential store | `GET /models` with the key | `401`; reissue/update env var |
| Local session/cookie (S2) | Source app login | Session/agent check before accepting traffic | `401/403 reauth_required`; user logs in again |
| Owner/device token (S3) | Protected store, device-bound | Official validation | Usually not refreshable by a bridge; do not productize |

Rules:

- Target config stores the **env var name**, not the secret.
- `/ready` checks upstream auth/models without generating content; `/health` only checks the process.
- On expiry, fail clearly and stop; do not silently fall back to a stale session or the Target’s default model.
- Persist target config in the official profile; the bridge process is started manually unless the operator explicitly asks for a service/autostart.

## 10. Decision table

| Mode | Bridge needed? | Auth owner | Persistent? | Stop condition |
|---|---|---|---|---|
| S1 | No (or thin) | API key | Yes, until revoked | Key invalid/revoked |
| S2a | Thin | Local session/API | Yes, while app/session lives | API unstable/undocumented |
| S2b | Agent-session | Source login | Yes, while session valid | Free-tier/client binding cannot be satisfied legitimately |
| S3 | Signed adapter | Owner/device credential | Often no | No official credential/contract |
| S4 | No deliverable | None | No | Always; evidence only |
