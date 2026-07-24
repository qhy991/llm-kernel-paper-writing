---
name: llm-kernel-paper-writing
description: Builds evidence-grounded research-paper logic, terminology ledgers, claim-evidence matrices, evaluation plans, experimental-table contracts, and figure narratives for LLM-driven GPU kernel generation and optimization. Use when drafting, revising, or auditing papers about CUDA/Triton/HIP/Metal/NPU kernels, kernel agents, SFT/RL, benchmarks, verification, performance analysis, experimental results tables, or ablations, especially for “科研写作”, “论文逻辑”, “实验表格”, arXiv HTML evidence, or avoiding invented terminology.
---

# LLM Kernel Paper Writing

Treat every paper claim as a scoped statement backed by primary evidence. This
skill owns domain evidence and terminology; compose it with `tech-paper-template`
or `benchmark-paper-template` for the general skeleton, `intro-drafter` for final
Introduction prose, and `pre-submission-reviewer` for submission review.

## 1. Freeze the paper contract

Copy `assets/paper-contract.json`. Record the research question, research object,
hard constraints, central tension, main claim, venue, and available artifacts.
Choose one primary type: model/post-training, agent/search, compiler/verification,
benchmark/dataset, or performance analysis. Read
`references/paper-type-playbooks.md`; do not draft while the main claim is
unsupported.

## 2. Mine primary evidence

Prefer official arXiv HTML because it preserves section structure, figure
groups, captions, and linked assets. Fall back in order: ar5iv HTML, official
PDF/source, author repository. Record the provider and all failures. Pass a
versioned ID such as `--id 2606.26383v1` when evidence must be pinned.

```bash
python scripts/extract_arxiv_evidence.py \
  --readme path/to/papers.md \
  --output-dir path/to/evidence \
  --download-images
```

The extractor emits candidates, not verified facts. Inspect the source context
before promoting any claim or term. Read `references/corpus-basis.md` for the
evidence boundary behind this skill and inspect `assets/corpus-manifest.json`
for the public snapshot identifiers and coverage. Install `requirements.txt`
in an isolated environment if the imports are unavailable. Use `--id-file` for
a pinned project corpus.

## 3. Build ledgers before prose

Copy `assets/evidence-ledger.json` and fill `claims`, `terms`, `comparisons`,
`figures`, and `limitations`. Preserve source locations, scope, mechanism status,
non-equivalences, hardware, workload, precision, budget, repeats, aggregation,
correctness gates, metrics, figure claims, and observed failures.
Use `references/evidence-ledgers.md` for field semantics and confound checks.

Run `python scripts/validate_evidence_ledger.py ledger.json --strict`. A missing
location, scope, baseline, or boundary blocks drafting.

## 4. Construct the argument

Use this chain unless the paper-type playbook gives a justified variant:

`stakes → concrete bottleneck → prior-work gap → mechanistic insight → method → correctness evidence → performance evidence → diagnostic evidence → boundary`

Each arrow must be explainable. A component without a preceding challenge is
unmotivated; a contribution without a later experiment is unsupported.

For the Introduction, use seven moves: setting, concrete bottleneck, prior-work
boundary, remaining failure, mechanism-level insight, scoped method/result, and
contributions mapped to later evidence.

Read `references/narrative-logic.md` before outlining sections.

## 5. Enforce terminology discipline

Classify every term as canonical concept, proper name, author-defined construct,
metric, or claim language. README tags and title adjectives are retrieval hints,
not definitions. Reject a new term unless it has an operational definition, a
distinction from adjacent concepts, evidence that uses it, and a stated scope.
Use `references/term-ontology.md`.

## 6. Make figures carry the proof

Plan the figure sequence as motivation → mechanism → headline result →
diagnosis/ablation → boundary. Every caption must define conditions, metric,
baseline, uncertainty or repeats, and the conclusion supported. Read
`references/figure-rhetoric.md`; use `scientific-figure-design` for bulk figure
mining, visual-language extraction, or final figure production.

## 7. Make tables preserve the comparison protocol

Derive every experimental table from comparison-ledger rows. Order columns as
scope/protocol → correctness/coverage → performance → cost → boundary. Keep
denominator, baseline mode, budget, selection rule, aggregation, repeats,
uncertainty, and failure policy visible in the table, caption, or an explicit
footnote. Do not rank cells across unmatched hardware, precision, budget,
correctness gate, or baseline. Read `references/table-rhetoric.md` when
planning, writing, or auditing result, ablation, cost, failure, sensitivity, or
cross-hardware tables.

## 8. Draft and audit

Write from the ledgers, not memory. Use exact hardware, workload, precision,
budget, metric, aggregation, and baseline. Mark mechanism statements as direct
evidence, supported inference, or hypothesis. End with limitations that narrow
the claim rather than generic future work.

When auditing an existing manuscript, report findings as:

- **blocker**: a false, unsupported, or invalidly compared headline claim;
- **major**: wording or missing protocol information that changes interpretation;
- **minor**: traceability, visibility, or presentation debt that does not change
  the result.

Treat protocol details in a footnote as visible only when they are unambiguous
and tied to each affected row. If baseline mode, correctness gate, selection
rule, repeats, or evidence grade differs across headline rows, split the table
or expose those fields as columns.

If no ledger exists, build a provisional one from the manuscript and verify it
against the smallest relevant local artifacts before judging support. Mark a
claim unverified when the artifacts are unavailable; do not fill the gap from
memory.

Return: paper contract, logic chain, section outline, claim-evidence matrix,
term ledger, comparison protocol, table plan, figure plan, limitations, then
prose.
See `EXAMPLES.md` for a worked evidence-to-outline example.
