---
name: fiction
type: standard
description: >
  Fiction writing — novels, novellas, short stories, flash fiction, and serialized
  narratives. All literary and genre fiction. Implements a 3-stage pipeline:
  outline design → serial write-review → assembly. Orchestrator
  delegates all tasks to subagents. ONE writer subagent per batch (1-5 chapters).
---

# Fiction Writing

## Kimi CLI Dispatch Adapter

This sub-skill may mention role names such as `fiction_writer` or older
`create_subagent` and `task` patterns. In Kimi CLI, translate them to direct
`Agent` calls:

- Use `subagent_type="coder"` for writers, file-writing fixers, assemblers, and format conversion.
- Use `subagent_type="plan"` for planners, reviewers, editors, and quality gates.
- Use `subagent_type="explore"` for reference intake, research, and read-only analysis.
- Put role rules, style constraints, anti-AI rules, input paths, output paths, and the concrete assignment into `Agent.prompt`; Kimi Agent has no `name` or `system_prompt` argument.
- Newly created subagents do not inherit main-agent context. Pass all necessary context explicitly, preferably through absolute file paths plus concise inline instructions.
- Launch independent work in bounded rounds. Use `run_in_background=true` only for non-blocking review or validation whose result is not immediately needed.

Orchestrate the full lifecycle of fiction: outline design, serial chapter writing with parallel review, and assembly. **The orchestrator never executes tasks directly** — all work (writing, reviewing, word count checking, assembly) is delegated to subagents via `create_subagent` + `task`.

> **CRITICAL — Serial Writing Rule**: Dispatch exactly ONE fiction_writer `task` call at a time. Each writer subagent handles 1-5 chapters per batch. NEVER dispatch multiple fiction_writer tasks in the same message. Wait for the current writer to finish + word count check + satellite file updates before dispatching the next writer. This is NON-NEGOTIABLE regardless of chapter dependency analysis.

> **CRITICAL — Review → Fix Brief → Dispatched Subagent**: When a review finds issues, translate them into a detailed fix brief (file paths, quoted findings, expected outcome, scope boundary, self-check) and dispatch a fresh subagent to apply the fix. Dispatched subagents re-read context, run self-checks, and preserve voice — inline sed/edit_file fixes create collateral damage. See "Review Checkpoint" below for dispatch patterns.

> **CRITICAL — Anti-Read-Loop Rule**: The orchestrator must dispatch its first subagent (requirement_analyst or fiction_writer) within 10 iterations. If the orchestrator has spent 10+ iterations only reading files without creating any subagent, it is in a read-loop. Stop reading, write plan.md from what you have, and dispatch the first subagent immediately.

> **CRITICAL — Delivery Strategy**: Write the full target by default. Only for very large novels (hundreds of chapters or 500K+ words) where the scope is genuinely impractical in one session, deliver the first few volumes with full quality (review + assembly + .docx) and ask the user for feedback. Even then, **Stage 1 must produce the complete fine outline for the entire novel first** so subsequent sessions write strictly from it. If the user asks to write everything at once, keep going. Re-dispatch on timeouts; rotate fresh writers on context fill. Always assemble + convert to .docx before ending.

Sub-skill of [general-writing](../SKILL.md). Inherits shared creative writing principles, anti-AI discipline, and quality gate framework.

## Trigger Keywords

小说, novel, short story, 短篇, 中篇, 长篇, 章节, chapter, 故事, narrative fiction, 微小说, flash fiction, 连载, 网文, web novel, 仙侠, 玄幻, 言情, 悬疑, 科幻, 奇幻

## Workflow Decision Tree

```
User Query
  │
  ├─ Flash fiction (< 1k words)
  │   → single writer subagent, no state documents, no review pipeline
  │
  ├─ Short fiction (1k-15k words)
  │   → Stage 1 (light outline, single volume) → Stage 2 → Stage 3
  │
  ├─ Novella / novel (15k+ words)
  │   → Stage 1 (full 3-phase) → Stage 2 → Stage 3
  │
  ├─ Provides outline + asks for writing
  │   → Stage 2 → Stage 3
  │
  └─ Asks for outline only → Stage 1 → convert outline.md to .docx → deliver
```

Infer genre, length, POV, tense, tone, audience, protagonist, structural model, and constraints from the user's request and any uploaded files. The orchestrator analyzes and infers all parameters autonomously; for complex requests, deploy a subagent to analyze requirements in depth. Never prompt the user for clarification.

---

## File Paths

### Output Directory Structure

```
{workspace}/
├── research/                                    # User uploads copied here (Step 0)
│   └── {uploaded_file}                          # Preserved original filename
├── {project_name}.outline.md                    # Master outline (foundation + volume structure + file index)
├── {project_name}.outline_vol{NN}.md            # Per-volume working outline (chapter status + working window)
├── {project_name}.final.md                      # Final assembled output (Stage 3)
├── documents/
│   ├── {project_name}.outline_raw.md            # Full chapter specs archive (planning layer)
│   ├── {project_name}.characters.md             # Character profiles (state layer)
│   ├── {project_name}.world.md                  # World bible (state layer)
│   ├── {project_name}.foreshadowing.md          # Foreshadowing registry (state layer)
│   ├── {project_name}.threads.md                # Thread tracker (state layer)
│   └── {project_name}.chapter_summaries.md      # Done blocks (record layer)
└── chapters/
    ├── {project_name}.ch01.md                   # Chapter output files
    └── ...
```

### User-Uploaded Files

Before Stage 1, copy all user-uploaded files (reference materials, existing outlines, character sheets, world-building docs) to `{workspace}/research/`. Preserve original filenames. Reference these copies (not originals) in all subagent task prompts — subagents may run in sandboxed environments without access to the original paths.


## Stage 1: Outline Design

**Read [outline-guide.md](./outline-guide.md) first.** It defines the project workspace structure, file templates, update mechanism, and integrity rules.

**Goal**: Create the project workspace at `{workspace}/` with all files per outline-guide.md Modules section. Three-phase process: macro → coarse outline (粗纲) → fine outline (细纲).

### Phase 1: Macro — Foundation + Characters + World

Sequential-then-parallel. First extract requirements, then design structure, then build world and characters in parallel.

**Step 1** — `requirement_analyst`

`create_subagent`:
- `name`: `"requirement_analyst"`
- `system_prompt`: "You analyze fiction writing requests. Extract genre, length, POV, tone, audience, constraints, and structural model from the user query and any uploaded files. Output a structured requirements document."
- `description`: "Extract fiction requirements from user query"

`task`:
- `agent`: `"requirement_analyst"`
- `prompt`: Include full user query text + uploaded file paths (from `{workspace}/research/`). Specify return format: structured markdown covering genre, subgenre, length target, POV, tense, tone, audience, protagonist sketch, structural model, constraints. All fields must have specific values.

**Step 2** — `structure_designer`

`create_subagent`:
- `name`: `"structure_designer"`
- `system_prompt`: "You design fiction story structures. Given requirements, produce: premise, theme, plot point sequence (8-15 events), total chapter count, and word count plan."

`task`:
- `agent`: `"structure_designer"`
- `prompt`: Inline the full requirements output from Step 1 (paste content, not file reference). Specify return: premise (1 sentence), theme, ordered plot points (8-15), total chapter count, per-chapter word target.

**Step 3** — parallel (dispatch both `task` calls in a single message):

**`world_builder`**

`create_subagent`:
- `name`: `"world_builder"`
- `system_prompt`: "You create fictional settings. Produce: key locations with sensory details (sight/sound/smell), world rules (what is possible/impossible), props inventory. Every location needs a narrative function."

`task`:
- `agent`: `"world_builder"`
- `prompt`: Inline requirements (Step 1) + structure (Step 2) outputs. Return: locations table, world rules, props inventory.

**`character_designer`**

`create_subagent`:
- `name`: `"character_designer"`
- `system_prompt`: "You design fictional characters. For each character produce: role, desire, fear, arc trajectory (start→end), voice signature, relationships, and contradiction. Characters must create mutual conflict." Inline Core Architecture, Depth Layers, and Relationship Design from `references/character-building.md`.

`task`:
- `agent`: `"character_designer"`
- `prompt`: Inline requirements (Step 1) + structure (Step 2) outputs. Return: character profiles per `characters.md` template, relationship web with tension sources.

**Phase 1 Output** — orchestrator creates files per outline-guide.md Modules section. At this point `outline.md` contains Foundation, Plot Points, File Index, Progress. Volume Structure and Chapter Status are empty.

### Phase 2: Coarse Outline (粗纲) — Volume Structure

**`volume_planner`**

`create_subagent`:
- `name`: `"volume_planner"`
- `system_prompt`: "You divide a novel into volumes (卷), each a self-contained narrative arc. For each volume produce: title, chapter range, core conflict, character focus, arc trajectory (start→end state), key events (3-5), turning point. Volumes connect — each end state feeds the next start state."

`task`:
- `agent`: `"volume_planner"`
- `prompt`: Inline Foundation + plot points + character arcs + world rules (paste content). Return: ordered volume list. Success criteria: all plot points assigned, arcs span coherently, end states chain.

Orchestrator writes Volume Structure into `outline.md`, validates coverage.

### Phase 3: Fine Outline (细纲) — Per-Chapter Specs

One volume per `task` call. Parallelize across volumes.

**`micro_outline_designer`**

`create_subagent`:
- `name`: `"micro_outline_designer"`
- `system_prompt`: "You design per-chapter specs for one volume. Per chapter: POV, scene count, word target, core conflict, hook-in, hook-out, key beats, foreshadowing IDs, dependencies. Chapters must serve the volume's arc. Dependencies form a valid DAG."

`task` (multiple calls in one message for parallel volume processing):
- `agent`: `"micro_outline_designer"`
- `prompt`: Inline: volume spec + `characters.md` + `world.md` + `foreshadowing.md`. Return: ordered chapter specs for this volume.

**Phase 3 Process**: Dispatch per volume → merge into `outline_raw.md` → create per-volume `outline_vol{NN}.md` files (chapter status + seed Working Window) → populate master `outline.md` (volume status, file index, progress) → validate cross-volume continuity.

### Dependency Graph

Build from `outline_raw.md` chapter `Deps` fields:
- Chapters within a volume: generally sequential.
- Independent POV threads across volumes: parallelizable.
- Volume-opening chapters: depend on previous volume's final chapter.

---

## Stage 2: Write-Review Pipeline

**CRITICAL**: Writing is SERIAL — dispatch ONE fiction_writer `task` call at a time. Reviews are PARALLEL — dispatched alongside the next writer. Never dispatch multiple fiction_writer tasks in the same message. This is NON-NEGOTIABLE.

> **Design Principle — File-Path-Based Communication**: The fiction_writer reads `outline.md` and satellite files directly from the shared workspace. The orchestrator passes **file paths, not inlined content**. This keeps the orchestrator lightweight and ensures writers always see the latest state.

> **Review Pipeline — Always Dispatch**: After every batch completes and quality check passes, dispatch review tasks in the SAME message as the next fiction_writer. Reviews run in the background — they don't block the next writer — so there's no speed cost to running them. Every batch gets reviewed; reviews produce the findings that become fix briefs in the Review Checkpoint.

### Batch Selection

The orchestrator selects the next batch:
1. Identify the next contiguous range of chapters to write.
2. Assign **1-5 chapters** to a single writer subagent. Batch size depends on total chapter count:
   - ≤ 20 chapters total → 1-2 per batch
   - 21-100 chapters → 2-3 per batch
   - 101-200 chapters → 3-5 per batch
   - > 200 chapters → 5 per batch
3. **ONE writer per batch** — never split a batch across multiple writer subagents.

### Writer Setup

**`fiction_writer`**

`create_subagent`:
- `name`: `"fiction_writer"`
- `description`: "Write fiction chapter(s) from outline spec, update satellite files"
- `system_prompt`: Compose per [references/writer-system-prompt.md](./references/writer-system-prompt.md) — 14 components including role, genre constraints, voice rules, anti-AI, dialogue, hooks, expansion techniques, quality self-check. **Additionally include**: "After writing each chapter, update satellite files that exist and were affected. Read the File Index in outline.md to locate available satellite files. Not every file needs updating for every chapter — only update what's present and relevant."

### Chapter Dispatch

`task` (**ONE call per batch — NEVER multiple fiction_writer tasks in the same message**):
- `agent`: `"fiction_writer"`
- `prompt` — pass file paths + metadata, NOT inlined content:

```
Write chapter(s) {N} (to {M} if multi-chapter batch).

## File Paths
- Volume outline: {workspace}/{project_name}.outline_vol{NN}.md
  → Read "Working Window" for chapter spec, previous summary + hook-out, next chapter preview
- Master outline: {workspace}/{project_name}.outline.md
  → Read "File Index" to locate all satellite files (characters, foreshadowing, threads, world, chapter_summaries)
- Previous chapter: {workspace}/chapters/{project_name}.ch{N-1}.md
- Output: {workspace}/chapters/{project_name}.ch{NN}.md

## Writing Requirements
- Target: {word_count} words per chapter
- {style/genre/tone requirements}

## Post-Writing: Update Satellite Files (MANDATORY)
After writing each chapter, update the satellite files that exist and were affected (paths in master outline.md § File Index). Common updates include:
1. outline_vol{NN}.md — Chapter Status (WRITING→DONE + word count), Working Window (slide forward)
   outline.md — Progress (increment count/words)
2. chapter_summaries.md — Append Done block (200-300w summary + characters + hook-out + foreshadowing + threads)
3. characters.md — Update Current State, Last Seen, Arc for changed characters
4. foreshadowing.md — New plants→OPEN, paid→CLOSED
5. threads.md — New→ACTIVE, advanced→update Last Ch, resolved→RESOLVED
6. world.md — Update Last Used, add new locations/rules/props
Note: Not all files may exist or need updating for every chapter. Only update files that are present and affected by the chapter's content. If the File Index lists additional satellite files beyond this list, update those too when relevant.

## Return Format
Return: chapter file path(s) + word count per chapter + hook-out + characters appearing
```

**Volume-opening chapters**: mention the volume header info (title, core conflict, turning point) directly in the task prompt — do NOT pass the `outline_raw.md` path. `outline_raw.md` can be 300KB+ and will exhaust the writer's token budget.
**Final chapters**: mention to pay special attention to foreshadowing registry + character arc completion.

### Per-Batch Completion Flow

After fiction_writer returns, dispatch ALL of the following in a **single message** (4-5 `task` calls):

1. **Next `fiction_writer`** — write next batch of chapters (same format as above)

2. **`quality_checker`** (NON-BLOCKING, runs in parallel with next writer):
   - `system_prompt`: "Run `GW_SKILL_DIR=\"${KIMI_GENERAL_WRITING_SKILL_DIR:-$(pwd)/.agents/skills/general-writing}\"; python \"$GW_SKILL_DIR/scripts/check_chapter_quality.py\" <file> --min-words <target> --lang auto`. Return JSON with word_count, em_dash density, english_leakage. Highlight any FAIL items."
   - `prompt`: Check `chapters/{project_name}.ch{NN}.md` against target word count, em-dash density ≤5 per 1000 chars, no English leakage.
   - On FAIL: coordinator dispatches a fix subagent with a detailed brief (max 2 retries).

3. **`continuity_editor`** (NON-BLOCKING):
   - `system_prompt`: See `../review.md`. Inline `references/consistency.md`.
   - `prompt`: Review chapters {N}-{M} for continuity against satellite files. Return numeric score (0-100) and verdict: PASS (≥85) / WARNING (75-84) / REVISE (<75).

4. **`style_editor`** (NON-BLOCKING):
   - `system_prompt`: See `../review.md`. Inline `../anti-ai.md` + `references/quality-checklist.md`.
   - `prompt`: Review chapters {N}-{M} for style, em-dash density, AI vocabulary patterns, English leakage. Return score + verdict.

5. **`satellite_reviewer`** (NON-BLOCKING):
   - `prompt`: Verify satellite files updated correctly after chapters {N}-{M} (Chapter Status, Working Window, chapter_summaries, characters, foreshadowing, threads). Return PASS/FAIL per file.

**Step 3: Review Checkpoint — Collect, Consolidate, Fix**

When the parallel reviewers (quality_checker, continuity_editor, style_editor, satellite_reviewer) return, **collect all findings first**, then dispatch fixes:

1. **Collect**: Read all reviewer verdicts and findings for the batch.
2. **Consolidate per chapter**: Merge findings from different reviewers into one list per chapter (e.g., Ch03 has em-dash issue from style_editor + name error from continuity_editor + word count fail from quality_checker).
3. **Dispatch one fix subagent per chapter**: Write a single brief covering all issues for that chapter and dispatch a fresh `fiction_writer` (or `proofreader` for mechanical fixes). The brief must include: file path, quoted findings from each reviewer, expected outcome, scope boundary (what not to touch), self-check to run before returning.
4. For mechanical fixes spanning multiple chapters (e.g., name replacement), batch into one dispatch.

**Verdict actions**:
- All PASS — proceed to next batch
- Any WARNING/REVISE/FAIL — consolidate findings, dispatch fix subagent(s), re-check once
- FORCED PASS (after 2 fix attempts) — add remaining issues to backpatch queue, proceed

### Pipeline Flow

```
Batch 1: [fiction_writer → Ch1-3 + update satellites]
              ↓
          dispatch in ONE message:
          ┌─ [fiction_writer → Ch4-6]          ← next batch (SERIAL)
          ├─ [quality_checker → Ch1-3]          ← PARALLEL
          ├─ [continuity_editor → Ch1-3]        ← PARALLEL
          ├─ [style_editor → Ch1-3]             ← PARALLEL
          └─ [satellite_reviewer → Ch1-3]       ← PARALLEL
              ↓
          ★ REVIEW CHECKPOINT for Ch1-3 ★
            → PASS: proceed
            → WARNING/REVISE/FAIL: dispatch fix subagent → re-check
              ↓
          dispatch in ONE message:
          ┌─ [fiction_writer → Ch7-9]
          ├─ [quality_checker → Ch4-6]
          ├─ [continuity_editor → Ch4-6]
          ├─ [style_editor → Ch4-6]
          └─ [satellite_reviewer → Ch4-6]
          ...
```

### Final Batch Protocol

The final batch has no next writer to parallelize with. The final chapters (climax/resolution) need the most care.

1. Dispatch `fiction_writer` for the final batch, wait for completion
2. Dispatch quality_checker + continuity_editor + style_editor + satellite_reviewer in parallel, wait for all to return
4. Process review results per Step 3 above, dispatch fix subagents for any WARNING/REVISE
5. Clear any previously deferred review checkpoints
6. Proceed to Stage 3 only after all reviews have been processed

### Cross-Chapter Review

After all chapters are written and per-chapter reviews complete:

1. **`structural_editor`** — reads all chapters + Volume Structure. See `../review.md` for definition. Returns: structural assessment + fix recommendations.
2. **`pacing_editor`** — reads all chapters + Volume Structure. Returns: per-chapter pacing assessment + tension curve analysis.

`create_subagent`:
- `name`: `"pacing_editor"`
- `system_prompt`: "You evaluate fiction pacing: hook effectiveness, scene-level rhythm (goal-conflict-outcome), action-vs-reflection balance, tension curve. Check against `references/quality-checklist.md` § Hook & Suspense and § Pacing & Rhythm."

### Volume Boundary Review

When the last chapter in a volume completes, trigger the Volume Boundary Review protocol per `references/consistency.md` § Cross-Volume Continuity. All 4 steps executed by subagents.

---

## Stage 3: Assembly & Delivery

All work delegated to subagents. **This stage runs whenever writing stops** — whether the full novel is complete or a planned volume delivery point is reached.

### Step 1: Assemble — `assembly_agent`

`create_subagent`:
- `name`: `"assembly_agent"`
- `system_prompt`: "You assemble fiction manuscripts. Concatenate chapter files in order with a table of contents organized by volume. Output a single markdown file."

`task`:
- `agent`: `"assembly_agent"`
- `prompt`: Read all `chapters/{project_name}.ch*.md` files written so far. Concatenate with TOC (by volume). Write to `{workspace}/{project_name}.final.md`.

### Step 2: Backpatch — `backpatch_agent` (if queue non-empty)

If the backpatch queue contains items, dispatch per `../review.md` § Backpatch Protocol.

`create_subagent`:
- `name`: `"backpatch_agent"`
- `system_prompt`: "You fix narrative inconsistencies in completed fiction manuscripts. Follow the Backpatch Protocol: sort by severity, apply minimal fixes (max 2 paragraphs each), verify against satellite files, update chapter_summaries.md."

### Step 3: Convert to .docx

Convert the assembled markdown to .docx using the `md2docx` pipeline (the docx skill's md2docx route). If the user requests a different format (e.g., `.pdf`), use the corresponding skill instead.

Output: `{workspace}/{project_name}.final.docx`

**This step is mandatory every time Stage 3 runs.** Raw `.md` without a formatted deliverable is not an acceptable end state.

### Final Output

- `{workspace}/{project_name}.final.md`
- `{workspace}/{project_name}.final.docx`

### Long Novel: Volume Delivery Points

For very large novels (hundreds of chapters or 500K+ words) where the full scope is split across sessions:
- Stage 1 produces the **complete fine outline for the entire novel** before any writing begins. This ensures all sessions write from the same outline with no deviation.
- Enter Stage 3 at each volume delivery point. The assembled files contain all chapters written so far.
- Satellite files remain in the workspace for the next session to pick up from.
- When the entire novel is finally complete, the last Stage 3 run produces the definitive `{project_name}.final.md` and `{project_name}.final.docx` containing the full work.

---

## Core Principles

1. **Orchestrator = lightweight coordinator.** Passes file paths to subagents, dispatches tasks, checks quality. Never writes prose, never summarizes chapters, never manually updates satellite files. The fiction_writer handles both writing and satellite updates.
2. **File-path-based communication.** Pass the correct volume outline (`outline_vol{NN}.md`) + master outline (`outline.md`) + previous chapter path to fiction_writer. The writer reads the volume outline for chapter specs/window and the master outline for satellite file paths. Never inline satellite file content into task prompts.
3. **Serial writing, parallel review.** ONE fiction_writer at a time. After quality check, dispatch the next writer + review tasks for the previous batch in a SINGLE message.
4. **Reviews → fix brief → dispatched subagent.** When a review finds an issue, write a detailed fix brief (file paths, quoted findings, expected outcome, scope boundary, self-check) and dispatch a fresh subagent. Inline edits create collateral damage. See "Review Checkpoint" § for dispatch patterns.
5. **Writer owns satellite updates.** The fiction_writer updates outline.md, chapter_summaries.md, characters.md, foreshadowing.md, threads.md after writing. The satellite_reviewer verifies updates in parallel.
6. **Final batch is never skipped for review.** The last batch's chapters (climax/resolution) are the most important to review. Never trade review coverage for assembly time.
7. **Quality over quantity.** Polished chapters with review + .docx are better than rushed chapters with no assembly. Always assemble + convert to .docx before ending.
8. **User instructions take priority.** When user requirements conflict with this skill's defaults, adapt the framework to serve the user's intent.
9. **Language consistency.** All content — prose, dialogue, narration, subagent names, prompts — must match the user's language. Never mix languages unless the user explicitly requests it.
10. **Rewrites are in-place.** No version proliferation.

---

## Reference Files

| File | When to Read | Content |
|------|-------------|---------|
| [outline-guide.md](./outline-guide.md) | Before Stage 1 | Project workspace, file templates, update mechanism, sliding window, integrity rules |
| [references/writer-system-prompt.md](./references/writer-system-prompt.md) | Before creating `fiction_writer` | 14-component system prompt assembly guide |
| [../anti-ai.md](../anti-ai.md) | Inlined into writer + style_editor prompts | AI pattern avoidance rules |
| [../review.md](../review.md) | Before Stage 2 review dispatch | Shared editor definitions, quality gate, backpatch protocol |
| [../scripts/check_chapter_quality.py](../scripts/check_chapter_quality.py) | `quality_checker` subagent runs it | Chapter quality verification (word count + em-dash density + English leakage) |
| [references/quality-checklist.md](./references/quality-checklist.md) | Review editors + final_check_agent | Per-chapter quality checklist, hook/pacing checks, assembly checklist |
| [references/consistency.md](./references/consistency.md) | `continuity_editor` + volume boundary review | Satellite file discipline, cross-volume continuity protocol |
| [references/content-expansion.md](./references/content-expansion.md) | Inlined into writer prompt (via writer-system-prompt.md) | 7 expansion techniques with genre priorities |
| [references/character-building.md](./references/character-building.md) | `character_designer` + writer prompt | Character depth, voice, relationships, introduction rules |
