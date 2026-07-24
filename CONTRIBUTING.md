# Contributing

Contributions should improve evidence quality, terminology discipline,
experimental comparability, or reproducibility.

## Skill and reference changes

State:

- the concrete writing failure being addressed;
- the paper type and research scope;
- the primary-source evidence supporting a new domain rule;
- the adjacent concept or term that must not be conflated;
- the test, fixture, or worked example that exercises the change.

Do not add stylistic rules based only on preference or isolated stock phrases.

## Corpus-derived changes

Record canonical paper IDs and source versions. Keep direct observations,
structural observations, supported inferences, and hypotheses separate.

Do not submit downloaded paper HTML, PDFs, or images. Commit identifiers,
source URLs, hashes, extraction metadata, and aggregate statistics instead.

## Code changes

Run:

```bash
python3 -m unittest discover -s tests -v
python3 -m py_compile scripts/*.py tests/*.py
ruff check scripts tests
python3 scripts/validate_evidence_ledger.py \
  assets/example-solar-ledger.json --strict
```

Network-facing tests must have an offline fixture and must not depend on the
current availability of arXiv.

## Pull requests

Keep changes focused and explain the user-visible effect. By contributing, you
agree that your original contribution is licensed under the repository's MIT
license and that you have the right to submit any included material.
