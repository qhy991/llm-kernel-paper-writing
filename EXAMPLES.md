# Worked examples

## Example 1: turn K-Search evidence into a method-paper skeleton

### Raw primary evidence

Paper: K-Search, arXiv `2602.19128`.

- §1: direct program-space evolutionary search may discard a sound
  multi-step optimization intent when an intermediate implementation fails or
  does not immediately improve performance.
- §3 and Figure 1: the method separates a high-level optimization intent from
  local program instantiation; a world model maintains Open/Closed search-tree
  state and applies Insert/Update/Prune.
- §3.4 and Figure 2: a search trace shows an initially unsuccessful split-K
  idea later reintroduced in a stronger context.
- §4 and Figure 3: systems are compared under 120 candidate evaluations and
  three runs on FlashInfer workloads.
- §4.4: small-batch GQA is a negative subgroup because split-K coordination
  overhead can dominate.

### Evidence-grounded central chain

1. **Stakes**: serving kernels such as GQA, MLA, and MoE need deep,
   architecture-specific optimization.
2. **Bottleneck**: evaluation is expensive and structural transformations may
   require non-monotonic intermediate steps.
3. **Gap**: program-space evolution binds a strategy to one sampled
   implementation and may discard the strategy too early.
4. **Insight**: represent optimization intent and implementation attempts as
   different state transitions.
5. **Mechanism**: a world-model-guided search tree prioritizes intents while
   Local Refinement tolerates temporary defects.
6. **Evidence**: fixed-budget repeated comparison plus a process trace and
   generated-kernel analysis.
7. **Boundary**: small-batch GQA can regress; one trace supports mechanism
   plausibility but is not a population-level causal estimate.

### Valid term entries

```json
[
  {
    "term_en": "Search State",
    "term_zh": "搜索状态",
    "class": "author_defined",
    "scope": "K-Search's fixed-budget optimization tree and its reported Open/Closed node semantics",
    "paper_id": "2602.19128",
    "evidence_location": "§3.2–§3.3 and Figure 1",
    "source_wording": "structured search-tree state with Open and Closed nodes",
    "operational_definition": "The explicit tree of completed and pending optimization actions maintained by the world model.",
    "metric_or_test": "Inspect Open/Closed node transitions and Insert/Update/Prune actions in the reported search trace.",
    "synonyms": [],
    "not_equivalent_to": [
      "prompt history",
      "program archive alone"
    ],
    "confidence": "direct"
  },
  {
    "term_en": "co-evolving intrinsic world model",
    "term_zh": "共演化内在世界模型",
    "class": "author_defined",
    "scope": "K-Search's planner and explicit tree updates under execution feedback",
    "paper_id": "2602.19128",
    "evidence_location": "§3.2–§3.3",
    "source_wording": "world model updates priorities and tree structure from execution feedback",
    "operational_definition": "An LLM-based planner whose explicit search-state beliefs are revised using observed candidate outcomes.",
    "metric_or_test": "Compare fixed-budget outcomes and search-state traces against program-space evolution and component removals.",
    "synonyms": [],
    "not_equivalent_to": [
      "any LLM that reasons",
      "a stochastic code generator"
    ],
    "confidence": "direct"
  }
]
```

### Invalid invented terminology

Reject “recursive optimization intelligence amplification.” The paper does not
define this expression, no state or metric operationalizes it, and it adds no
distinction beyond multi-turn search.

### Section outline

1. Introduction: non-monotonic optimization and intent/implementation failure.
2. Related Work: program-space evolution versus explicit planning.
3. Problem: fixed-budget kernel search.
4. Method:
   - Search State;
   - action selection;
   - Local Refinement;
   - world-model update with Insert/Update/Prune;
   - termination and budget.
5. Evaluation:
   - matched setup and correctness gate;
   - best-so-far fixed-budget results;
   - per-workload and threshold analysis;
   - search trace;
   - generated-kernel mechanisms;
   - negative subgroups and cost.
6. Limitations and conclusion.

### Related Work gate

The K-Search source alone is insufficient to draft its positioning against
other methods. Before writing Related Work, retrieve the nearest program-space
evolution and intent-level planning papers from their primary sources, populate
one `positioning` row per paper, and decide which are directly comparable
baselines. Do not turn K-Search's own summaries of other work into verified
comparison claims.

## Example 2: turn KernelBenchX evidence into a benchmark skeleton

Paper: KernelBenchX, arXiv `2605.04956`.

### Research question

Where do LLM-generated Triton kernels fail, why do they fail, and does
iterative refinement improve compilation, correctness, or hardware efficiency?

### Benchmark logic

`aggregate-score blind spot → category-aware task taxonomy + stronger
correctness protocol + efficiency metrics → unified method comparison →
capability-boundary findings`

### Finding format

Avoid:

> Iterative methods work better.

Use:

> Under the unified KernelBenchX pipeline, later GEAK iterations increase
> compile rate but reduce average speedup (§4, Figure 3). This separates syntax
> recovery from performance optimization; the conclusion is limited to the
> evaluated tasks, methods, hardware, and iteration budget.

### Figure sequence

1. Figure 1: benchmark contract—shared specification, generation methods,
   correctness, efficiency, and code-quality evaluation.
2. Category-wise correctness: which structures fail.
3. Iteration trajectory: compile/correctness versus speed.
4. Cross-hardware distribution: portability boundary.
5. Error-transition or case-study evidence: why failures occur.

### Required comparison fields

- 176 tasks and 15 categories;
- five evaluated methods;
- two-stage correctness protocol;
- hardware and precision per experiment;
- compile, semantic correctness, and speed metrics kept separate;
- aggregation and correctness filtering;
- category and hardware subgroup results;
- unsupported quantization cases;
- generation/iteration budget.

The benchmark's strongest contribution is the capability-boundary question and
measurement design, not the adjective “comprehensive.”
