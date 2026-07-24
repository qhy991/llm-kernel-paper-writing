# Narrative logic for LLM kernel papers

## Contents

- [The paper needs one center of gravity](#the-paper-needs-one-center-of-gravity)
- [Canonical argument chain](#canonical-argument-chain)
- [Abstract contract](#abstract-contract)
- [Introduction moves](#introduction-moves)
- [Observed Introduction variants](#observed-introduction-variants)
- [Method-section logic](#method-section-logic)
- [Evaluation-section logic](#evaluation-section-logic)
- [Mechanism language](#mechanism-language)
- [Related work](#related-work)
- [Discussion and conclusion](#discussion-and-conclusion)

## The paper needs one center of gravity

Do not organize the story around “LLMs can generate kernels.” That is a field
description, not a research tension. Select one falsifiable center:

- a policy improves while a static skill library becomes stale;
- a sound optimization intent is discarded because one implementation fails;
- correctness rewards admit reward hacking or lazy optimization;
- an agent-editable megakernel lacks a safe and portable edit surface;
- aggregate benchmark scores hide task-category capability boundaries;
- measured speedup does not say how far a kernel remains from hardware limits.

Every challenge, module, experiment, and figure should return to that tension.

## Canonical argument chain

Use:

`stakes → bottleneck → gap → insight → mechanism → evidence → boundary`

The links answer different questions:

- **stakes**: why this kernel/workload/system matters;
- **bottleneck**: what concrete technical failure prevents the desired outcome;
- **gap**: what the closest prior mechanisms cannot handle;
- **insight**: what property changes the way the problem should be represented;
- **mechanism**: which state, transformation, feedback, or invariant realizes
  the insight;
- **evidence**: which correctness, performance, diagnostic, and external-validity
  tests support the claim;
- **boundary**: where the mechanism is untested, loses, or depends on a condition.

Never replace the gap with “few works study X.” Never replace the insight with a
component list.

## Abstract contract

Write six compact moves:

1. task and consequence;
2. precise failure or unanswered question;
3. method and mechanism, not only the system name;
4. evaluation scope: tasks, hardware, baselines, and metric family;
5. two or three scoped results, including one diagnostic finding;
6. limitation, released artifact, or practical implication.

Benchmark abstracts should lead with the unanswered evaluation question and
their empirical findings. Verification papers should state what is guaranteed,
what is only empirically checked, and the trusted base. Performance-analysis
papers should distinguish achieved performance from theoretical or analytical
bounds.

## Introduction moves

### Move 1: establish the real system

Start with a concrete deployment or engineering setting:

- batch-1 decode is memory-bound;
- modern serving relies on GQA, MLA, MoE, or fused attention kernels;
- porting across Hopper, Blackwell, AMD, MUSA, or NPU changes constraints;
- PyTorch eager or vendor libraries establish a demanding reference.

Name the workload and cost. Avoid generic “AI is developing rapidly.”

### Move 2: decompose the technical difficulty

Use two or three coupled constraints, such as:

- tiling, layout, synchronization, and architecture-specific primitives;
- correctness plus performance plus search budget;
- compiler/runtime failure isolation plus GPU scheduling;
- numerical precision contract plus hardware portability;
- launch overhead plus intermediate HBM traffic.

The difficulty should predict the evaluation protocol later.

### Move 3: compare the nearest mechanisms

Organize prior work by the decision it makes, not a chronological list:

- one-shot generation versus feedback-driven optimization;
- direct program-space evolution versus intent-level planning;
- static retrieval versus frontier-aware skill maintenance;
- output testing versus specification/static/symbolic verification;
- aggregate runtime benchmark versus category-aware diagnostic evaluation;
- profiler measurement versus analytical SOL estimation.

State what each class handles before stating what it misses.

### Move 4: expose a concrete failure mode

Good failures are observable:

- a correct kernel is slower than the reference;
- a policy exploits the reward harness;
- an intermediate edit fails to compile although the multi-step direction is
  sound;
- a kernel passes weak output tests by chance;
- a bound is violated because the analysis omitted traffic;
- a method improves compile rate while reducing speedup.

Use a motivated example or early figure when the failure is hard to explain in
one sentence.

### Move 5: state the mechanism-level insight

Examples of valid insight form:

- decouple high-level optimization intent from low-level instantiation;
- confine the LLM to a verifiable translation and keep the bound computation
  deterministic;
- co-evolve knowledge selection and summarization with the policy frontier;
- restrict agent edits to a typed schedule IR and validate graph invariants
  before launch;
- stratify results by task structure because category explains more variation
  than method identity.

The insight should make at least one rejected alternative predictable.

### Move 6: present method and headline evidence

Give the minimum mechanism necessary to understand why the result is plausible.
Then state results with scope:

> On [tasks] under [hardware/precision/budget], [method] improves [metric]
> relative to [baseline]. [Ablation/trace/counterexample] supports the role of
> [mechanism], while [failure] limits the conclusion to [boundary].

Do not report a maximum without the typical statistic. Do not report a relative
gain without the denominator.

### Move 7: contributions

Contributions should be audit handles:

1. formulation or system mechanism;
2. environment, compiler, data, or benchmark artifact;
3. evaluation and headline result;
4. diagnostic finding, negative result, or released resource.

Each contribution maps to a section and at least one figure, table, algorithm,
equation, or artifact.

## Observed Introduction variants

### Five-paragraph method paper

K-Search uses:

1. real kernel importance;
2. manual optimization and budget difficulty;
3. structural failure of program-space evolution;
4. planning/instantiation separation;
5. fixed-budget results and mechanism callback.

Use this compact form when one insight explains one mechanism.

### Failure-first RL paper

Dr. Kernel uses:

1. kernel importance and manual difficulty;
2. why RL fits, then reward hacking and lazy optimization;
3. robust environment as prerequisite;
4. RL estimator, stability fixes, profiling reward, and results.

Use it when the environment and training objective are themselves
contributions.

### Claim-with-boundary system paper

AutoMegaKernel repeatedly pairs:

`claim → numerical evidence → evidence type → explicit non-claim`

Examples include distinguishing an empirical safety result from a formal proof,
self-relative search gains from external-baseline wins, and mixed-precision
gains from equal-precision comparisons. Use this pattern for systems with a
trusted base, safety gate, or precision trade-off.

### Evaluation-question benchmark paper

KernelBenchX uses:

1. field progress;
2. existing benchmark landscape;
3. unresolved capability-boundary questions;
4. taxonomy, stronger correctness, and efficiency measurements;
5. systematic comparison;
6. contributions and findings.

Use it when the paper's contribution is the question and measurement design.

### Analytical-bound paper

SOLAR uses:

1. why analytical ceilings matter to engineers, architects, and agents;
2. why counters, profilers, and pure LLM estimation do not derive the bound;
3. generative translation plus deterministic lifting and analysis;
4. a motivated headroom figure and three contribution classes;
5. use cases across kernels, models, hardware projection, and provisioning.

Use it when the central artifact maps programs to a physical or analytical
limit.

## Method-section logic

Order by dependency, not implementation chronology:

1. problem formulation and objective;
2. state and artifacts;
3. invariants, correctness gates, or trusted boundary;
4. core decision mechanism;
5. feedback/update loop;
6. termination and budget;
7. training or initialization;
8. implementation details needed for reproducibility.

Define every named module by inputs, outputs, state change, and failure it
prevents. If a method needs a reward, specify the correctness gate before the
performance term. If it uses profiling, state whether counters are observations,
rewards, prompts, or final metrics.

## Evaluation-section logic

Start with research questions, then build a claim-evidence matrix:

- **Can it produce valid kernels?** compile, execution, semantic correctness,
  hacking checks, specification/static/symbolic checks.
- **Are valid kernels faster?** latency, throughput, speedup threshold,
  geomean, tail, distribution, hardware bound.
- **Does the proposed mechanism cause the gain?** ablation, matched variant,
  search trace, training dynamics, counterexample.
- **Does it generalize?** workloads, shapes, precisions, devices, architectures,
  backends.
- **What does it cost?** tokens, candidates, GPU hours, wall time, memory,
  profiler calls.
- **Where does it fail?** error taxonomy, regressions, unsupported variants,
  weaker hardware, strict thresholds.

Report correctness before speed. An invalid kernel has no meaningful speedup.
Separate:

- compile rate;
- execution rate;
- correctness rate;
- `Fast_p` or equivalent correctness-plus-speed rate;
- speed distribution among correct kernels.

For search, hold candidate-evaluation budget constant. For RL, report the
training environment, reward safeguards, data split/decontamination, and both
outcome and training-dynamics diagnostics. For hardware claims, state device,
software stack, precision, shapes, warmup, repeats, aggregation, and baseline.

## Mechanism language

Use three labels:

- **Directly observed**: the table, trace, counter, or output shows it.
- **Supported interpretation**: matched ablations and counterexamples are
  consistent with it.
- **Hypothesis**: plausible but not isolated by the reported experiment.

Do not write “X proves Y” when X is a single case study. Do not call a
correlation or training curve a causal explanation.

## Related work

Use comparison axes that reappear in the method:

- state representation;
- search/control policy;
- feedback and verification;
- knowledge persistence;
- training objective;
- target backend;
- correctness contract;
- evaluation budget and metric.

End each subsection with a boundary sentence explaining what decision your
method changes. Do not claim novelty merely because component names differ.

## Discussion and conclusion

State:

1. the narrow claim actually supported;
2. one or two mechanism findings;
3. observed regressions or negative results;
4. untested hardware/workloads/precision/budgets;
5. the trusted base or external dependency;
6. what evidence would be required to broaden the claim.

Avoid a generic “future work includes more models and hardware.” Name which
current conclusion is threatened by the missing experiment.
