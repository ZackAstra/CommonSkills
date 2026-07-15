---
name: stock-assistant
description: |
  股票信息原子能力 Skill。为 Agent 和 Daimon cron/code 提供 watchlist、报价、
  日 K、批量技术指标、Kimi search/fetch 等结构化数据能力。

  本 Skill 不负责 IM 投递、不画图、不写固定投资报告。Agent 应调用脚本取得 JSON，
  再按当前任务自由分析、画图或返回 Daimon cron_output。
metadata:
  openclaw:
    emoji: "📈"
    requires:
      bins: ["python3"]
      packages: ["requests>=2.28.0"]
---

# Stock Assistant

## 角色边界

本 Skill 只提供金融信息获取和轻量本地计算：

- 读取自选股
- 获取单股/批量报价
- 获取 A 股日 K 序列
- 计算 MA、RSI、MACD
- 组合批量技术数据包
- 调 Kimi Code search/fetch 获取新闻、公告、F10、研报等材料

本 Skill 不做：

- 不直接投递飞书或任何 IM
- 不画图
- 不写最终投资建议报告
- 不把策略判断写死

图表交给图表/数据可视化 Skill。投递交给 Daimon delivery。结论由 Agent 或 cron code 根据数据自由生成。

## 配置

公开配置在 `config.json`：

```json
{
  "watchlist": "watchlist.json"
}
```

敏感配置只写安装后的本机文件：

```text
~/.kimi/daimon/skills/stock-assistant/secrets.local.json
```

如果文件不存在，读取 `secrets.local.template.json` 创建：

```json
{
  "kimiPluginAPIKey": "YOUR_KIMI_PLUGIN_API_KEY"
}
```

不要把真实 key 写入 repo asset。不要在 stdout、报告、cron output 或日志里打印 key。

## 调用约定

唯一公开入口：

```bash
python3 ~/.kimi/daimon/skills/stock-assistant/scripts/stock_atom.py <domain> <action> [args]
```

也可以在源码树或测试目录中运行。脚本自动以自身上级目录作为 Skill 根目录；如需覆盖，设置：

```bash
STOCK_ASSISTANT_HOME=/path/to/stock-assistant
```

stdout 只输出 JSON envelope：

```json
{
  "ok": true,
  "data": {},
  "sources": [],
  "warnings": [],
  "asOf": "2026-05-08T15:00:00+08:00"
}
```

失败时：

```json
{
  "ok": false,
  "error": {
    "code": "missing_kimi_plugin_api_key",
    "message": "Missing kimiPluginAPIKey",
    "retryable": false
  }
}
```

Agent 调用脚本时应解析 JSON。`ok=false` 时不要继续把结果当作数据使用。

## 原子命令

### 配置与自选股

```bash
python3 scripts/stock_atom.py config validate
python3 scripts/stock_atom.py watchlist list
```

`watchlist list` 会读取 `watchlist.json`。如果存在真实股票，会自动忽略 `_example` 示例股；否则返回示例股，方便测试。

### 报价

```bash
python3 scripts/stock_atom.py quote get --code 600519.SH
python3 scripts/stock_atom.py quote batch --codes 600519.SH,000858.SZ
python3 scripts/stock_atom.py quote snapshot
```

- A 股报价来自同花顺分时接口。
- 港股/美股报价为雪球 best effort。
- `quote snapshot` 默认读取 watchlist。

### 日 K 序列

```bash
python3 scripts/stock_atom.py series kline --code 600519.SH --interval 1d --limit 300
python3 scripts/stock_atom.py series batch --codes 600519.SH,000858.SZ --interval 1d --limit 300
python3 scripts/stock_atom.py series watchlist --interval 1d --limit 300
```

第一版只支持 A 股 `interval=1d`，数据来自东方财富日 K。

### 指标

指标命令接收 kline JSON，可直接传字符串，也可用 `@file`：

```bash
python3 scripts/stock_atom.py indicator ma --period 250 --input-json @kline.json
python3 scripts/stock_atom.py indicator rsi --period 14 --input-json @kline.json
python3 scripts/stock_atom.py indicator macd --input-json @kline.json
```

批量指标接收 `series batch/watchlist` 的 `data`：

```bash
python3 scripts/stock_atom.py indicator batch \
  --indicators ma:20,ma:60,ma:250,rsi:14,macd \
  --input-json @series-batch.json
```

### Bundle

`bundle` 同时返回 quote、series、latest indicators 和 indicator series，适合 Agent 面对多股票时少写循环。

```bash
python3 scripts/stock_atom.py bundle technical \
  --codes 600519.SH,000858.SZ \
  --interval 1d \
  --limit 300 \
  --indicators ma:20,ma:60,ma:250,rsi:14,macd

python3 scripts/stock_atom.py bundle watchlist-technical \
  --interval 1d \
  --limit 300 \
  --indicators ma:20,ma:60,ma:250,rsi:14,macd
```

`bundle` 只返回数据，不判断买卖、不画图、不投递。

### Kimi Search / Fetch

这些命令需要 `secrets.local.json` 中的 `kimiPluginAPIKey`：

```bash
python3 scripts/stock_atom.py research search --query "贵州茅台 今日 公告" --limit 5
python3 scripts/stock_atom.py research fetch --url "https://basic.10jqka.com.cn/600519/finance.html"

python3 scripts/stock_atom.py research batch-search \
  --queries-json '["贵州茅台 今日 公告","五粮液 今日 公告"]'

python3 scripts/stock_atom.py research batch-fetch \
  --urls-json '["https://basic.10jqka.com.cn/600519/company.html"]'
```

## Cron Code 示例

### 250 日均线附近筛选

```python
import json
import subprocess
from pathlib import Path
from daimon_runtime import cron_output

SKILL = str(Path.home() / ".kimi/daimon/skills/stock-assistant")

def atom(*args):
    p = subprocess.run(
        ["python3", f"{SKILL}/scripts/stock_atom.py", *args],
        text=True,
        capture_output=True,
        check=True,
    )
    env = json.loads(p.stdout)
    if not env.get("ok"):
        raise RuntimeError(env.get("error", {}).get("message", "stock atom failed"))
    return env["data"]

def run(ctx):
    bundle = atom(
        "bundle", "watchlist-technical",
        "--interval", "1d",
        "--limit", "300",
        "--indicators", "ma:250,rsi:14,macd",
    )
    hits = []
    for item in bundle["items"]:
        quote = item.get("quote") or {}
        price = quote.get("price")
        ma250 = item.get("indicators", {}).get("ma250")
        if price and ma250 and abs(price - ma250) / ma250 <= 0.01:
            hits.append(f"{item['name']}({item['code']}): price={price}, MA250={ma250}")
    if not hits:
        return None
    return cron_output("接近250日均线:\n" + "\n".join(hits), metadata={"hits": hits})
```

### 双股技术对比

```python
bundle = atom(
    "bundle", "technical",
    "--codes", "600519.SH,000858.SZ",
    "--interval", "1d",
    "--limit", "300",
    "--indicators", "ma:20,ma:60,ma:250,rsi:14,macd",
)
```

把 `bundle["items"]` 转成 DataFrame 后，交给图表 Skill 或本地绘图代码画图；本 Skill 不负责画图。
