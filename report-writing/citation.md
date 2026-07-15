# Citation Management Reference

## Citation Format — Standard Markdown Footnotes

Cite sources with **standard Markdown footnotes**. Build each footnote directly
from the fields a search tool returns (Title, URL, and Date when available).

**In body text** — reference marker immediately after the claim, no space:

```markdown
全球市场规模达 500 亿美元[^oica-2024]，同比增长 12%[^oica-2024]。
```

**At the end of the section** — one definition per source:

```markdown
[^oica-2024]: OICA. World Motor Vehicle Production Statistics. 2024. https://www.oica.net/production-statistics/
[^mofcom-2024]: 商务部. 中国汽车贸易质量报告. 2024. https://wms.mofcom.gov.cn/...
```

**Rules**:
- The `id` is just a stable handle. Derive a short token from the source (e.g.
  domain + topic) and **reuse the same `id` every time you cite that source**.
- Each definition **must contain the URL** — it is the deduplication key.
  Include Title and Date when the search result provides them.
- One citation can support several consecutive sentences from the same source,
  but each distinct data point should be individually cited.
- In table cells, a space before the marker is fine for readability: `98.5% [^src]`.
- **Do not number citations yourself and do not write a separate reference list.**
  Definitions live inline at the end of each section; the assembly step
  deduplicates by URL and the docx/pdf conversion assigns the displayed numbers
  (1, 2, 3 …) by order of appearance.

## Source Tier System

### T1 — Preferred
Government official sites, international organizations (UN, World Bank, IMF, WHO), top-tier peer-reviewed journals (Nature, Science, The Lancet, IEEE Transactions), official corporate filings (10-K, annual reports), authoritative technical documentation

### T2 — Acceptable
Major wire services (Reuters, Bloomberg, AP, AFP), newspapers of record (NYT, WSJ, FT), recognized think tanks and consulting firms (McKinsey Global Institute, Brookings, BCG), official company blogs and press releases

### Rejected — Never cite
Content farms, SEO aggregator sites, anonymous forum posts, unverified social media, self-published sources without peer review, vendor whitepapers with unsubstantiated product claims

**Conflict resolution**: Same fact, multiple sources → prefer T1. Multiple T1 → prefer most recent. T1 sources conflict → note the discrepancy in text.

## Deduplication (assembly)

When sections are merged into `{filename}.agent.final.md`:

1. Collect every footnote definition across sections.
2. **Merge by URL**: definitions pointing at the same URL become one source.
3. Leave the in-text `[^id]` references as written — the downstream docx/pdf
   conversion renumbers by first appearance after URL dedup.
4. Verify every `[^id]` reference has a matching definition; re-dispatch the
   writer for any section with a dangling reference.

The reference style requested by the user (e.g. GB/T 7714) is a *presentation*
concern handled at conversion time — writers only need to supply Title, Date,
and URL in the footnote definition.
