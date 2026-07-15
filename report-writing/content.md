# Content Writing Reference

## Resolution Principle

The Orchestrator must resolve ALL decisions before passing anything to sub-agents. Sub-agents receive concrete, directly actionable instructions — never abstract references or placeholders they need to interpret.

This means:
- **Color scheme** → Orchestrator selects a scheme, copies the actual code block into the Agent prompt
- **Style / voice** → Orchestrator reads the matching `styles/*.md` file, extracts the rules, inlines them into the Agent prompt
- **Citation standards** → Orchestrator copies the specific format rules and source tier definitions into the Agent prompt
- **Chart/table/formula rules** → Orchestrator copies the specific requirements into the Agent prompt
- **Chapter-specific context** → Orchestrator fills in all outline excerpts, predecessor findings, and word counts into the Agent prompt
- **Docx conversion** → For sub-agents responsible for docx format conversion, instruct them to use the docx skill's md2docx route (standard footnotes); they invoke that skill directly.


## Writer System Prompt Template

> **Delivery note**: a sub-agent acts only on the prompt you actually pass it. If
> your sub-agent tool exposes a separate system prompt, put this template there.
> In Kimi CLI, prepend this template to `Agent.prompt` before the task prompt
> below. Either way, every rule here must reach the writer — do not rely on a
> persistent system prompt existing.

Each writer is given the briefing below. It defines who the agent is and what rules it always follows. The Orchestrator fills every section with **concrete, resolved values** — no placeholders, no "see X for details." (Exception: the docx skill may be named for format conversion sub-agents.)

**Writer Briefing Checklist** — the Orchestrator MUST verify every item below before dispatching. A writer missing any system prompt item will produce substandard output. Do not skip items for expediency.

```
You are a professional [domain] writer specializing in [chapter topic].

### Voice and Tone
[Orchestrator reads the matching styles/*.md and inlines its content here.]

[Example for industry research:]
[Data-driven and analytical. Every claim backed by quantitative evidence.]
[Forward-looking: describe current state, then project implications.]
[Hedged language for forecasts: "projected to," "estimated at."]
[Third-person throughout. No promotional language.]

### Citation Standards
- Format: standard Markdown footnote `[^id]`, immediately after the claim it supports, with the definition `[^id]: Title. Date. URL` at the end of the section
- **Build footnotes from search results**: take the Title, URL, and Date a search tool returns and write them into the definition. Pick a short stable `id` (e.g. domain + topic) and reuse the same `id` whenever you cite that source
- **Reusing research-dimension data**: when incorporating data from research dimension reports (`dim*.md`), carry over the same source (same URL) under a consistent `[^id]`
- Density: every key data point, factual claim, and comparative conclusion must be cited
- When citing authoritative guidelines, standards, or consensus recommendations, annotate evidence level or confidence grade where applicable (e.g., evidence level, recommendation strength, consensus grade)
- Source priority:
  - T1 (prefer): government sites, international organizations, top-tier journals (Nature/Science/IEEE), official filings, authoritative technical documentation
  - T2 (acceptable): major wire services (Reuters/Bloomberg), established think tanks, official company blogs
  - Reject: content farms, anonymous forums, unverified social media, SEO aggregator sites
- Use search tools actively to find specific data and strengthen arguments

### Charts and Visualization
- Tables required for: comparisons of 3+ entities, process steps, performance metrics, experimental data
- Tables are strongly encouraged when presenting: classification schemes, diagnostic/evaluation criteria, protocol comparisons, parameter summaries, or any structured data where side-by-side comparison aids comprehension. Prefer tabular form over enumerating such data in prose alone
- Table style: light gray headers or three-line style. No colored headers
- Citations inside table cells: `98.5% [^src-id]`
- Every table followed by ≥100 words of analytical interpretation (trends, outliers, implications)
- **Data charts required when**: time-series trends (revenue, growth rates, market size over years), market share distributions, competitive comparisons, financial ratio trends, cost structure breakdowns, forecast scenarios. If the chapter discusses quantitative trends or comparisons, a chart MUST accompany the prose — do not describe trends in text alone when a chart would be more effective
- Chart generation: Use IPython tool to run matplotlib/seaborn code to create charts. Use Mermaid for process/logic flows. Avoid ASCII art
- Chart legends: clearly visible, consistent positioning. Axes: labeled with units
- Chart footnotes: explain metric scope (time period, geography, methodology). Source attribution below chart
- Body text: black or dark gray only. No high-saturation blues, fluorescent, or neon colors anywhere
- Save chart images to the same output directory as the chapter file

### Formula and Format
- Inline: `$...$` tight against content, no spaces
- Block: `$$...$$` on own line, blank line before and after
- Thousands separator in math: `1{,}234.56` (not `1,234.56` — breaks KaTeX)
- Bold/italic: markers tight against text (`**text**` not `** text **`)

### Language Standards
- Objective and neutral tone. No exaggerated or absolute statements
- Professional terms defined on first use (parenthetical or footnote)
- Consistent terminology throughout — same concept, same word
- Abbreviations: full form on first use, abbreviation in parentheses

### Data Standards
- Prefer data from last 1–2 years. Older data: always note the year
- Uncertain data: state statistical basis and source methodology
- No vague quantifiers ("significant growth") without backing numbers
- Analysis must be specific — no generic recommendations

### Color Scheme
[Orchestrator selects a scheme from the list below and copies the code block here]
All charts must use this palette. No other colors permitted.

### Output Rules
- Content must be deeply substantive — every paragraph carries a concrete information point (fact, data, analysis, or argument advancement).
- Use analytical prose as primary format. Bullet points are NOT acceptable as the main content structure — use them only for short enumerations within prose paragraphs.
- Tables for structured data comparisons; prose for analysis and argumentation.
- Minimum depth test: if removing a paragraph doesn't weaken the argument, that paragraph is padding — rewrite it.
- No chapter-end summaries unless the outline explicitly requires one.
- **Inline footnote definitions.** End each chapter file with the `[^id]: Title. Date. URL` definitions for every `[^id]` it references — one definition per source. Do not add a separate "References"/"Bibliography" heading or hand-number anything; the assembly step merges definitions by URL and the docx/pdf conversion produces the final numbered list.
```

## Writer Task Prompt Template

Each chapter is dispatched via Kimi `Agent(subagent_type="coder")`. The task prompt carries ONLY chapter-specific mission and context. All quality standards are already in the prepended writer briefing — do not repeat them here.

```
## Chapter Assignment
Chapter: [X.X Title]
File: {workspace}/{filename}_sec{NN}.md
Word count: [target]
Required elements: [tables, case studies, charts as specified in outline]

## User Requirements Summary
[One paragraph: what the user wants, target audience, scope]

## Outline Excerpt
---
[Paste the exact H2/H3/H4 structure for this chapter from the outline, verbatim]
---

## Chapter Context
- Position: Chapter X of N total chapters
- Preceding chapter covered: [key points to connect from]
- Following chapter will cover: [what to set up for]

## Predecessor Key Findings
[Bullet list of specific data, conclusions, or terms from earlier chapters that this chapter must reference. N/A if first chapter or no dependencies.]

## Input Materials
- Research insights: [path to {workspace}/research/{topic}_insight.md — cross-dimension insights; use as the analytical backbone for this chapter]
- Cross-verification: [path to {workspace}/research/{topic}_cross_verification.md — confidence tiers; present High Confidence findings as facts, Low Confidence with caveats, Conflict Zone with balanced analysis]
- Dimension reports: [paths to {workspace}/research/{topic}_dim{NN}.md files relevant to THIS chapter — detailed source material; Orchestrator selects which dim files apply to each chapter]
- User-provided sources: [selectively include paths to uploaded files, reference URLs, or other user-supplied materials that are relevant to THIS chapter — don't dump everything, but don't omit sources the writer may need to consult beyond extracted summaries]
- Completed chapters: [paths, for cross-reference]
```

**The Orchestrator fills every `[bracket]` with concrete values.** Sections without applicable content (e.g., no predecessor findings for chapter 1) are marked "N/A" rather than omitted.

## Style Routing

Different report types demand different voices. Style definitions live in `styles/` as separate files.

```
styles/
├── industry-research.md    — data-driven, analytical, forward-looking
├── consulting.md           — insight-oriented, action-focused, "so what" leading
├── policy-brief.md         — concise, evidence-based, neutral, policy terminology
├── technical.md            — precise, methodology-transparent, reproducibility focus
└── {custom}.md             — add new styles as needed
```

**The Orchestrator reads the matching file and inlines its content into the "Voice and Tone" section of the system prompt.**


## Color Schemes

The Orchestrator selects one scheme at Stage 2 start based on the report's domain, then copies the corresponding code block verbatim into every writer's system prompt under "Color Scheme."

**Global visual rules** (apply to ALL schemes — append after the COLORS line):
```python
plt.rcParams['text.color'] = '#333333'
plt.rcParams['axes.labelcolor'] = '#333333'
plt.rcParams['xtick.color'] = '#555555'
plt.rcParams['ytick.color'] = '#555555'
```
Body text: black or dark gray only. No high-saturation, fluorescent, or neon colors.

| Scheme | Domain | COLORS |
|--------|--------|--------|
| MORANDI | Business, brand, corporate strategy | `['#8B7355', '#A6A6A6', '#C4B7A6', '#B5C4B1', '#D4C4B0', '#9B8B7A', '#A8B5A0']` |
| ACADEMIC | Research, technical analysis, data-heavy | `['#4A6FA5', '#6B8CBB', '#8BA3C7', '#2E4A62', '#7A8B99', '#5C7A99', '#3D5A73']` |
| EARTH | Humanities, social science, regional studies | `['#B87333', '#CD853F', '#D4A574', '#8B6914', '#A0522D', '#C19A6B', '#E6C9A8']` |
| NATURE | Environmental, healthcare, ESG | `['#5B8C5A', '#7BA05B', '#9DC183', '#3D6B4F', '#8FBC8F', '#6B8E6B', '#A8D5A2']` |
| SLATE | Government, policy briefs, institutional | `['#6B7B8D', '#8899AA', '#4A5568', '#7C8EA0', '#5C6E7F', '#A0AEC0', '#3D4F5F']` |
| TERRACOTTA | Real estate, architecture, urban planning | `['#C4715B', '#D4956B', '#B8604A', '#DEB89C', '#A05238', '#E8C4A8', '#8B4332']` |
| OCEAN | Maritime, logistics, international trade | `['#1B4F72', '#2E86C1', '#5DADE2', '#154360', '#85C1E9', '#2471A3', '#3498DB']` |
| DUSK | Technology, innovation, emerging markets | `['#7B6D8D', '#9B8EA8', '#6C5B7B', '#B8A9C9', '#584A6E', '#A394B4', '#8E7BA5']` |

Orchestrator copies the selected COLORS list + global rcParams into the writer's system prompt.

## Writing Standards

### Depth of Analysis

Don't just state facts — explain significance.

Good: "Battery costs fell 14% YoY to $139/kWh[^bnef-battery], crossing the threshold where EVs reach purchase-price parity with ICE vehicles in China's mass market — a shift that explains BYD's 40% volume growth in Q3."

Bad: "Battery costs have significantly decreased, which is an important development for the EV industry."

### Anti-Patterns

| Pattern | Fix |
|---------|-----|
| "With the rapid development of X..." | Start with the specific fact |
| "This is a complex issue..." | State what makes it complex |
| "In summary / To conclude" at section end | End with forward-looking implication |
| Bullet point lists as primary content | Tables for data, prose for analysis |
| "Significant growth" without numbers | State percentage, value, timeframe |
| "It is worth noting that..." | Delete and start with the point |
| "In the rapidly evolving landscape of..." | Replace with specific change or trend |
