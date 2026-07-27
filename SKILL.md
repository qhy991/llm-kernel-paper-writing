---
name: llm-kernel-paper-writing
description: Builds evidence-grounded paper logic, Introduction problem derivations, Related Work positioning matrices, claim-evidence ledgers, evaluation plans, table/figure narratives, and anti-defensive prose audits for LLM-driven kernel, inference-engine, and agentic-systems research. Use when drafting, revising, or auditing abstracts, Introductions, Related Work, methods, experiments, or full papers about CUDA/Triton/HIP/Metal/NPU kernels, kernel agents, self-evolving engines, SFT/RL, benchmarks, verification, or performance analysis, especially for “科研写作”, “论文逻辑”, literature positioning, removing AI-style caveats/templates, arXiv HTML evidence, or avoiding invented terminology.
---

# LLM Kernel Paper Writing

Treat every paper claim as a scoped statement backed by primary evidence. This
skill owns domain evidence and terminology; compose it with `tech-paper-template`
or `benchmark-paper-template` for the general skeleton. Use `intro-drafter` only
after the research task and argument chain are stable, and use
`pre-submission-reviewer` for the final submission audit.

## 1. Freeze the paper contract and argument checksum

Copy `assets/paper-contract.json`. Record the research question, research object,
hard constraints, central tension, main claim, venue, and available artifacts.
Choose one primary type: model/post-training, agent/search, compiler/verification,
benchmark/dataset, or performance analysis. Read
`references/paper-type-playbooks.md`; do not draft while the main claim is
unsupported.

Before writing the Introduction, compress the paper into four statements:

1. the judgment or decision the paper must enable;
2. why existing evidence or mechanisms cannot make that judgment;
3. the paper's mechanism-level treatment;
4. the strongest supported finding and its scope.

Use this checksum to control the abstract, Introduction, Related Work,
contributions, and conclusion. If these sections imply different papers, repair
the contract before editing sentences.

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
evidence boundary behind this skill. Install `requirements.txt` in an isolated
environment if the imports are unavailable. Use `--id-file` for a pinned corpus
manifest.

## 3. Build ledgers before prose

Copy `assets/evidence-ledger.json` and fill `claims`, `terms`, `comparisons`,
`positioning`, `figures`, and `limitations`. `positioning` is the literature
matrix; `comparisons` is the experimental protocol matrix. Do not merge them.
Preserve source locations, scope, mechanism status, non-equivalences, hardware,
workload, precision, budget, repeats, aggregation, correctness gates, metrics,
figure claims, and observed failures.
Use `references/evidence-ledgers.md` for field semantics and confound checks.

Run `python scripts/validate_evidence_ledger.py ledger.json --strict`. A missing
location, scope, baseline, or boundary blocks drafting.

## 4. Derive the argument before drafting

Use this chain unless the paper-type playbook gives a justified variant:

`stakes → concrete bottleneck → prior-work gap → mechanistic insight → method → correctness evidence → performance evidence → diagnostic evidence → boundary`

Each arrow must be explainable. A component without a preceding challenge is
unmotivated; a contribution without a later experiment is unsupported.

The Introduction is a derivation, not a field tour. Establish what must be
decided, show why current evidence cannot decide it, identify the technical
cause, define the paper's problem and treatment, preview the decisive findings,
then state contributions mapped to later evidence. Audit for logical jumps,
background that changes no belief, unsupported claims, and conclusions broader
than the evidence.

Read `references/narrative-logic.md` before outlining sections.

## 5. Position Related Work

Start from nearest neighbors: papers addressing the same question, setting, or
directly competing mechanism. Expand through their references and later
citations only as needed to cover foundational and recent routes. Fill one
`positioning` row per retained paper, including question, assumptions, mechanism,
evaluation, finding, boundary, relation to this paper, exact citation location,
and baseline implication.

Group prose by research route, not chronology. Each paragraph states what the
route solves, where its evidence applies, and which decision this paper changes.
Compare the closest work directly. Derive the gap from conditional differences;
do not use “few studies,” “no one,” or “first” without a search record that can
support the claim. If a method is directly comparable, consider it as a
baseline; otherwise record the condition that prevents a fair comparison.

## 6. Enforce terminology discipline

Classify every term as canonical concept, proper name, author-defined construct,
metric, or claim language. README tags and title adjectives are retrieval hints,
not definitions. Reject a new term unless it has an operational definition, a
distinction from adjacent concepts, evidence that uses it, and a stated scope.
Use `references/term-ontology.md`.

## 7. Make figures carry the proof

Plan the figure sequence as motivation → mechanism → headline result →
diagnosis/ablation → boundary. Every caption must define conditions, metric,
baseline, uncertainty or repeats, and the conclusion supported. Read
`references/figure-rhetoric.md`; use `scientific-figure-design` for bulk figure
mining, visual-language extraction, or final figure production.

## 8. Make tables preserve the comparison protocol

Derive every experimental table from comparison-ledger rows. Order columns as
scope/protocol → correctness/coverage → performance → cost → boundary. Keep
denominator, baseline mode, budget, selection rule, aggregation, repeats,
uncertainty, and failure policy visible in the table, caption, or an explicit
footnote. Do not rank cells across unmatched hardware, precision, budget,
correctness gate, or baseline. Read `references/table-rhetoric.md` when
planning, writing, or auditing result, ablation, cost, failure, sensitivity, or
cross-hardware tables.

## 9. Draft macro-to-micro and remove defensive prose

Write from the ledgers, not memory. Use exact hardware, workload, precision,
budget, metric, aggregation, and baseline. Mark mechanism statements as direct
evidence, supported inference, or hypothesis.

Before line editing, write the job of each section and the
claim → reason/evidence → implication chain of each paragraph. Resolve a
reviewer concern at the claim, evidence, or section level before adding a
sentence. Prefer a positive scoped statement over “we do not claim,” “this does
not mean,” or “our goal is not”; place a material limitation once where it
changes interpretation, usually in the protocol, results boundary, or
limitations. Do not turn the abstract, Introduction, or contributions into a
review response.

Delete stock transitions, duplicated summaries, unsupported superlatives,
symmetrical component lists without causal roles, and sentences that only
announce structure or pre-empt hypothetical criticism. Keep required caveats,
but integrate them into the claim's scope. Read the macro-first prose audit in
`references/narrative-logic.md`.

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

Return: paper contract, four-statement checksum, logic chain, section outline,
literature-positioning matrix, claim-evidence matrix, term ledger, experimental
comparison protocol, table plan, figure plan, limitations, style-audit findings,
then prose.
See `EXAMPLES.md` for a worked evidence-to-outline example.
