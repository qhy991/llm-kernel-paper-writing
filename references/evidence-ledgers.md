# Evidence ledgers

The ledgers are the interface between reading and writing. Populate them before
drafting paragraphs.

## Contents

- [Paper contract](#paper-contract)
- [Claim ledger](#claim-ledger)
- [Term ledger](#term-ledger)
- [Comparison ledger](#comparison-ledger)
- [Figure ledger](#figure-ledger)
- [Limitation ledger](#limitation-ledger)
- [Evidence promotion gate](#evidence-promotion-gate)

## Paper contract

Required fields:

- `paper_type`: one primary playbook, using `model-or-post-training`,
  `agent-or-search`, `compiler-or-verification`, `benchmark-or-dataset`, or
  `performance-analysis`;
- `research_question`: answerable by the planned evidence;
- `research_object`: kernel, model, agent, compiler, benchmark, or analysis;
- `hard_constraints`: semantics, hardware, precision, budget, deployment;
- `central_tension`: one observable contradiction or failure;
- `mechanistic_insight`: one sentence, not a component list;
- `main_claim`: one falsifiable scoped statement;
- `intended_venue`: venue or audience whose evidence standard is being targeted;
- `artifacts`: code, definitions, logs, results, profiles, traces, figures;
- `claim_exclusions`: what the paper will not claim.

## Claim ledger

Every claim contains:

```json
{
  "id": "C1",
  "claim_type": "artifact|outcome|mechanism|generalization|boundary",
  "text": "One falsifiable statement.",
  "scope": {
    "workloads": [],
    "hardware": [],
    "precision": [],
    "software": [],
    "budget": "",
    "selection_rule": ""
  },
  "evidence": [
    {
      "location": "paper-id §4.2 Table 1",
      "kind": "table",
      "observation": "",
      "provenance": "primary"
    }
  ],
  "mechanism_status": "direct|supported-inference|hypothesis",
  "counterevidence": [],
  "boundary": ""
}
```

Rules:

- `claim_type` controls the evidence gate: outcome, mechanism, and
  generalization claims must be linked from a comparison row.
- A result claim needs direct evidence and a boundary.
- A mechanism claim needs an ablation, matched comparison, trace, profile, or
  formal argument.
- A case study can establish existence or plausibility, not population effect.
- A maximum cannot stand in for central tendency.
- Relative change includes absolute values.

## Term ledger

```json
{
  "term_en": "",
  "term_zh": "",
  "class": "canonical_concept|proper_name|author_defined|metric|claim_language",
  "scope": "",
  "paper_id": "",
  "evidence_location": "",
  "source_wording": "",
  "operational_definition": "",
  "metric_or_test": "",
  "synonyms": [],
  "not_equivalent_to": [],
  "confidence": "direct|supported|candidate"
}
```

Rules:

- `candidate` terms never enter final prose as established terminology.
- `scope` states the paper, system, task, or measurement regime in which the
  definition is valid.
- Proper names preserve spelling and are not pluralized into a method class.
- Author-defined terms use the paper's scope.
- Claim language must be replaced by its operational test.
- A term without `not_equivalent_to` is likely too vague.

## Comparison ledger

```json
{
  "id": "E1",
  "claim_ids": ["C1"],
  "workload": "",
  "input_shapes": "",
  "hardware": "",
  "software_stack": "",
  "precision": "",
  "baseline": "",
  "baseline_mode": "",
  "correctness_gate": "",
  "budget": "",
  "warmup": "",
  "repeats": "",
  "aggregation": "",
  "metric": "",
  "uncertainty": "",
  "exclusions": ""
}
```

`baseline_mode` should state eager, compile, vendor library, expert kernel,
previous agent, analytical bound, or self-relative default. These denominators
are not interchangeable.

## Figure ledger

```json
{
  "id": "F1",
  "claim_id": "C1",
  "role": "motivation|mechanism|result|diagnosis|boundary",
  "five_second_takeaway": "",
  "evidence_source": "",
  "comparison_objects": [],
  "visual_anchor": "1x|diagonal|bound|threshold|baseline",
  "conditions": "",
  "uncertainty": "",
  "caption_conclusion": ""
}
```

One figure gets one primary claim. A method figure must show state or artifact
changes, not only named boxes.

## Limitation ledger

Classify each limitation:

- **observed regression**: a tested subgroup loses;
- **coverage gap**: unsupported operator, shape, architecture, precision;
- **measurement threat**: timing noise, harness mismatch, profiler distortion;
- **comparison threat**: unequal model, budget, hardware, or baseline;
- **causal uncertainty**: mechanism inferred but not isolated;
- **trusted-base assumption**: unchecked handwritten or vendor component;
- **external-validity gap**: benchmark does not model production conditions.

Each limitation states which claim it narrows and what evidence would remove it.

## Evidence promotion gate

Promote a candidate into final prose only if:

1. the source is primary or explicitly labeled secondary;
2. the exact location is recorded;
3. scope and denominator are present;
4. evidence level is named;
5. conflicting evidence was checked;
6. the statement has a boundary.

The validator checks structure. Human source inspection is still required.
