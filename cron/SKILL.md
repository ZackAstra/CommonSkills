---
name: cron
description: Author and manage recurring, one-time scheduled, or manually triggerable local-conversation automation when the current session exposes a `Cron` external tool. Use when the user wants scheduled local client conversations, one-shot future jobs, nightly jobs, manual trigger jobs, or asks to create, update, inspect, test, or debug cron jobs through a single `Cron` tool with action-based parameters.
---

# Cron

Use this skill when the current session exposes a single `Cron` tool and the user needs cron job
authoring or operations guidance.

Do not assume every session has this tool. If `Cron` is unavailable, inspect the local Daimon docs
or source before promising cron support.

## Goal

1. Decide whether the user needs a persisted scheduled/manual local conversation, including a one-time future job, or just an immediate one-off action.
2. Use the single `Cron` tool instead of editing persisted state by hand.
3. Choose the smallest correct trigger and workspace binding.
4. Validate with `status` or a safe manual `trigger` after changes when useful.

Every cron job you create or update must be `local_conversation`. Do not create
`agent_turn`, `code`, `condition`, channel/IM, or external-delivery cron jobs
even if the tool schema still exposes those shapes.

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
- For `create`, `execution.kind` must be `"local_conversation"` and
  `delivery.targets` must be `[]`.

## User-facing replies

Cron tool results are internal state. Do not paste the raw tool result JSON back to the user unless
they explicitly ask for debugging details.

After `create` or `update` succeeds, reply with a short natural-language confirmation that includes
only the useful user-facing fields:

- job name or task summary
- trigger time or schedule
- job id
- local conversation workspace, when it helps disambiguate where results will go

Do not include the full `trigger`, `execution`, `delivery`, or stored job JSON in the user-facing
reply.

## Use cron when it is the right abstraction

Use cron when the task is:

- a one-time future timestamp with `kind: "once"`
- recurring on a schedule
- a stored workflow that should be manually triggerable later

Only use cron for work that can be represented as a local client conversation
created in a workspace. If the user asks for future channel delivery, IM
delivery, push notifications, external posting, deterministic code execution,
or condition-gated execution, say that cron jobs are local-conversation jobs and
offer to schedule the work as a local conversation.

Do not force cron when the user only wants:

- an immediate action right now that does not need to be stored or triggered later
- a long-lived worker or daemon

## Ask only for missing job-shaping facts

If the request is underspecified, clarify only:

- when it should run
- what it should execute
- which local workspace should own the generated conversation, when it is not clear

Do not ask where results should be delivered. Default scheduled model work to a
new local conversation in the current or selected workspace, with
`execution.kind: "local_conversation"` and `delivery.targets: []`.

If the user already gave enough information, create or update the job directly.

## Default shape

Use this shape for scheduled model work:

- `execution.kind: "local_conversation"`
- `execution.workspacePath`: the current or explicitly selected absolute local workspace path
- `delivery: { "targets": [] }`

Do not invent delivery targets. Do not create cron jobs that send to a channel,
IM route, webhook, external destination, or notification client.

## Action guide

### `action: "create"`

Use for new jobs.

```json
{
  "action": "create",
  "name": "Nightly project review",
  "trigger": { "kind": "cron", "expr": "0 0 * * *" },
  "execution": {
    "kind": "local_conversation",
    "prompt": "Review this project and identify the highest-priority maintenance task.",
    "workspacePath": "/Users/me/Client Projects/demo-app"
  },
  "delivery": {
    "targets": []
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
- For recurring jobs where the user did not explicitly request an exact minute, avoid scheduling at
  minute `0` / the top of the hour or minute `30` / the half hour. Choose a stable off-peak minute
  for that job, preferably in the `7` through `23` or `37` through `53` ranges, to avoid top- and
  half-hour task congestion across many jobs.
- If the user explicitly asks for an exact time such as `9:00` or `9:30`, a specific minute,
  market-open timing, a deadline, or any other time-sensitive exact schedule, honor the requested
  timing.

### `once`

Use for a persisted one-time future job at a specific timestamp.

- Shape: `{"kind": "once", "at": "2026-04-27T09:00:00+08:00"}`
- Build `at` from the current Shell time plus the user's requested time.
- Prefer including the local offset to avoid ambiguity.

### `manual`

Use when the user wants a stored workflow that does not auto-run.

- Shape: `{"kind": "manual"}`
- Validate later with `{"action":"trigger","jobId":"..."}` if useful.

## Execution selection

Use only `local_conversation`.

For every configured model `prompt`, assume the prompt is a user request to the agent, written to
satisfy the user's intent. Do not write it as scheduler/operator instructions, cron mechanics,
manifests, delivery policy, or hidden metadata unless the user explicitly asked for those words to
appear in the agent's task.

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
- it supports `cron`, `once`, and `manual` triggers only
- it does not support `condition` triggers in v1

Do not use `agent_turn` or `code` execution shapes in client-facing guidance.

## Delivery

Every created job needs a `delivery` object. Local conversation cron jobs must
use an empty target list because output stays in the created local conversation.

```json
{
  "delivery": {
    "targets": []
  }
}
```

Do not add channel, IM, webhook, notification, or external delivery targets.

## Validation workflow

After creating or updating a job:

1. Run `Cron(action=status)` to confirm the stored shape.
2. If safe, run `Cron(action=trigger)` once.
3. Confirm the job uses `execution.kind: "local_conversation"` and
   `delivery.targets: []`.
4. Confirm the generated run creates or updates a local conversation when you
   trigger it.

## Common failure modes

- choosing cron for an immediate one-off action that does not need stored scheduling
- translating local-time requirements into UTC cron expressions
- treating one-time future jobs as unsupported even though `kind: "once"` is valid
- trying to use `agent_turn`, `code`, or `condition` cron shapes for client-facing work
- adding delivery targets to `local_conversation`, which must use `delivery.targets: []`
- using a `condition` trigger with `local_conversation`, which is unsupported in v1
- updating a job without any editable fields

## Source of truth

Prefer local Daimon docs and source over memory.

If you are working inside the Daimon adapter repo, inspect:

- `packages/daimon/src/core/cron/tool-shared.ts`
- `packages/daimon/src/core/cron/execution.ts`
- `packages/daimon/src/core/cron/triggers.ts`
- `packages/daimon/src/core/cron/delivery.ts`
