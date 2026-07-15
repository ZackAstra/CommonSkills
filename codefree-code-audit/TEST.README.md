# codefree-code-audit Skill 测试与审查指南

本文档说明如何测试 `codefree-code-audit` skill 是否正常工作，以及如何审查其执行过程、分批情况和进度状态。

---

## 1. 快速测试方法

### 1.1 触发 Skill

在任意代码项目目录下，向 AI 发送以下指令触发审计：

```
使用 codefree-code-audit 对这个项目进行安全审计
```

或指定参数：

```
使用 codefree-code-audit 审计 /path/to/project，审计类型 web
```

### 1.2 预期触发信号

Skill 正常触发时，AI 会：
1. 明确提及进入 **6 阶段审计流水线**（Phase 0 → Phase 5）
2. 开始执行 **Phase 0：代码预处理与类型识别**
3. 输出项目统计信息（文件数、LOC、项目类型）
4. 如果文件数 > 50 或 LOC > 5000，会明确说明**正在执行强制分批**

---

## 2. 如何查看进度

所有进度信息持久化在 `.codefree/codefree-code-audit/` 目录下，可随时查看。

### 2.1 查看整体进度

读取文件：

```bash
cat .codefree/codefree-code-audit/phase1/progress.json
```

预期内容示例：

```json
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
    "B005": {"status": "pending", "files": 38, "loc": 1400}
  }
}
```

**状态含义**：
- `completed`：该批次已完成审计
- `in_progress`：该批次正在审计中
- `pending`：该批次等待执行
- `incomplete`：该批次覆盖率不足，需要补审

### 2.2 询问 AI 当前进度

直接向 AI 提问：

```
审计进度如何？当前在哪个 Phase？完成了多少批次？
```

AI 应当能根据 `progress.json` 回答准确的进度信息。

---

## 3. 如何查看分批情况

### 3.1 查看批次规划

```bash
cat .codefree/codefree-code-audit/phase0/batches.json
```

预期看到类似以下结构：

```json
{
  "total_files": 150,
  "total_loc": 8000,
  "batch_rule_applied": true,
  "batches": [
    {
      "id": "B001",
      "type": "config",
      "priority": "high",
      "files": ["package.json", "tsconfig.json"],
      "loc": 150
    },
    {
      "id": "B002",
      "type": "entry",
      "priority": "high",
      "files": ["src/extension.ts"],
      "loc": 850
    },
    {
      "id": "B003",
      "type": "complex",
      "priority": "normal",
      "files": ["src/utils/BigProcessor.ts"],
      "loc": 2500
    },
    {
      "id": "B004",
      "type": "normal",
      "priority": "normal",
      "files": ["src/commands/*.ts"],
      "loc": 1200
    }
  ]
}
```

**分批规则检查点**：
- 文件数 > 50 是否被拆分？
- LOC > 5000 是否被拆分？
- 单文件 > 1000 行是否单独成批？
- 配置文件（package.json 等）是否优先批次？
- 入口点文件（main.ts、extension.ts 等）是否优先批次？

### 3.2 查看当前批次的扫描结果

```bash
ls .codefree/codefree-code-audit/phase1/batch_*.json
```

每个批次应有独立的 `batch_B00X_scan.json` 文件。

---

## 4. 如何审查覆盖率

### 4.1 查看批次覆盖率报告

```bash
cat .codefree/codefree-code-audit/phase2.5/batch_coverage.json
```

预期内容：

```json
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

**审查要点**：
- 每个批次的 `coverage_rate` 是否为 `100%`
- `status` 为 `incomplete` 时，`missing_files` 是否被列出
- AI 是否对 `incomplete` 批次进行了补审

### 4.2 查看文件级检查清单

```bash
cat .codefree/codefree-code-audit/phase2.5/file_checklist.json
```

预期看到每个文件的审计状态：

```json
[
  {
    "file": "src/controller/UserController.java",
    "tier": "T1",
    "status": "audited",
    "findings": 3,
    "audit_time": "2026-04-30 10:00"
  },
  {
    "file": "src/filter/AuthFilter.java",
    "tier": "T1",
    "status": "unaudited",
    "findings": 0,
    "audit_time": null
  }
]
```

---

## 5. 如何审查跨批次依赖

```bash
cat .codefree/codefree-code-audit/phase2/dependencies.json
```

预期内容：

```json
{
  "B001": {
    "depends_on": [],
    "exports": ["ExtensionContext", "Configuration"]
  },
  "B002": {
    "depends_on": ["B001"],
    "reason": "ExtensionContext 来自 B001 的 extension.ts"
  }
}
```

**审查要点**：
- 依赖关系是否合理
- 是否按拓扑顺序处理（先处理无依赖的批次）
- 依赖的批次是否都已完成

---

## 6. 测试检查清单

在审计过程中，逐项确认以下检查点：

| 检查项 | 验证方法 | 通过标准 |
|-------|---------|---------|
| Skill 正常触发 | AI 提及 6 阶段流水线 | AI 明确输出 Phase 0-5 流程 |
| Phase 0 执行 | 查看 `phase0/batches.json` | 文件存在且包含批次规划 |
| 强制分批生效 | 查看 `phase0/batches.json` | 文件数>50 或 LOC>5000 时被拆分 |
| 优先批次 | 查看 `phase0/batches.json` | 配置文件和入口点文件在优先批次 |
| Phase 1 进度 | 查看 `phase1/progress.json` | 每完成一个批次状态更新为 completed |
| 覆盖率检查 | 查看 `phase2.5/batch_coverage.json` | 所有批次 coverage_rate 为 100% |
| 文件清单 | 查看 `phase2.5/file_checklist.json` | 每个文件都有明确的审计状态 |
| 依赖追踪 | 查看 `phase2/dependencies.json` | 跨批次依赖关系被记录 |
| 中间结果持久化 | 查看 `.codefree/codefree-code-audit/` 目录 | 每个 phase 都有对应的输出文件 |
| 漏洞输出 | 查看 `.codefree/codefree-code-audit/findvulns/` | 每个漏洞有独立文件夹和报告 |

---

## 7. 常见问题排查

### 7.1 Skill 没有触发

- 确认指令中是否包含关键词：代码审计、安全审计、漏洞挖掘、audit 等
- 确认 skill 是否已正确安装到 skills 目录

### 7.2 没有生成分批文件

- 确认项目文件数是否 <= 50 且 LOC <= 5000（小项目可能不需要分批）
- 检查 AI 是否正确执行了 Phase 0

### 7.3 进度文件未更新

- 向 AI 明确要求："请更新 progress.json 并保存当前批次结果"
- 检查 `.codefree/codefree-code-audit/` 目录是否有写入权限

### 7.4 覆盖率不足 100%

- 向 AI 要求："请检查 batch_coverage.json，对 incomplete 的批次进行补审"
- 确认 AI 是否正确执行了 Phase 2.5 覆盖率扫雷

---

## 8. 自动化测试脚本（可选）

以下脚本可用于快速验证审计结果结构：

```bash
#!/bin/bash
# test-audit-structure.sh

AUDIT_DIR=".codefree/codefree-code-audit"

echo "=== 检查审计目录结构 ==="

# 检查必需的文件和目录
files=(
  "$AUDIT_DIR/phase0/batches.json"
  "$AUDIT_DIR/phase0/project_type.json"
  "$AUDIT_DIR/phase1/progress.json"
  "$AUDIT_DIR/phase2.5/batch_coverage.json"
  "$AUDIT_DIR/phase2.5/file_checklist.json"
)

for f in "${files[@]}"; do
  if [ -f "$f" ]; then
    echo "[OK] $f"
  else
    echo "[MISSING] $f"
  fi
done

echo ""
echo "=== 检查批次文件 ==="
ls -1 $AUDIT_DIR/phase1/batch_*.json 2>/dev/null || echo "[MISSING] 无批次扫描结果文件"

echo ""
echo "=== 检查漏洞输出 ==="
ls -1 $AUDIT_DIR/findvulns/ 2>/dev/null || echo "[MISSING] 无漏洞输出目录"

echo ""
echo "=== 检查覆盖率 ==="
if [ -f "$AUDIT_DIR/phase2.5/batch_coverage.json" ]; then
  python3 -c "
import json
with open('$AUDIT_DIR/phase2.5/batch_coverage.json') as f:
    data = json.load(f)
for batch, info in data.items():
    status = 'OK' if info.get('coverage_rate') == '100%' else 'FAIL'
    print(f'[{status}] {batch}: {info.get(\"coverage_rate\", \"N/A\")}')
"
fi
```

---

## 9. 向 AI 提出的审查指令

在审计过程中，你可以随时向 AI 发送以下指令来审查状态：

```
# 查看当前进度
请显示当前审计进度，包括已完成和待完成的批次。

# 查看分批详情
请显示批次规划详情，包括每个批次的文件数、LOC 和优先级。

# 查看覆盖率
请检查 batch_coverage.json，确认是否有未覆盖的文件。

# 查看文件清单
请显示 file_checklist.json 中状态为 unaudited 的文件。

# 查看依赖关系
请显示跨批次依赖关系，确认处理顺序是否正确。

# 强制补审
B002 批次覆盖率不足，请对 missing_files 进行补审并更新结果。
```

---

## 10. 目录结构速查

```
.codefree/codefree-code-audit/
├── phase0/
│   ├── batches.json          ← 批次规划（查看分批）
│   └── project_type.json     ← 项目类型识别
├── phase1/
│   ├── progress.json         ← 整体进度（查看进度）
│   ├── batch_B001_scan.json  ← 批次扫描结果
│   ├── batch_B002_scan.json
│   ├── scan_results.json
│   ├── known_vulns.json
│   └── risk_points.json
├── phase2/
│   ├── batch_B001_paths.json
│   ├── dependencies.json     ← 跨批次依赖
│   ├── key_paths.json
│   └── attack_surface.json
├── phase2.5/
│   ├── batch_coverage.json   ← 批次覆盖率（查看覆盖率）
│   ├── coverage_matrix.csv
│   └── file_checklist.json   ← 文件级清单
├── phase3/
│   ├── batch_B001_analysis.json
│   ├── exploit_chains.json
│   └── vulnerability_analysis.json
├── phase4/
│   ├── report.html
│   ├── vulnerabilities.json
│   └── batch_summary.json
├── phase5/
│   ├── patches.json
│   ├── before_after.json
│   └── test_cases.json
├── shared/
│   └── state.json            ← 多Agent共享状态
└── findvulns/                ← 漏洞输出目录
    ├── VULNS-001/
    │   ├── 漏洞报告.md
    │   └── poc.py
    └── CodeFreeCodeAuditReport.md
```
