# Narrative logic for LLM kernel papers

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

Use the abstract as the paper's argument checksum before revising the
Introduction. First write one sentence:

> We determine [question] because [existing evidence cannot decide it], using
> [mechanism], and find [scoped answer].

If this sentence cannot be written without a component inventory or a list of
experiments, the research task is not yet compressed enough.

Write six compact moves:

1. task and consequence;
2. precise failure or unanswered question;
3. method and mechanism, not only the system name;
4. evaluation scope: tasks, hardware, baselines, and metric family;
5. two or three scoped results, including one diagnostic finding;
6. limitation, released artifact, or practical implication.

Select only the results needed to establish the answer. Do not turn the
abstract into an experiment log, hardware inventory, or contribution list.
Benchmark abstracts should lead with the unanswered evaluation question and
their empirical findings. Verification papers should state what is guaranteed,
what is only empirically checked, and the trusted base. Performance-analysis
papers should distinguish achieved performance from theoretical or analytical
bounds.

## Introduction moves

### Derive a problem rather than introduce a field

Before choosing paragraphs, write the Introduction's inference chain:

1. **Judgment**: what must a researcher, system, or evaluator determine?
2. **Insufficient evidence**: why can the closest mechanisms or measurements
   not support that judgment?
3. **Technical cause**: what concrete property creates the insufficiency?
4. **Problem**: what precisely will the paper formulate or resolve?
5. **Treatment**: what mechanism-level idea changes the situation?
6. **Answer**: which result resolves the judgment, and under what conditions?
7. **Audit handles**: which contributions make that answer inspectable?

This ordering is a derivation, not a rigid paragraph template. Background earns
space only when it supplies a premise needed by a later step. Prior work earns
space only when it establishes the evidence boundary. Method detail earns space
only when it makes the answer plausible.

Audit the chain before polishing prose:

- Which sentence changes the reader's belief about the problem?
- Where does the text jump from a broad trend to the paper's exact problem?
- Which gap is asserted without evidence from the nearest work?
- Which method component lacks a preceding failure it resolves?
- Which result or conclusion is broader than its recorded scope?

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

### Claim-with-scope system paper

For systems with a trusted base, safety gate, or precision trade-off, pair:

`claim → numerical evidence → evidence type → operative scope`

For example, name an empirical safety test rather than implying formal proof,
identify a gain as self-relative rather than external-baseline superiority, and
place mixed-precision results on the appropriate evidence board. Store excluded
claims in the ledger; do not repeat them as “we do not claim” sentences
throughout the abstract, Introduction, and contributions.

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

Related Work positions the paper; it does not prove that the field is large.
It must answer:

1. which research routes address the paper's problem;
2. how the paper differs from the closest work on concrete axes;
3. why that difference changes a meaningful scientific or engineering
   decision.

### Establish comparison coordinates

Freeze the paper's research question, conditions, method mechanism, main claim,
and evidence boundary before searching. Useful coordinates include:

- research question and decision enabled;
- model, workload, hardware, precision, and budget assumptions;
- state representation and editable/search unit;
- search or control policy;
- feedback, correctness contract, and acceptance authority;
- knowledge persistence or transfer rule;
- training objective;
- evaluation protocol, baseline, and metric;
- reported success, failure, and external-validity boundary.

Use only coordinates that affect the paper's position. A difference in names,
agent count, or component packaging is not a gap unless it changes behavior,
authority, evidence, or applicability.

### Search nearest neighbors first

Start with papers addressing the same question, using the same setting, or
directly competing for the same claim. Then follow their references and later
citations to add foundational work and recent branches. Retain a paper only if
it changes positioning, supplies a baseline, defines a route, or bounds a
claim. Record the exact primary-source location supporting every comparison.

Do not infer a paper's method or boundary from its title, abstract snippet, or
another paper's summary when the primary source is available. Do not use
“first,” “no prior work,” or “few studies” unless the search protocol and
coverage can sustain an absence claim.

### Build the positioning matrix

Use one row per paper:

| Work | Question | Assumptions | Mechanism | Evaluation | Finding | Boundary | Relation | Baseline implication |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |

“Relation” must be concrete: inherits, directly competes, changes the accepted
evidence, changes the target condition, or is not directly comparable because
of a named mismatch. A directly comparable method should be considered for the
experimental baseline. If it is excluded, preserve the reason in the matrix.

### Draft by research route

Group papers sharing a problem, assumption, or mechanism. Within each paragraph:

`shared problem → what the route establishes → conditions of its evidence → what this paper inherits or changes → why the change matters`

Give the nearest work a direct comparison rather than hiding it inside a broad
category. Derive the gap from the matrix: state both the condition under which
prior evidence is valid and the new condition or missing evidence addressed
here. End a subsection only when the reader can identify which decision changes.

Check every citation at sentence level. The cited source must support the
specific mechanism, finding, or boundary next to it.

## Macro-first prose audit

AI-assisted revision often repairs a local concern by appending a disclaimer,
qualifier, parenthesis, or transition. Repeated local repairs can make every
sentence defensible while leaving the section weak, repetitive, and
directionless. Audit from the paper contract downward.

### Resolve concerns at the right level

When a claim seems too strong or easy to misunderstand:

1. identify the exact claim and evidence boundary;
2. decide whether the issue changes the main claim, experimental protocol,
   interpretation, or only wording;
3. repair the claim or section logic;
4. add a limitation sentence only when it changes how reported evidence should
   be interpreted.

Prefer:

> Under [conditions], X affects Y through Z.

over:

> We do not claim A. This does not mean B. Our goal is not C, but rather to
> study X.

Required scientific boundaries remain mandatory. State them once, positively
and near the evidence they govern. Put material coverage or causal limitations
in the results boundary, Discussion, or Limitations. Do not advertise every
hypothetical reviewer attack in the abstract, contributions, or headline result.

### Restore paragraph and section logic

Give each section one job and each paragraph one inference:

`claim → reason or evidence → implication`

Delete or merge a sentence if it only repeats the previous sentence, announces
that a topic is important, previews obvious structure, or defends against an
unstated objection. Reorder the paragraph if a caveat appears before the claim
it scopes. Rebuild the section if consecutive sentences are individually true
but do not form a cumulative argument.

### Remove high-frequency AI residue

Rewrite unless the phrase carries necessary information:

- “It is important/worth noting that”;
- “To the best of our knowledge” without a documented search basis;
- “We do not claim,” “this does not imply,” or “our goal is not”;
- “not only ... but also ...” used as empty emphasis;
- repeated “however,” “moreover,” “in contrast,” or “therefore” where the
  relation is not actually present;
- contribution lists that restate the same claim with different adjectives;
- symmetrical module descriptions that name components without causal roles;
- generic limitations such as “more models and hardware remain future work.”

Do not ban a phrase mechanically. Preserve it when it is the clearest accurate
statement; otherwise replace the rhetorical shell with the underlying claim.

## Discussion and conclusion

State:

1. the narrow claim actually supported;
2. one or two mechanism findings;
3. observed regressions or negative results;
4. untested hardware/workloads/precision/budgets;
5. the trusted base or external dependency;
6. what evidence would be required to broaden the claim.

Select observed or claim-relevant limitations. Do not convert the section into a
catalog of speculative weaknesses.
Avoid a generic “future work includes more models and hardware.” Name which
current conclusion is threatened by the missing experiment.
