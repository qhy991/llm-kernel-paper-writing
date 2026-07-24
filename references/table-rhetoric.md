# Experimental-table rhetoric

Use an experimental table as a compressed comparison protocol, not a numeric
dump. A reader moving left to right should be able to recover:

`scope → correctness gate → outcome → cost → boundary`

## Contents

- [Evidence boundary](#evidence-boundary)
- [Table Contract](#table-contract)
- [Main result table](#main-result-table)
- [Correctness and failure tables](#correctness-and-failure-tables)
- [Ablation table](#ablation-table)
- [Cost and efficiency table](#cost-and-efficiency-table)
- [Cross-hardware table](#cross-hardware-table)
- [Aggregation and uncertainty](#aggregation-and-uncertainty)
- [Formatting and emphasis](#formatting-and-emphasis)
- [Caption Contract](#caption-contract)
- [Audit](#audit)

## Evidence boundary

A scan of 80 saved arXiv/ar5iv HTML snapshots found 419 printed Table captions
in 73 papers. Among 396 HTML-encoded tables, the median structure was 9 rows by
5 columns; 101 had at least 8 columns. Caption scans found 24 broad
run/seed/trial lexical signals and one explicit confidence-interval statement.
The broad signals include false positives such as hardware-execution wording
or model names. These counts are navigation evidence, not proof that
unmentioned protocols are absent from the paper body. They motivate making
captions more self-contained.

Representative patterns include:

- AutoTriton (`2507.05687`) separates compilation/call, execution, `fast_1`,
  and `fast_2`;
- FastKernels (`2605.23215`) preserves Attempted, Blocked, Correct,
  geomean speedup, `fast@1`, and `fast@1.5` denominators;
- KernelBenchX (`2605.04956`) shows Compile, Correct, and Correct/Compile
  before conditionally aggregated speed;
- KernelCraft (`2603.08721`) couples success with iterations, tokens, and
  repeated runs;
- KernelFoundry (`2603.12440`) uses a source-device by target-device
  crossover to test hardware specificity.

Inspect the primary table, caption, and surrounding text before reusing any
metric or protocol.

## Table Contract

Fill this before arranging cells:

```text
Table ID:
Primary claim:
Analysis unit: task / kernel / run / device / configuration
Row object:
Column condition:
Workload / split / input shape:
Hardware / precision / software stack:
Budget / sampling / selection rule:
Baseline and baseline mode:
Correctness gate:
Metric / formula / denominator / good direction:
Aggregation:
Repeats / uncertainty:
Timeout / failure / missing-value policy:
Emphasis rule:
Data provenance:
Claim boundary:
```

Block the table if denominator, selection rule, or failed-sample policy is
unknown.

## Main result table

Prefer a two-level header:

```text
Method | Protocol | Coverage | Correctness              | Performance       | Cost
       | Budget   | N/Block | Compile | Execute | Correct | Fast@τ | Geo. spd. | /task
```

Define metrics operationally:

```text
Speedup = T_baseline / T_method
Correct rate = N_correct / N_attempted
Fast@τ = N(correct and speedup >= τ) / N_total
```

If speedup is aggregated only over correct kernels, show the correct count in
the same visible table. Separate eager, compiled, vendor, expert, production,
and analytical-bound baselines; they are not interchangeable. Disclose
best-of-N, best-turn, checkpoint selection, target-specific tuning, and every
other selection step that can change the result.

Do not:

- merge compile, execution, and semantic correctness into one Accuracy;
- compare one-shot, best-of-N, and iterative search without a matched budget;
- substitute maximum speedup for central tendency;
- silently drop timeout, OOM, unsupported, blocked, or incorrect tasks;
- rank results across different hardware, precision, baseline, or gate.

## Correctness and failure tables

Order stage gates causally:

```text
Attempted
→ Compiled
→ Launched/Called
→ Completed without timeout
→ Functionally/Semantically Correct
→ Numerically within tolerance
→ Faster than baseline
```

State whether each denominator is all tasks, attempted tasks, compiled tasks,
or the preceding stage. For a failure taxonomy, distinguish compilation,
runtime, timeout, OOM, wrong output, numerical mismatch, nondeterminism,
verifier rejection, performance regression, and unknown/other. Say whether
classes are first-terminal-stage or multi-label.

Use missing-value tokens with one meaning each:

- `0/N`: measured N objects and observed zero successes;
- `N/A`: not applicable;
- `NM`: not measured;
- `NS`: not supported;
- `CF`: compilation failure;
- `TO`: timeout;
- `OOM`: out of memory.

Do not report speed for an incorrect kernel. Zero observed false accepts is an
empirical result under the tested distribution, not a soundness proof.

## Ablation table

Treat an ablation as a matched intervention:

```text
Variant | Exact intervention | Correct n/N | Main metric | Δ vs Full | Budget | Runs/CI
```

Keep task, model/checkpoint, prompt, sampling, selection rule, hardware,
software, stopping rule, and budget fixed. Put Full in a fixed anchor row and
show `Δ vs Full`. Report a diagnostic matched to the mechanism: use
round-to-best or profiler calls for search efficiency, failure-stage changes
for correctness mechanisms, and measured work/resource counters for
performance mechanisms.

Disclose per-variant retuning and unmatched training checkpoints. A
leave-one-out configuration supports a scoped component contribution; it does
not alone establish a universal causal mechanism.

## Cost and efficiency table

Keep two cost families separate.

Agent/search cost:

```text
LLM calls; input/output tokens; candidate evaluations; compilations;
benchmark runs; profiler/verifier calls; wall time; GPU-hours; API cost;
cost/attempt; cost/correct
```

Generated-system cost:

```text
kernel latency; throughput; peak memory; compile latency; warm-up;
verification overhead; runtime overhead; measured energy
```

Bind cost to correctness or a fixed quality threshold. State concurrency,
tokenizer, model/provider/version, API-price date, included/excluded stages,
and the treatment of failed tasks. Parallel wall time is not total compute;
kernel runtime is not agent search cost.

## Cross-hardware table

Name the artifact-transfer protocol:

1. fixed binary;
2. fixed generated source, recompiled on the target;
3. fixed source with target-specific compile flags/configuration;
4. target-specific regeneration or retuning.

The first two are closer to portability/transfer; the latter two primarily
show adaptability. Include source and target hardware, software stack,
artifact policy, target information used, workload/shape/dtype, target-local
baseline, correctness, budget, unsupported cases, and worst-device result.

For multiple devices, use a source-device by target-device matrix. Rank only
within a target-device column. Keep measured and projected results separate.

## Aggregation and uncertainty

Separate:

- repeat-timing variability for one kernel/input/device;
- stochastic seed or search-trajectory variability;
- heterogeneity across tasks.

Use median plus IQR or named percentiles for microbenchmarks, mean plus
standard deviation or a confidence interval for repeated stochastic runs, and
median/geomean/ECDF for skewed across-task speedups. For small `n`, show raw
values, a range, or `n/N`; do not fabricate a stable CI.

Record warmup, synchronization, repeats, clocks/power policy, aggregation
level, bootstrap unit, confidence level, and random seed. If ranking
differences are within measurement noise, do not create a best method from
extra decimal places.

## Formatting and emphasis

- Put units and `↑/↓` in headers.
- Use consistent decimals and precision no finer than measurement noise.
- Prefer `n/N (%)` for small samples.
- Use grouped headers, booktabs-style rules, and few or no vertical lines.
- Keep baseline groups and method order stable across tables.
- Explain bold, underline, shading, color, and symbols in the caption.
- Rank only cells with matched hardware, precision, budget, baseline,
  selection rule, and correctness gate.
- Preserve regressions below `1×`; never rely on red/green alone.
- Move giant per-task matrices to the appendix; retain aggregate and decisive
  negative subgroups in the main text.
- Validate at final column width with text at least 7 pt.

Use a figure for distributions, trajectories, scaling, and phase changes. Use
a table for exact values, multi-metric protocols, and exceptions. If both show
the same data, the figure should expose the pattern and the table should
support exact audit.

## Caption Contract

Use:

> **[Narrow claim/question].** Under `[workload/split, hardware, precision,
> software, input, budget]`, compare `[methods]`. `[stage columns]` mean
> `[definitions]` with denominator `[N]`. `[metric]` is
> `[formula/denominator]`; `[↑/↓]` is better. Values are `[aggregation]` over
> `[runs/seeds/repeats]`; `[uncertainty]` means `[definition]`.
> `[timeout/OOM/blocked/incorrect]` follows `[policy]`. Emphasis marks only
> `[matched comparison set]`. The table supports `[conclusion]` within
> `[boundary]`.

Put secondary version and shape details in an explicit footnote or evaluation
setup, but keep every condition capable of changing rank visible or directly
referenced.

## Audit

- Can the reader identify analysis unit, scope, baseline, and denominator?
- Are compile, execution, semantic correctness, and performance separate?
- Is the budget and every selection rule explicit?
- Is aggregation over all tasks or only correct/supported tasks?
- Are repeats and uncertainty defined at the right sampling level?
- Do `0/N`, `N/A`, `NM`, failure, and unsupported have distinct meanings?
- Are Full ablation values identical to the main result under the same scope?
- Does cross-hardware mean fixed binary, same source, retune, or regenerate?
- Are projections separated from measurements?
- Do table, figure, abstract, and prose resolve to one result source?

If any answer is unknown, return to the comparison ledger before drafting the
caption or highlighting cells.
