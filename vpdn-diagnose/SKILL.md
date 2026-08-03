---
name: vpdn-diagnose
description: 综合 VPDN（江苏电信 dx_vpdn / JxTelecomVPDN / 奇安信 TrustAgent）Windows 拨号客户端故障排查。用于"VPDN 服务端访问失败"、651/628/691/618/800 等拨号错误、自检通过但连接失败、Clash/代理共存场景下的反复断连。覆盖代理劫持、Clash Verge 规则注入失效、RAS/Telephony 服务、WAN Miniport 驱动、WMI 权限、DNS、多 VPN 共存、ctEAO 虚拟网卡干扰。包含三层直连修复（系统代理例外 + mihomo IP-CIDR/进程规则 + find-process-mode）与运行时规则验证方法。
---

# VPDN Client Troubleshooting（全链路方法论文档）

本技能基于真实故障全链路复盘：江苏电信 VPDN（dx_vpdn + 奇安信 TrustAgent）在 Clash Verge 系统代理开启时反复报"VPDN 服务端访问失败"。核心教训：**不要只依赖"禁用代理"这类临时手段，也不要假定规则"加上就生效"——必须验证规则真正被运行时加载**。

## 0. 症状分类（入口路由，先定边界）

根据用户报告的症状，先确定主因方向，避免盲目全查：

| 症状 | 主因方向 | 处理路径 |
|------|----------|----------|
| 自检全通过 + "VPDN 服务端访问失败"（无具体错误码） | 认证 HTTP 请求被系统代理劫持 | **路径 A**（本场景主线） |
| 651 / 628 / 691 / 618 / 711 / 1062 | 拨号/隧道层：服务、驱动、权限、账号 | **路径 B** |
| 拨号成功但内网网页打不开 | DNS 配置（VPDN 虚拟网卡） | **路径 C** |
| 拨号成功但频繁掉线、路由错乱 | 多 VPN/代理共存冲突、路由表 | **路径 D** |
| 拨号成功但内网资源不可达 | SDP/零信任隧道（ctEAO-10 网卡）未建立 | **路径 D** |

**关键判据**：查询 `wevtutil qe Application ... RasClient EventID=20227`（见路径 B2）。
- 最近有 651/628/691 等事件 → 客户端**已进入拨号阶段**，代理不是主因 → 路径 B。
- **没有任何近期事件** → 请求根本没到拨号层，卡在认证 HTTP → 优先路径 A。

---

## 路径 A：认证请求被代理劫持（最常见，本场景主线）

### A0. 第一证据：读客户端日志（比任何猜测都可靠）

VPDN 客户端会写自己的运行日志，**直接暴露真实失败请求和目标服务器**：

- **dx_vpdn 客户端**：`C:\Users\<user>\dx_log.txt`（用户目录）或安装目录 `assets\dx_log.txt`
- 查找关键字：`api_updateCheck`、`new4a_qrcode_get`、`qrcode_state`、`Req http://`、`Err`

**典型失败模式（代理劫持的铁证）：**

```
api_updateCheck: Req http://134.225.85.56:9090/interfaceJX/ActionAPI/queryVersion.api {...}
api_updateCheck: Err 289 HTTPConnectionPool(host='127.0.0.1', port=7897): Read timed out. (read timeout=4)
new4a_qrcode_get: Req http://134.224.230.142:8000/... 
new4a_qrcode_get: Err 30 Expecting value: line 1 column 1 (char 0)
```

- `host='127.0.0.1', port=7897` → 客户端把认证请求**发给了本地代理**（Clash 混合端口）
- `Err 30 Expecting value`（空响应 JSON 解析失败）→ 代理返回了空/异常响应
- **修复成功的标志**：同一行变成 `Req OK 200 {'code': 0, 'msg': '获取二维码成功', ...}`

**从日志提取真实服务器段（关键，不要猜）：** 汇总所有失败 `Req http://<host>:<port>` 的 host。
- 江苏电信实测：`134.225.85.56:9090`（主）、`134.224.230.142:8000`（二维码认证）、`134.224.13.23:9090`（备份）→ 全部落在 **`134.224.0.0/15`**
- 此前 DNS 缓存里的 `ym.ctct.cn`、`imtwo.zdxlz.com` 是**浏览器流量，不是 VPDN 服务器**——以客户端日志为准，别被 DNS 缓存误导

**边界：客户端自身的 bug 不要修。** 备份 URL 形如 `http:// 134.224.13.23`（`http://` 后带空格 → host 变 `%20134.224.13.23`）时永远失败，这是客户端缺陷；只要主服务器可用即可，无需也无法修复。

### A1. 代理状态盘点（确认劫持链路）

```powershell
# 系统代理（WinINet，Python urllib/requests 都认）
Get-ItemProperty "HKCU:\Software\Microsoft\Windows\CurrentVersion\Internet Settings" -Name ProxyEnable,ProxyServer,ProxyOverride,AutoConfigURL
# 机器级代理（服务进程用）
netsh winhttp show proxy
```

- `AutoConfigURL`（SDP PAC）可能是奇安信/电信 SDP 客户端写入的，会劫持路由，应清除
- 若 `ProxyEnable=1` 且 `ProxyServer=127.0.0.1:7897`（Clash/verge-mihomo），与 A0 日志互相印证

### A2. 三层直连修复（不关全局代理，不影响其他流量）

按可靠度排序，**三层都做**（互为兜底）：

**L1 — 系统代理例外（源端旁路，最彻底）**
把 VPDN 服务器段加入 `ProxyOverride`，客户端请求直接不走代理：
```
HKCU\...\Internet Settings\ProxyOverride += ;134.224.*;134.225.*;134.224.0.0/15
```
- Python（urllib3/requests）与 WinINet 都识别该例外
- **必须同时配置 Clash Verge 自身的例外**（`verge.yaml` 的 `system_proxy_bypass` + `use_default_bypass: false`），否则 Clash 的"代理守护"每 30s 会把例外重置回默认值

**L2 — mihomo IP-CIDR/DOMAIN 直连规则（确定性兜底）**
即使请求到了 7897，也按目标地址直连：`IP-CIDR,134.224.0.0/15,DIRECT`（不依赖进程识别，最可靠）。

**L3 — PROCESS-NAME 进程规则（进程级兜底）**
`PROCESS-NAME,VPDN拨号客户端.exe,DIRECT`、`PROCESS-NAME,trustservice.exe,DIRECT` 等。
- **前提：必须设置 `find-process-mode: always`**。TUN 关闭时 mihomo 默认 `strict` 不对代理端口进来的连接做进程识别，PROCESS-NAME 规则会静默失效。

### A3. 规则注入的正确通道（最大的坑，务必验证）

**Clash Verge 全局 Merge.yaml 里的 `prepend-rules` 可能根本不会被加载**（本次踩坑：mihomo 运行时规则里完全没有，规则静默失效）。

正确且已验证的注入通道：
1. 打开 Clash Verge → 订阅 → 当前订阅的 **Rules 增强文件**（`profiles/<uid>.yaml`，type: rules），格式：
```yaml
prepend:
  - 'IP-CIDR,134.224.0.0/15,DIRECT'
  - 'PROCESS-NAME,VPDN拨号客户端.exe,DIRECT'
  - 'PROCESS-NAME,trustservice.exe,DIRECT'
append: []
delete: []
```
2. 该文件的 `prepend` 会合并进最终 `rules:`，mihomo 真正加载
3. 修改后重启 Clash Verge（或重载订阅）生效

**权威验证：mihomo 命名管道控制器查运行时规则**（不要只看生成的 yaml 文件）：

```powershell
# PowerShell 命名管道客户端（HTTP 协议），external-controller-pipe: \\.\pipe\verge-mihomo
$pipe = New-Object System.IO.Pipes.NamedPipeClientStream(".", "verge-mihomo", [System.IO.Pipes.PipeDirection]::InOut)
$pipe.Connect(3000)
$sw = New-Object System.IO.StreamWriter($pipe); $sw.AutoFlush = $true
$sw.WriteLine("GET /rules HTTP/1.1"); $sw.WriteLine("Host: localhost")
$sw.WriteLine("Authorization: Bearer set-your-secret"); $sw.WriteLine("Connection: close"); $sw.WriteLine("")
$sr = New-Object System.IO.StreamReader($pipe)
# 循环读取直至 Connection: close，然后 JSON 解析 rules[].payload/proxy
```
- 预期：`IP-CIDR 134.224.0.0/15 -> DIRECT` 出现在 `rules[0]`
- 其他可用端点：`GET /version`、`GET /configs`（确认 `find-process-mode: always`）
- secret 在 `config.yaml` 的 `secret` 字段；若 HTTP 控制器端口没监听，用管道

### A4. 防复发：启动脚本

代理工具会随开机/登录自动开启系统代理。若用户环境有开机脚本，需同步更新，否则重启后复发：
- 保留原有核心目标（如禁用 `ctEAO-10` 防 DNS 污染——不影响 VPDN 认证阶段，可保留）
- 强制开启代理的同时写入 VPDN 代理例外（L1），形成自愈闭环
- 示例：`disable_aonetun.ps1`（启动文件夹）——保留 ctEAO 禁用 + 清除 SDP PAC + 设置代理 + 写入 ProxyOverride 例外
- `.ps1` 含中文注释时**存为 UTF-8 带 BOM**，否则 PowerShell 5.1 可能误读

---

## 路径 B：拨号/隧道层错误（651 / 628 / 691 / 711 / 1062）

### B1. 服务健康（651/711/1062 常见根源）

```powershell
cmd /c "sc query RasMan & sc query TapiSrv & sc query Netman & sc query RemoteAccess"
```
- **Telephony (TapiSrv) 易被禁用/停止**，是 651 的常见直接原因
- RasMan 必须 RUNNING；RemoteAccess STOPPED 属正常
- 修复：`sc config TapiSrv start= auto` + `sc start TapiSrv`（管理员）

### B2. Windows 事件日志（判断是否到达拨号层）

```
wevtutil qe Application /q:"*[System[Provider[@Name='RasClient'] and EventID=20227 and TimeCreated[timediff(@SystemTime) <= 172800000]]]" /f:text /c:20
```
- 有 651/628/691 → 已到拨号层，按 B3 排查
- 无事件 → 卡在认证 HTTP，回路径 A

### B3. 驱动与权限

- WAN Miniport（PPPOE/PPTP/L2TP/IKEv2）是否正常：`pnputil /enum-devices /class Net`
- WMI 目录权限：`icacls C:\Windows\System32\LogFiles\WMI`（需当前用户 Full Control）
- 驱动异常：设备管理器卸载后扫描硬件变更

---

## 路径 C：DNS（拨号成功但网页打不开）

- VPDN 虚拟网卡 DNS 设为 `134.224.120.62`（电信 DNS；实测客户端也使用 `134.224.120.60`）
- `ipconfig /flushdns`

---

## 路径 D：多 VPN 共存 / SDP 隧道（ctEAO）

- 检查虚拟网卡：`Get-NetAdapter -IncludeHidden`（`ctEAO-10`/CtEAO Tunnel = 电信 SDP 信任网卡，trustcore 日志中称 "trust nc"）
- `trustservice.exe` 以 SYSTEM（Session 0）运行，认证 HTTP 由其发出；`No login, will not rebuild trust nc` 表示登录未完成前不重建网卡——**禁用 ctEAO-10 不影响认证阶段**，但若登录后内网不可达，需检查该网卡状态
- 其他 VPN（WireGuard/OpenVPN/TAP）路由冲突：`route print` 查多条 0.0.0.0 默认路由

---

## 综合验证方法（修完必须验证，按顺序）

1. **运行时规则验证**（权威）：mihomo 管道 `GET /rules` 确认直连规则在 `rules[0]`，`GET /configs` 确认 `find-process-mode: always`
2. **路由级验证**：`curl -x http://127.0.0.1:7897 http://<VPDN服务器>` 与 `curl`（直连）对比——**响应码/耗时一致**（如都 502/5s）说明流量已直连；若经代理超时（HTTP 000）说明仍走节点
   - 注意：若 VPDN 服务器仅在隧道内可达，需先拨号再验证
3. **客户端日志验证**：重启 VPDN 客户端，`dx_log.txt` 中 `Err 289/30/307` 消失，出现 `Req OK 200`
4. **其他流量回归**：`curl -x http://127.0.0.1:7897 https://www.google.com/generate_204` 应返回 204，确认全局代理未受影响

## 边界与注意事项

- **只放行 VPDN 目标/进程**，规则放最前但别全局 DIRECT，其他流量仍走代理
- **不要关 TUN**（用户环境是规则模式无 TUN），也别擅自全局禁用代理（会影响其他应用）
- **验证规则"真加载"**：生成 yaml 里有 ≠ 运行时加载，一律用管道 API 查
- 客户端日志是**第一证据**；DNS 缓存、`route print` 只能辅助
- 修复后重启 Clash Verge 会让改动落地；订阅更新可能重置 Rules 增强，需复查

## 使用诊断脚本

运行 `scripts/vpdn_diagnose.py` 采集快照（代理/服务/接口/事件/进程/端口/防火墙/DNS/WMI 权限/环境变量）。重点查看 `proxy_enable`、`proxy_override`、各服务状态与 RasClient 事件。

## 错误码快速参考

详见 `references/error-codes.md`。常用：
- **651** → Telephony 服务停止 / WAN Miniport / WMI 权限（先查 `sc query TapiSrv`）
- **628/691** → 无拨号权限 / 账号问题
- **800/807** → 服务器不可达 / 防火墙
- **1062/711** → RAS 服务未启动
- **无错误码的"服务端访问失败"** → 代理劫持认证请求（路径 A）

## 修复后验证清单

1. 完全退出 VPDN 客户端（托盘 → 退出）
2. 重新打开，点击"连接网络"
3. `dx_log.txt` 出现 `Req OK 200`（认证通过）
4. 若再失败：查 `wevtutil` RasClient 事件（到没到拨号层）、`dx_log.txt` 最新 Err（哪一步失败）
5. 向用户报告成功或具体错误码