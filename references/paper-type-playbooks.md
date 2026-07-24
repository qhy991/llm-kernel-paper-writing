# Paper-type playbooks

Select one primary playbook. A paper may use a secondary playbook, but it still
needs one center of gravity.

## Contents

- [Model or post-training paper](#1-model-or-post-training-paper)
- [Agent or search-system paper](#2-agent-or-search-system-paper)
- [Compiler, specification, or verification paper](#3-compiler-specification-or-verification-paper)
- [Benchmark or dataset paper](#4-benchmark-or-dataset-paper)
- [Performance-analysis or measurement paper](#5-performance-analysis-or-measurement-paper)
- [Cross-playbook experiment table](#cross-playbook-experiment-table)

## 1. Model or post-training paper

### Central question

Which data, objective, interaction structure, or optimization method changes
the model's ability to produce correct and performant kernels?

### Logic

`capability gap → data/environment failure → training insight → objective and
rollout design → stable learning → kernel outcome`

### Method must specify

- base model and initialization;
- data provenance, scale, filtering, and decontamination;
- task representation and target language;
- SFT/RL stages and why each is needed;
- reward equation, correctness gate, and anti-hacking checks;
- rollout turns, context, tools, termination, and sampling;
- actor/critic initialization when applicable;
- compute, hardware, and optimizer configuration.

### Evidence matrix

- base versus SFT versus SFT+RL;
- correctness, `Fast_p`, and speed distributions;
- training reward plus entropy, gradient norm, value fit, clip/ratio statistics;
- reward-hacking or invalid-output rate;
- data/objective/feedback ablations;
- test-time scaling with last-turn and best-history separated;
- matched-size and frontier-model baselines;
- contamination checks.

### Common overclaims

- training reward equals kernel performance;
- compile rate equals correctness;
- best-of-N equals single-sample ability;
- one strict-threshold win establishes broad optimization skill;
- “large-scale” without samples, rollouts, tokens, GPUs, or time.

## 2. Agent or search-system paper

### Central question

Which representation of state, action, memory, feedback, or search control lets
the system find better kernels under a fixed budget?

### Logic

`search failure → representation/control insight → agent loop → fixed-budget
search → trace/ablation → workload-dependent boundary`

### Method must specify

- state visible to each agent;
- action space and tools;
- planner, selector, generator, verifier, profiler, memory, and their interfaces;
- what persists across turns/tasks;
- feedback signals and update rules;
- candidate archive/frontier semantics;
- stopping rule, stagnation rule, and total budget;
- failure isolation and safe execution.

### Evidence matrix

- fixed number of candidate evaluations or equal wall-clock budget;
- same generator model and initial program across baselines;
- best-so-far curves with repeated runs;
- per-workload results, not only aggregate means;
- action/search trace showing how the mechanism changes decisions;
- component ablations;
- cost: tokens, compiles, profiler calls, time;
- regressions caused by synchronization, small shapes, or overhead.

### Common overclaims

- a better generator is presented as a better search policy;
- one trace is treated as population-level causality;
- maximum speedup hides low average or success rate;
- human/expert baseline conditions differ from agent conditions;
- “world model” or “memory” has no state/update definition.

## 3. Compiler, specification, or verification paper

### Central question

Which semantics, IR, invariant, or analysis makes generated kernels safe enough
to transform, execute, or retarget?

### Logic

`unsafe/unportable edit surface → formalizable restriction → IR/invariants →
validator or analysis → coverage/soundness evidence → trusted base and blind
spots`

### Method must specify

- source and target semantics;
- trusted computing base;
- IR types, operations, and invariants;
- soundness claim: proof, empirical check, or heuristic;
- unsupported constructs and rejection behavior;
- static/dynamic/symbolic checks;
- lowering, code generation, and runtime boundary;
- false-accept and false-reject implications.

### Evidence matrix

- positive corpus plus adversarial/negative cases;
- independent oracle or mechanized proof;
- false accepts, false rejects, and coverage;
- unsupported-variant tests that should fail loudly;
- correctness across devices/architectures;
- analysis or validation cost;
- performance after passing the correctness gate;
- equal-precision comparisons and numerical-quality tests.

### Common overclaims

- “correctness-by-construction” is called formal verification without proof;
- output testing is called semantic equivalence;
- zero observed failures becomes universal soundness;
- mixed-precision speedup is compared only to a higher-precision baseline;
- trusted handwritten components disappear from the claim.

## 4. Benchmark or dataset paper

### Central question

Which capability boundary or production mismatch is invisible to existing
evaluation, and how can it be measured reproducibly?

### Logic

`evaluation blind spot → design requirements → construction pipeline →
correctness oracle and metrics → systematic comparison → actionable findings`

### Construction must specify

- task provenance and licensing;
- workload/operator/category taxonomy;
- inputs, shapes, precision, and backend coverage;
- generation/annotation/validation pipeline;
- split and contamination strategy;
- correctness oracle and chance-pass protection;
- captured versus synthetic inputs;
- release artifacts and reproducibility.

### Evidence matrix

- benchmark comparison table;
- composition/statistical profile;
- baseline diversity;
- inter-method and inter-category results;
- cross-hardware and cross-precision analysis;
- error taxonomy;
- sensitivity to metric thresholds;
- iterative refinement trajectories;
- framework/production alignment;
- cost and reliability of the harness.

### Finding contract

Each finding states:

`population + condition + metric + effect + implication + boundary`

Example form:

> Across [categories] under [protocol], task structure explains [effect] more
> than method identity according to [analysis]. This indicates [implication],
> but the conclusion is limited to [scope].

### Common overclaims

- a new task collection is called a benchmark without a new evaluation axis;
- aggregate score hides correctness, speed, and failure composition;
- random tensors stand in for production inputs without validation;
- a benchmark-trained companion method contaminates the test set;
- benchmark difficulty is inferred from low model scores alone.

## 5. Performance-analysis or measurement paper

### Central question

How far is an implementation from a defensible hardware or analytical limit,
what causes the gap, and which decision does the analysis enable?

### Logic

`optimization decision needs a bound → existing measurement/estimation gap →
validated analytical representation → multi-fidelity bound → diagnosis and use
cases → model assumptions`

### Method must specify

- measured quantity versus theoretical/analytical quantity;
- program representation and translation;
- validation of any generative step;
- operation counts and memory-traffic model;
- fusion, cache, hierarchy, or communication assumptions;
- hardware specifications and calibration;
- bound direction and invalid region;
- precision and workload shape.

### Evidence matrix

- bound violations or consistency checks;
- coverage of operators and source languages;
- comparison with FLOP counters, profilers, roofline, or manual analysis;
- tighter-bound ablations: unfused/fused/cache-aware;
- optimization-headroom examples;
- cross-hardware projection;
- sensitivity to model parameters;
- inverse design or provisioning case;
- known sources of looseness.

### Common overclaims

- achieved throughput is called a bound;
- a profiler is said to predict theoretical performance;
- an optimistic roofline is treated as achievable SOL;
- model assumptions are hidden;
- projected hardware results are written as measured results.

## Cross-playbook experiment table

Before writing results, complete one row per headline claim:

| Claim | Correctness gate | Workload | Hardware | Precision | Baseline | Budget | Repeats | Metric | Aggregation | Diagnostic | Boundary |
|---|---|---|---|---|---|---|---|---|---|---|---|

Any blank cell must be justified or treated as a limitation.
