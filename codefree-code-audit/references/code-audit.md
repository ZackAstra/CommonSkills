# 代码审计方法论

## 元思考框架

### 核心认知模型

```
代码审计 = Source-Sink分析 + 污点传播 + 安全缺陷识别
```

### 三层审计模型

| 层次 | 关注焦点 | 典型问题 |
|-----|---------|---------|
| **数据层** | 用户输入处理 | 输入验证、过滤绕过 |
| **逻辑层** | 业务流程缺陷 | 权限绕过、条件竞争 |
| **执行层** | 危险函数调用 | 注入、文件操作、命令执行 |

### 污点传播分析

```
Source（污染源） → 污点传播 → Sink（汇聚点）
     ↓                  ↓            ↓
  用户输入          数据流动      危险操作
```

---

## Source-Sink模型

### Source（污染源）

| 类型 | 典型示例 |
|-----|---------|
| **HTTP参数** | $_GET、$_POST、request.getParameter() |
| **HTTP头** | User-Agent、Cookie、Referer |
| **文件输入** | 文件上传、文件读取 |
| **环境变量** | getenv()、System.getenv() |
| **数据库** | 查询结果、数据库存储的数据 |

### Sink（汇聚点）

| 类型 | 典型示例 |
|-----|---------|
| **SQL执行** | mysql_query()、executeQuery() |
| **命令执行** | exec()、eval()、Runtime.exec() |
| **文件操作** | file_get_contents()、include() |
| **输出** | echo、print、response.getWriter() |
| **反序列化** | unserialize()、readObject() |

### Sanitizer（净化器）

| 类型 | 典型示例 |
|-----|---------|
| **输入验证** | 正则匹配、白名单验证 |
| **编码** | htmlspecialchars()、addslashes() |
| **参数化查询** | PreparedStatement、ORM |

---

## 审计流程

### 1. 项目识别

#### 技术栈识别

- 框架：Spring、Struts2、ThinkPHP、Laravel
- 语言：Java、PHP、Python、Go
- 数据库：MySQL、PostgreSQL、Oracle、MSSQL

#### 目录结构分析

```
src/                  # 源代码
config/              # 配置文件
lib/                 # 第三方库
uploads/             # 上传目录
templates/           # 模板文件
```

### 2. 攻击面识别

#### 入口点定位

- 路由映射文件
- 控制器/Action类
- API接口定义
- 表单处理函数

#### 危险函数搜索

| 语言 | 危险函数 |
|-----|---------|
| PHP | exec()、system()、eval()、include() |
| Java | Runtime.exec()、ProcessBuilder、反射 |
| Python | eval()、exec()、os.system() |

### 3. 污点追踪

#### 静态分析

1. 从Source开始追踪
2. 识别数据流向
3. 检查是否经过Sanitizer
4. 确认是否到达Sink

#### 动态验证

1. 构造测试用例
2. 触发代码路径
3. 验证漏洞存在
4. 评估利用价值

---

## 常见漏洞模式

### SQL注入

#### 识别特征

```php
// 危险
$sql = "SELECT * FROM users WHERE id = " . $_GET['id'];

// 安全
$sql = "SELECT * FROM users WHERE id = ?";
$stmt = $pdo->prepare($sql);
$stmt->execute([$_GET['id']]);
```

#### 审计要点

- 检查SQL拼接
- 检查参数化查询
- 检查ORM使用
- 检查存储过程

### XSS漏洞

#### 识别特征

```php
// 危险
echo $_GET['message'];

// 安全
echo htmlspecialchars($_GET['message'], ENT_QUOTES);
```

#### 审计要点

- 检查输出编码
- 检查上下文感知
- 检查CSP配置
- 检查DOM操作

### 文件上传

#### 识别特征

```php
// 危险
move_uploaded_file($_FILES['file']['tmp_name'], 'uploads/' . $_FILES['file']['name']);

// 安全
$ext = pathinfo($_FILES['file']['name'], PATHINFO_EXTENSION);
if (!in_array($ext, ['jpg', 'png', 'gif'])) {
    die('Invalid file type');
}
```

#### 审计要点

- 检查文件类型验证
- 检查文件名过滤
- 检查上传目录配置
- 检查执行权限

### 权限绕过

#### 识别特征

```php
// 危险
if ($_SESSION['user_type'] == 'admin') {
    // 敏感操作
}

// 安全
if (hasPermission($_SESSION['user_id'], 'admin_panel')) {
    // 敏感操作
}
```

#### 审计要点

- 检查权限验证
- 检查会话管理
- 检查水平越权
- 检查垂直越权

---

## 框架专项审计

### Spring框架

#### SpEL注入

```
触发点：@Value、@PreAuthorize、@Cacheable
审计：检查表达式解析点
```

#### 反序列化

```
触发点：Jackson、Fastjson、XML解析
审计：检查反序列化配置
```

### ThinkPHP框架

#### 路由绕过

```
审计：检查路由配置
关注：s参数、模块/控制器参数
```

### Laravel框架

#### SQL注入

```
审计：检查DB::raw()、原生SQL
关注：whereRaw()、orderByRaw()
```

---

## 审计工具

### 静态分析工具

| 工具 | 语言 | 特点 |
|-----|------|------|
| SonarQube | 多语言 | 规则库丰富 |
| FindBugs | Java | 模式匹配 |
| RIPS | PHP | 深度分析 |
| Bandit | Python | 安全检查 |

### 辅助工具

| 工具 | 用途 |
|-----|------|
| grep | 关键词搜索 |
| regex | 正则匹配 |
| AST解析 | 代码结构分析 |
| 数据流分析 | 污点追踪 |

---

## 审计最佳实践

### 1. 上下文感知

理解代码的业务逻辑，而不是孤立地检查单个函数

### 2. 数据流优先

追踪数据从输入到输出的完整路径

### 3. 权限边界

检查权限验证是否在所有敏感操作前执行

### 4. 框架特性

理解框架的安全机制和常见漏洞

### 5. 历史漏洞

关注已知漏洞和修复模式

---

## 核心洞察

1. **污点传播是核心**：从Source追踪到Sink是审计主线
2. **Sanitizer是关键**：有效的净化可以阻断漏洞利用
3. **框架双刃剑**：框架提供安全机制但也可能引入新漏洞
4. **权限验证需全面**：水平越权和垂直越权都要检查
5. **业务逻辑漏洞**：复杂的业务流程往往隐藏逻辑缺陷

---

## 代表性案例索引

| 文档编号 | 主题 | 核心技术点 |
|---------|------|-----------|
| **10005** | ZbzCMS 2.1 审计 | PHP CMS审计 |
| **10022** | 西湖论剑-信呼oa审计复盘 | OA审计 |
| **10126** | 从0开始学习代码审计之百家CMS | PHP审计入门 |
| **10150** | MetInfo CMS代码审计-PHP | PHP框架审计 |
| **12009** | 记一次实战代码审计 | 实战审计流程 |