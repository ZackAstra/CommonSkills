---
name: impacts-scope-mcp
description: 通过 MCP 工具分析突发事件的影响范围。提供两种模式：1) 便捷模式一键分析；2) 原子模式让 LLM 自主理解数据模型并编排查询步骤。当用户需要了解某个事件的影响半径、涉及隐患点及受影响村/社区时调用。
---

# 影响范围分析（MCP 方式）

当用户需要分析某个事件的影响范围时，你可以通过 impacts MCP 服务获取原始结构化数据，然后基于数据生成专业、简洁、适合应急指挥场景的影响范围描述。

本 Skill 提供 **两种调用模式**，请根据用户问题的复杂度灵活选择：

---

## 模式一：便捷模式（推荐用于简单场景）

当用户只说"分析事件XXX的影响范围"，没有指定自定义条件时，直接调用便捷工具一步完成。

### 工具：`mcp__impacts__analyze_impact_scope`

**功能**：封装了完整的"查事件 → 矩形预筛选 → haversine精算 → join家庭表"流程，一键返回影响范围结构化数据。

**参数**：
```json
{"event_id": "事件唯一标识ID"}
```

**返回示例**：
```json
{
  "event_location": [26.387869, 111.328589],
  "radius_km": 3.0,
  "event_level": 4,
  "affected_households": [
    {"village_name": "苍子岭社区", "hazard_name": "龙庭水岸滑坡"}
  ]
}
```

---

## 模式二：原子模式（推荐用于复杂场景）

当用户的问题包含以下任意一种复杂条件时，使用原子模式：
- 指定了**自定义查询半径**（如"周边 5 公里"）
- 要求**分步查看**中间结果（如"先查隐患点，再查涉及社区"）
- 指定了**社区名反向查询**（如"苍子岭社区有哪些隐患点"）
- 需要**对比多个事件**或**跨事件分析**

### 执行策略

```
Step 1: 调用 mcp__impacts__get_database_schema() 了解数据模型
Step 2: 根据用户问题和 schema，自主决定调用哪些原子工具
Step 3: 基于所有查询结果生成专业描述
```

### 原子工具列表

#### 1. `mcp__impacts__get_database_schema`

**功能**：获取 impacts 相关的数据库表结构、字段含义、关联关系和业务规则。

**建议**：任何复杂查询前**先调用此工具**，了解数据模型后再决定后续查询策略。

**参数**：无

**返回关键信息**：
- **CT_EVENT**（突发事件主表）：ID, LONGITUDE, LATITUDE, EVENT_LEVEL
- **CT_RISK_HAZARD**（隐患点表）：ID, RISK_HAZARD_NAME, LONGITUDE, LATITUDE
- **CT_RISK_AFFECTED_FAMILY**（关联中间表）：RISK_HAZARD_ID, FAMILY_ID
- **CT_FAMILY**（家庭表）：ID, VILLAGE, LONGITUDE, LATITUDE
- **关联关系**：
  - `CT_RISK_AFFECTED_FAMILY.RISK_HAZARD_ID → CT_RISK_HAZARD.ID`
  - `CT_RISK_AFFECTED_FAMILY.FAMILY_ID → CT_FAMILY.ID`
- **业务规则**：
  - 事件等级 → 默认半径：1=红色(10km), 2=橙色(7km), 3=黄色(5km), 4=蓝色(3km)
  - 空间计算使用 haversine 公式，单位公里

#### 2. `mcp__impacts__get_event`

**功能**：根据事件ID查询事件基本信息（位置、等级）。

**参数**：
```json
{"event_id": "2038878010727825410"}
```

**返回示例**：
```json
{
  "id": "2038878010727825410",
  "longitude": 111.328589,
  "latitude": 26.387869,
  "event_level": 4,
  "default_radius_km": 3.0
}
```

#### 3. `mcp__impacts__get_hazards_nearby`

**功能**：查询指定经纬度周边 radius_km 范围内的所有隐患点。内部使用矩形预筛选 + haversine 精算。

**参数**：
```json
{
  "latitude": 26.387869,
  "longitude": 111.328589,
  "radius_km": 5.0
}
```

**返回示例**：
```json
{
  "center": [26.387869, 111.328589],
  "radius_km": 5.0,
  "total": 8,
  "hazards": [
    {
      "id": "2013136748124639234",
      "name": "龙庭水岸滑坡",
      "latitude": 26.391101,
      "longitude": 111.309694,
      "distance_km": 1.916
    }
  ]
}
```

#### 4. `mcp__impacts__get_affected_villages`

**功能**：根据隐患点ID列表，查询受影响的村/社区及隐患点名称。内部 JOIN 中间表 → 家庭表 → 隐患点表。

**参数**：
```json
{"hazard_ids": ["2013136748124639234", "2027227411859636226"]}
```

**返回示例**：
```json
{
  "total": 7,
  "items": [
    {"village_name": "苍子岭社区", "hazard_name": "龙庭水岸滑坡"},
    {"village_name": "二七社区", "hazard_name": "龙庭水岸滑坡"}
  ]
}
```

---

## 典型场景示例

### 场景 A：简单分析（便捷模式）

**用户**："分析事件 2038878010727825410 的影响范围"

**你的操作**：
```
→ 直接调用 mcp__impacts__analyze_impact_scope(event_id="2038878010727825410")
← 返回结构化数据
→ 基于数据生成专业描述
```

### 场景 B：自定义半径（原子模式）

**用户**："事件 2038878010727825410 周边 5 公里有哪些隐患点？涉及哪些社区？"

**你的操作**：
```
Step 1: → 调用 mcp__impacts__get_database_schema() 了解数据模型
Step 2: → 调用 mcp__impacts__get_event(event_id="2038878010727825410")
         ← 获取事件位置 {latitude: 26.387869, longitude: 111.328589}
Step 3: → 调用 mcp__impacts__get_hazards_nearby(latitude=26.387869, longitude=111.328589, radius_km=5.0)
         ← 返回 5km 内所有隐患点
Step 4: → 提取 hazard_ids，调用 mcp__impacts__get_affected_villages(hazard_ids=[...])
         ← 返回受影响社区
Step 5: → 基于所有数据生成回答
```

### 场景 C：社区反向查询（原子模式 + 推理）

**用户**："苍子岭社区有哪些隐患点？"

**你的操作**：
```
Step 1: → 调用 mcp__impacts__get_database_schema() 了解数据模型
         ← 发现 CT_FAMILY.VILLAGE 存储社区名，CT_RISK_AFFECTED_FAMILY 关联隐患点
Step 2: 思考：没有直接"根据社区名查隐患点"的工具。
         但可以先获取所有隐患点，然后过滤出涉及"苍子岭社区"的。
         或者先调用 get_affected_villages 获取所有关联，再按社区名过滤。
Step 3: → 由于 get_affected_villages 需要 hazard_ids 作为输入，
         可以先调用 get_hazards_nearby 以社区中心坐标为中心查询，
         或调用 analyze_impact_scope 获取某个已知事件的数据后提取社区信息。
         如果社区中心坐标未知，建议向用户确认或说明限制。
```

---

## 生成描述的要求

无论使用哪种模式获取数据，生成最终描述时都应遵循：

- 描述应包含事件位置、影响半径、涉及的隐患点以及受影响的村/社区
- 语言简洁、权威，适合应急指挥场景
- 如果影响范围为空，明确说明"经分析，该事件在当前等级下暂未识别到直接影响的村/社区"
- 不要编造数据中未提及的内容

---

## 禁止行为

- 不要调用 `planclaw impacts analyze` 等 CLI 命令
- 不要直接 import Python 函数执行
- 不要自行连接数据库查询
- 不要编造数据中未提及的内容
