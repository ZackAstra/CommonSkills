# One-Click Configuration and Persistence

## 1. Definition

“One-click” means one **repeatable, safe** command that takes the discovered environment to a verified working state:

```text
preflight → discover profile → backup → add-only provider/model
→ read-back verify → start bridge → /ready → probe → evidence/rollback
```

It does **not** mean autostart, a system service, or a universal config editor. Default startup remains manual; the script can be placed on the desktop or invoked from a shortcut.

## 2. Division of responsibility

| Layer | Responsibility | Reusable? |
|---|---|---|
| Orchestration | Preflight, backup, idempotency, read-back, start/ready/probe, record | Yes |
| Target adapter | Locate profile, parse format, add provider/model, verify schema | Target-specific |
| Bridge | Protocol/auth/session/images/usage | Per Source mode |
| Runtime | Start/stop, PID, logs, port | Yes |

Do not build a universal YAML/JSON/TOML rewriter. Use the target’s official schema/CLI/UI where possible. If text editing is unavoidable, use a structured parser, back up first, and read back the result.

## 3. Inputs: discover, don't hardcode

- Target profile path and format/version.
- Target restart command or launch method.
- Provider ID, base URL, model ID, capabilities (text/stream/image/tools/reasoning).
- Secret source: user env var name or credential-store entry.
- Bridge script, port, `/health`, `/ready`.
- Backup directory and rollback procedure.

Defaults are defaults, not contracts. The script must accept overrides.

## 4. Flow

1. **Preflight**
   - Node/runtime present.
   - Source auth valid (`/models` or session check); if expired, stop with `reauth_required`.
   - Target not running, or its config can be safely edited (warn if it may overwrite on exit; prefer an offline edit).
   - Port free; existing bridge is the expected one.
2. **Discover**
   - Use `scripts/discover-app.ps1` for a read-only first pass (process, command line, ports, candidate configs).
   - Find the live profile via process args/logs/installation root; confirm with the user if ambiguous.
   - Detect format and schema version.
3. **Backup**
   - Timestamped copy next to the config or in a state directory.
   - Record the path in the output and a manifest.
4. **Apply add-only**
   - Add provider key and model row; preserve all existing keys/rows.
   - Do not touch the default-model row.
   - Store the secret reference (env var name), not the secret.
5. **Read back**
   - Parse the file again; assert provider/model exist, defaults unchanged, no duplicate.
   - If the target validates config on start, start it once to catch schema errors.
6. **Start bridge**
   - Manual script, hidden process, PID/log metadata.
   - Wait for `/health` and `/ready`.
7. **Probe**
   - Models, text, stream, image (if claimed), error mapping.
   - Send a unique token and confirm it in the Target and bridge logs.
8. **Record**
   - Model ID, profile path, auth source, capabilities, limitations, backup/rollback, evidence paths.

## 5. Idempotency contract

- Provider ID is stable and unique.
- If it exists with identical values → no-op, exit 0.
- If it exists with different values → require an explicit `-Update`/confirmation; never silently overwrite.
- Model IDs are unique within the provider.
- If the format supports a marker (comment, `managedBy` field), use it; otherwise record the added block in a manifest.
- Running the script twice must produce an empty diff on the second run.
- Running start twice must detect the existing bridge, not spawn a second listener.

## 6. Secrets

- Prefer a user-level environment variable or the OS credential manager.
- Config stores the variable name/placeholder only.
- Never write secrets into logs, error bodies, screenshots, or Git.
- On Windows, user-level env vars can be set with `[Environment]::SetEnvironmentVariable(name, value, 'User')`; do not use machine-level without explicit consent. `setx` does not affect the current process.
- Document how to rotate/revoke and what happens when the secret expires.

## 7. Persistence and auth expiry

- Target configuration goes into the official profile; it must survive app restart.
- The bridge does not autostart; the one-click script starts it manually.
- `/health` = process alive. `/ready` = upstream auth/model usable without generation.
- On expiry:
  - S1: return `401`, instruct to update the key/env var.
  - S2: return `401/403 reauth_required`, instruct to log in to the Source.
  - S3: do not claim persistence; the owner/device credential usually cannot be refreshed by a bridge.
- Never silently fall back to the Target’s default model or a cached answer.

## 8. Acceptance tests

1. Run the install script twice; second run is a no-op and the config diff is empty.
2. Restart the Target; the provider/model is still present and the default model is unchanged.
3. Start the bridge twice; second start reports “already running”.
4. Stop and restart the bridge; `/ready` passes with valid auth.
5. Invalidate/expire the Source auth; `/ready` returns a clear 401/403 with reauth instructions.
6. Probe text, stream, and image (if claimed); verify usage includes cache tokens.
7. Stop the bridge; the Target errors rather than silently answering from its default.
8. Restore the backup; the Target returns to its original state.

## 9. Rollback

1. Stop the bridge and the Target.
2. Restore the backed-up profile, or remove only the added provider/model block.
3. Start the Target; confirm the original default model.
4. Remove temp files/sessions; keep redacted logs.
5. Record what failed and why.

## 10. Anti-patterns

- A “universal” config editor that rewrites arbitrary YAML/JSON/TOML.
- Writing the API key into the Target config or a log.
- Changing the default model to make the new one “work”.
- Autostart/service installation without being asked.
- No backup, no read-back, no idempotency.
- Treating `/health` as proof that upstream auth works.
- Silently falling back to the default model on bridge failure.
- Claiming persistence for a session/owner token that expires.
