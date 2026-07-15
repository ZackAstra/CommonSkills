---
name: longread
description: >
  Use this skill when an agent (main agent or subagent) encounters a file too
    large to read in a single pass — e.g. cat, read_file, or Read tool hits size
    limits or truncates output. First assess whether the file is suitable for
    chunk-based parallel reading, then proceed accordingly. Supports PDF, DOCX,
    TXT, MD, PPTX files. NOT for structured data (CSV, DTA, XLSX, etc.).
user-invocable: true
allowed-tools: Shell, ReadFile, Agent, Glob
argument-hint: <file_path>
---

# Longread Skill

In this document, `{workspace}` means the user's default selected workspace.

Use this skill when a file is too large to read in a single pass (e.g. cat, read_file, or Read tool hits size limits or truncates output).

## Step 0: Assess Suitability (REQUIRED)

Before splitting, determine whether the file is actually suitable for the chunk-and-summarize pattern. **Not all large files benefit from this approach.**

### Files SUITABLE for this skill (non-structured, prose-like content):
- PDF documents (reports, papers, books, manuals)
- DOCX documents (articles, contracts, essays)
- TXT / MD files (long-form text, documentation)
- PPTX files (slide decks with text content)

### Files NOT suitable — use code instead:
- **CSV, TSV, DTA, XLS/XLSX** — structured/tabular data. Use pandas, Stata, or other data tools to query, filter, aggregate. Splitting rows across chunks destroys data integrity.
- **JSON, JSONL** — structured data. Use jq or Python to parse and extract.
- **Log files** — typically need grep/awk/filtering, not summarization.
- **Source code files** — use grep, AST tools, or targeted reads with offset/limit.

### Also consider whether the task itself fits the pattern:
- **Suitable tasks**: summarization, information extraction, question answering over prose, finding specific sections in a long document.
- **Unsuitable tasks**: statistical analysis, counting, aggregation, joins, sorting, exact search — these need code, not parallel reading.

**If the file or task is unsuitable, do NOT proceed with this skill.** Instead, use the appropriate tool (Python/pandas for data, grep for logs, targeted Read with offset for code, etc.) and tell the user why you chose that approach.

---

## Workflow (only after confirming suitability)

## Kimi CLI Runtime Notes

Kimi CLI does not support ok_computer-style dynamic `create_subagent` plus
separate `task` calls. Use the built-in `Agent` tool directly:

- Use `subagent_type="explore"` for chunk readers.
- Put role instructions and task details into `prompt`; do not use `name` or
  `system_prompt` parameters.
- Newly created subagents do not inherit the main agent's context. Pass the
  original user question, chunk path, output expectation, and any constraints in
  every prompt.
- If this skill is running inside a subagent and the `Agent` tool is unavailable,
  either read chunks sequentially or ask the parent agent to launch chunk readers.

### Step 1: Split the Document

```bash
SKILL_DIR="${KIMI_SKILL_DIR:-$(pwd)/.agents/skills/longread}"
python "$SKILL_DIR/scripts/split_doc.py" <file_path>
```

The script will output JSON with chunk file paths:
```json
{
  "status": "success",
  "chunk_files": ["{workspace}/chunks/doc_part_1.txt", ...],
  "num_chunks": 5
}
```

### Step 2: Launch Reader Subagents

```
Use the Agent tool to launch one reader per chunk.

Each Agent tool invocation should include:
- `description`: "Read chunk {NN}"
- `subagent_type`: "explore"
- `prompt`: "You are a document reader. Read {chunk_file_path} and answer the original question: {user_question}. Extract key information, preserve page/section references when present, and summarize concisely. Write your answer in the user's language."
```

### Step 3: Launch in Bounded Rounds

For each chunk file, launch readers in bounded rounds, normally 3-5 at a time:

```
Agent(subagent_type="explore") -> Read {workspace}/chunks/doc_part_1.txt and summarize the key points.
Agent(subagent_type="explore") -> Read {workspace}/chunks/doc_part_2.txt and summarize the key points.
...
```

### Step 4: Aggregate Results

After all subagents complete, combine their summaries to answer the user's original question.

## Script Options

The split script supports:
- PDF, DOCX, TXT, MD, PPTX files
- Default chunk size: 32k tokens with 10% overlap
- Output directory: `{workspace}/chunks/`
