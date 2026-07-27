# LLM Kernel Paper Writing

**Evidence-grounded research writing for LLM-driven GPU kernel systems.**

[中文说明](README.zh-CN.md) · [Skill](SKILL.md) ·
[Worked examples](EXAMPLES.md) · [Corpus basis](references/corpus-basis.md)

LLM Kernel Paper Writing is an open agent skill and a small deterministic
toolchain for turning research artifacts into scoped claims, defensible
terminology, matched experimental comparisons, and a coherent technical-paper
argument.

It is designed for papers about CUDA, Triton, HIP, Metal, and NPU kernels;
kernel-generation agents and search systems; post-training and reinforcement
learning; benchmarks and datasets; compiler or verification systems; and
performance analysis.

The core rule is simple: draft from a claim-evidence ledger, not from model
memory.

## What is included

- A concise agent workflow in [`SKILL.md`](SKILL.md).
- A four-statement argument checksum that aligns the abstract, Introduction,
  Related Work, contributions, and conclusion.
- Nearest-neighbor literature positioning kept separate from experimental
  comparison protocols.
- Paper-type playbooks for model training, agents/search, compilers and
  verification, benchmarks, and performance analysis.
- A paper contract plus a strict claim-evidence ledger schema.
- Terminology discipline for separating canonical concepts, proper names,
  author-defined constructs, metrics, and claim language.
- Figure and experimental-table rhetoric grounded in comparison protocols.
- An arXiv HTML evidence extractor that preserves source locations, captions,
  figure context, hashes, and candidate status.
- A deterministic ledger validator that blocks unsupported or underspecified
  claims before prose drafting.
- A macro-first audit that removes defensive AI-writing residue without hiding
  material scientific limitations.
- A public corpus manifest and worked examples based on primary arXiv sources.

## Workflow

```text
Research artifacts
  -> paper contract
  -> judgment / evidence gap / treatment / finding checksum
  -> primary-source evidence
  -> literature positioning
  -> claim / term / experimental-comparison ledgers
  -> argument chain
  -> table and figure plans
  -> scoped prose
  -> pre-submission audit
```

## Install as an agent skill

Clone the repository directly into a supported skill directory:

```bash
git clone https://github.com/qhy991/llm-kernel-paper-writing.git \
  ~/.agents/skills/llm-kernel-paper-writing
```

Install the optional arXiv extraction dependencies:

```bash
python3 -m pip install -r \
  ~/.agents/skills/llm-kernel-paper-writing/requirements.txt
```

Then ask the agent to use `llm-kernel-paper-writing`.

## Quick start

Copy the templates into a paper project:

```bash
cp assets/paper-contract.json path/to/paper/paper-contract.json
cp assets/evidence-ledger.json path/to/paper/evidence-ledger.json
```

Fill the ledger, then run the strict gate:

```bash
python3 scripts/validate_evidence_ledger.py \
  path/to/paper/evidence-ledger.json --strict
```

The blank template is intentionally invalid. A filled example is provided:

```bash
python3 scripts/validate_evidence_ledger.py \
  assets/example-solar-ledger.json --strict
```

## Mine arXiv HTML evidence

Prefer versioned arXiv HTML when a paper version matters:

```bash
python3 scripts/extract_arxiv_evidence.py \
  --id 2606.26383v1 \
  --output-dir evidence-output/solar \
  --download-images
```

For a list of papers:

```bash
python3 scripts/extract_arxiv_evidence.py \
  --readme path/to/papers.md \
  --output-dir evidence-output/corpus
```

The extractor emits **candidates for human verification**, not authoritative
claims or definitions. Every output records its source location and status.

For reproducible tests or offline review, use a local HTML file:

```bash
python3 scripts/extract_arxiv_evidence.py \
  --id 2606.26383v1 \
  --html-file path/to/source.html \
  --output-dir evidence-output/local
```

## Evidence boundary

The skill was distilled from a 2026-07-24 snapshot of
[Awesome-LLM-Kernel-Agent](https://github.com/qhy991/Awesome-LLM-Kernel-Agent)
and primary arXiv HTML.

- 80 unique arXiv IDs were requested.
- 70 yielded figures through official arXiv HTML.
- ar5iv recovered 5 additional papers.
- The analyzed visual corpus contained 75 usable papers, 645 figure groups, and
  735 assets.

These counts describe a pinned snapshot, not an exhaustive census or a quality
ranking. See [`assets/corpus-manifest.json`](assets/corpus-manifest.json) and
[`references/corpus-basis.md`](references/corpus-basis.md).

The repository does not redistribute downloaded paper HTML or images. Run the
extractor against primary sources when local evidence is needed.

## Development

```bash
python3 -m pip install -r requirements.txt
python3 -m unittest discover -s tests -v
python3 -m py_compile scripts/*.py tests/*.py
ruff check scripts tests
python3 /path/to/skill-creator/scripts/quick_validate.py .
```

## Related project

[Scientific Figure Design](https://github.com/qhy991/Scientific-Figure-Design)
provides the complementary figure-production workflow: claim-first Figure
Contracts, editable Draw.io sources, paper-wide palettes, vector export, and
publication-size validation.

## License

Original work in this repository is released under the [MIT License](LICENSE).
Paper titles, method names, and source references remain the property of their
respective authors and publishers.
