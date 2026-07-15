---
name: seaborn-visualization
description: charting, plotting, graphing, visualization, seaborn, matplotlib, pandas reports, Chinese chart labels, and data-viz code in Daimon's managed Python runtime. Covers both interactive (PythonRun, when the user is waiting) and cron (scheduled/recurring) callers.
---

# Seaborn Visualization

Use this skill for charting, plotting, graphing, visualization, seaborn, matplotlib, pandas, Chinese chart labels, visual reports, and data-viz code in Daimon's managed Python runtime.

Use pandas DataFrames for tabular data and seaborn for statistical charts. Use matplotlib only for the `Agg` backend, layout, fonts, and saving — never call `plt.show()`. The bundled CJK fonts (`NotoSansCJKsc`) handle Chinese chart labels.

Daimon's managed Python execution passes a context dict to the entry function and expects JSON-serializable data back. From your code, import helpers:

```python
from daimon_runtime import setup_plot, save_figure
```

Call `setup_plot(ctx)` before creating figures. It configures matplotlib `Agg`, the runtime cache, bundled CJK fonts, seaborn defaults, and negative sign rendering.

Save figures and other outputs under `ctx["runDir"]`. `save_figure` leaves figures open by default; pass `close=True` (or call `plt.close(fig)`) after saving when a task creates many figures.

## Pick the right caller

There are two callers, distinguished by who is waiting:

- **Interactive — the user asked for a chart now.** Use the `PythonRun` tool. Do NOT create a cron job for one-off requests.
- **Cron — recurring or scheduled.** Use a cron `execution.kind: "code"` job with a `<task>/<file.py>` module exposing `run(ctx)`.

### Interactive: `PythonRun`

When the user is waiting on the chart in this conversation, call `PythonRun({ code, function_name?, timeoutMs? })`. The tool runs your code immediately in the managed runtime and returns `{ ok, output, runDir, files, ... }`. It defaults to a 600000ms timeout; omit `timeoutMs` for ordinary charts, and set it only when the requested one-shot analysis clearly needs a different bounded budget. After it returns, deliver the file paths under `runDir`/`files` to the user (e.g. attach as media in your reply).

```python
def main(ctx):
    from daimon_runtime import setup_plot, save_figure
    import pandas as pd
    import seaborn as sns
    import matplotlib.pyplot as plt

    setup_plot(ctx)
    df = pd.DataFrame({"x": [...], "y": [...]})
    fig, ax = plt.subplots(figsize=(9, 5))
    sns.lineplot(data=df, x="x", y="y", ax=ax)
    media = save_figure(ctx, fig, "chart.png", close=True)
    return {"chart": media, "rows": len(df)}
```

The tool returns the absolute path of `chart.png`. Use that path to deliver the chart to the user.

### Cron: `execution.kind: "code"`

For scheduled or recurring work, create a cron code job with `execution.kind: "code"` and a task-relative `<task>/<file.py>` module under the owning agent's `~/.kimi/daimon/agents/<agentId>/code/cron/<task>/` directory. The managed `runner.py` imports the module, calls `run(ctx)`, and expects a JSON-serializable return.

```python
from daimon_runtime import setup_plot, save_figure, cron_output

def run(ctx):
    setup_plot(ctx)
    # ... build DataFrame, plot ...
    return cron_output(
        text="Chart generated.",
        media=[save_figure(ctx, fig, "chart.png")],
        metadata={"rows": len(df)},
    )
```

`cron_output` is the structured shape that cron delivery consumes. Do not use it from `PythonRun`; return a plain dict there.
