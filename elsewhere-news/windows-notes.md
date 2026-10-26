**Windows hosts:** On Windows, `bash` on `PATH` is usually the WSL launcher (`C:\Windows\System32\bash.exe`) and fails with `execvpe(/bin/bash)` when no distribution is installed. The pinned `.sh` client also rejects non-ASCII query arguments under Git Bash. Use the bundled native client instead; it enforces the same read-only route allowlist, key format, bearer auth, and error mapping:

```powershell
pwsh -NoProfile -ExecutionPolicy Bypass -File {baseDir}/scripts/elsewhere-api.ps1 check-version
pwsh -NoProfile -ExecutionPolicy Bypass -File {baseDir}/scripts/elsewhere-api.ps1 /me/context lang=zh
```

Use `pwsh` (PowerShell 7) when available, otherwise `powershell`; both decode responses as UTF-8. The PowerShell client is the supported Windows transport. The pinned `.sh` client remains canonical on POSIX hosts; never substitute any other credential or transport path.
