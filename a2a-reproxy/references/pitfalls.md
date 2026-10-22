# Pitfalls

Each entry: symptom → root cause → action. Keep the evidence; "it worked once" is not evidence.

## Source classification and roles

| Symptom | Root cause | Action |
|---|---|---|
| Extracted URL/model is treated as a usable API | S4 static evidence, no legitimate credential | classify as S4; deliver evidence only; do not claim a working proxy |
| Built a bridge for a direct API + key | S1 was misclassified as S2/S3 | prefer direct Target config; use a bridge only for a real protocol/auth need |
| Agent-session result contains tools/reasoning overhead | S2b is an embedded agent, not a pure model | accept and document the semantics; select a general agent; set context headroom |
| Same app behaves inconsistently as Source and Target | role confusion | classify the role first; Source runs its own agent loop, Target also runs its own loop; do not copy one role's config/behavior to the other |
| Signed relay treated as a normal provider | S3 requires owner/device-bound signing | stop without official credential/contract; do not brute-force |
| Free-tier model fails outside the Source client | policy binds access to the client/agent | use the supported path or a standard provider; do not impersonate the client |
| Internal local port returns 401 and is assumed to be the only route | vendor may expose an official CLI/Agent SDK with PAT/service-account auth | check official docs first; use the SDK/CLI instead of extracting tokens |

## Discovery and analysis

| Symptom | Root cause | Action |
|---|---|---|
| GitHub clone fails with `invalid index-pack` | large pack, flaky transfer | download the archive (`codeload.../tar.gz`) and inspect docs/source directly |
| asar header parse returns garbage | wrong offset (header starts after the 16-byte pickle prefix) | parse `headerSize`/`jsonLen` correctly; data starts at `8 + headerSize` |
| strings show endpoints but requests fail | static strings do not reveal signing, owner binding, or feature flags | combine static evidence with a live request and upstream error codes |
| anti-debug blocks inspection | protected app | do not bypass; use documented surfaces, official keys, or another route |

## Auth, signatures, credentials

| Symptom | Root cause | Action |
|---|---|---|
| `401 invalid token` / `missing super agent security headers` | URL + bearer alone is insufficient; per-request signing is required | identify the official signing contract or stop |
| `40301 client version too low` | app version header is checked | use the official client or obtain sanctioned access; do not spoof blindly |
| `40104 unsupported sign version / invalid signature` | wrong sign version, key, canonical string, or binding | verify `v1`, HMAC-SHA256 hex, seconds timestamp, key source; do not brute-force permutations |
| `40103 time sync` | clock skew or wrong unit (ms vs s) | sync the clock; use seconds |
| `40105 risk control` | device/install/host/context binding | assume the signature is bound; do not attempt evasion |
| web token works for web, not for desktop relay | different credential scopes | use the desktop owner token legitimately, or a standard provider |
| token expires after restart | short-lived session token | obtain refreshable official credentials; document the limitation |
| `safeStorage` decrypt fails | OS user/machine binding | do not extract; use the app itself or official access |

**Rule:** signatures are not puzzles to brute-force. If the scheme is not documented and the owner token is protected, the route is not viable.

## Free tier and policy

| Symptom | Root cause | Action |
|---|---|---|
| `403 FreeTierError` on direct cloud calls | free model is restricted to the Source client | use the Source's local session API, or a paid/standard provider; do not evade the restriction |
| `402 Insufficient account funds` | paid model, no balance | choose a free/standard model or fund the account |
| custom no-tool agent gets `FreeTierError` | free tier is tied to specific built-in agents/routes | use the supported built-in agent; don't fake the client |
| `503` from a custom agent | agent/provider mismatch or upstream unavailable | fall back to a supported agent; inspect the Source log |

Policy limits are requirements, not obstacles. A bridge that only works by impersonating a client is out of scope.

## Agent vs model semantics

| Symptom | Root cause | Action |
|---|---|---|
| 1+ minute responses, huge token counts | Source agent runs tools/verification loops | choose a general agent; instruct "answer directly, no tools, no verification" |
| `finish_reason: tool_calls` | turn ended in an intermediate tool state | continue the agent loop or select a non-tool agent; do not treat as final |
| reasoning text appears in the Target | bridge returned reasoning as content | select final assistant text; clean reasoning only as a labeled fallback |
| empty `content`, non-empty reasoning | model produced only reasoning | return an explicit error or a cleaned fallback; never silently empty |
| image request triggers file reads | agent tries to inspect the attachment path | attach rendered images, state they are visible, and choose a no-tool agent |
| history makes every call expensive | entire conversation replayed into an agent with a large system prompt | send the latest user turn for image tasks; trim history deliberately |
| first text part is a plan | bridge accepted any text before `finish=stop` | wait for a `finish=stop` text message; ignore `tool-calls` text |
| reasoning tokens > 0 but no reasoning in output | token count is not a channel | inspect content parts and `fallback`; do not infer leakage from tokens |
| `reasoning_only` / `tool_calls_only` 502 | strict final-text guard | not a bridge bug; retry/rephrase or enable a labeled fallback |

## Images and files

| Symptom | Root cause | Action |
|---|---|---|
| image part ignored | Source expects a file/attachment, not `image_url` | decode data URL, write temp file, pass path/URI in the Source's file field |
| `file://` rejected on Windows | path format/escaping | use the Source's accepted URI/path form; test both |
| temp files accumulate | no TTL | sweep every N minutes, delete on completion, cap total size |
| remote URL fetches internal hosts | SSRF | allowlist or block private/link-local addresses; cap size and redirects |
| base64 appears in logs | debug logging of the full request | redact content parts; log only counts and MIME types |

## Streaming and protocol

| Symptom | Root cause | Action |
|---|---|---|
| Target shows nothing on stream | malformed SSE frames or missing `[DONE]` | emit `data: {...}\n\n` frames, final finish chunk with usage, then `data: [DONE]` |
| usage missing in stream | usage only added to non-stream response | include usage in the final chunk (some clients require `stream_options.include_usage`) |
| client hangs after answer | stream not closed | close the response after `[DONE]`; abort upstream on client disconnect |
| doubled `/v1` | Target appends `/v1` to a base that already has it | test both base forms; expose one canonical path |
| tools silently broken | Chat↔Responses/Anthropic translation drops tool schemas | translate tools explicitly or declare unsupported |

## Usage and context

| Symptom | Root cause | Action |
|---|---|---|
| 271 tokens for a 19K request | cache-read tokens omitted | `prompt = input + cache_read + cache_write` |
| context overflow at 200K | agent system/tools + history exceed the real budget | leave headroom (e.g., 180K), trim history, measure |
| output truncated | `maxTokens` above the upstream cap | match the provider cap; surface `finish_reason: length` |
| usage 0 / missing | upstream non-stream response without usage | estimate and label it, or read usage from the Source API/log |

## Target configuration

| Symptom | Root cause | Action |
|---|---|---|
| new provider not in the picker | wrong profile, missing model row, missing header/key placeholder, no restart | confirm the live profile path; add a model row; restart; check Target logs |
| edit "did nothing" | desktop/web/CLI profiles differ | find the profile the running process reads (argv, logs, install dir) |
| default model changed unexpectedly | `agent-default-model` or equivalent was edited | remove the override; keep the original default row |
| existing providers disappeared | patch row replaced the whole `config` instead of merging | restore from backup; add only the new provider key |
| model name shown is the display name | UI displays `name`, not `id` | verify the actual model ID in the request/log/usage |
| Target still uses its default model | model not selected in UI, or request explicitly uses default | select the bridge model; check the model ID in bridge logs |
| config works until reboot | process-local env/temp config | persist the provider in the official profile, not just an env var |

## Runtime and operations

| Symptom | Root cause | Action |
|---|---|---|
| `EADDRINUSE` | old adapter still listening | find the listener PID (`Get-NetTCPConnection -LocalPort 8787`), stop it, then restart |
| `taskkill /PID` behaves oddly in Git Bash | MSYS path conversion | use PowerShell `Stop-Process -Id <pid>` or `taskkill //PID` |
| bridge dies when the terminal closes | started as a child of the shell | start hidden via `Start-Process`, write PID/log, or use a service if the operator asks |
| can't stop the bridge | stale PID file | verify the listener's command line; kill only the matching process |
| health check passes but chat fails | liveness only checks the process | add a minimal upstream/model check to `/health` or run the probe |
| port reachable from other machines | bound `0.0.0.0` | bind `127.0.0.1`; use a local token if other local users are untrusted |

## Validation and false success

| Symptom | Root cause | Action |
|---|---|---|
| bridge returns `pong` instantly | stub/hardcoded response | inspect the code path and upstream usage; delete the stub |
| Target says "completed" but no model call | UI state, not model evidence | check bridge log, upstream usage, and model ID |
| one successful text test, image fails | capability not implemented | test each modality separately; mark unsupported until proven |
| numbers look plausible but wrong | usage estimated or cached | compare with upstream usage; check cache fields |
| "it works on my machine" | profile/env drift | record versions, paths, ports, and the exact model ID |

## One-click, persistence, Windows

| Symptom | Root cause | Action |
|---|---|---|
| Script works on one machine only | hardcoded drive/user/install path/port/process name | discover via process/args/logs/config roots; accept parameters; keep defaults overridable |
| Second run duplicates provider/model or overwrites edits | no idempotency contract | stable provider ID; same values → no-op; different values → explicit update; read back |
| Config disappears after restart | wrote to a temp/env-only location | write to the official profile; restart the Target and verify |
| `/health` is 200 but chat returns 401 | liveness is not auth readiness | add `/ready` that checks upstream auth/models without generation |
| Bridge works until the token expires | no expiry preflight/reauth path | return `401/403 reauth_required`; document rotation; do not silently fall back |
| API key ends up in a config/log/screenshot | secret stored as plain text | user env var/credential store; config stores the variable name; redact logs |
| Autostart appears after a “one-click” install | script installed a service/scheduled task | keep startup manual unless explicitly requested |
| `Start-Process` fails on a path with spaces | argument list not quoted | quote the script/exe path; test with a space-containing path |
| Git Bash rewrites `/ready` into a Windows path | MSYS path conversion before PowerShell sees it | invoke PowerShell directly, or pass `ready` (no leading slash); do not debug the bridge for this |
| PowerShell blocks the `.ps1` | execution policy | invoke with `-ExecutionPolicy Bypass -File` for that run; do not change machine policy by default |
| Python helper fails with GBK decoding | default Windows code page | set `PYTHONUTF8=1` for that process; keep files UTF-8 |
| `taskkill /PID` behaves oddly in Git Bash | MSYS path conversion | use PowerShell `Stop-Process -Id` or `taskkill //PID` |
| Port check fails on an older Windows | `Get-NetTCPConnection` unavailable | fall back to `netstat -ano` parsing or document the requirement |

## Security and hygiene

- Never commit tokens, `service.json`, `auth.json`, owner-token files, or captured headers.
- Temporary debug relays: in-memory capture, explicit authorization, delete config afterwards, restore normal startup.
- Do not weaken anti-debug, signature verification, safeStorage, or free-tier checks.
- If a requested step requires bypassing a control, stop and report the boundary instead of engineering around it.
- Redact logs; do not paste secrets into issues, chat, or the skill itself.
