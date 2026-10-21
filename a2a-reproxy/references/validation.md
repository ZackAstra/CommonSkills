# Validation

## 1. Evidence hierarchy

Strongest to weakest:

1. **Upstream usage / provider-side record** for the exact request (model ID, tokens, finish reason).
2. **Bridge log** showing model, route, session, upstream status, usage, latency.
3. **Target log / database** showing the selected provider and model ID.
4. **Target UI** showing the model name and answer.
5. **A message that looks right** with no other evidence.

A UI answer alone is not proof: it may come from the default model, a stub, or a cached response. Collect at least levels 1–3 for acceptance.

## 2. Layer matrix

Run top to bottom; do not skip a failing layer.

| # | Layer | Check | Pass criterion |
|---|---|---|---|
| 0 | Source mode | classify S1/S2a/S2b/S3/S4 with evidence | route matches the mode; S3 without official credentials stops; S4 is evidence only |
| 1 | Source app | use the model in the Source's own UI/CLI | it answers, including the intended modality |
| 2 | Source API | `/models`, direct chat/session call | 2xx, correct model, usable content |
| 3 | Bridge liveness | `GET /health` | 200, process is the expected one |
| 4 | Bridge readiness | `GET /ready` | upstream auth/model ready without a generation call |
| 5 | Bridge models | `GET /v1/models` | exact model ID present |
| 6 | Bridge text | probe with a unique token | non-empty content, `finish_reason: stop`, usage |
| 7 | Bridge stream | `stream: true` | valid SSE, deltas, usage, `[DONE]` |
| 8 | Bridge image | attach a known image, ask for its text | correct text from the image |
| 9 | Target select | pick the bridge model, send unique token | bridge log shows the request and model ID |
| 10 | Target text/stream | normal chat | answer + usage; no fallback to default model |
| 11 | Target image | attach image | correct answer; no tool loop |
| 12 | Auth expiry | invalidate/expire the Source credential; call `/ready` and chat | clear `401/403 reauth_required`; no stale/cached/default answer |
| 13 | Persistence | restart Target, bridge, machine | add-only config survives; manual start works; `/ready` passes with valid auth |
| 14 | One-click idempotency | run the install script twice; diff the config | second run is a no-op; no duplicate rows; default unchanged |
| 15 | Regression | default model still works | original provider/default unaffected |

## 3. Commands

Windows: use `curl.exe` (included in modern Windows) or the PowerShell equivalents below. In Git Bash, `/ready` may be rewritten into a Windows path before PowerShell sees it; pass `ready` or invoke PowerShell directly.

### Health, readiness, and models

```bash
curl -sS http://127.0.0.1:8787/health
curl -sS http://127.0.0.1:8787/ready
curl -sS -H "Authorization: Bearer local-placeholder" \
  http://127.0.0.1:8787/v1/models
```

Windows PowerShell equivalents:

```powershell
Invoke-RestMethod -Uri "http://127.0.0.1:8787/health"
Invoke-RestMethod -Uri "http://127.0.0.1:8787/ready"
Invoke-RestMethod -Uri "http://127.0.0.1:8787/v1/models" `
  -Headers @{ Authorization = "Bearer local-placeholder" }
```

### Text

```bash
curl -sS http://127.0.0.1:8787/v1/chat/completions \
  -H "Authorization: Bearer local-placeholder" \
  -H "Content-Type: application/json" \
  -d '{"model":"exact-model-id","messages":[{"role":"user","content":"Reply with exactly: BRIDGE_OK_7319"}],"max_tokens":32}'
```

Accept only if the content contains the unique token and the bridge log shows the same model/request.

### Stream

```bash
curl -N -sS http://127.0.0.1:8787/v1/chat/completions \
  -H "Authorization: Bearer local-placeholder" \
  -H "Content-Type: application/json" \
  -d '{"model":"exact-model-id","stream":true,"messages":[{"role":"user","content":"Count 1 to 3"}],"max_tokens":64}'
```

Check: role delta, content deltas, `finish_reason`, usage on the final chunk, `data: [DONE]`, connection closes.

### Image

```bash
curl -sS http://127.0.0.1:8787/v1/chat/completions \
  -H "Authorization: Bearer local-placeholder" \
  -H "Content-Type: application/json" \
  -d '{"model":"exact-model-id","messages":[{"role":"user","content":[
        {"type":"text","text":"Read the large text in this image. Output only that text."},
        {"type":"image_url","image_url":{"url":"data:image/png;base64,<...>"}}
      ]}],"max_tokens":128}'
```

Use an image with known text. Verify the output matches; "I see an image" is not image understanding.

### Probe script

```bash
node scripts/probe-openai-compatible.mjs \
  --base http://127.0.0.1:8787/v1 \
  --model exact-model-id \
  --prompt "Reply with exactly: BRIDGE_OK_7319" \
  --json
```

```bash
node scripts/probe-openai-compatible.mjs \
  --base http://127.0.0.1:8787/v1 \
  --model exact-model-id \
  --image ./fixture.png \
  --prompt "Read the large text in this image. Output only that text." \
  --stream
```

The probe prints status, latency, content, finish reason, usage, and warnings (reasoning-only, tool-call finish, missing usage, model mismatch). It never prints the key or image data. Exit code `0` means HTTP success with non-empty content; warnings still need human judgment.

## 4. Target-side checks

- **Model picker**: the new provider and model appear; the original default is still listed.
- **Request evidence**: the bridge log records the request immediately after the Target send; the model ID matches.
- **No fallback**: if the Target exposes a fallback flag, it is false. If not, temporarily stop the bridge and confirm the Target errors rather than silently answering from its default.
- **Usage**: compare bridge-reported prompt tokens with the Target display; include cache read.
- **Persistence**: restart the Target and re-check the picker; restart the machine and start the bridge manually.
- **Default regression**: send one message on the original default model.
- **Role check**: state whether the app is acting as Source or Target; confirm the profile/config belongs to that role. For the same app in both roles, do not reuse the other role’s assumptions.

## 5. Source-mode and role checks

| Mode | Minimal acceptance | Stop condition |
|---|---|---|
| S1 | neutral client calls `/models` and a minimal chat with the key | key invalid/revoked |
| S2a | Source local API works directly; thin bridge preserves streaming/usage | undocumented API is unstable or auth is not legitimately reusable |
| S2b | Source UI works; bridge returns final text and deletes the session | free-tier/client binding cannot be satisfied legitimately |
| S3 | official credential + documented signature contract + replay/window test | any of these missing → stop |
| S4 | evidence report only (endpoint/model IDs/auth requirements) | do not deliver a working bridge claim |

## 6. Auth expiry and one-click idempotency

### Auth expiry

- Invalidate or expire the Source credential in a controlled way.
- `GET /ready` must return a clear `401/403` with `reauth_required` and a next step.
- A chat request must fail clearly; it must not return a cached answer, a stale session result, or the Target’s default model.
- Restart the bridge with the expired credential; the failure must be reproducible and diagnosable.
- Restore valid auth; `/ready` and chat must recover without editing the Target config.

### One-click idempotency

- Run the install/configure script twice; the second run is a no-op and the config diff is empty.
- Provider/model count is unchanged on the second run; the default model is unchanged.
- Start the bridge twice; only one listener/process exists.
- Restore the backup; the Target returns to its original state and the original default model works.

## 7. Adversarial review

Answer all of these before declaring success:

1. Could this answer have come from the Target's default model? What evidence rules that out?
2. Could it have come from a stub, cache, or hardcoded string?
3. Did the upstream actually receive the request? Which log/usage proves it?
4. Is the model ID exactly the upstream ID, not a display name?
5. Is the response final `content`, or reasoning/tool intermediate?
6. Does the stream include usage and `[DONE]`?
7. Are cache-read tokens included in usage?
8. Is the context budget below the real model limit after agent overhead?
9. Was the Target's default model or existing provider changed?
10. Is the profile being edited the one the running process reads?
11. Are temp images/sessions/tokens cleaned up?
12. Did any step bypass a security control? If yes, stop.

## 8. Acceptance record template

```text
Date:
Source app/version:
Target app/version:
Bridge version/commit:
Model ID:
Bridge endpoint:
Target profile path:
Auth owner / expiry:
Capabilities verified: text / stream / image / tools / reasoning
Usage observed (prompt/completion/total, cached):
Latency:
Failure cases tested:
Known limitations:
Rollback:
Evidence paths (logs, DB rows, screenshots):
```

## 9. Rollback

1. Stop the bridge.
2. Restore the Target profile from the pre-change backup, or remove only the added provider row.
3. Restart the Target and confirm the original default model.
4. Delete temp images/sessions and the PID file.
5. Keep the logs for the record; redact before sharing.

## 10. Start/stop scripts

```powershell
.\scripts\start-bridge.ps1 -BridgeScript .\bridge.mjs -Port 8787
.\scripts\start-bridge.ps1 -BridgeScript .\bridge.mjs -Port 8787 -ReadyPath ready
.\scripts\start-bridge.ps1 -BridgeScript .\bridge.mjs -Port 8787 -TargetCommand "<target-exe>"
.\scripts\stop-bridge.ps1
.\scripts\stop-bridge.ps1 -Port 8787 -Force
```

Defaults: logs and PID metadata under `%LOCALAPPDATA%\a2a-reproxy`. The scripts never install autostart. `start` refuses to kill an occupied port; `stop` verifies the PID against the recorded script before killing. If execution policy blocks the scripts, invoke them with `powershell -NoProfile -ExecutionPolicy Bypass -File ...` rather than changing the machine policy.
