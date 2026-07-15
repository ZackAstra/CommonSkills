---
name: kimi-data-tools-v2
description: Use Daimon's built-in Kimi data tools for current web search, URL fetching, and stock finance data. Use when a task needs kimi_search_v2, kimi_fetch_v2, or kimi_finance_v2, especially in bundle or no-OpenClaw environments.
---

# Kimi Data Tools V2

Use these Daimon core tools when the active session exposes them:

- `kimi_search_v2`: search current web information.
- `kimi_fetch_v2`: fetch and extract content from a known URL.
- `kimi_finance_v2`: retrieve market data for verified stock tickers.

The old unsuffixed `kimi_search`, `kimi_fetch`, and `kimi_finance` tools may also exist in some
environments. Those are OpenClaw `kimi-search` plugin tools, not Daimon's v2 tools. Prefer the
`_v2` tools when the task calls for Daimon-owned data tooling.

The v2 tools use Daimon's Kimi Code API key from local Daimon configuration. They do not require
OAuth and do not require the OpenClaw `kimi-search` plugin.

## Search

Call `kimi_search_v2` when you need current facts, recent documentation, news, release notes,
papers, blogs, public company pages, or verification before another web or finance call.

Schema:

```json
{
  "type": "object",
  "additionalProperties": false,
  "properties": {
    "query": {
      "type": "string",
      "description": "The query text to search for."
    },
    "limit": {
      "type": "integer",
      "minimum": 1,
      "maximum": 20,
      "default": 5
    },
    "include_content": {
      "type": "boolean",
      "default": false
    }
  },
  "required": ["query"]
}
```

Examples:

```json
{
  "query": "Daimon Kimi data tools v2 documentation",
  "limit": 5
}
```

```json
{
  "query": "NVIDIA stock ticker exchange suffix",
  "limit": 3,
  "include_content": false
}
```

Use `include_content: true` only when summaries are insufficient; it can return much more text.

## Fetch

Call `kimi_fetch_v2` when you already have a URL and need the page content. It tries the Kimi fetch
service first, then falls back to direct HTTP fetching and text extraction when the service cannot
return the page.

Schema:

```json
{
  "type": "object",
  "additionalProperties": false,
  "properties": {
    "url": {
      "type": "string",
      "description": "The URL to fetch content from."
    }
  },
  "required": ["url"]
}
```

Example:

```json
{
  "url": "https://example.com/report"
}
```

Use search first if the URL is uncertain or you only have a page title, company name, or topic.

## Finance

Call `kimi_finance_v2` only for market data after verifying exact stock codes and exchange suffixes.
If the user gives a company name, abbreviation, or ambiguous ticker, verify it with `kimi_search_v2`
or another reliable source before calling finance.

Schema:

```json
{
  "type": "object",
  "additionalProperties": false,
  "properties": {
    "ticker": {
      "type": "string",
      "description": "Stock code(s), comma-separated, maximum 3."
    },
    "time": {
      "type": "string",
      "description": "Optional query time in format YYYY-MM-DD HH:MM:SS. Seconds should be 00."
    },
    "type": {
      "type": "string",
      "enum": ["open_summary", "close_summary", "realtime_price", "realtime_tech"],
      "default": "realtime_price"
    },
    "file_path": {
      "type": "string",
      "description": "File path to save data in CSV format."
    }
  },
  "required": ["ticker", "file_path"]
}
```

Supported ticker suffixes:

- A-shares: `.SH`, `.SZ`, `.BJ`
- Hong Kong stocks: `.HK`
- US stocks: `.US`

Examples:

```json
{
  "ticker": "AAPL.US",
  "type": "realtime_price",
  "file_path": "/tmp/aapl_realtime.csv"
}
```

```json
{
  "ticker": "000001.SZ,0700.HK",
  "time": "2026-05-29 10:30:00",
  "type": "close_summary",
  "file_path": "/tmp/market_summary.csv"
}
```

Safety boundaries:

- `kimi_finance_v2` provides market data only.
- Do not use it to provide trading advice, investment advice, order placement, portfolio execution,
  or guarantees about future returns.
- Explain uncertainty and source limitations when the user asks for analysis based on returned
  finance data.
