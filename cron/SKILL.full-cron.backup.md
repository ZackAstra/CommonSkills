---
name: cron
description: Author and manage recurring, one-time scheduled, or manually triggerable automation when the current session exposes a `Cron` external tool. Use when the user wants scheduled tasks, one-shot future jobs, nightly jobs, interval jobs, condition-based jobs, manual trigger jobs, or asks to create, update, inspect, test, or debug cron jobs through a single `Cron` tool with action-based parameters.
---

# Cron

Use this skill when the current session exposes a single `Cron` tool and the user needs cron job
authoring or operations guidance.

Do not assume every session has this tool. If `Cron` is unavailable, inspect the local Daimon docs
or source before promising cron support.

## Goal

1. Decide whether the user needs a persisted scheduled/manual job, including a one-time future job, or just an immediate one-off action.
2. Use the single `Cron` tool instead of editing persisted state by hand.
3. Choose the smallest correct trigger, execution mode, workspace binding, and delivery target set.
4. Validate with `status` or a safe manual `trigger` after changes when useful.

## Always pull the current time from Shell first

Before calling `Cron(action="create")` or `Cron(action="update")` for anything time-based, you MUST
fetch the current local time and timezone with Bash or Shell (for example
`date '+%Y-%m-%dT%H:%M:%S%z (%Z)'`). Use that command output as the authoritative "now":

- It is the basis for every `once` trigger's `at` field.
- It is the basis for any relative calculation (e.g. "in 10 minutes", "tomorrow 09:00").
- Cron expressions (`kind: "cron"`) are still evaluated in the Daimon daemon's local timezone — the Bash/Shell
  timestamp is what tells you which local time and timezone that is right now.

Do not rely on any pre-injected timestamp in the system prompt or on assumed session start time —
long-running sessions will produce stale scheduling if you skip this step.

## Cron tool shape

Use one tool:

```json
{
  "action": "create | update | delete | trigger | status",
  "...": "action-specific fields"
}
```

Key rules:

- `status` without `jobId` lists all jobs.
- `trigger` runs the job immediately regardless of its configured trigger kind.
- `update` requires `jobId` plus at least one editable field.
- For `create`, always include `trigger`, `execution`, and `delivery`.

## User-facing replies

Cron tool results are internal state. Do not paste the raw tool result JSON back to the user unless
they explicitly ask for debugging details.

After `create` or `update` succeeds, reply with a short natural-language confirmation that includes
only the useful user-facing fields:

- job name or task summary
- trigger time or schedule
- job id
- delivery target, when it helps disambiguate where results will go

Do not include the full `trigger`, `execution`, `delivery`, or stored job JSON in the user-facing
reply.

## Use cron when it is the right abstraction

Use cron when the task is:

- a one-time future timestamp with `kind: "once"`
- recurring on a schedule
- recurring by fixed interval
- gated by a condition module
- a stored workflow that should be manually triggerable later

Do not force cron when the user only wants:

- an immediate action right now that does not need to be stored or triggered later
- a long-lived worker or daemon

## Ask only for missing job-shaping facts

If the request is underspecified, clarify only:

- when it should run
- what it should execute
- where the results should go: channel delivery, a local conversation workspace, or no delivery

If the current surface is a local/client conversation, do not ask where results should go merely to
choose a delivery target. Default scheduled model work to a new local conversation in the current or
selected workspace, with `execution.kind: "local_conversation"` and `delivery.targets: []`.

If the user already gave enough information, create or update the job directly.

## Default by conversation surface

When the current session is a local/client conversation:

- use `local_conversation` by default for scheduled model work
- bind `workspacePath` to the current or explicitly selected workspace
- use `delivery: { "targets": [] }`
- use `agent_turn` with channel delivery only if the user explicitly asks to send, post, push,
  notify, or deliver the result to an IM/channel/external target

When the current session is an IM/channel conversation, use explicit `delivery.targets` only when the
user wants future results delivered to that route or another named target. Do not invent targets.

## Action guide

### `action: "create"`

Use for new jobs.

```json
{
  "action": "create",
  "name": "Nightly summary",
  "trigger": { "kind": "cron", "expr": "0 0 * * *" },
  "execution": {
    "kind": "agent_turn",
    "prompt": "Summarize nightly status for ops."
  },
  "delivery": {
    "targets": [
      { "channelId": "ops-main", "to": "@ops_room" }
    ]
  }
}
```

### `action: "update"`

Use for partial edits to an existing job.

```json
{
  "action": "update",
  "jobId": "cron-job-123",
  "enabled": false
}
```

### `action: "delete"`

Use to remove a persisted job.

```json
{
  "action": "delete",
  "jobId": "cron-job-123"
}
```

### `action: "trigger"`

Use for safe smoke tests or explicit manual execution.

```json
{
  "action": "trigger",
  "jobId": "cron-job-123"
}
```

### `action: "status"`

Use to inspect one job or the full set.

```json
{
  "action": "status"
}
```

```json
{
  "action": "status",
  "jobId": "cron-job-123"
}
```

## Trigger selection

### `cron`

Use for calendar schedules such as nightly, hourly, weekdays, or "every Monday".

- Shape: `{"kind": "cron", "expr": "..."}`
- Cron expressions are evaluated in the Daimon daemon's local timezone. Translate the user's intended
  local schedule directly instead of converting to UTC.

### `once`

Use for a persisted one-time future job at a specific timestamp.

- Shape: `{"kind": "once", "at": "2026-04-27T09:00:00+08:00"}`
- Build `at` from the current Shell time plus the user's requested time.
- Prefer including the local offset to avoid ambiguity.

### `interval`

Use for fixed cadence from the last fire time.

- Shape: `{"kind": "interval", "intervalMs": 600000}`
- Good for "every 10 minutes" or "every 6 hours".

### `condition`

Use when a code module decides whether the job should fire.

- Shape: `{"kind": "condition", "evaluate": "reports/should_run.py"}`
- Use a task-relative `.py` module path under the cron code task directory.
- The module must expose `should_fire(ctx)` and return a boolean.

### `manual`

Use when the user wants a stored workflow that does not auto-run.

- Shape: `{"kind": "manual"}`
- Validate later with `{"action":"trigger","jobId":"..."}` if useful.

## Execution selection

Cron has three execution shapes:

- `agent_turn`: run an independent background model turn that should report through `CronOutput`
  and then delivery.
- `local_conversation`: open a new normal local client conversation in a workspace and send the
  scheduled prompt there.
- `code`: run deterministic task-relative Python code.

For every configured model `prompt`, assume the prompt is a user request to the agent, written to
satisfy the user's intent. Do not write it as scheduler/operator instructions, cron mechanics,
manifests, delivery policy, or hidden metadata unless the user explicitly asked for those words to
appear in the agent's task.

### `agent_turn`

Use when the job should ask the model to reason, summarize, triage, or draft a message.

```json
{
  "kind": "agent_turn",
  "prompt": "Summarize overnight incidents and list only actionable follow-ups."
}
```

Optional fields may include:

- `agentId`: leave blank/unset by default. Only provide a non-empty `agentId` when the user or
  current context explicitly names the hosted agent that should run the turn.
- `workspacePath`: absolute Daimon workspace path for this `agent_turn`. Use it only when the user
  or current context explicitly selects a workspace/project; otherwise omit it and let Daimon use
  the default agent workspace.
- `timeoutMs`

Prefer short prompts with a clear output goal.
For delivery, cron `agent_turn` jobs should produce the final message content through `CronOutput`.
Do not instruct the agent to call `SendMessage` or any other direct delivery tool; Daimon delivers
the `CronOutput` result after the turn.

### `local_conversation`

Use when the scheduled work should become a normal local client conversation that the owner can
open, review, and continue in a specific workspace.

```json
{
  "kind": "local_conversation",
  "prompt": "Review this project and identify the highest-priority maintenance task.",
  "workspacePath": "/Users/me/Client Projects/demo-app"
}
```

Local conversation jobs use these rules:

- `workspacePath` is required and should be an absolute existing local workspace directory
- every run creates a new `origin: "client"` conversation with `activate: false`
- `prompt` is the user-visible query that appears in the created conversation; write it as the
  owner's direct request to the agent for satisfying the owner's intent, not as cron instructions,
  manifests, delivery policy, or hidden metadata
- the prompt is sent through the local-control conversation path unchanged
- the assistant response is stored in that conversation's Kimi Core records
- it does not use `CronOutput`
- it requires `delivery: { "targets": [] }`
- it supports `cron`, `once`, `interval`, and `manual` triggers only
- it does not support `condition` triggers in v1

Use this shape instead of `agent_turn` when the user wants a scheduled project conversation rather
than a background result delivered to a channel.

### `code`

Use when deterministic logic belongs in code rather than a model prompt.

```json
{
  "kind": "code",
  "module": "reports/daily_summary.py"
}
```

Code jobs use these rules:

- module paths must be task-relative `.py` paths under the cron code task directory
- modules must expose `run(ctx)`
- `workspacePath` is not supported for Python `code` cron jobs in v1; use `ctx["taskDir"]` and
  `ctx["runDir"]` instead
- return values must be JSON-serializable
- `None` suppresses delivery
- `{ "text": "...", "media": [...], "metadata": {...} }` maps to structured cron output

## Delivery

Every created job needs a `delivery` object. Jobs that deliver to channels need explicit delivery
targets. `local_conversation` is the exception: it must use an empty target list because its output
stays in the created local conversation.

```json
{
  "delivery": {
    "targets": [
      {
        "channelId": "ops-main",
        "to": "@ops_room"
      }
    ]
  }
}
```

Optional target fields may include:

- `accountId`
- `threadId`

Do not invent channel ids. Use targets that match the current Daimon config.

For a local conversation cron job, use:

```json
{
  "delivery": {
    "targets": []
  }
}
```

## Validation workflow

After creating or updating a job:

1. Run `Cron(action=status)` to confirm the stored shape.
2. If safe, run `Cron(action=trigger)` once.
3. Check execution and delivery results separately.
4. If code or condition modules are involved, verify the referenced path and return shape.

## Common failure modes

- choosing cron for an immediate one-off action that does not need stored scheduling
- translating local-time requirements into UTC cron expressions
- treating one-time future jobs as unsupported even though `kind: "once"` is valid
- forgetting that deliverable `create` calls need explicit delivery targets
- adding delivery targets to `local_conversation`, which must use `delivery.targets: []`
- using a `condition` trigger with `local_conversation`, which is unsupported in v1
- updating a job without any editable fields
- using a module path outside the cron code task directory
- returning non-JSON data from a code job

## Source of truth

Prefer local Daimon docs and source over memory.

If you are working inside the Daimon adapter repo, inspect:

- `packages/daimon/src/core/cron/tool-shared.ts`
- `packages/daimon/src/core/cron/execution.ts`
- `packages/daimon/src/core/cron/triggers.ts`
- `packages/daimon/src/core/cron/delivery.ts`
