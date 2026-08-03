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
| 651 | Modem cannot find dial port | 1) Reset network adapter (disable/enable) <br>2) Uninstall/reinstall WAN Miniport driver <br>3) Check WMI folder permissions (`C:\Windows\System32\LogFiles\WMI`) <br>4) **先查 Telephony (TapiSrv) 服务是否停止**（实测最常见原因）|
| 618 | Specified port not open | Check if port is occupied by another application; restart modem |
| 633 | Modem in use or not configured for dial-out | Close other VPN/dial programs; check port configuration |
| 635 | Unknown error | General system failure; restart and retry |
| 645 | Internal authentication error | Check system credentials and retry |

### Authentication / Permission Errors

| Code | Meaning | Fix |
|------|---------|-----|
| 691 | Wrong username/password or online limit exceeded | 1) Check credentials <br>2) If already online elsewhere, disconnect or wait 3 minutes <br>3) Apply for dial permission via IT ticket if new user <br>4) New users wait 30 minutes for address assignment |
| 628 | Connection closed - no dial permission | Apply for VPN access via IT ticket (specify: external network + VPN permission) |
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

---

## Client Log Error Patterns（客户端日志错误模式，实测最重要）

VPDN 客户端（dx_vpdn）写日志到 `C:\Users\<user>\dx_log.txt`。**这是定位"服务端访问失败"的第一证据**，比任何猜测都可靠。搜索关键字：`api_updateCheck` / `new4a_qrcode_get` / `Req http://` / `Err`。

### 代理劫持模式（系统代理开启时的典型失败）

```
api_updateCheck: Req http://134.225.85.56:9090/interfaceJX/ActionAPI/queryVersion.api {...}
api_updateCheck: Err 289 HTTPConnectionPool(host='127.0.0.1', port=7897): Read timed out. (read timeout=4)
new4a_qrcode_get: Req http://134.224.230.142:8000/api/openapi/4aauth1/jxOauth/qrCode/get/sys_bhkhd
new4a_qrcode_get: Err 30 Expecting value: line 1 column 1 (char 0)
```

- `Err 289 ... host='127.0.0.1', port=7897` → 认证请求被发到本地代理（Clash 混合端口）并超时
- `Err 30 Expecting value` → 代理返回空响应，JSON 解析失败
- **修复成功标志**：`Req OK 200 {'code': 0, 'msg': '获取二维码成功', 'data': 'UAM-...'}`

### 客户端自身 bug（忽略，不可修复）

```
Req http:// 134.224.13.23:9090/...   ← http:// 后带空格
Err 307 ... host='%20134.224.13.23' ... getaddrinfo failed
```
备份服务器 URL 拼接错误，永远失败。主服务器（134.225.85.56）可用即可，无需处理。

### 实测服务器地址（江苏电信 VPDN）

| 用途 | 地址 | 段 |
|------|------|-----|
| 版本检查主服务器 | `134.225.85.56:9090` | 134.224.0.0/15 |
| 备份服务器（客户端 bug 不可用） | `134.224.13.23:9090` | 134.224.0.0/15 |
| 二维码/OAuth 认证 | `134.224.230.142:8000` | 134.224.0.0/15 |
| VPDN DNS | `134.224.120.60 / 134.224.120.62` | 134.224.0.0/15 |

直连规则应覆盖 **`134.224.0.0/15`**（含 134.224.x 与 134.225.x）。

---

## Proxy Conflict Scenario (Signature Error Pattern)

When the VPDN client self-check passes (all components OK, TrustService running) but clicking "Connect Network" immediately shows **"VPDN server access failed"** with no specific error code, this is the **proxy conflict** scenario.

### Symptoms
- Integrity check: all green
- Zero Trust check: TrustService running
- No RasClient events in Windows Event Log (or events from days ago)
- `netsh interface show interface` shows physical network is connected
- System proxy is enabled (usually `127.0.0.1:7897` for Clash/verge-mihomo, or `127.0.0.1:1080` for v2rayN)
- `dx_log.txt` 显示 `Err 289/30`（见上文客户端日志模式）

### Why it happens
VPDN clients communicate with the authentication server via HTTP/HTTPS before establishing the PPP tunnel. When a system proxy is active, these requests are intercepted by the proxy tool (e.g., verge-mihomo) and routed through its own tunnel (WireGuard, etc.), which cannot reach the internal VPDN server.

### Fix（三层，不关全局代理）
1. **L1 系统代理例外**：`ProxyOverride` 加 `134.224.*;134.225.*;134.224.0.0/15`，并在 Clash Verge `verge.yaml` 配 `system_proxy_bypass`（否则代理守护会重置）
2. **L2 mihomo 直连规则**：`IP-CIDR,134.224.0.0/15,DIRECT`（写入订阅的 Rules 增强文件 `prepend:`，不是全局 Merge.yaml）
3. **L3 进程规则**：`PROCESS-NAME,VPDN拨号客户端.exe,DIRECT` 等 + `find-process-mode: always`

### 验证
- mihomo 管道 `GET /rules` 确认 `IP-CIDR 134.224.0.0/15 -> DIRECT` 在 `rules[0]`
- `curl -x http://127.0.0.1:7897 http://134.225.85.56:9090/...` 与直连结果一致（实测均 502）
- 重启 VPDN 客户端，`dx_log.txt` 出现 `Req OK 200`

---

## Error Code 651 Deep Dive

Code 651 is the most common dial failure after the proxy issue is ruled out.

### Cause 0（实测最常见）：Telephony (TapiSrv) 服务停止
```powershell
cmd /c "sc query TapiSrv"
cmd /c "sc config TapiSrv start= auto & sc start TapiSrv"   # 管理员
```
RAS 拨号依赖 TAPI 接口，Telephony 不运行则 PPPoE 隧道无法建立，报 651。

### Cause 1: Network Adapter Driver
1. Open Device Manager -> Network Adapters
2. Find the physical adapter (Ethernet/Wi-Fi)
3. Right-click -> Disable, then right-click -> Enable
4. If still failing: Uninstall driver -> Action -> Scan for hardware changes
5. Restart computer

### Cause 2: WMI Log Permissions
1. Navigate to `C:\Windows\System32\LogFiles\WMI`
2. Right-click -> Properties -> Security -> Advanced
3. Select current user -> Edit -> check Full Control
4. Apply -> OK -> Restart

### Cause 3: Router/WAN Miniport
1. Uninstall WAN Miniport (PPPOE) from Device Manager
2. Scan for hardware changes to reinstall
3. Restart computer

### Cause 4: ISP Line Issue
- Check cable connection
- Try manual dial from Network Connections (rasphone)
- If manual dial also fails, contact administrator