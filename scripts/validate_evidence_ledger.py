#!/usr/bin/env python3
"""Validate an LLM-kernel paper evidence ledger before drafting."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

PAPER_TYPES = {
    "model-or-post-training",
    "agent-or-search",
    "compiler-or-verification",
    "benchmark-or-dataset",
    "performance-analysis",
}
CLAIM_TYPES = {"artifact", "outcome", "mechanism", "generalization", "boundary"}
COMPARISON_REQUIRED_CLAIM_TYPES = {"outcome", "mechanism", "generalization"}
MECHANISM_STATUSES = {"direct", "supported-inference", "hypothesis"}
TERM_CLASSES = {
    "canonical_concept",
    "proper_name",
    "author_defined",
    "metric",
    "claim_language",
}
TERM_CONFIDENCE = {"direct", "supported", "candidate"}
POSITIONING_PROXIMITIES = {
    "nearest-neighbor",
    "foundational",
    "recent-route",
    "baseline-only",
}
FIGURE_ROLES = {"motivation", "mechanism", "result", "diagnosis", "boundary"}
LIMITATION_CLASSES = {
    "observed_regression",
    "coverage_gap",
    "measurement_threat",
    "comparison_threat",
    "causal_uncertainty",
    "trusted_base_assumption",
    "external_validity_gap",
}


def present(value: Any) -> bool:
    if isinstance(value, str):
        return bool(value.strip())
    if isinstance(value, (list, dict)):
        return bool(value)
    return value is not None


class Validator:
    def __init__(self) -> None:
        self.errors: list[str] = []
        self.warnings: list[str] = []

    def require(self, condition: bool, path: str, message: str) -> None:
        if not condition:
            self.errors.append(f"{path}: {message}")

    def warn(self, condition: bool, path: str, message: str) -> None:
        if not condition:
            self.warnings.append(f"{path}: {message}")

    def required_keys(self, value: Any, path: str, keys: list[str]) -> None:
        self.require(isinstance(value, dict), path, "must be an object")
        if not isinstance(value, dict):
            return
        for key in keys:
            self.require(key in value, f"{path}.{key}", "missing required key")


def validate_contract(v: Validator, contract: Any) -> None:
    keys = [
        "paper_type",
        "research_question",
        "research_object",
        "hard_constraints",
        "central_tension",
        "mechanistic_insight",
        "main_claim",
        "argument_checksum",
        "intended_venue",
        "artifacts",
        "claim_exclusions",
    ]
    v.required_keys(contract, "paper_contract", keys)
    if not isinstance(contract, dict):
        return
    for key in keys:
        v.require(present(contract.get(key)), f"paper_contract.{key}", "must be filled")
    v.require(
        contract.get("paper_type") in PAPER_TYPES,
        "paper_contract.paper_type",
        f"must be one of {sorted(PAPER_TYPES)}",
    )
    checksum = contract.get("argument_checksum")
    checksum_keys = ["judgment", "evidence_gap", "treatment", "headline_finding"]
    v.required_keys(checksum, "paper_contract.argument_checksum", checksum_keys)
    if isinstance(checksum, dict):
        for key in checksum_keys:
            v.require(
                present(checksum.get(key)),
                f"paper_contract.argument_checksum.{key}",
                "must be filled before drafting the Introduction",
            )


def validate_claims(v: Validator, claims: Any) -> dict[str, str]:
    v.require(isinstance(claims, list) and bool(claims), "claims", "must be non-empty")
    claim_types: dict[str, str] = {}
    if not isinstance(claims, list):
        return claim_types
    for index, claim in enumerate(claims):
        path = f"claims[{index}]"
        keys = [
            "id",
            "claim_type",
            "text",
            "scope",
            "evidence",
            "mechanism_status",
            "counterevidence",
            "boundary",
        ]
        v.required_keys(claim, path, keys)
        if not isinstance(claim, dict):
            continue
        claim_id = claim.get("id")
        v.require(present(claim_id), f"{path}.id", "must be filled")
        v.require(claim_id not in claim_types, f"{path}.id", "must be unique")
        if present(claim_id):
            claim_types[str(claim_id)] = str(claim.get("claim_type") or "")
        v.require(
            claim.get("claim_type") in CLAIM_TYPES,
            f"{path}.claim_type",
            f"must be one of {sorted(CLAIM_TYPES)}",
        )
        v.require(present(claim.get("text")), f"{path}.text", "must be falsifiable")
        scope = claim.get("scope")
        scope_keys = [
            "workloads",
            "hardware",
            "precision",
            "software",
            "budget",
            "selection_rule",
        ]
        v.required_keys(scope, f"{path}.scope", scope_keys)
        if isinstance(scope, dict):
            for key in scope_keys:
                v.require(
                    present(scope.get(key)),
                    f"{path}.scope.{key}",
                    "must be filled; use 'not applicable' with a reason if needed",
                )
        evidence = claim.get("evidence")
        v.require(
            isinstance(evidence, list) and bool(evidence),
            f"{path}.evidence",
            "must contain direct evidence",
        )
        if isinstance(evidence, list):
            for e_index, item in enumerate(evidence):
                e_path = f"{path}.evidence[{e_index}]"
                v.required_keys(
                    item, e_path, ["location", "kind", "observation", "provenance"]
                )
                if isinstance(item, dict):
                    for key in ("location", "kind", "observation", "provenance"):
                        v.require(
                            present(item.get(key)), f"{e_path}.{key}", "must be filled"
                        )
        v.require(
            claim.get("mechanism_status") in MECHANISM_STATUSES,
            f"{path}.mechanism_status",
            f"must be one of {sorted(MECHANISM_STATUSES)}",
        )
        v.require(present(claim.get("boundary")), f"{path}.boundary", "must be filled")
        if claim.get("mechanism_status") != "direct":
            v.warn(
                bool(claim.get("counterevidence")),
                f"{path}.counterevidence",
                "supported inference or hypothesis should record counterevidence",
            )
    return claim_types


def validate_terms(v: Validator, terms: Any) -> None:
    v.require(isinstance(terms, list), "terms", "must be an array")
    if not isinstance(terms, list):
        return
    for index, term in enumerate(terms):
        path = f"terms[{index}]"
        keys = [
            "term_en",
            "term_zh",
            "class",
            "scope",
            "paper_id",
            "evidence_location",
            "source_wording",
            "operational_definition",
            "metric_or_test",
            "synonyms",
            "not_equivalent_to",
            "confidence",
        ]
        v.required_keys(term, path, keys)
        if not isinstance(term, dict):
            continue
        for key in (
            "term_en",
            "class",
            "scope",
            "paper_id",
            "evidence_location",
            "source_wording",
            "operational_definition",
            "not_equivalent_to",
            "confidence",
        ):
            v.require(present(term.get(key)), f"{path}.{key}", "must be filled")
        v.require(
            term.get("class") in TERM_CLASSES,
            f"{path}.class",
            f"must be one of {sorted(TERM_CLASSES)}",
        )
        v.require(
            term.get("confidence") in TERM_CONFIDENCE,
            f"{path}.confidence",
            f"must be one of {sorted(TERM_CONFIDENCE)}",
        )
        if term.get("class") in {"author_defined", "metric", "claim_language"}:
            v.require(
                present(term.get("metric_or_test")),
                f"{path}.metric_or_test",
                "author-defined terms, metrics, and claim language require "
                "an operational test",
            )
        if term.get("confidence") == "candidate":
            v.warnings.append(
                f"{path}: candidate term must not be presented as "
                "established terminology"
            )


def validate_positioning(v: Validator, positioning: Any) -> None:
    v.require(
        isinstance(positioning, list) and bool(positioning),
        "positioning",
        "must be a non-empty literature-positioning matrix",
    )
    if not isinstance(positioning, list):
        return
    required = [
        "id",
        "work",
        "proximity",
        "research_question",
        "assumptions",
        "mechanism",
        "evaluation",
        "main_finding",
        "boundary",
        "relation_to_this_paper",
        "citation_location",
        "baseline_implication",
    ]
    seen_ids: set[str] = set()
    for index, item in enumerate(positioning):
        path = f"positioning[{index}]"
        v.required_keys(item, path, required)
        if not isinstance(item, dict):
            continue
        for key in required:
            v.require(
                present(item.get(key)),
                f"{path}.{key}",
                "must be filled; use 'not applicable' with a reason if needed",
            )
        item_id = item.get("id")
        v.require(item_id not in seen_ids, f"{path}.id", "must be unique")
        if present(item_id):
            seen_ids.add(str(item_id))
        v.require(
            item.get("proximity") in POSITIONING_PROXIMITIES,
            f"{path}.proximity",
            f"must be one of {sorted(POSITIONING_PROXIMITIES)}",
        )


def validate_comparisons(
    v: Validator, comparisons: Any, claim_ids: set[str]
) -> set[str]:
    covered_claim_ids: set[str] = set()
    v.require(
        isinstance(comparisons, list) and bool(comparisons),
        "comparisons",
        "must be non-empty",
    )
    if not isinstance(comparisons, list):
        return covered_claim_ids
    required = [
        "id",
        "claim_ids",
        "workload",
        "input_shapes",
        "hardware",
        "software_stack",
        "precision",
        "baseline",
        "baseline_mode",
        "correctness_gate",
        "budget",
        "warmup",
        "repeats",
        "aggregation",
        "metric",
        "uncertainty",
        "exclusions",
    ]
    for index, comparison in enumerate(comparisons):
        path = f"comparisons[{index}]"
        v.required_keys(comparison, path, required)
        if not isinstance(comparison, dict):
            continue
        for key in required:
            v.require(
                present(comparison.get(key)),
                f"{path}.{key}",
                "must be filled; use 'not applicable' with a reason if needed",
            )
        for claim_id in comparison.get("claim_ids", []):
            v.require(
                claim_id in claim_ids,
                f"{path}.claim_ids",
                f"unknown claim id {claim_id!r}",
            )
            if claim_id in claim_ids:
                covered_claim_ids.add(claim_id)
    return covered_claim_ids


def validate_figures(v: Validator, figures: Any, claim_ids: set[str]) -> None:
    v.require(
        isinstance(figures, list) and bool(figures),
        "figures",
        "must be a non-empty figure plan",
    )
    if not isinstance(figures, list):
        return
    required = [
        "id",
        "claim_id",
        "role",
        "five_second_takeaway",
        "evidence_source",
        "comparison_objects",
        "visual_anchor",
        "conditions",
        "uncertainty",
        "caption_conclusion",
    ]
    for index, figure in enumerate(figures):
        path = f"figures[{index}]"
        v.required_keys(figure, path, required)
        if not isinstance(figure, dict):
            continue
        for key in required:
            v.require(
                present(figure.get(key)),
                f"{path}.{key}",
                "must be filled; use 'not applicable' with a reason if needed",
            )
        v.require(
            figure.get("claim_id") in claim_ids,
            f"{path}.claim_id",
            "must reference an existing claim",
        )
        v.require(
            figure.get("role") in FIGURE_ROLES,
            f"{path}.role",
            f"must be one of {sorted(FIGURE_ROLES)}",
        )


def validate_limitations(
    v: Validator, limitations: Any, claim_ids: set[str]
) -> None:
    v.require(
        isinstance(limitations, list) and bool(limitations),
        "limitations",
        "must be non-empty",
    )
    if not isinstance(limitations, list):
        return
    required = [
        "id",
        "claim_ids",
        "class",
        "observation",
        "claim_boundary",
        "evidence_needed",
    ]
    for index, limitation in enumerate(limitations):
        path = f"limitations[{index}]"
        v.required_keys(limitation, path, required)
        if not isinstance(limitation, dict):
            continue
        for key in required:
            v.require(present(limitation.get(key)), f"{path}.{key}", "must be filled")
        v.require(
            limitation.get("class") in LIMITATION_CLASSES,
            f"{path}.class",
            f"must be one of {sorted(LIMITATION_CLASSES)}",
        )
        for claim_id in limitation.get("claim_ids", []):
            v.require(
                claim_id in claim_ids,
                f"{path}.claim_ids",
                f"unknown claim id {claim_id!r}",
            )


def validate(data: Any) -> Validator:
    v = Validator()
    top_keys = [
        "paper_contract",
        "claims",
        "terms",
        "positioning",
        "comparisons",
        "figures",
        "limitations",
    ]
    v.required_keys(data, "ledger", top_keys)
    if not isinstance(data, dict):
        return v
    validate_contract(v, data.get("paper_contract"))
    claim_types = validate_claims(v, data.get("claims"))
    claim_ids = set(claim_types)
    validate_terms(v, data.get("terms"))
    validate_positioning(v, data.get("positioning"))
    compared_claim_ids = validate_comparisons(
        v, data.get("comparisons"), claim_ids
    )
    for claim_id, claim_type in claim_types.items():
        if claim_type in COMPARISON_REQUIRED_CLAIM_TYPES:
            v.require(
                claim_id in compared_claim_ids,
                f"claims[{claim_id}].comparison_coverage",
                f"{claim_type} claim must be linked from a comparison row",
            )
    validate_figures(v, data.get("figures"), claim_ids)
    validate_limitations(v, data.get("limitations"), claim_ids)
    return v


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("ledger", type=Path)
    parser.add_argument(
        "--strict", action="store_true", help="treat warnings as failures"
    )
    args = parser.parse_args()
    try:
        data = json.loads(args.ledger.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}")
        return 2
    result = validate(data)
    for item in result.errors:
        print(f"ERROR: {item}")
    for item in result.warnings:
        print(f"WARNING: {item}")
    print(
        json.dumps(
            {
                "errors": len(result.errors),
                "warnings": len(result.warnings),
                "strict": args.strict,
            }
        )
    )
    return 1 if result.errors or (args.strict and result.warnings) else 0


if __name__ == "__main__":
    raise SystemExit(main())
