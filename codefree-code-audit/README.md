# CodeFree Code Audit

AI 驱动的代码安全审计解决方案，提供结构化的漏洞挖掘方法论、工程化审计流水线和可验证的质量保障机制。

---

## 功能概述

- **6 阶段审计流水线**：Preprocessing → Scan → KeyPath → CoverageSweep → DeepSemantics → Report → Fix
- **强制分批机制**：大项目自动拆分批次，确保上下文不溢出、覆盖率 100%
- **项目类型自动识别**：支持 Web 应用、VSCode 插件、Node.js CLI、Electron 应用、微服务等
- **覆盖率扫雷（Phase 2.5）**：专门解决 LLM 跳过"不重要"代码的倾向，强制检查每个批次覆盖率
- **反幻觉设计**：所有中间结果持久化到文件系统，支持断点续传和外部审查
- **多 Agent 协作**：侦察、扫描、分析、验证四类 Agent 串行/并行/混合协作
- **DKTSS 评分体系**：从可发现性、知识要求、时间成本、严重程度、稳定性五个维度量化漏洞
- **PoC 验证**：所有漏洞报告必须包含可执行的验证脚本
- **增量审计**：自动检测 git 变动，支持仅审计变更文件及其影响域

---

## 组成部分

本产品为单一 Skill 包，所有功能自包含：

| 组成部分 | 类型 | 作用 | 安装路径 |
|---------|------|------|---------|
| `codefree-code-audit` | **Skill** | 核心方法论、领域知识库、执行流程、输出规范，提供完整审计框架和参考文档 | `skills/codefree-code-audit/` |

> Skill 已内含完整的执行流程（审计准备→深度审计→漏洞输出）、输出规范、质量保障和参数说明，无需额外安装 Command 文件。

---

## Skill

### 作用

Skill 是核心方法论、执行流程和知识库，为 AI 提供结构化的审计思维框架、领域专项知识、工程化流程约束、输出规范和质量保障。它包含完整的审计执行流程（审计准备→深度审计→漏洞输出），可直接响应用户审计指令。

### 目录结构

```
codefree-code-audit/
├── SKILL.md                          # 核心方法论框架、元思考模型、决策循环、执行流程、输出规范
├── TEST.README.md                    # 测试与审查指南
└── references/                       # 领域专项参考文档（按需加载）
    ├── ai-code-audit-pipeline.md     # 6 阶段流水线、分批机制、覆盖率保障
    ├── ai-code-audit-poc-verification.md  # PoC 验证、多 Agent 协作
    ├── poc-validation-by-project-type.md  # 按项目类型的定制化验证策略
    ├── code-audit.md                 # Source-Sink 模型、框架审计
    ├── web-injection.md              # Web 注入、WAF 绕过
    ├── deserialization.md            # 反序列化、Gadget 链
    ├── binary-exploitation.md        # 二进制安全、ROP
    ├── reverse-engineering.md        # 逆向分析
    ├── domain-pentest.md             # 域渗透、内网横向移动
    ├── privilege-escalation.md       # 提权、EDR 规避
    ├── redteam-ctf.md                # 红队攻防、CTF
    ├── fuzzing.md                    # Fuzzing 策略
    ├── rce-persistence.md            # RCE、持久化
    └── case-index.md                 # 按 CVE/技术分类的案例库
```

### 核心能力

| 能力 | 说明 | 所在文档 |
|------|------|---------|
| 6 阶段流水线 | Phase 0-5 标准化审计流程 | `ai-code-audit-pipeline.md` |
| 强制分批机制 | 文件数>50 或 LOC>5000 自动分批 | `ai-code-audit-pipeline.md` |
| 项目类型识别 | Web/VSCode 插件/CLI/Electron 自动识别 | `ai-code-audit-pipeline.md` |
| 覆盖率扫雷 | Phase 2.5 强制检查每个批次覆盖率 100% | `ai-code-audit-pipeline.md` |
| 反幻觉规则 | 中间结果持久化 + 文件引用验证 | `ai-code-audit-pipeline.md` |
| EALOC 资源分配 | 有效审计代码行数公式，优化 Agent 成本 | `ai-code-audit-pipeline.md` |
| DKTSS 评分 | 漏洞五维量化评分体系 | `ai-code-audit-pipeline.md` |
| 多 Agent 协作 | 侦察/扫描/分析/验证 Agent 串并行协作 | `ai-code-audit-pipeline.md` |
| 项目类型 PoC 验证 | VSCode 插件/Web/CLI/Electron 定制化验证 | `poc-validation-by-project-type.md` |

### 过程文件目录

所有审计中间结果持久化在 `.codefree/codefree-code-audit/`，支持外部工具检查和人工审视：

```
.codefree/codefree-code-audit/
├── phase0/           # 批次规划、项目类型识别
├── phase1/           # 安全扫描结果、进度状态
├── phase2/           # 关键路径、跨批次依赖
├── phase2.5/         # 覆盖率扫雷、文件检查清单
├── phase3/           # 深度语义分析、利用链
├── phase4/           # 审计报告
├── phase5/           # 修复建议
├── shared/           # 多 Agent 共享状态
└── findvulns/        # 漏洞输出
```

---

## 安装

### 单一 Skill 安装

```
skills/
└── codefree-code-audit/                # Skill 目录
    ├── SKILL.md                         # 核心方法论 + 执行流程 + 输出规范
    ├── TEST.README.md
    └── references/
        └── ...
```

> Skill 已自包含所有功能（方法论、执行流程、输出规范、质量保障），无需额外安装 Command 文件。

### 安装路径

根据你的 AI 平台要求，将文件放置到对应的 skills 目录：

- **CodeFree插件**: `~/.codefree/common/config/skills/`
- **其他平台**: 参考对应平台的 skill 安装文档

---

## 测试与审查

Skill 内置完整的可测试性和可审查性设计：

- 所有过程文件对用户透明，可随时读取
- 支持外部脚本轮询 `progress.json` 获取实时进度
- 支持发送审查指令让 AI 汇报当前状态

详见 `TEST.README.md`：
- 如何验证 Skill 是否正常触发
- 如何查看分批详情和进度状态
- 如何审查覆盖率是否达到 100%
- 自动化测试脚本示例
- 可向 AI 发送的审查指令集合

---

## 触发关键词

用户消息中包含以下关键词时，建议激活本产品：

代码审计、安全审计、漏洞挖掘、audit、code review、security scan、渗透测试、红队、CTF、漏洞验证、PoC、代码安全、注入、反序列化、XSS、SQLi、RCE

---

## License

MIT
