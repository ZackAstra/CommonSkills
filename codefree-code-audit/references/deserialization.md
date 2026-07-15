# 反序列化安全研究方法论

## 元思考框架

### 核心认知模型

```
反序列化漏洞 = 对象状态恢复 + 方法自动调用 + 恶意对象注入
```

### 三层攻击模型

| 层次 | 关注焦点 | 典型问题 |
|-----|---------|---------|
| **数据层** | 序列化数据格式 | 协议识别、数据提取 |
| **逻辑层** | 反序列化触发点 | readObject、unserialize触发 |
| **利用层** | Gadget链构造 | 原语组合、利用链构建 |

### Gadget链构造思维

```
入口点 → 中间链 → 触发点 → 危险操作
  ↓        ↓        ↓        ↓
readObject  getter   invoke   exec/Runtime
```

**核心洞察**："万物皆可Gadget" —— 任何实现Serializable接口的类都可能成为利用链的一环

---

## Java反序列化

### CommonCollections链

#### CC1链（JDK 8u65之前）

```
AnnotationInvocationHandler.readObject()
  → Map.entrySet()
    → LazyMap.get()
      → ChainedTransformer.transform()
        → ConstantTransformer.transform()
        → InvokerTransformer.transform() → Runtime.exec()
```

#### CC6链（JDK 8u65+）

```
HashSet.readObject()
  → HashMap.put()
    → TiedMapEntry.hashCode()
      → LazyMap.get()
        → ChainedTransformer.transform()
```

### Fastjson反序列化

#### AutoType绕过

| 版本 | 绕过方法 |
|-----|---------|
| < 1.2.24 | 无需绕过 |
| 1.2.25-1.2.41 | 修改AutoType支持列表 |
| 1.2.42-1.2.45 | 双层嵌套绕过 |
| 1.2.47+ | 利用MiscCodec |

### 二次反序列化

#### 核心技术

```
SignedObject.getObject()
  → 触发二次反序列化
  → 绕过黑名单检测
```

**关键洞察**：二次反序列化是协议降级的关键突破口

### 代理封装绕过

#### JdkDynamicAopProxy

```
检测逻辑：只校验代理接口，不检查被代理对象
利用链：
  → JdkDynamicAopProxy.invoke()
    → 委托给真实对象
      → TemplatesImpl.getOutputProperties()
        → 恶意字节码加载
```

---

## PHP反序列化

### Laravel反序列化

#### 核心触发点

```
__destruct() → __toString() → __call() → 危险函数
```

### ThinkPHP反序列化

#### 典型利用链

```
Model.__destruct()
  → Model.save()
    → Connection.query()
      → PDO.query()
```

---

## .NET反序列化

### ViewState

#### MAC验证绕过

```csharp
// 关键参数
__VIEWSTATEGENERATOR
__VIEWSTATEENCRYPTED
```

### BinaryFormatter

#### 已知Gadget

- TypeConfuseDelegate
- TextFormattingRunProperties

---

## 版本边界速查

### JDK版本差异

| 特性 | 版本范围 | 影响 |
|-----|---------|------|
| RMI远程加载 | 6u132, 7u122, 8u113+ | 受限 |
| LDAP远程加载 | 11.0.1, 8u191, 7u201, 6u211+ | 受限 |
| CC1链 | JDK 8u65之前 | 可用 |
| CC6链 | JDK 8u65+ | 可用 |

### 框架版本差异

| 框架 | 影响版本 | 利用方法 |
|-----|---------|---------|
| Fastjson | 1.2.47+ | MiscCodec绕过 |
| Shiro | < 1.4.2 | RememberMe反序列化 |
| WebLogic | 10.3.6.0 | T3协议反序列化 |

---

## 黑名单绕过策略

### 原理

黑名单必有遗漏，因为无法穷举所有可能的Gadget

### 常见绕过方法

1. **代理封装**：绕过接口检查
2. **二次反序列化**：SignedObject触发
3. **嵌套调用**：多层代理绕过
4. **未知类利用**：使用非黑名单类

---

## 核心洞察

1. **万物皆可Gadget**：任何Serializable类都可能成为利用链的一环
2. **二次反序列化是关键**：SignedObject实现协议降级
3. **黑名单必有遗漏**：代理封装是高版本绕过的通用思路
4. **版本敏感**：同一漏洞点在不同版本需要不同利用方法
5. **Gadget链本质**：原语的组合与放大

---

## 代表性案例索引

| 文档编号 | 主题 | 核心技术点 |
|---------|------|-----------|
| **10011** | WeblogicT3反序列化浅析 | T3协议、CC链 |
| **10017** | ysoserial-CommonsBeanutils的shiro无依赖链改造 | CB链、Shiro |
| **10088** | 最新Laravel反序列化漏洞 | PHP反序列化 |
| **10144** | 利用shiro反序列化注入冰蝎内存马 | Shiro、内存马 |
| **15246** | 通天星CMSv6 Jasper反序列化漏洞分析 | Jasper |