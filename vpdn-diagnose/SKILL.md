---
name: vpdn-diagnose
description: Comprehensive VPDN (Virtual Private Dial Network) client troubleshooting for Windows. Use when users report VPDN dial-up errors, "VPDN server access failed", connection failures, self-check passes but dial fails, or any VPDN client (dx_vpdn, JxTelecomVPDN) issues. Covers proxy conflicts, WAN Miniport driver issues, RAS service failures, firewall blocks, DNS problems, and common error codes (651, 628, 691, 618, 800, 807, 1062, 711). Also use when the VPDN client self-check passes but "Connect Network" fails.
---

# VPDN Client Troubleshooting

Diagnose and fix VPDN dial-up client issues on Windows without affecting other configurations.

## Core Diagnostic Flow

Always run in this order. Stop when the root cause is found and fixed.

### Step 1: Proxy Conflict Check (Most Common)

**Why this matters first:** VPDN clients often use HTTP/HTTPS to authenticate with the server before establishing the dial-up tunnel. If a system proxy (Clash/verge-mihomo/v2rayN/etc.) is active, these requests are hijacked and fail to reach the VPDN server.

1. Read `HKCU\Software\Microsoft\Windows\CurrentVersion\Internet Settings\ProxyEnable` from registry
2. If `ProxyEnable = 1`, read `ProxyServer` value
3. **If proxy is 127.0.0.1 or localhost:**
   - This is likely the root cause
   - **Fix:** Disable system proxy temporarily (`ProxyEnable = 0`)
   - Ask user to close and reopen VPDN client, then retry
   - If successful, instruct user to add VPDN server domain to their proxy tool's bypass/direct list
4. **If proxy is a corporate proxy:** Check if VPDN server address is in the bypass list

**Verification:** After fix, check `ProxyEnable` again; should be 0.

### Step 2: Service Health Check

Check these Windows services via `sc query`:

| Service | Expected State | Error If Missing |
|---------|---------------|------------------|
| RasMan | RUNNING | 1062, 711 |
| RemoteAccess | STOPPED (normal) or RUNNING | 800 |
| Telephony | RUNNING | 711, 1062 |
| NetworkConnections | RUNNING | 711 |
| RemoteAccessConnectionManager | RUNNING | 711, 1062 |
| TrustService (if Zero Trust) | RUNNING | Auth failures |

**Fix:** `services.msc` → find service → start + set to Automatic.

### Step 3: Network Adapter & Route Check

1. Check `netsh interface show interface` for:
   - Active physical adapter (Ethernet/WLAN) in "已连接" state
   - No unexpected default gateway conflicts
2. Check `ipconfig /all`:
   - DNS servers should be reachable (not 127.0.0.1 unless intentionally set)
   - Physical adapter has valid IP (not 169.254.x.x autoconfig)
3. Check `route print` for multiple default routes (0.0.0.0) with low metric
   - If multiple adapters have 0.0.0.0 routes, VPDN may pick wrong interface

**Fix:** Disable unused adapters temporarily; renew DHCP (`ipconfig /renew`)

### Step 4: Windows Event Log Deep Dive

Query `Application` log for `RasClient` source, Event ID 20227 (last 48h):

```
wevtutil qe Application /q:"*[System[Provider[@Name='RasClient'] and EventID=20227 and TimeCreated[timediff(@SystemTime) <= 172800000]]]" /f:text /c:20
```

Extract the **error code** from each event. Cross-reference with `references/error-codes.md`.

**Key insight:** If recent events show 651, 628, 618, 691, the client CAN reach the server (proxy is not the issue). The problem is at the dial-up/tunnel layer.

**If NO recent RasClient events:** The client never reached the dial stage. Focus on proxy/network/firewall.

### Step 5: WAN Miniport Driver Check (651 errors)

In Device Manager → Network adapters:
- Look for **WAN Miniport (PPPOE)** / **WAN Miniport (PPTP)** / **WAN Miniport (L2TP)**
- If yellow triangle or missing, uninstall then scan for hardware changes

**Also check:** `C:\Windows\System32\LogFiles\WMI` permissions. If folder is read-only, 651/711 errors occur. Ensure current user has Full Control.

### Step 6: Firewall & Antivirus Check (807, 360 false positives)

- Check `netsh advfirewall show currentprofile` for inbound block
- Add VPDN client directory to antivirus whitelist (360, 金山毒霸, Windows Defender)
- Check if UDP 500/4500 or TCP 1723 are blocked by firewall

### Step 7: DNS Configuration (Post-dial webpage issues)

If dial succeeds but cannot open websites:
- Set DNS to `134.224.120.62` on the VPDN virtual adapter
- Flush DNS cache: `ipconfig /flushdns`

## Self-Check Passes But Connection Fails

This is the signature of the **proxy conflict** scenario:
- Client files are intact (integrity check OK)
- Zero Trust service is running (if applicable)
- VPN start/close programs are OK
- But HTTP auth requests to VPDN server are intercepted by the proxy

**Immediate action:** Check and disable system proxy before any other troubleshooting.

## Multiple VPN Coexistence

If user has WireGuard, OpenVPN, Clash, or other VPN active:
1. Check `netsh interface show interface` for active virtual tunnels
2. Check `netstat -ano` for UDP 500/4500 listeners (IPsec/IKE)
3. If another VPN owns the routing table, VPDN may conflict

**Fix:** Temporarily disable other VPNs, test VPDN alone.

## Recurrence Prevention (Proxy Bypass)

If the root cause was a system proxy (Clash, v2rayN, verge-mihomo, etc.), simply disabling it is temporary — the proxy tool will likely re-enable it on next launch, node switch, or config reload. Provide the user with a permanent bypass rule.

### Preferred approach: PROCESS-NAME rules

When the VPDN server domain is unknown or embedded in a binary client, bypass by **process name** is the most reliable method:

1. Identify the VPDN client executables (e.g., `VPDN拨号客户端.exe`, `dx_TrustAgent.exe`, `vpn_start.exe`)
2. In the proxy tool's rule configuration, add `PROCESS-NAME` rules directing those executables to `DIRECT`

Examples for common proxy tools:

| Tool | Rule syntax | Where to add |
|------|-------------|--------------|
| **Clash / Mihomo / Clash Verge** | `- 'PROCESS-NAME,VPDNClient.exe,DIRECT'` | Profile's `prepend` rules list |
| **v2rayN** | `"processName": ["VPDNClient.exe"]` in routing rules | Routing → Rules |
| **Sing-box** | `{ "process_name": ["VPDNClient.exe"], "outbound": "direct" }` | Route rules |

**Why PROCESS-NAME over DOMAIN:**
- VPDN client binaries often hardcode server IPs or use encrypted configs
- DNS resolution may happen inside the tunnel, making domain-based rules ineffective
- Process-level bypass survives IP changes and config updates

### Alternative: IP-CIDR bypass

If the user knows the VPDN server subnet (check `route print` while connected), add an `IP-CIDR` rule for that CIDR to `DIRECT`.

### Verification after rule setup

1. Keep the proxy tool running with system proxy enabled
2. Open VPDN client and click "Connect Network"
3. If connection succeeds, the bypass rule is working
4. Run `netstat -ano` to confirm VPDN traffic does not go through the proxy port (e.g., 7897)

## Using the Diagnostic Script

Run `scripts/vpdn_diagnose.py` via PythonRun to collect a comprehensive snapshot:
- Registry proxy settings
- Service statuses
- Network interfaces and routes
- Windows event logs (last 48h)
- Active connections and port listeners
- DNS configuration

The script outputs a JSON file for analysis. Run it first on any VPDN issue.

## Error Code Quick Reference

For detailed error code meanings and fixes, see `references/error-codes.md`.

Common codes to watch for:
- **651** → WAN Miniport / WMI permissions / driver
- **628** → No dial permission / connection closed by server
- **691** → Wrong credentials / online limit exceeded / no permission
- **618** → Port not open / modem issue
- **800** → Cannot reach VPDN server (network down / firewall / DNS)
- **807** → Firewall blocking / network quality
- **1062** → RAS services not started
- **711** → RAS services or WMI permissions
- **-1** → Already on internal network (no need to dial)
- **718** → Remote service interrupted (server-side)

## Verification After Fix

After any fix, always:
1. Close VPDN client completely (tray icon → exit)
2. Reopen VPDN client
3. Click "Connect Network"
4. Check Windows Event Viewer for new RasClient 20227 events if it fails again
5. Report success or the new error code to the user
