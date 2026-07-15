---
name: codefree-code-audit
description: |
  CodeFree安全研究方法论体系 - 提供结构化的代码安全审计思维框架和实践指导。

  Use this skill when:
  - CTF竞赛需要系统化解题方法论支持
  - 红队攻防场景需要完整的攻击链规划思路
  - 代码审计工作依赖Source-Sink分析模型
  - AI驱动的代码审计需要工程化流程与覆盖率保障机制
  - 恶意软件逆向分析需要系统性方法指导
  - 安全研究和漏洞挖掘需要结构化思维框架
  - 分析漏洞攻击路径（涵盖Web注入、反序列化、二进制、域渗透等领域）
  - 研究安全防护绕过技术（包括WAF、EDR、沙箱等）

  Triggers: LLM安全、智能体审计、自动化审计、PoC验证、覆盖率保障、Fuzzing、二进制安全、反序列化、域渗透、横向移动、提权、免杀、WAF绕过、逆向分析、CTF、红队攻防、代码审计、渗透测试、安全研究、漏洞挖掘
license: MIT
---

# 代码安全审计方法论

本技能提供CodeFree提炼的代码安全审计方法论框架，涵盖漏洞挖掘、安全研究、代码审计、红队攻防等多个领域的系统性思维体系。

## About This Skill

本技能是一个模块化、自包含的安全研究方法论包，通过提供专业化的工作流程、分析模型和领域知识，将通用AI代理转变为配备程序化知识的专业安全研究助手。它专注于提供结构化的思考框架和方法论指导，而非基础安全知识传授。

## What This Skill Provides

1. **结构化思维框架** - 安全研究思维金字塔（L1-L4四层级）和通用决策循环
2. **跨领域核心公式** - 覆盖Web安全、代码审计、二进制安全、域渗透等领域的漏洞分析公式
3. **领域专项参考** - 针对Web注入、反序列化、二进制、逆向分析、Fuzzing等专项技术的详细方法论
4. **AI代码审计工程** - 6阶段流水线、覆盖率保障、质量保障体系
5. **实战案例索引** - 按技术和CVE分类的案例库

## Core Principles

### Concise is Key

本技能聚焦于方法论框架和思维模型，避免冗余的基础知识讲解。假设使用者已具备基础安全知识，仅提供需要结构化的高级方法论和实战经验总结。

### Progressive Disclosure

本技能采用三级加载系统管理上下文：
1. **元数据**（name + description）- 始终在上下文中（~100词）
2. **SKILL.md主体** - 技能触发时加载（<5k词）
3. **参考资源**（references/）- 根据需要按需加载

## Anatomy of This Skill

```
codefree-code-audit/
├── SKILL.md (required)
│   ├── YAML frontmatter metadata
│   └── Markdown instructions
└── references/
    ├── web-injection.md
    ├── deserialization.md
    ├── binary-exploitation.md
    ├── domain-pentest.md
    ├── code-audit.md
    ├── ai-code-audit-pipeline.md
    ├── ai-code-audit-poc-verification.md
    ├── poc-validation-by-project-type.md  （新增）
    ├── fuzzing.md
    ├── privilege-escalation.md
    ├── rce-persistence.md
    ├── redteam-ctf.md
    ├── reverse-engineering.md
    └── case-index.md
```

### SKILL.md

包含核心方法论框架、元思考模型、决策循环和快速导航指引。

### References (references/)

按领域组织的详细方法论文档，仅在Claude确定需要时加载：
- **领域专项**：web-injection.md, binary-exploitation.md, reverse-engineering.md等
- **工程方法**：ai-code-audit-engineering.md, ai-code-audit-cases.md
- **案例索引**：case-index.md

## Core Framework

### Meta-Thinking Pyramid

```
┌─────────────────────────────────────────────────────────────────────────┐
│                        安全研究思维金字塔                                │
├─────────────────────────────────────────────────────────────────────────┤
│  L4: 防御反推    ← 依据补丁/过滤规则/安全机制反推绕过路径                │
│  L3: 边界探索    ← 在已知攻击面中挖掘边界异常情况                        │
│  L2: 假设验证    ← 构建推理链条并逐步验证假设                            │
│  L1: 攻击面识别  ← 定位数据与指令未分离的接口                            │
└─────────────────────────────────────────────────────────────────────────┘
```

### Decision Loop

```
输入定位 → 上下文解析 → 假设构建 → payload生成 → 响应评估 → 循环优化
     ↑                                                              │
     └──────────────────────────────────────────────────────────────┘
```

### Cross-Domain Core Formulas

| 领域 | 核心公式 | 关键要点 |
|------|----------|----------|
| **通用** | 漏洞 = 边界失控 + 状态不一致 + 信任假设违背 | 揭示所有漏洞的根本原因 |
| **代码审计** | 漏洞 = Source可达Sink && 无有效Sanitizer | 基于污点传播分析 |
| **AI代码审计** | 审计 = 6阶段流水线 + 覆盖率保障 + 真实环境验证 | 消除幻觉、实现100%覆盖 |
| **二进制** | 利用 = 信息泄露 + 原语构造 + 控制流劫持 | 原语的组合与放大效应 |
| **域渗透** | 攻击 = 信任链逐级瓦解 | 委派配置错误导致整域沦陷 |

## 执行流程

### 第一阶段：审计准备

1. **Git 状态检测与扫描目标确定**
   - 检查当前目录是否为 git 仓库
   - 获取变动文件列表（包含未暂存和已暂存的变更）：
     * `git diff --name-only`
     * `git diff --cached --name-only`
   - **若存在变动文件** → 仅将变动文件作为审计目标，同时识别变动涉及的模块和依赖影响范围
   - **若不存在变动文件** → 扫描整个项目，执行全量审计
   - 确定审计目标路径（默认：当前目录）
   - 识别项目类型（Web应用、VSCode插件、CLI工具、Electron应用、二进制、库文件等）
   - 确定审计范围和优先级

2. **应用元思考框架**
   - L1: 攻击面识别 - 定位数据与指令未分离的接口
   - L2: 假设验证 - 构建推理链条并逐步验证假设
   - L3: 边界探索 - 在已知攻击面中挖掘边界异常情况
   - L4: 防御反推 - 依据补丁/过滤规则/安全机制反推绕过路径

3. **选择审计方法论**
   根据项目类型选择对应模块：
   - Web注入漏洞 → references/web-injection.md
   - 反序列化漏洞 → references/deserialization.md
   - 二进制安全 → references/binary-exploitation.md
   - 域渗透/内网 → references/domain-pentest.md
   - 代码审计 → references/code-audit.md
   - AI代码审计工程 → references/ai-code-audit-pipeline.md
   - AI代码审计实战 → references/ai-code-audit-poc-verification.md
   - 逆向分析 → references/reverse-engineering.md
   - Fuzzing → references/fuzzing.md
   - 提权/绕过 → references/privilege-escalation.md
   - 红队/CTF → references/redteam-ctf.md

### 第二阶段：深度审计

4. **Source-Sink分析**
   - 识别数据输入点（Source）
   - 追踪数据流向（若为增量审计，重点分析变动文件引入的新Source/Sink及既有依赖影响）
   - 定位危险操作点（Sink）
   - 检查Sanitizer有效性

5. **决策循环执行**
   - 输入定位 → 上下文解析 → 假设构建 → payload生成 → 响应评估 → 循环优化

6. **参考案例索引**
   - 检索相关CVE或技术的具体实战案例
   - 应用已知漏洞模式
   - 构建针对性测试场景

### 第三阶段：漏洞输出

7. **创建输出目录**
   - 在目标路径下创建 `./.codefree/codefree-code-audit/findvulns` 文件夹
   - 为每个发现的漏洞创建独立子文件夹

8. **生成漏洞报告**
   每个漏洞文件夹包含：
   - `漏洞报告.md` - 中文详细漏洞报告，包括：
     * 漏洞名称
     * 漏洞等级（严重/高危/中危/低危）
     * 漏洞描述
     * 影响范围
     * 技术细节
     * 复现步骤
     * 修复建议
   - `poc.py` / `poc.sh`等 - PoC可执行脚本

9. **生成总览报告**
   - 生成 `CodeFreeCodeAuditReport.md` 汇总报告
   - 包含漏洞统计、风险评级、修复优先级。生成最终报告后需要询问用户是否启动一键修复。

## 输出规范

### ./.codefree/codefree-code-audit/findvulns/ 目录结构

```
./.codefree/codefree-code-audit/findvulns/
├── VULNS-001/
│   ├── 漏洞报告.md
│   ├── poc.py
│   └── payload.txt
├── VULNS-002/
│   ├── 漏洞报告.md
│   ├── poc.sh
│   └── exploit.py
└── CodeFreeCodeAuditReport.md
```

### 漏洞报告模板

```markdown
# [漏洞名称]

## 漏洞等级
严重 / 高危 / 中危 / 低危

## 漏洞描述
[详细描述漏洞的技术原理和攻击方式]

## 影响范围
- 受影响版本：[版本信息]
- 影响组件：[组件名称]
- 影响场景：[使用场景]

## 技术细节
- 漏洞类型：[类型]
- 攻击向量：[攻击路径]
- 利用条件：[前置条件]

## 复现步骤
1. [步骤1]
2. [步骤2]
3. [步骤3]

## 修复建议
- [具体修复方案]
- [代码示例]
- [验证方法]

## 参考
- [相关CVE]
- [技术文档链接]
```

## 质量保障

- **Git 智能切换**：自动检测 git 变动状态，有变动则聚焦增量文件，无变动则执行全量审计
- **覆盖率保障**：确保审计覆盖所有关键文件和代码路径（增量审计需覆盖变动文件及其直接影响域）
- **反幻觉验证**：中间结果持久化 + 真实环境验证 + 文件引用验证
- **三级验证**：机器扫描 → AI深度分析 → 人工复核
- **PoC验证**：所有漏洞报告必须包含可执行的验证脚本

## 参数说明

- **目标路径**：待审计的项目路径（可选，默认当前目录）
- **审计类型**：指定审计类型（可选，如 web、binary、general）
- **输出目录**：指定输出目录（可选，默认 ./.codefree/codefree-code-audit/findvulns）

## Quick Navigation

根据具体研究场景选择对应的方法论模块：

| 场景 | 参考文档 | 核心方法 |
|------|----------|----------|
| Web注入漏洞 | [references/web-injection.md](references/web-injection.md) | 语义差异利用、WAF绕过策略树 |
| 反序列化漏洞 | [references/deserialization.md](references/deserialization.md) | Gadget链构造、版本边界速查 |
| 二进制安全 | [references/binary-exploitation.md](references/binary-exploitation.md) | ROP谱系、House of系列 |
| 域渗透/内网 | [references/domain-pentest.md](references/domain-pentest.md) | 委派攻击、持久化矩阵 |
| 代码审计 | [references/code-audit.md](references/code-audit.md) | Source-Sink模型、框架审计 |
| AI代码审计工程 | [references/ai-code-audit-pipeline.md](references/ai-code-audit-pipeline.md) | 6阶段流水线、强制分批机制、项目类型识别、EALOC分配、覆盖率保障 |
| AI代码审计实战 | [references/ai-code-audit-poc-verification.md](references/ai-code-audit-poc-verification.md) | PoC验证、多Agent协作、真实环境验证 |
| **基于项目类型的 PoC 验证** | [references/poc-validation-by-project-type.md](references/poc-validation-by-project-type.md) | **VSCode插件/Web/CLI/Electron的定制化验证策略** |
| 逆向分析 | [references/reverse-engineering.md](references/reverse-engineering.md) | VM对抗、沙箱绕过六维度 |
| Fuzzing | [references/fuzzing.md](references/fuzzing.md) | 目标选择矩阵、覆盖率驱动 |
| 提权/绕过 | [references/privilege-escalation.md](references/privilege-escalation.md) | 免杀技术层次、EDR规避 |
| 红队/CTF | [references/redteam-ctf.md](references/redteam-ctf.md) | 完整攻击链、云安全 |
| 案例索引 | [references/case-index.md](references/case-index.md) | 按技术/CVE分类的案例库 |

## Usage Guide

1. **明确研究目标**：确定要分析的漏洞类型或具体攻击场景
2. **查阅对应模块**：根据快速导航表选择合适的方法论文档
3. **应用元思考框架**：利用L1-L4思维金字塔指导分析全过程
4. **参考案例索引**：检索相关CVE或技术的具体实战案例
5. **AI审计场景**：
   - **强制执行分批机制**：大项目必须分批，每批不超过 50 个文件或 5000 行代码
   - **前置识别项目类型**：不要默认认为是 web 项目，先识别是 Web、VSCode插件、CLI 还是其他类型
   - **优先审计入口点**：配置文件、入口点文件必须单独批次优先审计
   - **严格覆盖率检查**：Phase 2.5 必须检查每个批次的覆盖率是否达到 100%
   - **使用 6 阶段流水线**：Preprocessing → Scan → KeyPath → CoverageSweep → DeepSemantics → Report → Fix
6. **持续迭代优化**：根据实际情况动态调整研究策略

**重要提醒**：
- **不要默认假设项目类型**：TS 项目不一定是 Web，可能是 VSCode 插件、Electron 应用或 Node.js CLI
- **强制分批**：文件数 > 50 或 LOC > 5000 必须分批，否则会导致覆盖率不足
- **入口点优先**：package.json、extension.ts、main.ts 等入口点必须优先审计
- **覆盖率 100%**：Phase 2.5 扫雷阶段必须确保所有批次覆盖率 100%，不能有遗漏

## Meta-Thinking Principles

### 1. 假设-验证循环
安全研究的核心流程：提出假设 → 实施测试 → 持续迭代优化

### 2. 边界条件思维
边界异常情况是各类漏洞的共同滋生点

### 3. 防御反推
从已知防御措施逆向推导攻击路径是高效研究策略

### 4. 链式思维
单一漏洞价值有限，只有漏洞链组合才能实现完整攻击

### 5. 版本敏感性
同一漏洞在不同版本需要采用不同的利用方法

### 6. 语义差异
不同组件对同一输入的解析差异是实现绕过的关键

### 7. 工程化思维
AI代码审计必须依赖系统化流程，不能单纯依赖LLM的随机能力

## Key Insights

### Web安全
- 漏洞根源：数据与指令未能正确分离
- JNDI版本边界：JDK 8u191 之后需要采用不同的利用路径
- WAF绕过核心：利用语义差异

### 反序列化
- 核心理念："万物皆可Gadget"，任何Serializable类都可能成为利用链的一环
- 二次反序列化是协议降级的关键突破口（SignedObject）
- 黑名单策略必有遗漏，代理封装是高版本绕过的通用思路

### 二进制安全
- 利用链本质：原语的组合与放大
- glibc版本决定可用技术栈（2.27引入tcache、2.32启用safe-linking）
- IO利用演进：vtable检查之后，_wide_data成为新的突破口

### 域渗透
- SPN查询优于端口扫描（精度更高且更隐蔽）
- 委派配置错误可能导致整个域被攻陷
- 最隐蔽的攻击往往利用合法的域功能而非直接利用漏洞

### 逆向分析
- 逆向本质：信息熵降低的过程
- VM保护破解三路径：opcode还原、z3约束求解、插桩爆破
- Triton + Z3 + AI 构成 OLLVM 反混淆的现代范式

### 红队攻防
- 完整攻击链：边界突破→权限提升→内网穿透→横向移动→域控夺取→持久化维持
- "内网密码复用"是基于经验驱动的横向移动关键
- 云原生新攻击面：K8S hostPath 滥用 + tolerations 配置错误

### AI代码审计
- 核心本质：为LLM配备"资深审计员的工作框架"
- Skill定位：编码工作方法和质量标准，而非知识传授
- **强制分批机制**：文件数 > 50 或 LOC > 5000 必须分批，确保大项目覆盖率 100%
- **项目类型识别前置**：Phase 0 必须先识别项目类型（Web/VSCode插件/CLI/Electron等），不能默认是 Web
- **入口点优先审计**：配置文件和入口点文件必须单独批次优先审计，高效识别攻击面
- 覆盖率机制：模板覆盖矩阵 + 文件清单 + 实时状态追踪（Phase 2.5）
- 反幻觉策略：中间结果持久化 + 真实环境验证 + 文件引用验证
- 资源优化：EALOC公式 + Tier分层 + 动态分组（成本降低67%）
- 质量保障：Phase 2.5扫雷 + DKTSS评分 + PoC验证 + 三级验证体系
- 6阶段流水线：预处理→扫描→关键路径→覆盖扫雷→深度语义→报告生成→修复建议
- 三层架构：Layer1机器广度扫描 + Layer2 AI深度分析 + Layer3语义追踪
