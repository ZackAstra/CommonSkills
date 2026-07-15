# VPDN Error Code Reference

## Error Codes by Category

### Server Reachability Errors (Network/Proxy/DNS)

| Code | Meaning | Fix |
|------|---------|-----|
| 800 | Network cannot reach VPDN server | Check internet connection, restart, check firewall |
| 807 | Firewall/antivirus blocking or poor network quality | Disable firewall temporarily, retry, check antivirus whitelist |
| 868 | Remote server not responding | Check network connection to server |
| 619 | ISP server failure or line fault | Contact ISP/administrator |
| -1 | Already on internal network, no need to dial | Verify if already connected to target network |

### Dial Port / Driver Errors

| Code | Meaning | Fix |
|------|---------|-----|
| 651 | Modem cannot find dial port | 1) Reset network adapter (disable/enable) <br>2) Uninstall/reinstall WAN Miniport driver <br>3) Check WMI folder permissions (`C:\Windows\System32\LogFiles\WMI`) |
| 618 | Specified port not open | Check if port is occupied by another application; restart modem |
| 633 | Modem in use or not configured for dial-out | Close other VPN/dial programs; check port configuration |
| 635 | Unknown error | General system failure; restart and retry |
| 645 | Internal authentication error | Check system credentials and retry |

### Authentication / Permission Errors

| Code | Meaning | Fix |
|------|---------|-----|
| 691 | Wrong username/password or online limit exceeded | 1) Check credentials <br>2) If already online elsewhere, disconnect or wait 3 minutes <br>3) Apply for dial permission via IT ticket if new user <br>4) New users wait 30 minutes for address assignment |
| 628 | Connection closed — no dial permission | Apply for VPN access via IT ticket (specify: external network + VPN permission) |
| 647 | Account disabled | Contact administrator |
| 648 | Password expired | Reset password |
| 649 | Account has no dial-in permission | Apply for permission via IT ticket |
| 718 | Remote service interrupted | Contact administrator (server-side issue) |

### Service Errors

| Code | Meaning | Fix |
|------|---------|-----|
| 1062 | Virtual dial service not started | Start these services: RemoteAccessConnectionManager, NetworkConnections, Telephony |
| 711 | Required services not running | Same as 1062: start RemoteAccessConnectionManager, NetworkConnections, Telephony; also check WMI permissions |
| 720 | PPP protocol negotiation failed | Check encryption settings; try different VPN protocol |

### VPN Tunnel Errors

| Code | Meaning | Fix |
|------|---------|-----|
| 806 | VPDN connection cannot complete | 1) Open TCP port 1723 and IP protocol 47 (GRE) on router/firewall <br>2) Ensure VPDN server is pingable <br>3) Update router/firewall firmware <br>4) Check DHCP IP assignment on VPDN host |
| 678 | Remote computer not responding | 1) Check/replace network cable <br>2) Try manual dial from Network Connections <br>3) Contact administrator to check ISP line |

### Post-Connection Errors

| Code | Meaning | Fix |
|------|---------|-----|
| Dial success but no web | DNS issue | Set DNS to `134.224.120.62` on the VPDN virtual adapter |
| 蓝屏 | Dial software conflict | Uninstall recently installed software; check for driver conflicts |

## Proxy Conflict Scenario (Signature Error Pattern)

When the VPDN client self-check passes (all components OK, TrustService running) but clicking "Connect Network" immediately shows **"VPDN server access failed"** with no specific error code, this is the **proxy conflict** scenario.

### Symptoms
- Integrity check: all green
- Zero Trust check: TrustService running
- No RasClient events in Windows Event Log (or events from days ago)
- `netsh interface show interface` shows physical network is connected
- System proxy is enabled (usually `127.0.0.1:7897` for Clash/verge-mihomo, or `127.0.0.1:1080` for v2rayN)

### Why it happens
VPDN clients communicate with the authentication server via HTTP/HTTPS before establishing the PPP tunnel. When a system proxy is active, these requests are intercepted by the proxy tool (e.g., verge-mihomo) and routed through its own tunnel (WireGuard, etc.), which cannot reach the internal VPDN server.

### Fix
1. Disable system proxy: `HKCU\Software\Microsoft\Windows\CurrentVersion\Internet Settings\ProxyEnable = 0`
2. Close and reopen VPDN client
3. Retry connection
4. If successful, add the VPDN server domain to the proxy tool's bypass/direct list for future use

## Error Code 651 Deep Dive

Code 651 is the most common dial failure after the proxy issue is ruled out.

### Cause 1: Network Adapter Driver
1. Open Device Manager → Network Adapters
2. Find the physical adapter (Ethernet/Wi-Fi)
3. Right-click → Disable, then right-click → Enable
4. If still failing: Uninstall driver → Action → Scan for hardware changes
5. Restart computer

### Cause 2: WMI Log Permissions
1. Navigate to `C:\Windows\System32\LogFiles\WMI`
2. Right-click → Properties → Security → Advanced
3. Select current user → Edit → check Full Control
4. Apply → OK → Restart

### Cause 3: Router/WAN Miniport
1. Uninstall WAN Miniport (PPPOE) from Device Manager
2. Scan for hardware changes to reinstall
3. Restart computer

### Cause 4: ISP Line Issue
- Check cable connection
- Try manual dial from Network Connections (rasphone)
- If manual dial also fails, contact administrator
