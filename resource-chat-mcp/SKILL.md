---
name: resource-chat-mcp
description: 通过 MCP 工具实现应急资源问数与物资调派分析。提供两种能力：1) 资源问数（查询周边监控、仓库、避难场所、救援队伍、医疗卫生、应急专家、防护目标、消防水源、家庭住户、应急人员等）；2) 物资调派（查询可用仓库及库存）。支持有 event_id 和无 event_id 场景。当用户询问周边有哪些应急资源、需要调拨物资、或需要资源分布与调派分析时调用。
---

# 资源问数与调派分析（MCP 方式）

当用户需要查询应急资源分布或进行物资调派时，你可以通过 resources MCP 服务获取原始结构化数据，然后基于数据生成专业、简洁、适合应急指挥场景的分析结论。

本 Skill 采用 **原子模式**：先调用 `get_database_schema()` 了解数据模型，再根据用户问题自主决定调用哪些原子工具逐步取数，最后基于所有查询结果生成专业描述。

---

## 执行策略

```
Step 1: 调用 mcp__resources__get_database_schema() 了解数据模型
Step 2: 根据用户问题和 schema，自主决定调用哪些原子工具
Step 3: 基于所有查询结果生成专业描述
```

---

## 原子工具列表

### 1. `mcp__resources__get_database_schema`

**功能**：获取 resources 相关的数据库表结构、字段含义、关联关系和业务规则。

**建议**：任何查询前**先调用此工具**，了解数据模型后再决定后续查询策略。

**参数**：无

**返回关键信息**：
- **CT_EVENT**（突发事件主表）：ID, LONGITUDE, LATITUDE, EVENT_LEVEL
- **CT_CAMERA**（监控）：ID, CAMERA_NAME, LONGITUDE, LATITUDE
- **CT_WAREHOUSE**（应急仓库）：ID, WAREHOUSE_NAME, LONGITUDE, LATITUDE, WAREHOUSE_CONTACTS_ID
- **CT_RESCUE_TEAM**（救援队伍）：ID, RESCUE_TEAM_NAME, LONGITUDE, LATITUDE
- **CT_EMERGENCY_SHELTER**（避难场所）：ID, SHELTER_NAME, LONGITUDE, LATITUDE
- **CT_HOSPITAL**（医疗卫生）：ID, HOSPITAL_NAME, LONGITUDE, LATITUDE
- **CT_EXPERT**（应急专家）：ID, CONTACTS_ID, LONGITUDE, LATITUDE
- **CT_PROTECT_TARGET**（防护目标）：ID, TARGET_NAME, LONGITUDE, LATITUDE
- **CT_DATA_WATERHEAD**（消防水源）：id, name, longitude, latitude（小写引号列）
- **CT_FAMILY**（家庭住户）：ID, LONGITUDE, LATITUDE, FAMILY_HEAD_ID, DIRECTION_ID, REFUGE_ID
- **CT_EMERGENCY_MEMBER**（应急人员）：ID, MEMBER_CODE, LONGITUDE, LATITUDE
- **CT_CONTACTS**（联系人）：ID, NAME, PHONE
- **CT_RESOURCE**（物资库存）：ID, RESOURCE_TYPE_CODE, WAREHOUSE_ID, RESOURCE_STORE_NUM
- **CT_RESOURCE_TYPE**（物资类型）：ID, RESOURCE_TYPE_CODE, RESOURCE_TYPE_NAME
- **关联关系**：
  - `CT_WAREHOUSE.WAREHOUSE_CONTACTS_ID → CT_CONTACTS.ID`
  - `CT_RESOURCE.WAREHOUSE_ID → CT_WAREHOUSE.ID`
  - `CT_RESOURCE.RESOURCE_TYPE_CODE → CT_RESOURCE_TYPE.RESOURCE_TYPE_CODE`
- **业务规则**：
  - 事件等级 → 默认半径：1=红色(10km), 2=橙色(7km), 3=黄色(5km), 4=蓝色(3km)
  - 有 event_id 时：默认按事件等级取半径，未明确时回退 5km
  - 无 event_id 时：资源问数与调派分析默认半径 30km

---

### 2. `mcp__resources__query_nearby_resources`

**功能**：查询指定经纬度周边 radius_km 范围内的各类应急资源。内部使用矩形预筛选 + haversine 精算。

**参数**：
```json
{
  "latitude": 26.387869,
  "longitude": 111.328589,
  "radius_km": 5.0,
  "resource_types": ["camera", "warehouse", "emergency_shelter"],
  "top_n": 5
}
```

**resource_types 可选值**：
- `camera` — 监控
- `warehouse` — 应急仓库
- `rescue_team` — 救援队伍
- `emergency_shelter` — 避难场所
- `hospital` — 医疗卫生
- `expert` — 应急专家
- `protect_target` — 防护目标
- `waterhead` — 消防水源
- `family` — 家庭住户
- `emergency_member` — 应急人员

**返回示例**：
```json
{
  "center": [26.387869, 111.328589],
  "radius_km": 5.0,
  "resource_types": ["监控", "应急仓库", "避难场所"],
  "total": 8,
  "resources": {
    "监控": [
      {"id": "cam_001", "name": "路口监控1", "latitude": 26.389, "longitude": 111.33, "distance_km": 1.2}
    ],
    "避难场所": [...]
  }
}
```

---

### 3. `mcp__resources__query_warehouses_with_inventory`

**功能**：查询指定经纬度周边 radius_km 范围内的应急仓库及物资库存。

**参数**：
```json
{
  "latitude": 26.387869,
  "longitude": 111.328589,
  "radius_km": 5.0,
  "material_type_code": "sandbag",
  "min_quantity": 6.0,
  "top_n": 5
}
```

**返回示例**：
```json
{
  "center": [26.387869, 111.328589],
  "radius_km": 5.0,
  "material_type_code": "sandbag",
  "min_quantity": 6.0,
  "total": 3,
  "warehouses": [
    {
      "warehouse_id": "wh_001",
      "warehouse_name": "一号应急仓库",
      "longitude": 111.31,
      "latitude": 26.39,
      "contact_name": "李四",
      "contact_phone": "13900139000",
      "straight_distance_km": 2.5,
      "resources": [
        {"resource_type_code": "sandbag", "resource_type_name": "沙袋", "available_quantity": 100.0}
      ]
    }
  ]
}
```

---

### 4. `mcp__resources__get_material_types`

**功能**：获取所有物资类型编码与名称的映射表。

**建议**：在调用 `query_warehouses_with_inventory` 前，如不确定物资编码，可先调用此工具确认。

**参数**：无

**返回示例**：
```json
{
  "total": 50,
  "items": [
    {"resource_type_code": "sandbag", "resource_type_name": "沙袋"},
    {"resource_type_code": "life_jacket", "resource_type_name": "救生衣"}
  ]
}
```

---

## 典型场景示例

### 场景 A：资源问数（有 event_id）

**用户**："事件 2031537089816346625 周边有哪些避难场所"

**你的操作**：
```
Step 1: → 调用 mcp__resources__get_database_schema() 了解数据模型
Step 2: → 调用 impacts MCP 的 get_event(event_id="2031537089816346625")
         ← 获取事件位置 {latitude: 26.387869, longitude: 111.328589}
Step 3: → 调用 mcp__resources__query_nearby_resources(
           latitude=26.387869, longitude=111.328589, radius_km=5.0,
           resource_types=["emergency_shelter"], top_n=5)
         ← 返回周边避难场所列表
Step 4: → 基于数据生成回答
```

---

### 场景 B：资源问数（无 event_id）

**用户**："永州市区附近有哪些医院"

**你的操作**：
```
Step 1: → 调用 mcp__resources__get_database_schema() 了解数据模型
Step 2: → 从用户问题中提取地点"永州市区"
Step 3: → 调用 gaode_map 工具进行地理编码，获取经纬度
         ← 返回 {latitude: 26.45, longitude: 111.6}
Step 4: → 调用 mcp__resources__query_nearby_resources(
           latitude=26.45, longitude=111.6, radius_km=30.0,
           resource_types=["hospital"], top_n=5)
         ← 返回周边医院列表
Step 5: → 基于数据生成回答
```

---

### 场景 C：调派分析（有 event_id）

**用户**："调取事件 2031537089816346625 的 6 个沙袋"

**你的操作**：
```
Step 1: → 调用 mcp__resources__get_database_schema() 了解数据模型
Step 2: → 调用 impacts MCP 的 get_event(event_id="2031537089816346625")
         ← 获取事件位置 {latitude: 26.387869, longitude: 111.328589}
Step 3: → 调用 mcp__resources__get_material_types() 确认物资编码
         ← 发现 "沙袋" 对应编码 "sandbag"
Step 4: → 调用 mcp__resources__query_warehouses_with_inventory(
           latitude=26.387869, longitude=111.328589, radius_km=5.0,
           material_type_code="sandbag", min_quantity=6, top_n=5)
         ← 返回有库存的仓库列表
Step 5: → 基于数据生成调派建议
```

---

### 场景 D：调派分析（无 event_id）

**用户**："永州体育馆需要 50 件救生衣，从哪里调拨最近"

**你的操作**：
```
Step 1: → 调用 mcp__resources__get_database_schema() 了解数据模型
Step 2: → 从用户问题中提取地点"永州体育馆"
Step 3: → 调用 gaode_map 工具进行地理编码，获取经纬度
         ← 返回 {latitude: 26.45, longitude: 111.6}
Step 4: → 调用 mcp__resources__get_material_types() 确认物资编码
         ← 发现 "救生衣" 对应编码 "life_jacket"
Step 5: → 调用 mcp__resources__query_warehouses_with_inventory(
           latitude=26.45, longitude=111.6, radius_km=30.0,
           material_type_code="life_jacket", min_quantity=50, top_n=5)
         ← 返回有库存的仓库列表
Step 6: → 基于数据生成调派建议
```

---

## 工具调用策略

- **优先使用 resources MCP 取数工具**：当用户需要查找某点位周边的应急资源（如医院、仓库、避难场所等）时，优先直接调用 `mcp__resources__query_nearby_resources` 或 `mcp__resources__query_warehouses_with_inventory` 查询数据库。不要主动使用高德地图的周边搜索功能替代 resources 工具。
- **高德地图工具使用限制**：除非用户明确提及需要使用高德/地图搜索、地理编码、路线规划等功能，否则不主动调用上游高德地图相关 MCP tool。仅在无 event_id 且必须从地名获取经纬度时，可视需要使用地理编码工具。

---

## 生成描述的要求

无论使用哪种模式获取数据，生成最终描述时都应遵循：

- 资源问数：列出资源名称、距离、位置、联系人，按距离由近到远排序
- 调派分析：列出推荐仓库、距离、库存、联系人，给出调拨优先级建议
- 语言简洁、权威，适合应急指挥场景
- 如果查询结果为空，明确说明"指定范围内未查询到符合条件的资源/仓库"
- 不要编造数据中未提及的内容

---

## 禁止行为

- 不要调用 `planclaw` CLI 命令
- 不要直接 import Python 函数执行
- 不要自行连接数据库查询
- 不要编造数据中未提及的内容
