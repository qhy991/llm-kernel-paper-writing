# Terminology ontology and anti-invention rules

## Contents

- [Classify before defining](#classify-before-defining)
- [Platform and programming terms](#platform-and-programming-terms)
- [Workloads and kernel structure](#workloads-and-kernel-structure)
- [GPU execution and performance](#gpu-execution-and-performance)
- [Compilation, specification, and verification](#compilation-specification-and-verification)
- [Model training and RL](#model-training-and-rl)
- [Agent and search terms](#agent-and-search-terms)
- [Evaluation terms and metrics](#evaluation-terms-and-metrics)
- [Claim-language gate](#claim-language-gate)

## Classify before defining

Every extracted expression belongs to one of:

| Class | Meaning | Example | Writing rule |
|---|---|---|---|
| canonical concept | established technical concept | arithmetic intensity, SFT | define from a primary or standard source |
| proper name | named artifact, model, benchmark, or system | KernelBench, SOLAR | preserve capitalization; do not generalize it |
| author-defined construct | paper-specific operational concept | lazy optimization, Search State | quote/paraphrase the paper's definition and scope |
| metric | measurement with formula/protocol | `Fast_p`, SOL score | include denominator, threshold, population, aggregation |
| claim language | strength/scope adjective | robust, large-scale, SOTA | replace with measurable evidence or delete |

A title, README tag, or acronym expansion is not automatically a definition.

## Platform and programming terms

- **CUDA**: NVIDIA's parallel-computing platform and programming model. Distinguish
  CUDA C++ source, PTX, SASS, CUDA libraries, and CUDA runtime behavior.
- **Triton**: a Python-embedded DSL and compiler stack for GPU kernels. Do not
  call Triton “high-level CUDA”; the programming and compilation models differ.
- **HIP**: AMD's C++ runtime/programming interface for portable GPU code.
- **Metal**: Apple's graphics and compute API; Metal Shading Language kernels
  target Apple GPUs.
- **NPU**: generic neural-processing-unit class, not one ISA. State the concrete
  device, toolchain, and ISA.
- **MUSA**: Moore Threads' GPU programming stack. MusaCoder (`2606.04847`) uses
  it as a native target, not as a synonym for CUDA.
- **CANN/Ascend C/Ascend DSL**: Huawei Ascend software/toolchain terms. Keep
  compiler, DSL, runtime, and hardware distinct.
- **CUTLASS**: NVIDIA's templated CUDA primitives for dense linear algebra.
- **PTX**: NVIDIA virtual ISA. It is not final machine code.
- **ISA**: the architecturally visible instruction contract. KernelCraft
  (`2603.08721`) varies ISA documentation density; documentation is not the ISA.

## Workloads and kernel structure

- **GEMM**: general matrix-matrix multiplication. Include dimensions, layouts,
  transpose flags, dtype, batch, and epilogue.
- **HGEMM**: half-precision GEMM; specify the actual input/accumulation/output
  precisions.
- **elementwise / pointwise operator**: each output element depends on a small
  corresponding input set. This does not imply memory coalescing.
- **reduction**: combines a dimension using an associative or ordered operator;
  numerical behavior may depend on reduction order.
- **kernel fusion**: combines operations to remove launch and/or intermediate
  memory traffic. State which boundaries disappear.
- **persistent kernel**: keeps work resident across multiple logical operations
  or steps. It is not synonymous with megakernel.
- **megakernel**: a single kernel coordinating a large computation graph or
  model region. AutoMegaKernel (`2606.09682`) restricts it through a typed
  schedule IR and static validation.
- **attention / GQA / MLA / MoE**: distinct workloads. State the exact variant,
  direction, sequence length, head configuration, routing, and sparsity.
- **paged KV cache**: a non-contiguous cache organization for serving. It
  changes indexing and memory behavior; do not reduce it to generic attention.

## GPU execution and performance

- **latency**: elapsed time for a specified operation and measurement boundary.
  Separate kernel-only from end-to-end latency.
- **throughput**: completed work per unit time. State the work unit.
- **speedup**: `baseline_time / method_time` unless explicitly defined
  otherwise. Name the baseline and report regressions below 1×.
- **arithmetic intensity**: operations per byte moved at a specified memory
  level. FLOP/byte at HBM is not interchangeable with L2 or register intensity.
- **memory-bound / compute-bound**: regime relative to a stated performance
  model and hierarchy level; not a permanent property of an operator name.
- **roofline model**: upper performance envelope from peak compute and memory
  bandwidth versus arithmetic intensity.
- **Speed-of-Light (SOL) bound**: a workload/hardware-specific theoretical or
  analytical minimum time or maximum performance. SOLAR (`2606.26383`) separates
  unfused, fused, and cache-aware bounds.
- **headroom**: gap between achieved performance and a stated bound. Define the
  ratio and direction.
- **occupancy**: active warps/blocks relative to hardware capacity. Higher
  occupancy is not automatically faster.
- **coalesced memory access**: warp accesses combine into efficient memory
  transactions. Define alignment and layout.
- **tiling**: partitions computation/data into blocks matched to locality and
  parallelism. Include tile shape and memory level.
- **HBM / L2 / shared memory / registers**: different hierarchy levels with
  different capacity, bandwidth, visibility, and lifetime.
- **Tensor Cores / WMMA**: matrix-multiply hardware and programming interfaces.
  State supported dtype, shape, and accumulation.
- **warp shuffle**: intra-warp register exchange. It is not shared memory.
- **double buffering**: overlaps transfer of the next tile with computation on
  the current tile; show that overlap actually occurs.

## Compilation, specification, and verification

- **intermediate representation (IR)**: structured program form between source
  and target. Name its semantics and invariants.
- **Affine Loop IR**: SOLAR's executable representation with affine loops and
  named dimensions, used as a validated bridge before deterministic lifting
  (`2606.26383`, Figure 2).
- **Einsum graph**: operation graph expressed through tensor contractions;
  SOLAR uses it for deterministic analysis, not as generic agent memory.
- **static verification/checking**: establishes properties without running the
  candidate. State the checked properties and assumptions.
- **dynamic testing**: executes candidates on selected inputs. Passing tests is
  evidence, not universal semantic equivalence.
- **equivalence checking**: checks semantic equivalence under a defined model;
  distinguish proof, solver-based checking, and sampled comparison.
- **symbolic execution**: executes with symbolic values/path constraints.
  Model2Kernel (`2603.24595`) uses a model-aware variant for CUDA safety.
- **specification language**: expresses required behavior or constraints. A
  task prompt alone is not necessarily a formal specification.
- **correctness-by-construction**: only acceptable when the construction space
  and invariants exclude named failures. AutoMegaKernel explicitly distinguishes
  empirical validator evidence from a mechanized proof.
- **soundness / completeness**: formal properties relative to a semantics.
  Do not infer them from zero observed failures.
- **trusted computing base**: components and assumptions outside the checked
  claim. Always state it for safety or verification work.

## Model training and RL

- **supervised fine-tuning (SFT)**: gradient training on input-output examples.
  “Fine-tuning” may include other objectives; do not silently equate them.
- **reinforcement learning (RL)**: policy optimization from reward-bearing
  interaction or sampled outcomes. Name the algorithm and environment.
- **GRPO**: group-relative policy optimization. State grouping and advantage
  construction; the acronym alone does not define a training protocol.
- **REINFORCE / leave-one-out advantage**: policy-gradient estimators.
  daVinci-kernel and Dr. Kernel use paper-specific multi-agent/turn-level forms.
- **TRLOO**: Dr. Kernel's Turn-level REINFORCE Leave-One-Out estimator for
  multi-turn RL (`2602.05885`); do not use it as a generic synonym for RL.
- **Rejection Fine-Tuning (RFT)**: CUDA Agent retains selected positive,
  well-formed trajectories to initialize the actor (`2602.24286`).
- **value pretraining**: initializes a critic/value function before agentic RL;
  CUDA Agent diagnoses its removal with explained variance and trajectory
  length (`2602.24286`, Figure 5).
- **reward hacking**: obtains reward through evaluator loopholes or invalid
  behavior rather than the intended objective. Name the exploit and safeguard.
- **lazy optimization**: correct/trivial outputs that gain little meaningful
  speed; Dr. Kernel operationalizes it through stricter speed thresholds and
  profiling feedback (`2602.05885`).
- **profiling-based reward/rejection sampling**: uses profiling-derived evidence
  in reward or sample selection. State which signal and whether it is causal.
- **Mismatch Rejection Sampling (MRS)**: Dr. Kernel's filtering of samples
  affected by rollout/train-engine likelihood mismatch. Report the importance
  ratio or rejection criterion; do not treat it as a generic correction method.
- **test-time scaling**: spends more inference/search budget. Separate
  last-turn, best-history, pass@k, and candidate count.
- **AST-level decontamination**: checks structural program overlap rather than
  only string identity. State threshold and corpus.

## Agent and search terms

- **iterative refinement**: generate, execute/inspect, revise. State retained
  state, feedback, rounds, and stopping rule.
- **evolutionary search**: selection and variation over a population/archive.
  Name the selection and mutation operators.
- **quality-diversity / MAP-Elites**: maintains diverse elites across behavior
  descriptors. It is not a generic name for any multi-candidate search.
- **multi-agent system**: roles with distinct state, policy, tools, or objective.
  Multiple prompts alone do not establish meaningful agency.
- **skill library**: reusable instructions/strategies with retrieval and update
  semantics. State how a skill is verified, deduplicated, selected, and retired.
- **frontier-aware skill evolution**: daVinci-kernel's construct for re-evaluating
  skill usefulness as policy competence changes (`2606.16497`).
- **world model**: a model of transitions/outcomes used for prediction or
  planning. K-Search's intrinsic world model maintains a structured search
  state and priorities (`2602.19128`); generic LLM reasoning is not enough.
- **Search State / Closed / Open / frontier**: K-Search's explicit tree state,
  visited actions, and pending optimization hypotheses.
- **Local Refinement**: repeated implementation attempts for one high-level
  intent until stagnation; this protects an intent from one faulty sample.
- **Insert / Update / Prune**: K-Search tree edits with defined state effects.
- **memory**: specify content, lifetime, write policy, retrieval, and consumer.
- **RAG**: retrieval-augmented generation. Retrieval without grounding or
  provenance should not be called evidence.

## Evaluation terms and metrics

- **compile rate**: fraction that compile; says nothing about execution safety or
  correctness.
- **execution rate**: fraction that run under the harness; says nothing about
  semantic correctness.
- **pass rate**: fraction passing a defined oracle and input set.
- **`Fast_p`**: fraction of tasks producing a correct kernel with speedup above
  threshold `p`; record whether it is single-sample, `@k`, last-turn, or best.
- **pass@k / best-of-k**: probability or observed fraction with at least one
  success among `k`; not directly comparable to pass@1.
- **geometric mean**: appropriate for multiplicative ratios; report exclusions,
  zeros, and correctness filtering.
- **fixed evaluation budget**: equal number of candidate executions or other
  costly decisions; not automatically equal wall-clock or token cost.
- **correctness harness**: tests, isolation, timeouts, and anti-cheating logic.
  Name inputs and stochasticity.
- **hardware portability**: results across devices under comparable semantics;
  one source compiling on two devices is only partial evidence.

## Claim-language gate

The following expressions are not technical terms unless operationalized:

- framework, system, automated, autonomous, agentic;
- comprehensive, robust, general, production, end-to-end;
- large-scale, full-stack, hardware-aware, self-improving;
- state-of-the-art, optimal, efficient, high-performance;
- co-evolving, adaptive, frontier-aware.

Convert each into a test:

- **large-scale** → tasks, trajectories, tokens, GPUs, time;
- **robust** → perturbations, failure taxonomy, confidence, cross-setting rate;
- **hardware-aware** → counters, constraints, cost model, device-specific rule;
- **end-to-end** → input, output, excluded stages, human intervention;
- **production** → captured inputs, framework contract, deployment baseline;
- **SOTA** → benchmark version, hardware, precision, budget, date, and baseline;
- **co-evolving** → which states update each other, update rule, and ablation.

If the test is absent, remove or weaken the expression.
