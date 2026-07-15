# Citation Management Reference (Academic Papers)

## Citation Format — Standard Markdown Footnotes

During writing, all sections cite sources with **standard Markdown footnotes**.
Build each footnote from the source's metadata (authors/title, year, and DOI or
URL).

**In body text**:

```markdown
Transformer architectures[^vaswani-2017] underpin most modern LLMs, and scaling
laws[^kaplan-2020] predict their performance.
```

**At the end of the section** — one definition per source:

```markdown
[^vaswani-2017]: A. Vaswani et al. Attention is all you need. 2017. https://arxiv.org/abs/1706.03762
[^kaplan-2020]: J. Kaplan et al. Scaling laws for neural language models. 2020. https://arxiv.org/abs/2001.08361
```

**Rules**:
- The `id` is a stable handle (e.g. `firstauthor-year`). **Reuse the same `id`
  for the same work**; the URL/DOI is the deduplication key.
- Each definition **must contain a URL or DOI**. Include authors/title and year.
- Do not number citations yourself and do not write a separate reference list —
  definitions live inline at the end of each section. Assembly deduplicates by
  URL and the docx/pdf conversion produces the numbered/styled reference list.

## Target Reference Style (presentation only)

The displayed reference style depends on the venue. The Orchestrator determines
it from the user's query (e.g. "IEEE format," "APA style," "NeurIPS submission")
and passes it to the conversion step. **Writers do not need to format to the
target style** — they only supply authors/title, year, and URL/DOI in the
footnote definition; the conversion renders the chosen style.

| Style | Typical Venues | In-Text Convention | Reference Format |
|-------|---------------|-------------------|-----------------|
| IEEE | IEEE transactions, most CS conferences | `[1]`, `[2]` numbered | `[1] A. Author, "Title," *Journal*, vol. X, pp. Y-Z, Year.` |
| APA 7th | Psychology, social sciences | `(Author, Year)` | `Author, A. B. (Year). Title. *Journal*, *volume*(issue), pages. DOI` |
| ACM | ACM conferences and journals | `[Author Year]` or numbered | ACM Reference Format |
| Chicago Author-Date | Humanities, some social sciences | `(Author Year)` | Author. Year. "Title." *Journal* Volume(Issue): Pages. |
| GB/T 7714-2015 | Chinese academic journals | `[1]`, `[2]` numbered | `[1] Author. Title[J]. Journal, Year, Vol(Issue): Pages.` |
| Vancouver | Medical and biomedical journals | `(1)`, `(2)` numbered | `1. Author. Title. Journal. Year;Vol(Issue):Pages.` |

**Default**: numbered (IEEE) style; Chinese-language papers default to GB/T 7714-2015.

## Source Tier System

### T1 — Preferred
Peer-reviewed journals (Nature, Science, IEEE Transactions, ACL Anthology, etc.), top-tier conference proceedings (NeurIPS, ICML, CVPR, ACL, AAAI, etc.), official datasets with published papers, textbooks from established publishers

### T2 — Acceptable
Preprints with significant citations (arXiv papers with 50+ citations), established technical blogs from research labs (Google AI Blog, Meta AI), well-cited survey papers, official documentation for tools and frameworks

### Rejected — Never cite
Unreviewed preprints with zero citations (unless the user's own work), content farms, anonymous forums, unverified social media, vendor marketing materials

**Academic-specific notes**:
- Prefer the published version over the preprint when available
- For concurrent/recent work, citing preprints is acceptable with a note
- Self-citation: acceptable when genuinely relevant, but flag if >20% of references are self-citations

## Deduplication (assembly)

When sections are merged into `{filename}.agent.final.md`:

1. Collect every footnote definition across sections.
2. **Merge by URL/DOI**: definitions pointing at the same work become one source.
3. Leave the in-text `[^id]` references as written — the downstream conversion
   renumbers by first appearance and renders the target style.
4. Verify every `[^id]` reference has a matching definition; re-dispatch the
   writer for any section with a dangling reference.
