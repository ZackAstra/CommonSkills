# AI代码审计工程化方法论

## 核心理念

LLM进行代码审计的核心挑战不在于能力不足，而是缺乏系统化的工作方法和质量标准。Skill（技能协议）的目标是为LLM配备"资深审计员的工作框架"，解决覆盖率低、幻觉率高、优先级混乱等关键痛点。

**本质定位**：不是教导LLM"什么是SQL注入"，而是编码资深审计员多年积累的工作方法和质量标准。

---

## 裸跑LLM vs Skill驱动对比

| 评估维度 | 裸跑LLM | Skill驱动 |
|---------|---------|-----------|
| 覆盖率 | 10-30%（仅聚焦热点代码） | 100%（全量扫描覆盖） |
| 准确性 | 高误报/漏报/行号错误 | 低误报（反幻觉规则约束） |
| 优先级 | 无序（随机审计） | 分级（T1-T2-T3层次） |
| 上下文管理 | 无（需手动管理） | 有（每Phase持久化到文件） |
| 流程稳定性 | 不稳定 | 6阶段标准化流水线 |
| 可复现性 | 低（每次结果不同） | 高（流程标准化） |
| 大项目适配性 | 差（>50K LOC开始丢失上下文） | 优（EALOC动态分组+多Agent协作） |

---

## 6阶段审计流水线

有效的审计Skill不是单一的大prompt，而是一条严格的工程化流水线。

```
Phase 0 → Phase 1 → Phase 2 → Phase 2.5 → Phase 3 → Phase 4 → Phase 5
预处理    安全扫描   关键路径    覆盖扫雷   深度语义   报告生成   修复建议
```

### 关键设计原则

- **不信任LLM记忆**：所有中间结果必须持久化到文件系统
- **明确输入输出**：每个Phase都有清晰的定义和质量标准
- **通过文件系统传递**：可随时重读恢复上下文，支持断点续传
- **可测试可审查**：所有过程文件对用户透明，支持外部工具检查和人工审视

### Phase 0：代码预处理与类型识别

**目标**：工程度量层 + 项目类型识别 + 批次规划

**工具链**：`git clone`、`mvn compile`、项目构建工具

**输出内容**：
- **项目类型识别报告**（Web应用、VSCode插件、Node.js CLI、Electron应用、微服务等）
- 项目统计报表（代码行数LOC、文件数量、模块数量、Controller数量）
- 复杂度评分（圈复杂度、认知复杂度）
- EALOC值（Effective Audit Lines of Code）
- **批次规划清单**（强制分批策略）

**新增强制分批机制**：
```
分批规则（必须遵守）：
1. 文件数 > 50：必须分批，每批不超过 50 个文件
2. LOC > 5000：必须分批，每批不超过 5000 行代码
3. 单文件 > 1000 行：标记为复杂文件，单独分批
4. 框架配置文件（package.json、pom.xml、composer.json）：独立批次优先审计
5. 入口点文件（main.ts、app.js、extension.ts）：单独批次优先审计

批次编号规则：B001、B002、B003...
每批次结束后，必须持久化结果到文件 .codefree/codefree-code-audit/phase0/batch_B00X.json
清空 LLM 上下文，重新加载下一批次

**分批可审查性**：
- 批次规划结果写入 `.codefree/codefree-code-audit/phase0/batches.json`
- 用户可通过读取该文件验证分批规则是否正确应用
- 若项目应分批但未分批，视为 Phase 0 执行失败
- 用户可发送"显示批次规划"指令要求 AI 汇报分批详情
```

**项目类型识别规则**：
```
VSCode插件识别：
- package.json 中存在 "contributes": { "commands": [...] }
- "activationEvents" 字段存在
- "engines": { "vscode": "..." }

Node.js CLI识别：
- package.json 中 "bin" 字段存在
- src/bin/ 目录存在
- commander、yargs 等 CLI 库依赖

Web应用识别：
- package.json 中存在 express、koa、fastify 等 Web 框架依赖
- pom.xml 中存在 spring-boot-starter 依赖
- composer.json 中存在 laravel/framework 依赖

Electron应用识别：
- package.json 中存在 electron 或 electron-builder 依赖
- main.js 或 main.ts 存在
- renderer/ 目录存在

微服务识别：
- 多模块结构（存在多个 package.json/pom.xml）
- Dockerfile 或 docker-compose.yml 存在
- gRPC、Thrift 等微服务框架依赖
```

**特点**：纯自动化脚本执行，不涉及漏洞发现逻辑，但增加了项目类型识别和强制分批规划

### Phase 1：安全扫描（分批执行）

**目标**：项目侦察，建立完整代码索引

**工具**：
- 基于人工规则的正则表达式匹配
- OWASP Top10规则库
- 历史漏洞比对数据库

**分批执行流程**：
```
1. 读取 Phase 0 生成的批次规划清单 .codefree/codefree-code-audit/phase0/batches.json
2. 读取项目类型识别报告 .codefree/codefree-code-audit/phase0/project_type.json
3. 按批次顺序执行扫描（B001 → B002 → B003...）
4. 每批扫描完成后：
   - 保存结果到 .codefree/codefree-code-audit/phase1/batch_B00X_scan.json
   - 更新系统状态 .codefree/codefree-code-audit/phase1/progress.json
   - 清空 LLM 上下文（保留批次清单和进度）
   - 继续下一批次
5. 所有批次完成后，汇总所有批次结果生成：
   - .codefree/codefree-code-audit/phase1/scan_results.json（全量扫描结果）
   - .codefree/codefree-code-audit/phase1/known_vulns.json（已知漏洞标记）
   - .codefree/codefree-code-audit/phase1/risk_points.json（风险点初步定位）
```

**基于项目类型的入口点识别**：
```
VSCode插件入口点：
- extension.ts/extension.js 中的 activate() 函数
- package.json → contributes.commands 中的命令定义
- package.json → contributes.views 中的视图定义
- context.subscriptions 中的事件监听器

Web应用入口点：
- Router配置文件：routes/*.js、router/*.ts、routes.go
- Controller类：*Controller.java、*Controller.ts、*.go
- API定义：api/*.js、swagger.yaml、openapi.json
- Express/Koa app.use()、app.get/post() 等路由注册

Node.js CLI入口点：
- bin/ 目录下的可执行文件
- commander/yargs .command() 或 .action() 定义
- process.argv 直接处理的参数解析

Electron应用入口点：
- main.js/main.ts 中的 electron.app 事件
- BrowserWindow 创建代码
- ipcMain/on 监听的主进程消息
- preload.js 中的 contextBridge 暴露

通用入口点：
- package.json 的 scripts 字段
- 配置文件：config/*.js、.env
- 初始化文件：init.js、bootstrap.js、main.go
```

**输出**：
- 全量代码扫描结果（分批次汇总）
- 已知漏洞标记
- 风险点初步定位（按入口点分类）

### Phase 2：关键路径分析（分批执行）

**目标**：识别调用链、数据流、控制流等关键漏洞路径

**方法**：
- 数据流分析（Source-Sink模型）
- 控制流追踪
- 调用链重构

**分批执行流程**：
```
1. 读取 Phase 1 的批次结果 .codefree/codefree-code-audit/phase1/batch_*.json
2. 读取项目类型报告 .codefree/codefree-code-audit/phase0/project_type.json
3. 按批次顺序分析关键路径：
   - 每批的入口点 → 数据流 → 危险函数
   - 跨批次依赖关系追踪（记录在 dependencies.json）
4. 每批分析完成后：
   - 保存结果到 .codefree/codefree-code-audit/phase2/batch_B00X_paths.json
   - 更新跨批次依赖关系 .codefree/codefree-code-audit/phase2/dependencies.json
   - 清空 LLM 上下文
5. 所有批次完成后：
   - 合并所有批次的关键路径
   - 构建全局调用链图谱 .codefree/codefree-code-audit/phase2/key_paths.json
   - 生成攻击面报告 .codefree/codefree-code-audit/phase2/attack_surface.json
```

**基于项目类型的分析重点**：
```
VSCode插件分析重点：
- 用户输入：命令参数、选中文本、配置项
- 危险操作：workspace.fs、workspace.openTextDocument、window.showInformationMessage
- 常见漏洞：命令注入（通过终端命令执行）、路径遍历（通过文件路径操作）、XSS（通过 WebView）

Web应用分析重点：
- 用户输入：HTTP参数、Cookie、Header
- 危险操作：SQL执行、文件操作、命令执行、反序列化
- 常见漏洞：SQL注入、XSS、文件上传、反序列化

Node.js CLI分析重点：
- 用户输入：命令行参数、stdin、配置文件
- 危险操作：child_process.exec/spawn、fs操作、eval
- 常见漏洞：命令注入、路径遍历、任意文件读写

Electron应用分析重点：
- 用户输入：渲染进程输入、IPC消息、本地文件
- 危险操作：remote模块（旧版）、contextBridge暴露、shell.openExternal
- 常见漏洞：IPC注入、RCE（通过 nodeIntegration）、协议劫持
```

**输出**：
- 关键路径图谱（分批次汇总）
- 潜在漏洞点列表（按入口点分类）
- 攻击面识别结果（基于项目类型）
- 跨批次依赖关系图

### Phase 2.5：覆盖率扫雷（分批验证）

**目标**：确保审计覆盖率100%，让"遗漏"无处藏身

**重要性**：这是针对LLM天然倾向的设计，因为LLM容易跳过"看起来不重要"的代码，而漏洞恰恰隐藏在这些地方。分批执行后，必须强制检查每个批次的覆盖情况。

**核心机制**：
1. 模板覆盖矩阵
2. 大模块拆分跟踪
3. 文件覆盖率清单
4. 实时状态更新
5. **批次完整性检查**（新增）

**批次完整性检查（新增）**：
```
检查规则（强制执行）：
1. 每个批次的文件覆盖率必须达到 100%
   - 统计每个批次 .codefree/codefree-code-audit/phase1/batch_B00X_scan.json 中的文件列表
   - 对比 Phase 0 的批次规划 .codefree/codefree-code-audit/phase0/batches.json
   - 缺失文件立即标记为"未审计"

2. 跨批次依赖完整性检查
   - 检查 .codefree/codefree-code-audit/phase2/dependencies.json 中的所有依赖
   - 确保依赖的批次都已完成审计
   - 未完成的依赖批次优先审计

3. 入口点完整性检查
   - 检查 Phase 1 识别的所有入口点
   - 确保每个入口点都被审计
   - 未审计的入口点单独批次强制审计

4. 配置文件完整性检查
   - 检查 package.json、pom.xml、composer.json 等配置文件
   - 确保所有配置都被审计
   - 配置中的依赖、脚本、环境变量都已被分析

批次覆盖率状态文件：.codefree/codefree-code-audit/phase2.5/batch_coverage.json
{
  "B001": {
    "total_files": 47,
    "audited_files": 47,
    "coverage_rate": "100%",
    "status": "completed"
  },
  "B002": {
    "total_files": 52,
    "audited_files": 48,
    "coverage_rate": "92%",
    "status": "incomplete",
    "missing_files": ["src/views/Dashboard.tsx", "src/api/user.ts"]
  }
}
```

详见下方"覆盖率保障机制"章节。

### Phase 3：深度语义理解（分批执行）

**目标**：AI深度分析，理解代码的实际行为

**方法**：
- 语义分析
- 逻辑推理
- 全链路推理流程图生成

**分批执行流程**：
```
1. 读取 Phase 2 的关键路径 .codefree/codefree-code-audit/phase2/key_paths.json
2. 读取批次依赖关系 .codefree/codefree-code-audit/phase2/dependencies.json
3. 按拓扑顺序执行深度分析（先处理无依赖的批次）
4. 每批分析完成后：
   - 保存结果到 .codefree/codefree-code-audit/phase3/batch_B00X_analysis.json
   - 保存利用链追踪结果到 .codefree/codefree-code-audit/phase3/batch_B00X_chains.json
   - 清空 LLM 上下文
5. 所有批次完成后：
   - 合并所有批次的漏洞分析
   - 构建全局利用链图谱 .codefree/codefree-code-audit/phase3/exploit_chains.json
   - 生成风险等级评估报告 .codefree/codefree-code-audit/phase3/vulnerability_analysis.json
```

**补充**：
- DAST（动态应用安全测试）补充
- 上下文关联分析

**基于项目类型的分析策略**：
```
VSCode插件深度分析重点：
- WebView 内容安全策略分析
- 命令执行参数过滤检查
- 文件路径操作的路径遍历风险
- 外部命令调用的命令注入风险
- 配置加载的不安全反序列化

Web应用深度分析重点：
- SQL注入的完整数据流追踪
- XSS 的上下文感知分析
- 文件上传的完整路径分析
- 反序列化 gadget 链构造
- CSRF 的完整攻击链

Node.js CLI深度分析重点：
- 命令行参数的注入风险
- 文件操作的路径遍历
- 子进程执行的命令注入
- 依赖包的已知漏洞（npm audit）
- 配置文件解析的安全问题

Electron应用深度分析重点：
- IPC 消息的注入风险
- nodeIntegration 的 RCE 风险
- contextBridge 的安全暴露检查
- 外部协议的劫持风险
- preload 脚本的 XSS 风险
```

**输出**：
- 深度漏洞分析报告（分批次汇总）
- 利用链追踪（全局图谱）
- 风险等级评估（基于项目类型）

### Phase 4：报告生成（汇总阶段）

**目标**：标准化输出专业审计报告

**方法**：
- 模板渲染
- 统一报告格式
- 结构化数据输出

**汇总流程**：
```
1. 读取所有批次的分析结果 .codefree/codefree-code-audit/phase3/batch_*.json
2. 读取全局利用链图谱 .codefree/codefree-code-audit/phase3/exploit_chains.json
3. 合并所有漏洞，按以下维度分类：
   - 按严重程度：Critical、High、Medium、Low
   - 按项目类型：VSCode插件、Web应用、CLI、Electron
   - 按入口点：命令入口、HTTP入口、IPC入口
   - 按批次归属：B001、B002、B003...
4. 生成以下文件：
   - .codefree/codefree-code-audit/phase4/report.html（可视化审计报告）
   - .codefree/codefree-code-audit/phase4/vulnerabilities.json（结构化漏洞数据）
   - .codefree/codefree-code-audit/phase4/exploit_chains.json（完整利用链）
   - .codefree/codefree-code-audit/phase4/batch_summary.json（批次执行摘要）
```

**输出内容**：
- 漏洞详情与成因（按批次和入口点分类）
- 静态数据流证据
- 动态验证证据（如已验证）
- 修复建议

### Phase 5：自动化修复建议（汇总阶段）

**目标**：提供针对性的代码修复指导

**方法**：
- 补丁生成
- 安全代码示例
- 修复方案对比

**汇总流程**：
```
1. 读取所有漏洞报告 .codefree/codefree-code-audit/phase4/vulnerabilities.json
2. 基于项目类型生成修复建议：
   - VSCode插件：命令过滤、路径规范化、WebView CSP
   - Web应用：参数化查询、输出编码、输入验证
   - CLI：参数清洗、路径校验、子进程隔离
   - Electron：IPC 验证、contextBridge 限制、nodeIntegration 关闭
3. 生成以下文件：
   - .codefree/codefree-code-audit/phase5/patches.json（补丁代码）
   - .codefree/codefree-code-audit/phase5/before_after.json（修复前后对比）
   - .codefree/codefree-code-audit/phase5/test_cases.json（测试建议）
```

**输出**：
- 具体修复代码
- 修复前后对比
- 测试建议

---

## 三层审计架构

```
┌─────────────────────────────────────────────────────────┐
│ Layer 3: 语义追踪层          │
│ - 全链路推理流程图                                      │
│ - 利用链追踪                                            │
│ - 上下文关联分析                                        │
└─────────────────────────────────────────────────────────┘
┌─────────────────────────────────────────────────────────┐
│ Layer 2: AI加深度层（双快模型） │
│ - 语义理解                                              │
│ - 逻辑推理                                              │
│ - 复杂漏洞分析                                          │
└─────────────────────────────────────────────────────────┘
┌─────────────────────────────────────────────────────────┐
│ Layer 1: 机器打广层             │
│ - 规则引擎                                              │
│ - 正则匹配                                              │
│ - 快速扫描                                              │
└─────────────────────────────────────────────────────────┘
```

### Layer 1：机器打广

- **目标**：快速覆盖大量代码
- **方法**：规则引擎、正则匹配
- **优势**：执行速度快、覆盖范围广
- **局限**：误报率高、缺乏上下文理解

### Layer 2：AI加深度

- **目标**：深度分析复杂漏洞
- **方法**：语义理解、逻辑推理
- **优势**：精准识别、理解代码意图
- **局限**：需要上下文、计算成本高

### Layer 3：语义追踪层

- **目标**：全链路追踪利用链
- **方法**：全链路推理流程图、利用链追踪
- **优势**：完整攻击路径、上下文关联
- **局限**：计算成本最高

---

## EALOC资源分配公式

### 核心公式

```
EALOC = Effective Audit Lines of Code
       = LOC × 复杂度系数 × 风险系数 × 模块权重
```

### Tier分层机制

| Tier层级 | 特征描述 | Agent优先级 | 审计深度 |
|---------|---------|-----------|----------|
| **T1** | Controller层、认证授权、外部接口 | 最高 | 深度语义分析 |
| **T2** | Service层、业务逻辑、数据处理 | 高 | 中等深度分析 |
| **T3** | Entity/VO、工具类、配置文件 | 中 | 快速扫描 |

### 资源分配策略

- **单Agent预算**：15,000 LOC
- **大模块拆分**：当EALOC超过15,000时，自动拆分成多个子任务
- **成本优化**：通过EALOC公式，可减少67% Agent成本但不降质量

### 动态分组示例

```
# module-biz [21K LOC → 3个Agent]
# | 子任务 | Agent | 文件范围 | 文件数 | EALOC | 状态
---|--------|--------|----------|--------|-------|--------
1a | Agent 1a | controller/ | service/ | 147 | 7,000 | 完成
1b | Agent 1b | dao/ | mapper/ | utils/ | 280 | 8,500 | 完成
1c | Agent 1c | entity/ | vo/ | query/ | 500 | 5,500 | 部分完成
```

---

## 覆盖率保障机制

### Phase 2.5：覆盖率扫雷

这是整个流水线中最关键的设计，专门解决LLM"跳过不重要代码"的天然倾向。

### 1. 模板覆盖矩阵

**生成时机**：Phase 1侦察结束时

**贯穿生命周期**：整个审计生命周期

**矩阵结构**：

```
# | 模块路径 | LOC | EALOC | Controller类 | 风险评估 | 分组Agent | Phase状态
---|---------|-----|-------|--------------|----------|-----------|-----------
1 | mobile-auth | 5,208 | 5,208 | 6 | High | Agent 1 | 完成
2 | mobile-gateway | 12,988 | 7,580 | 8 | High | Agent 2 | 完成
3 | mobile-biz | 132,000 | 37,700 | 48 | High | Agent 3 | 部分完成
4 | mobile-common | 5,000 | 600 | 6 | Low | Agent 4 | 未开始
5 | mobile-parent | 8 | 0 | 1 | - | 跳过 | 无代码
```

**关键原则**：
- 每个子模块必须有一行记录
- 包括"看起来不重要"的模块：工具模块、纯POM、无代码模块
- 不能简单省略：省略了就没人知道它被跳过了
- 必须注明跳过原因：如"无代码"、"纯配置"、"已废弃"

### 2. 大模块拆分跟踪

**触发条件**：模块EALOC > 单Agent预算（15,000）

**拆分策略**：
- 按功能模块拆分（controller/、service/、dao/）
- 按文件类型拆分（entity/、vo/、query/）
- 确保每个子任务EALOC在合理范围内

**动态追踪表**：

```
# module-biz [21K LOC → 3个Agent]
# | 子任务 | Agent | 文件范围 | 文件数 | 状态 | 覆盖率 | 未完成数
---|--------|--------|----------|--------|------|--------|----------
1a | Agent 1a | controller/ | service/ | 147 | 完成 | 100% | 0
1b | Agent 1b | dao/ | mapper/ | utils/ | 280 | 完成 | 100% | 0
1c | Agent 1c | entity/ | vo/ | query/ | 500 | 部分完成 | 87% | 65
```

**自动触发机制**：
- Agent 3c覆盖率只有87%
- 意味着有65个文件没审完
- 门禁立即为这65个文件自动归为Agent
- 不是等所有模块都审完才发现

### 3. 文件覆盖率清单

**目的**：防止Agent"偷懒"

**问题场景**：
- Agent标记module-auth为"完成"
- 实际上只读了Controller层
- 跳过了Filter、配置文件、工具类

**解决方案**：

每个Agent的输出必须包含明确文件清单：

```
# 文件路径 | Tier | 状态 | 发现数 | 审计时间
---|-------------------|------|--------|--------|-----------
1 | .../controller/UserController.java | T1 | 完成 | 3 | 2026-03-12 10:00
2 | .../service/UserService.java | T2 | 完成 | 1 | 2026-03-12 10:05
3 | .../filter/AuthFilter.java | T1 | 未审计 | 0 | -
4 | .../config/SecurityConfig.java | T2 | 未审计 | 0 | -
5 | .../utils/StringUtils.java | T3 | 未审计 | 0 | -
```

**验证逻辑**：
- 对比清单与实际文件列表
- 发现未审计文件立即标记
- 强制Agent补全未审计文件

### 4. 实时状态更新

**关键原则**：
- 不是审完所有模块再统一报表
- 每完成一个Agent审计就立即更新对应行
- 任何时候都能查看当前进度

**状态流转**：

```
未开始 → 审计中 → 完成 → 待评审 → 已验证 → 已修复
```

---

## 反幻觉规则设计

### LLM幻觉类型

1. 编造代码片段：记得某个文件大概长什么样，但具体符号和变量名开始瞎猜
2. 编造调用链：审计报告中出现不存在的调用链
3. 错误行号：标注的漏洞行号实际不存在
4. 错误漏洞类型：把SQLi标记为XSS

### 反幻觉规则

#### 1. 中间结果持久化

**规则**：不信任LLM的记忆，所有中间结果都保存到文件

**实现**：

```
# Phase 1输出
.codefree/codefree-code-audit/phase1/scan_results.json

# Phase 2输出
.codefree/codefree-code-audit/phase2/key_paths.json
.codefree/codefree-code-audit/phase2/attack_surface.json

# Phase 2.5输出
.codefree/codefree-code-audit/phase2.5/coverage_matrix.csv
.codefree/codefree-code-audit/phase2.5/file_checklist.json

# Phase 3输出
.codefree/codefree-code-audit/phase3/vulnerability_analysis.json
.codefree/codefree-code-audit/phase3/exploit_chains.json
```

**优势**：
- 任何时候都可以重读恢复上下文
- 可以验证LLM输出是否基于真实代码
- 便于追踪和调试
- 支持外部测试脚本验证文件是否存在且内容合法

#### 2. 文件引用验证

**规则**：所有文件引用必须经过验证

**验证逻辑**：

```python
def validate_file_reference(file_path):
    # 1. 检查文件是否存在
    if not file_exists(file_path):
        return False, "文件不存在"

    # 2. 检查行号是否有效
    if line_number > file_line_count(file_path):
        return False, "行号超出范围"

    # 3. 检查代码片段是否匹配
    actual_code = read_code_snippet(file_path, line_number)
    if not code_matches(actual_code, claimed_code):
        return False, "代码片段不匹配"

    return True, "验证通过"
```

#### 3. 调用链追踪验证

**规则**：所有调用链必须能追溯到实际代码

**验证方法**：
- 使用AST（抽象语法树）分析
- 构建完整的调用图谱
- 验证每个节点是否存在

#### 4. 漏洞类型验证

**规则**：漏洞类型必须与代码特征匹配

**验证逻辑**：
- SQLi → 检查是否有SQL拼接
- XSS → 检查是否有用户输入输出
- RCE → 检查是否有命令执行
- 反序列化 → 检查是否有readObject/unserialize

---

## 多Agent协作机制

### Agent类型

#### 1. 侦察Agent

- 职责：项目结构分析、依赖识别、攻击面识别
- 输入：项目代码
- 输出：项目统计报表、模块列表、依赖树

#### 2. 扫描Agent

- 职责：基于规则的快速扫描
- 输入：代码文件、规则库
- 输出：扫描结果、潜在漏洞点

#### 3. 分析Agent

- 职责：深度语义分析、漏洞确认、利用链追踪
- 输入：扫描结果、代码上下文
- 输出：漏洞分析报告、利用链

#### 4. 验证Agent

- 职责：PoC生成、真实环境验证
- 输入：漏洞描述、代码上下文
- 输出：验证结果、PoC代码

### 协作模式

#### 串行模式

```
侦察Agent → 扫描Agent → 分析Agent → 验证Agent
```

- 适用场景：小型项目（<10K LOC）
- 优势：上下文连贯、资源占用少
- 劣势：速度慢

#### 并行模式

```
侦察Agent
    ↓
    ├→ 扫描Agent1 ─→ 分析Agent1 ─→ 验证Agent1
    ├→ 扫描Agent2 ─→ 分析Agent2 ─→ 验证Agent2
    └→ 扫描Agent3 ─→ 分析Agent3 ─→ 验证Agent3
```

- 适用场景：大型项目（>50K LOC）
- 优势：速度快、资源利用充分
- 劣势：需要协调、上下文共享

#### 混合模式

```
侦察Agent
    ↓
扫描Agent（并行）
    ↓
分析Agent（串行+并行混合）
    ↓
验证Agent（并行）
```

- 适用场景：中型项目（10K-50K LOC）
- 优势：平衡速度与质量
- 推荐：默认模式

### 状态同步

- 共享状态文件：`shared/state.json`
- 消息队列：Agent间通信（RabbitMQ/Kafka）
- 锁机制：防止并发冲突
- 心跳检测：监控Agent状态

---

## DKTSS评分体系

### 评分维度

#### D：Discoverability（可发现性）

- 漏洞被发现的难易程度
- 评分：1-10（10=最容易发现）

#### K：Knowledge（知识要求）

- 利用漏洞所需的知识水平
- 评分：1-10（10=最低知识要求）

#### T：Time（时间成本）

- 审计该漏洞所需时间
- 评分：1-10（10=时间成本最低）

#### S：Severity（严重程度）

- 漏洞的实际危害
- 评分：1-10（10=最严重）

#### S：Stability（稳定性）

- 利用成功率
- 评分：1-10（10=最稳定）

### 评分公式

```
总分 = (D + K + T) × (S × 0.5 + S_stability × 0.5)
```

### 分级标准

| 分数范围 | 等级 | 优先级 | 响应时间 |
|---------|------|--------|----------|
| 90-100 | P0 | 紧急 | 立即 |
| 70-89 | P1 | 高 | 24小时 |
| 50-69 | P2 | 中 | 1周 |
| 30-49 | P3 | 低 | 1月 |
| <30 | P4 | 极低 | 下个版本 |

---

## 质量保障机制

### 1. 三级验证

- L1：语法验证 - 代码是否能编译通过
- L2：逻辑验证 - 漏洞利用链是否完整
- L3：环境验证 - 真实环境中PoC能否触发

### 2. 人工抽查

- 随机抽查10%的审计结果
- 重点抽查高风险漏洞
- 记录抽查结果，优化规则

### 3. 持续学习

- 记录误报案例
- 更新规则库
- 优化评分体系

### 4. 回归测试

- 定期对已知漏洞进行回归测试
- 确保不会重复发现
- 验证修复方案有效性

---

## 工程实现建议

### 技术栈

- LLM：GLM等
- 规则引擎：自定义正则规则库
- 容器化：Docker用于验证环境
- 协调层：消息队列（RabbitMQ/Kafka）
- 存储：文件系统 + 数据库

### 目录结构

```
.codefree/codefree-code-audit/
├── phase0/           # 预处理结果
│   ├── stats.json
│   └── ealoc.csv
├── phase1/           # 安全扫描结果
│   ├── scan_results.json
│   └── known_vulns.json
├── phase2/           # 关键路径分析
│   ├── key_paths.json
│   └── attack_surface.json
├── phase2.5/         # 覆盖率扫雷
│   ├── coverage_matrix.csv
│   └── file_checklist.json
├── phase3/           # 深度语义分析
│   ├── vulnerabilities.json
│   └── exploit_chains.json
├── phase4/           # 报告生成
│   └── report.html
├── phase5/           # 修复建议
│   └── patches.json
└── shared/           # 共享状态
    └── state.json
```

### 配置文件

```json
{
  "agent_budget": 15000,
  "parallel_agents": 4,
  "phase_timeout": 3600,
  "coverage_threshold": 100,
  "false_positive_threshold": 0.1
}
```

---

## 最佳实践

### 1. 从小到大

- 先用小型项目（<5K LOC）验证流程
- 逐步扩大到中型项目（5K-50K LOC）
- 最后挑战大型项目（>50K LOC）

### 2. 持续监控

- 实时监控各Phase状态
- 及时发现并处理异常
- 定期生成审计报告

### 3. 迭代优化

- 根据实际效果调整参数
- 优化Agent协作模式
- 更新规则库和评分体系

### 4. 文档化

- 记录所有决策和配置
- 维护完整的审计日志
- 便于问题追踪和知识沉淀

---

## 常见问题

### Q1：如何处理超大项目（>100K LOC）？

**A**：
1. 使用多Agent并行模式
2. 按模块拆分，独立审计
3. 增加Phase 2.5的检查频率
4. 考虑分布式架构

### Q2：如何平衡速度与质量？

**A**：
1. 使用混合模式（串行+并行）
2. Tier分层，重点关注T1/T2
3. 设置合理的超时时间
4. 采用增量审计策略

### Q3：如何处理未知漏洞类型？

**A**：
1. 依赖Phase 3的语义分析
2. 使用Layer 3的语义追踪
3. 人工介入确认
4. 记录案例，更新规则库

### Q4：如何降低误报率？

**A**：
1. 实施Phase 2.5覆盖率扫雷
2. 使用真实环境PoC验证
3. 应用反幻觉规则
4. 人工抽查与持续学习

---

## 分批机制详细说明

### 为什么需要强制分批？

**核心问题**：LLM 上下文窗口有限，项目大了会丢失上下文

**症状表现**：
1. 漏洞发现率下降：大项目扫描出的漏洞数量明显少于实际应发现的
2. 覆盖率不完整：部分文件被跳过，特别是工具类、配置文件
3. 调用链断裂：跨文件的依赖关系无法完整追踪
4. 重复审计：同一文件可能被多次审计，浪费资源

**根本原因**：
1. LLM 无法记住之前处理过的所有文件
2. 没有强制性的覆盖率检查机制
3. 依赖项目人员手工判断批次大小，容易出现误判
4. 没有考虑到文件数和 LOC 的双重约束

### 分批规则（强制执行）

#### 规则1：文件数限制

```
条件：总文件数 > 50
批次大小：每批不超过 50 个文件
原因：文件多即使代码少，也会占用上下文
例外：单个批次如果 LOC < 2000，可以合并到下一批次
```

**示例**：
- 项目有 150 个文件
- 自动分成 3 批：B001(50个文件)、B002(50个文件)、B003(50个文件)

#### 规则2：代码行数限制

```
条件：总 LOC > 5000
批次大小：每批不超过 5000 行代码
原因：LOC 多的文件需要更多上下文理解
例外：如果是框架配置文件，可以单独批次不受此限制
```

**示例**：
- 项目有 20 个文件，共 15,000 行代码
- 按 LOC 分成 3 批：B001(5000行)、B002(5000行)、B003(5000行)

#### 规则3：复杂文件单独批次

```
条件：单文件 LOC > 1000
批次大小：单独成批
原因：复杂文件需要深度分析，不能与其他文件混在一起
标记：在批次清单中标注为"复杂文件"
```

**示例**：
- src/utils/BigProcessor.ts 有 2500 行代码
- 单独成批：B003_complex_file，优先审计

#### 规则4：框架配置文件优先批次

```
条件：package.json、pom.xml、composer.json、go.mod 等
批次大小：单独成批，优先于普通文件批次
原因：配置文件定义了项目结构、依赖、脚本，优先级最高
```

**示例**：
- package.json 单独成批：B001_config
- pom.xml 单独成批：B002_config
- 然后再处理普通代码文件

#### 规则5：入口点文件优先批次

```
条件：main.ts、app.js、extension.ts、index.go、Application.java 等
批次大小：单独成批，优先于普通文件批次
原因：入口点定义了攻击面，必须优先分析
```

**示例**：
- VSCode插件：extension.ts 单独成批：B003_entry
- Web应用：app.ts 单独成批：B004_entry
- 然后再处理 Controller、Service 等业务代码

### 批次规划示例

#### VSCode 插件项目（150 个文件，8,000 LOC）

```
B001_config（优先）
  - package.json
  - tsconfig.json
  - .vscodeignore
  文件数：3，LOC：150

B002_entry（优先）
  - src/extension.ts
  文件数：1，LOC：850

B003_complex_file（单独批次）
  - src/utils/BigProcessor.ts
  文件数：1，LOC：2500

B004（普通批次）
  - src/commands/*.ts
  文件数：15，LOC：1200

B005（普通批次）
  - src/views/*.ts
  文件数：25，LOC：1100

B006（普通批次）
  - src/providers/*.ts
  文件数：20，LOC：800

B007（普通批次）
  - src/utils/*.ts（除 BigProcessor.ts）
  文件数：30，LOC：700

B008（普通批次）
  - src/tests/*.ts
  文件数：45，LOC：600

B009（配置文件）
  - .vscode/*.json
  文件数：10，LOC：100

总计：9 个批次，每个批次都在合理范围内
```

#### Java Web 应用项目（300 个文件，50,000 LOC）

```
B001_config（优先）
  - pom.xml
  - application.yml
  - application.properties
  文件数：3，LOC：200

B002_entry（优先）
  - com/example/Application.java
  文件数：1，LOC：150

B003（Controller 层）
  - com/example/controller/*.java
  文件数：20，LOC：3000

B004（Service 层 - 批次1）
  - com/example/service/auth/*.java
  - com/example/service/user/*.java
  文件数：30，LOC：4500

B005（Service 层 - 批次2）
  - com/example/service/product/*.java
  - com/example/service/order/*.java
  文件数：35，LOC：4800

B006（DAO 层 - 批次1）
  - com/example/dao/mapper/*.java
  文件数：40，LOC：4200

B007（DAO 层 - 批次2）
  - com/example/dao/repository/*.java
  文件数：35，LOC：3900

B008（Entity 层）
  - com/example/entity/*.java
  文件数：60，LOC：5400

B009（VO/DTO 层）
  - com/example/vo/*.java
  - com/example/dto/*.java
  文件数：45，LOC：4800

B010（工具类）
  - com/example/utils/*.java
  文件数：26，LOC：2800

总计：10 个批次，每个批次都在合理范围内
```

### 批次执行流程

```
┌─────────────────────────────────────────────────────────────┐
│ Phase 0: 批次规划                                              │
│ - 读取所有文件列表                                            │
│ - 应用分批规则                                                │
│ - 生成批次清单 .codefree/codefree-code-audit/phase0/batches.json                     │
│ - 生成项目类型报告 .codefree/codefree-code-audit/phase0/project_type.json          │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│ Phase 1: 分批扫描                                            │
│ B001 → 保存结果 → 清空上下文 → B002 → 保存结果 → 清空上下文  │
│ ... → 最后汇总所有批次结果                                    │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│ Phase 2: 分批关键路径分析                                    │
│ 按批次顺序分析，记录跨批次依赖 .codefree/codefree-code-audit/phase2/dependencies.json│
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│ Phase 2.5: 批次覆盖率检查（强制）                            │
│ - 检查每个批次的文件覆盖率是否 100%                           │
│ - 发现遗漏立即标记                                           │
│ - 生成覆盖率报告 .codefree/codefree-code-audit/phase2.5/batch_coverage.json         │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│ Phase 3: 分批深度语义分析                                    │
│ 按拓扑顺序分析（先处理无依赖的批次）                          │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│ Phase 4: 汇总报告                                            │
│ 合并所有批次结果，生成最终报告                                │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│ Phase 5: 汇总修复建议                                        │
│ 生成修复补丁，基于项目类型定制                                │
└─────────────────────────────────────────────────────────────┘
```

### 批次执行最佳实践

#### 1. 上下文管理

```
每个批次必须执行的步骤：
1. 读取批次清单 .codefree/codefree-code-audit/phase0/batches.json
2. 读取项目类型报告 .codefree/codefree-code-audit/phase0/project_type.json
3. 读取上一批次的依赖关系（如存在）
4. 处理当前批次
5. 保存当前批次结果
6. 更新系统状态 .codefree/codefree-code-audit/phase*/progress.json
7. 清空 LLM 上下文（只保留批次清单和进度）
8. 继续下一批次
```

**测试与审查支持**：
- 所有步骤的中间结果必须写入 `.codefree/codefree-code-audit/` 目录
- 用户或外部工具可随时读取 progress.json 审视当前进度
- 若某步骤未生成对应文件，视为该步骤执行失败
- 支持断点续传：重新加载时可从已完成的批次继续

#### 2. 跨批次依赖追踪

```
依赖关系文件 .codefree/codefree-code-audit/phase2/dependencies.json：
{
  "B001": {
    "depends_on": [],
    "exports": ["ExtensionContext", "Configuration"]
  },
  "B002": {
    "depends_on": ["B001"],
    "reason": "ExtensionContext 来自 B001 的 extension.ts"
  },
  "B003": {
    "depends_on": ["B001", "B002"],
    "reason": "Configuration 来自 B001，Command 来自 B002"
  }
}

处理顺序：
- 先处理 B001（无依赖）
- 再处理 B002（依赖 B001，已完成）
- 最后处理 B003（依赖 B001、B002，均已完成）
```

#### 3. 批次完整性检查

```
每完成一个批次，立即检查：
1. 文件覆盖率：所有文件都被审计了吗？
2. 入口点覆盖率：所有入口点都被分析了吗？
3. 依赖完整性：依赖的批次都完成了吗？
4. 配置完整性：配置文件都审计了吗？

发现遗漏：
- 立即标记为"未审计"
- 在下一批次优先处理
- 不能等到最后再发现
```

**可审查性要求**：
- 完整性检查结果必须写入 `.codefree/codefree-code-audit/phase2.5/batch_coverage.json`
- 任何 `status: "incomplete"` 的批次必须列出 `missing_files`
- 用户可通过读取该文件直接审视哪些批次未通过检查
- AI 必须响应用户的审查指令，如"显示当前覆盖率"或"列出未审计文件"

#### 4. 进度追踪

```
系统状态文件 .codefree/codefree-code-audit/phase1/progress.json：
{
  "total_batches": 9,
  "completed_batches": 3,
  "current_batch": "B004",
  "overall_progress": "33%",
  "batches": {
    "B001": {"status": "completed", "files": 47, "loc": 1500},
    "B002": {"status": "completed", "files": 52, "loc": 1800},
    "B003": {"status": "completed", "files": 35, "loc": 1200},
    "B004": {"status": "in_progress", "files": 40, "loc": 1600},
    "B005": {"status": "pending", "files": 38, "loc": 1400},
    "B006": {"status": "pending", "files": 45, "loc": 1700}
  }
}

任何时候都能查看当前进度，确保不会遗漏
```

**进度可审视性**：
- progress.json 必须每完成一个批次就实时更新，不能等全部完成再写
- 状态字段必须是以下之一：`pending` / `in_progress` / `completed` / `incomplete`
- 用户发送"审计进度如何"时，AI 必须读取 progress.json 并汇报准确状态
- 支持外部脚本或工具轮询 progress.json 获取实时进度

### 分批机制的优势

#### 1. 100% 覆盖率保证

```
传统方式：
- 项目大 → LLM 记不住 → 随机跳过文件 → 覆盖率低

分批方式：
- 强制分批 → 每批都能完整审计 → 覆盖率 100%
```

#### 2. 上下文完整性

```
传统方式：
- 一次性加载所有文件 → 上下文溢出 → 后面的文件被忽略

分批方式：
- 每批文件少 → 上下文完整 → 所有文件都被充分分析
```

#### 3. 依赖关系清晰

```
传统方式：
- 所有文件混在一起 → 依赖关系混乱 → 调用链断裂

分批方式：
- 明确批次依赖 → 依赖关系清晰 → 调用链完整
```

#### 4. 可中断可恢复

```
传统方式：
- 中途失败 → 需要重新开始 → 资源浪费

分批方式：
- 每批独立 → 中断后可恢复 → 继续未完成的批次
```

#### 5. 优先级明确

```
传统方式：
- 所有文件同等对待 → 优先级不明确

分批方式：
- 配置文件、入口点优先 → 攻击面优先识别 → 高效审计
```

---

## 总结

AI代码审计工程化的核心是：

1. **系统化流程**：6阶段流水线，每个Phase有明确输入输出
2. **资源优化**：EALOC公式指导，减少67%成本不降质量
3. **覆盖率保障**：Phase 2.5确保100%覆盖，无遗漏
4. **质量保障**：反幻觉规则、真实环境验证、DKTSS评分
5. **工程化实现**：多Agent协作、中间结果持久化、标准化输出
6. **分批机制**：强制分批确保大项目也能100%覆盖，无遗漏
7. **项目类型识别**：前置识别项目类型，定制化审计策略
8. **入口点优先**：优先审计入口点，高效识别攻击面

通过这些机制，AI代码审计可以从"随机游走式"变成"系统化作战"，实现覆盖率100%、幻觉率趋近0的目标。