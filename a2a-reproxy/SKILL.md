---
name: a2a-reproxy
description: Agent-to-agent model capability reverse proxying (A2A_reproxy / 反向代理). Use when (1) a user provides an API endpoint/key/model and asks to configure it into a target agent (DSH, Codex, Trae, Qoder, Kimi Code, Pi, opencode, etc.), or (2) a user asks to reverse-proxy a source agent's default model for use in another agent. Covers source classification (standard API vs agent session vs signed relay vs static extraction), source-vs-target role separation, Windows-first incremental/add-only configuration, dynamic discovery, one-click setup, persistence, and auth-expiry checks. Triggers include A2A_reproxy, agent 模型反代, 默认模型反代, 模型能力桥接, local OpenAI adapter, and reasoning/image/usage/config-profile issues in a bridge.
---

# A2A Reproxy

## 核心目的

把一个 **Source（模型宿主）** 的模型能力，安全、可验证、可回滚地交给一个 **Target（消费方）**。先分清三个对象：

- **模型 / Provider**：endpoint、model ID、真实 context/output 上限、模态、计费。
- **Agent 框架**：session、system prompt、工具循环、权限、reasoning/answer 通道。
- **桥（Adapter/Reproxy）**：只做协议、鉴权、会话、文件/图片、流式与用量转换，不是第三个 Agent。

最重要的判断不是“URL 看起来是否 OpenAI 兼容”，而是 **Source 到底提供了什么**。

## 先分类 Source（路线由它决定）

| 模式 | 判定证据 | 可行路线 | 交付 / 停止条件 |
|---|---|---|---|
| **S1 标准 API + Key** | 官方文档/控制台、独立签发的 key；中性客户端可调 `/models` 与 chat | Target 直连；必要时加薄协议/鉴权代理 | Target 的增量 provider 配置；不需要桥时不要造桥 |
| **S2a 本地标准 API** | Source 在本机暴露 OpenAI 兼容或同类 API，只有鉴权/路径差异 | 薄桥：鉴权注入、路径/模型映射 | 桥 + Target 增量配置 |
| **S2b Agent 登录态 / Session** | 模型只在 Source 客户端/本地 session 内可用；直连云 API 返回免费档/权限错误 | Agent-session 桥：创建会话、提交消息/附件、取最终文本、清理 | 必须接受“嵌套 Agent”语义；免费档/工具/上下文限制写入交付说明 |
| **S3 签名 / 私有 Relay** | 逐请求签名、owner/device/install 绑定；只有 URL+token 会报缺头/签名错误 | 仅有官方凭证与公开签名契约时才做签名适配 | 无合法凭证/契约 → 停止；不要爆破签名、不要绕过反调试 |
| **S4 仅逆向出配置** | 从制品/日志只拿到 URL、model ID、header 名称，没有可用凭证或 session | 只作为可行性/架构证据 | 不把它叫作“可用的反代”或“已接好” |

**关键区分**：

- “直接给我 API 和 key”通常是 **S1**：优先直连，桥是可选层。
- “把源 Agent 里的默认模型反代出来”可能是 **S2b**（登录态/session）、**S3**（签名 relay）或 **S4**（只有静态配置）。默认模型的 URL 不是凭证；model ID 也不是授权。
- 逆向得到 endpoint/model 名称，只能证明“它请求哪里”，不能证明“你能合法地请求”。

一句话：**“直接给 API+key”是 S1；“从 Agent 里反代默认模型”先落到 S2/S3/S4，再决定是否建桥。**

## 第一性原则

1. **先分类，再选路**：Source 模式决定架构，而不是 URL 的外观。
2. **默认不改本地配置**：能只读发现、直连、用官方 UI 完成，就不写文件。
3. **最小修改**：必须改时只做增量（新增 provider/model、用户级环境变量），不覆盖、不改默认。
4. **只改变一个变量**：先验证 Source，再验证桥，再验证 Target；不要同时改 endpoint、auth、model、prompt。
5. **证据优先**：上游 usage、桥日志、Target 日志/DB、UI，至少两个独立来源一致才算成功。
6. **安全边界**：不破解签名、不绕过反调试/DRM/free-tier、不导出受保护凭据；被挡住就换路线或申请正式凭证。
7. **契约最小化**：桥只暴露 Target 需要的 OpenAI 子集；不要复制 Source 的全部 Agent 语义。
8. **Windows 默认**：PowerShell 优先；路径来自环境变量/进程/配置发现；Node 探针跨平台。
9. **动态发现、低耦合**：不写死盘符、用户名、安装目录、端口或进程名；一切通过参数/发现获得。
10. **一键可重复、持久化、可解释**：配置重启后还在；鉴权动态预检；每个失败能定位到地址/协议/凭证/模型/权限/上下文/工具中的一层。

## 修改预算（从低到高）

| 级别 | 动作 | 默认策略 | 必要条件 |
|---|---|---|---|
| **L0** | 只读发现、直连、官方 UI 配置 | 首选 | 无 |
| **L1** | Target 新增 provider/model 行 | 允许的默认落点 | add-only，保留原 provider 和默认模型 |
| **L2** | 新增用户级环境变量/凭据条目 | 需要时使用 | 只写用户级；不写机器级；不落日志 |
| **L3** | 新增本地桥进程/脚本 | S2/S3 需要时 | 手动启停，不自启动；端口可配置 |
| **L4** | 修改既有配置行/默认模型/系统设置 | 默认禁止 | 明确同意、备份、回滚方案、读回验证 |

**Never**：整体覆盖配置文件、改默认模型、把 key 写进 Target 配置或日志、装开机自启/系统服务、关闭安全控制、在未授权时抓取/复用 owner token。

## 主体角色

| 角色 | 拥有什么 | 不负责什么 |
|---|---|---|
| Source Agent | Provider 配置、登录态、session/agent、工具、免费档策略 | 不应被当作纯模型；它的 reasoning 不一定是答案 |
| Target Agent | 自己的 Agent loop、工具、权限、UI、reasoning 展示 | 不应直接读取 Source 的凭据或内部 session |
| Bridge | 协议转换、鉴权注入、会话生命周期、图片/文件、SSE、usage、清理 | 不应偷偷改模型、上下文或工具语义 |
| Upstream Provider | 模型能力、真实上限、计费/免费策略 | 不关心 Target 的 Agent 框架 |
| Credential Store | token/API key/OAuth | 不写日志、不进 Git、不跨 owner 复用 |
| Runtime Supervisor | 端口、进程、启停、健康/就绪检查 | 不负责业务鉴权 |
| Operator | 授权、配置、测试、回滚 | 不应把“假成功”当成功 |
| Verifier | 日志、DB、usage、对抗性检查 | 不只看 UI 文案 |

### 同一个程序，两种角色

同一个 Agent 软件在 Source 和 Target 角色下执行的内容不同，不能复用同一套判断：

| 程序（示例） | 作为 Source | 作为 Target |
|---|---|---|
| OpenCode | 本地 session/agent；免费档可能绑定客户端；模型经由它的 Agent loop | 配置 provider；它自己的 Agent loop/工具照常运行，只是模型请求指向桥 |
| DSH | 若该版本暴露本地 session/API，则暴露的是它的 profile/Agent loop | 在 profile 中新增 provider；它自己的 Agent loop/UI 不变 |
| TeleAgent | 默认 relay 是签名/owner 绑定；默认模型不是公开 API | 仅当该版本支持自定义 OpenAI provider 时才可作为 Target |
| Codex | 若该版本暴露本地 session/API，才谈得上 Source | `config.toml` 的 provider/profile；它自己的 Agent loop 不变 |

规则：

- **Source 角色**：它的登录态、system prompt、工具循环、免费档策略都在链路里；你接到的是“它的 Agent 能力”，不只是模型。
- **Target 角色**：它自己的 Agent loop 仍在运行；桥只提供模型端点，不能复制/替代 Target 的工具与权限。
- 因此：Source 侧的 Agent 选择、附件提示、工具策略属于桥的契约；Target 侧的 Agent 行为不应被桥改写。
- 以实际版本能力为准；不要把“某程序能当 Target”推断成“它也能当 Source”。

**工具的两个含义**：Agent tool（shell/read/browser）是业务能力；分析工具（进程/端口/配置/日志/asar/strings）是调查手段。不要把“分析工具能读文件”误认为“模型有工具能力”。

## 决策树

```text
Source 分类
├─ S1 标准 API + Key
│  ├─ Target 支持该协议 → 直连（最优）
│  └─ Target 只支持另一种协议 → 协议桥（Chat/Responses/Anthropic）
├─ S2a 本地标准 API
│  └─ 薄桥：鉴权/路径/模型映射
├─ S2b Agent 登录态 / Session
│  └─ Agent-session 桥：session 生命周期 + 文本/图片/usage
├─ S3 签名 / 私有 Relay
│  ├─ 有官方 owner 凭证 + 公开签名契约 → 签名适配器
│  └─ 没有 → 停止；换标准 Provider 或申请官方接口
└─ S4 仅静态配置
   └─ 只作证据；不要声称可交付
```

不要因为“能发一个请求”就默认能复用：签名、免费档、owner/device 绑定、host/URL 绑定都可能让请求在真实上游失败。

## 两个标准场景

### A. “提供给你 API，帮我配到 XXXX 中去”

输入：base URL、key、精确 model ID、协议、真实 context/output 上限、是否支持图片/工具。

1. 归为 **S1**；确认 Target 是否可直接使用该协议。能直连就不建桥。
2. 动态发现 Target 的 live profile 与配置格式（进程参数、日志、安装目录、官方配置入口）。
3. add-only 新增 provider/model；key 放用户级环境变量或凭据存储，配置里只放变量名/占位符；默认模型不动。
4. 先直连 probe，再让 Target 选中新模型；验证文本/流式/图片（按能力）。
5. 生成可重复执行的一键安装脚本：备份、幂等、读回验证、失败回滚。
6. 重启 Target 验证持久化；记录限制（模型 ID、上下文、计费、过期）。

### B. “把 XXXX 里面的默认模型反代出来，我要在 YYYY 里面使用”

1. 先判定 XXXX 的 Source 模式：S1 / S2a / S2b / S3 / S4。
2. 找到“默认模型”的精确 model ID 与真正的鉴权所有者；默认模型通常只是路由名，不等于公开 endpoint。
3. S1/S2a：薄桥或直连；S2b：Agent-session 桥（session、附件、最终文本、usage、清理）；S3：无官方凭证则停止；S4：只给证据。
4. 在 YYYY 中 add-only 新增 provider/model，保留原默认模型。
5. 验证文本/流式/图片/用量；确认没有回退到 YYYY 的默认模型。
6. 写清“这是模型能力，还是嵌套 Agent 能力”，以及工具/reasoning/上下文/免费档限制。

## 工作流

### 0. 约束与授权

确认 Source/Target、Source 模式、是否允许桥接、凭证来源是否合法、是否接受免费档/计费、是否需要图片/工具、是否要求配置持久化、是否允许新增环境变量。写清“不做什么”。

### 1. 动态发现（不要猜路径）

- **进程/端口**：进程名、可执行文件、命令行、监听端口；用 `Get-CimInstance Win32_Process`、`Get-NetTCPConnection`，或 `scripts/discover-app.ps1`。
- **Target profile**：进程参数（`--config`/`--profile`/`--user-data-dir`）、日志、安装目录、用户配置根；确认正在运行的那个 profile。
- **Source 配置**：官方配置入口、本地 API/session、日志/DB；受保护的 token 存储不读取、不导出。
- **能力**：真实 context/output、模态、工具、reasoning 变体；以 Provider 目录/官方文档为准。
- 所有脚本用参数接收路径/端口/进程名，不写死盘符、用户名、安装目录。

### 2. 写契约

```text
Target → Bridge: POST /v1/chat/completions
Bridge → Source: <标准 API / 本地 API / session API>
Model ID: <精确 ID>
Auth: <谁持有、如何注入、是否逐请求、过期如何预检>
Images: <是否支持、如何转附件>
Streaming: <原样/重组/合成>
Usage: <input+output，含 cache read/write>
Ready: <如何检查上游鉴权/模型可用，不产生生成调用>
Errors: <401/403/429/5xx 如何映射>
Session/TTL: <创建/复用/删除/清理>
```

### 3. 最小实现

先实现 `GET /v1/models`、`POST /v1/chat/completions`、SSE、usage、`/health` 与 `/ready`。图片桥接再做 content parts → 文件/附件；reasoning 只做通道选择，不把 reasoning 当 content 返回。

### 4. 分层验证

Source 自身 → Source API/session → 桥 → Target 选中模型 → Target 文本/流式/图片 → 重启 Target → 重启桥/机器。任一层失败不要跳到下一层。

### 5. 一键化与持久化

- 先生成 **target-specific** 的安装/配置脚本，再谈“一键”；不要做通用 YAML/JSON/TOML 改写器。
- 脚本必须：预检 → 发现 → 备份 → add-only 应用 → 读回验证 → 启动桥 → `/ready` → probe → 输出回滚。
- 幂等：同一 provider/model 重复执行不产生重复行；值不同必须显式确认。
- 密钥不落配置：用户级环境变量/凭据存储；脚本只写变量名。
- 配置写入官方 profile，重启后仍在；桥手动启停，不装自启动。
- 鉴权预检：每次启动/使用前检查 Source 凭证；过期返回明确的 `reauth_required`，不静默失败。

### 6. 对抗性审查

- 成功是真模型，还是桩/缓存/UI 假象？
- Target 真的用了桥模型，还是回退默认模型？看 model ID、桥日志、上游 usage。
- 响应是最终 `content`，还是 reasoning/tool 中间态？
- usage 是否漏了 cache read？上下文是否把 Source Agent 的 system/tool 提示算进去？
- 配置是否覆盖了默认模型？profile 是否是运行中的那个？
- 一键脚本重复执行是否幂等？重启后配置是否还在？凭证过期是否可诊断？
- 临时文件/session/token 是否清理？是否绕过任何安全控制？如果是，停止。

## 一键配置与持久化（交付契约）

一键不等于开机自启。默认交付是 **一个可重复执行的手动脚本**：

```text
preflight → discover target profile → backup → add-only provider/model
→ read-back verify → start bridge → /ready → probe → evidence/rollback
```

- **持久化**：Target 配置写入官方 profile，重启 Target 后模型仍在；桥的启动是手动的，由脚本/快捷方式完成。
- **鉴权**：API key/session/owner token 都可能过期或撤销；`/ready` 做无生成的上游检查；过期时返回 `401/403 reauth_required` 并提示重新登录/更新环境变量。
- **低耦合**：脚本以参数接收 profile、桥脚本、端口、模型 ID；默认值只是默认值，不是硬编码契约。
- **幂等**：provider ID 稳定；存在且相同 → no-op；存在但不同 → 要求显式更新；模型行唯一。
- **可回滚**：首次修改前备份；记录备份路径；失败时恢复并停止桥。

详细设计见 `references/one-click.md`。

## 关键映射（通用规则）

| Source 概念 | Target 概念 | 规则 |
|---|---|---|
| Provider ID | Target provider route | 可自定义；桥内部使用 Source ID |
| Base URL | Target Base URL | Target 指向桥；桥再指向 Source |
| API Key/OAuth | Target apiKey/header | 真实凭据留在桥/凭据存储；Target 只用占位符/变量名 |
| Model ID | Target model ID | 逐字一致；不要拿展示名当 ID |
| context limit | contextWindow | 以 Provider/model 为准；Target 字段是预算，不能突破真实上限 |
| output limit | maxTokens | 精确匹配 Provider 上限 |
| tools | Target tools | 默认不透传；透传需单独设计 |
| image input | Target input | 桥把图片转成 Source 可读的附件/文件 |
| reasoning variants | reasoningEfforts | 只映射真实存在的档位 |
| cost/usage | Target usage | 含未缓存输入 + cache read/write |

详细案例见 `references/field-mapping.md`。

## 踩坑速查

- **把 S4 当 S1**：逆向出 URL/model 不等于有合法凭证；不要把静态线索交付成“可用反代”。
- **角色混淆**：同一个程序当 Source 时链路里有它的 Agent loop；当 Target 时它仍然运行自己的 loop。不要复制错一层。
- **硬编码路径/端口/进程名**：换机器就失效；先发现，再参数化。
- **签名/私有 relay**：URL+token 不够；不要盲试排列；无官方契约就停止。
- **免费档**：免费模型可能只允许 Source 客户端内部使用；不要绕过。
- **Agent vs 模型**：build/general Agent 可能跑工具；reasoning 可能被当答案；图片请求优先只发最新用户消息并明确“不要工具/验证”。
- **Usage 漏 cache**：只报 input 会严重低估上下文。
- **Context 预算**：Source Agent 会注入大量 system/tool 提示；不要把 Target 预算设成模型裸上限。
- **配置 profile**：桌面/Web/CLI profile 可能不同；改错位置看起来“没生效”。
- **Patch 语义**：配置行通常替换整个 config；追加 provider 时保留原行；不要动默认模型行。
- **一键脚本不幂等**：重复执行产生重复 provider/模型，或覆盖用户改动；必须读回验证。
- **假成功**：`pong`、UI“完成”、usage 0 都不等于真实模型成功。

详细清单见 `references/pitfalls.md`。

## 工具

- **动态发现**：`scripts/discover-app.ps1`（只读：进程、命令行、监听端口、候选配置文件；默认 Windows 环境）。
- **协议验证**：`scripts/probe-openai-compatible.mjs`（文本/流式/图片/usage/失败路径；不打印 key）。
- **运行时**：`scripts/start-bridge.ps1` / `scripts/stop-bridge.ps1`（手动、一键、可配置；不自启动）。
- **制品调查**：REA/asar/strings/进程/日志/DB（只读；用于 S2/S3/S4 的判定，不用于绕过控制）。
- **配置**：官方 profile/provider 入口；add-only；先备份；优先官方 UI/CLI。

## 交付物

1. Source 模式判定与路线选择（S1/S2a/S2b/S3/S4）。
2. 桥（S2/S3，或 Target 协议不兼容时的协议桥）与最小契约。
3. Target 的 add-only 增量配置/一键安装脚本（幂等、可回滚）。
4. 手动启停脚本（不自启动）。
5. 验证记录：Source、桥、Target、usage、鉴权过期、重启持久化。
6. 限制说明与回滚方法。

## 参考

- `references/source-modes.md`：S1–S4、双角色、动态发现、鉴权生命周期。
- `references/architecture.md`：架构模式、Adapter 契约、流式/图片/session、`/ready`。
- `references/field-mapping.md`：Target 配置形态、OpenCode→DSH 实例、TeleAgent 签名案例、上下文计算。
- `references/one-click.md`：一键配置、幂等、备份、持久化、鉴权预检。
- `references/pitfalls.md`：踩坑与错误码/根因。
- `references/validation.md`：分层验证、证据、重启/过期/幂等测试、对抗性清单。
