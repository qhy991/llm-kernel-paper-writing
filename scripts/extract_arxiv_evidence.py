#!/usr/bin/env python3
"""Extract writing evidence, figure context, and optional assets from arXiv HTML.

Outputs are candidates for human verification, not authoritative definitions or
claims. Official arXiv HTML is tried before ar5iv unless a local HTML file/root
is provided.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import mimetypes
import re
import time
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup, Tag

ARXIV_RE = re.compile(
    r"https?://(?:www\.)?arxiv\.org/(?:abs|html|pdf)/"
    r"(?P<id>\d{4}\.\d{4,5})(?P<version>v\d+)?",
    re.IGNORECASE,
)
SAFE_RE = re.compile(r"[^A-Za-z0-9._-]+")
SENTENCE_RE = re.compile(r"(?<=[.!?])\s+(?=[A-Z0-9])")
FIGURE_REF_RE = r"(?:Figure|Fig\.)\s*~?\s*{number}\b"
USER_AGENT = (
    "llm-kernel-paper-writing/1.0 "
    "(non-commercial research evidence extraction)"
)

RHETORICAL_PATTERNS: list[tuple[str, re.Pattern[str]]] = [
    (
        "gap_or_contrast",
        re.compile(
            r"\bhowever\b|\bnevertheless\b|\bdespite\b|\byet\b|"
            r"\bremain(?:s|ed)?\b|\black(?:s|ing)?\b|\blimitation",
            re.IGNORECASE,
        ),
    ),
    (
        "research_response",
        re.compile(
            r"\bto address\b|\bwe (?:propose|present|introduce|develop|build)\b",
            re.IGNORECASE,
        ),
    ),
    (
        "mechanistic_insight",
        re.compile(
            r"\bkey (?:insight|observation)\b|\bwe observe\b|"
            r"\bthis (?:suggests|reveals|motivates|enables)\b",
            re.IGNORECASE,
        ),
    ),
    (
        "evaluation",
        re.compile(
            r"\bwe (?:evaluate|benchmark|conduct|compare)\b|\bexperiments?\b",
            re.IGNORECASE,
        ),
    ),
    (
        "result",
        re.compile(
            r"\bresults? (?:show|demonstrate|indicate)\b|"
            r"\bachieve(?:s|d)?\b|\boutperform(?:s|ed)?\b|"
            r"\bsurpass(?:es|ed)?\b",
            re.IGNORECASE,
        ),
    ),
    ("contributions", re.compile(r"\bcontribution(?:s)?\b", re.IGNORECASE)),
    (
        "boundary",
        re.compile(
            r"\blimitation(?:s)?\b|\bwe do not\b|\bwe leave\b|"
            r"\bnot (?:a|an) (?:proof|guarantee)\b|\bfuture work\b",
            re.IGNORECASE,
        ),
    ),
]

CLAIM_PATTERN = re.compile(
    r"\b(?:show|demonstrate|find|observe|achieve|outperform|surpass|improve|"
    r"reduce|increase|decrease|reveal|validate)(?:s|d|ed)?\b|"
    r"\b\d+(?:\.\d+)?\s*(?:%|×|x|ms|us|µs|GB/s|TB/s|TFLOP/s)\b",
    re.IGNORECASE,
)
DEFINITION_PATTERN = re.compile(
    r"\bwe (?:call|term|refer to|denote|define|name)\b|"
    r"\b(?:is|are) defined as\b|\bstands for\b|"
    r"\b(?:denotes?|means?|refers? to)\b|"
    r"\b[A-Z][A-Za-z0-9-]*(?:[-\s][A-Za-z][A-Za-z0-9-]*){0,8}"
    r"\s*\([A-Z][A-Z0-9-]{1,12}\)",
    re.IGNORECASE,
)
ACRONYM_RE = re.compile(r"\b[A-Z][A-Z0-9-]{1,12}\b")
ACRONYM_STOP = {
    "A",
    "AN",
    "AND",
    "ARE",
    "AS",
    "AT",
    "BY",
    "FOR",
    "FROM",
    "GPU",
    "GPUS",
    "IN",
    "IS",
    "IT",
    "LM",
    "LLM",
    "LLMS",
    "OF",
    "ON",
    "OR",
    "OUR",
    "THE",
    "TO",
    "WE",
    "WITH",
}


def normalize(value: str | None) -> str:
    return re.sub(r"\s+", " ", value or "").strip()


def safe_name(value: str) -> str:
    return SAFE_RE.sub("-", value).strip("-")[:100] or "item"


def sha256_bytes(content: bytes) -> str:
    return hashlib.sha256(content).hexdigest()


def canonical_id(value: str) -> str:
    match = re.fullmatch(r"(\d{4}\.\d{4,5})(?:v\d+)?", value.strip())
    if not match:
        raise ValueError(f"invalid arXiv id: {value}")
    return match.group(1)


def refs_from_readme(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8")
    return list(
        dict.fromkeys(
            f"{match.group('id')}{match.group('version') or ''}"
            for match in ARXIV_RE.finditer(text)
        )
    )


def ids_from_readme(path: Path) -> list[str]:
    return list(dict.fromkeys(canonical_id(ref) for ref in refs_from_readme(path)))


def refs_from_id_file(path: Path) -> list[str]:
    refs: list[str] = []
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        value = raw_line.split("#", 1)[0].strip()
        if value:
            canonical_id(value)
            refs.append(value)
    return list(dict.fromkeys(refs))


def request_with_retries(
    session: requests.Session,
    url: str,
    timeout: float,
    retries: int,
) -> requests.Response:
    last_error: Exception | None = None
    for attempt in range(retries + 1):
        try:
            response = session.get(url, timeout=timeout)
            if response.status_code == 429 or response.status_code >= 500:
                response.close()
                raise requests.HTTPError(f"HTTP {response.status_code}")
            return response
        except requests.RequestException as exc:
            last_error = exc
            if attempt < retries:
                time.sleep(min(8.0, 2**attempt))
    raise RuntimeError(f"request failed for {url}: {last_error}")


def infer_extension(url: str, content_type: str | None) -> str:
    suffix = Path(urlparse(url).path).suffix.lower()
    if suffix and len(suffix) <= 8:
        return suffix
    guessed = mimetypes.guess_extension(
        (content_type or "").split(";", 1)[0].strip()
    )
    return guessed or ".bin"


def direct_caption(node: Tag) -> Tag | None:
    caption = node.find("figcaption", recursive=False)
    if isinstance(caption, Tag):
        return caption
    caption = node.find(class_="ltx_caption", recursive=False)
    if isinstance(caption, Tag):
        return caption
    caption = node.select_one("figcaption, .ltx_caption")
    return caption if isinstance(caption, Tag) else None


def caption_label(caption: Tag | None) -> str:
    if caption is None:
        return ""
    label = caption.select_one(".ltx_tag_figure, .ltx_tag")
    return normalize(label.get_text(" ", strip=True)) if label else ""


def top_level_figures(soup: BeautifulSoup) -> list[Tag]:
    nodes = [
        node
        for node in soup.select("figure.ltx_figure")
        if node.find_parent("figure") is None
        and "ltx_table" not in (node.get("class") or [])
    ]
    if not nodes:
        nodes = [
            node
            for node in soup.find_all("figure")
            if node.find_parent("figure") is None
            and "ltx_table" not in (node.get("class") or [])
        ]
    return [
        node
        for node in nodes
        if isinstance(node, Tag)
        and (
            node.find("img") is not None
            or node.find("svg") is not None
            or caption_label(direct_caption(node)).lower().startswith(
                ("figure", "fig.")
            )
        )
    ]


def extract_title(soup: BeautifulSoup, fallback: str) -> str:
    for selector in (
        "h1.ltx_title_document",
        "h1.title",
        "meta[name='citation_title']",
        "title",
    ):
        node = soup.select_one(selector)
        if not node:
            continue
        value = node.get("content") if node.name == "meta" else node.get_text(" ")
        if normalize(value):
            return normalize(value)
    return fallback


def extract_abstract(soup: BeautifulSoup) -> str:
    node = soup.select_one(".ltx_abstract, blockquote.abstract, #abstract")
    return normalize(node.get_text(" ", strip=True)) if node else ""


def direct_paragraphs(section: Tag) -> list[str]:
    paragraphs: list[str] = []
    for paragraph in section.select("p.ltx_p, p"):
        parent_section = paragraph.find_parent("section")
        if parent_section is section:
            text = normalize(paragraph.get_text(" ", strip=True))
            if text:
                paragraphs.append(text)
    return paragraphs


def extract_sections(soup: BeautifulSoup) -> list[dict]:
    records: list[dict] = []
    selectors = (
        "h2.ltx_title_section, h2.ltx_title_appendix, "
        "h3.ltx_title_subsection, h4.ltx_title_subsubsection"
    )
    headings = soup.select(selectors)
    if not headings:
        headings = soup.select("h2, h3, h4")
    for heading in headings:
        if not isinstance(heading, Tag):
            continue
        section = heading.find_parent("section")
        paragraphs = direct_paragraphs(section) if isinstance(section, Tag) else []
        records.append(
            {
                "level": int(heading.name[1]),
                "id": section.get("id") if isinstance(section, Tag) else None,
                "title": normalize(heading.get_text(" ", strip=True)),
                "paragraph_count": len(paragraphs),
            }
        )
    return records


def section_paragraphs(soup: BeautifulSoup, needles: tuple[str, ...]) -> list[str]:
    for heading in soup.select(
        "h2.ltx_title_section, h2.ltx_title_appendix, h2, "
        "h3.ltx_title_subsection, h3"
    ):
        title = normalize(heading.get_text(" ", strip=True)).lower()
        if any(needle in title for needle in needles):
            section = heading.find_parent("section")
            if isinstance(section, Tag):
                return direct_paragraphs(section)
    return []


def body_paragraph_blocks(soup: BeautifulSoup) -> list[tuple[str, str]]:
    """Return source-located body paragraphs, excluding captions and abstract."""
    blocks: list[tuple[str, str]] = []
    section_counts: Counter[str] = Counter()
    for paragraph in soup.select("p.ltx_p, p"):
        if paragraph.find_parent(["figure", "figcaption"]):
            continue
        if paragraph.find_parent(class_="ltx_abstract"):
            continue
        section = paragraph.find_parent("section")
        if not isinstance(section, Tag):
            continue
        heading = section.find(["h2", "h3", "h4"], recursive=False)
        section_name = normalize(
            heading.get_text(" ", strip=True) if isinstance(heading, Tag) else ""
        )
        section_name = section_name or str(section.get("id") or "unnamed section")
        text = normalize(paragraph.get_text(" ", strip=True))
        if not text:
            continue
        section_counts[section_name] += 1
        blocks.append(
            (
                f"{section_name}, paragraph {section_counts[section_name]}",
                text,
            )
        )
    return blocks


def split_sentences(text: str) -> list[str]:
    return [normalize(item) for item in SENTENCE_RE.split(text) if normalize(item)]


def rhetorical_cues(introduction: list[str]) -> list[dict]:
    cues: list[dict] = []
    for paragraph_index, paragraph in enumerate(introduction, start=1):
        for name, pattern in RHETORICAL_PATTERNS:
            match = pattern.search(paragraph)
            if match:
                start = max(0, match.start() - 120)
                end = min(len(paragraph), match.end() + 220)
                cues.append(
                    {
                        "move": name,
                        "paragraph": paragraph_index,
                        "matched": match.group(0),
                        "context": normalize(paragraph[start:end]),
                    }
                )
    return cues


def candidate_sentences(blocks: list[tuple[str, str]]) -> tuple[list[dict], list[dict]]:
    claims: list[dict] = []
    definitions: list[dict] = []
    seen_claims: set[str] = set()
    seen_definitions: set[str] = set()
    for location, text in blocks:
        for sentence in split_sentences(text):
            if CLAIM_PATTERN.search(sentence) and sentence not in seen_claims:
                seen_claims.add(sentence)
                claims.append(
                    {
                        "location": location,
                        "text": sentence,
                        "status": "candidate-requires-source-review",
                    }
                )
            if DEFINITION_PATTERN.search(sentence) and sentence not in seen_definitions:
                seen_definitions.add(sentence)
                definitions.append(
                    {
                        "location": location,
                        "text": sentence,
                        "status": "candidate-requires-source-review",
                    }
                )
    return claims[:100], definitions[:100]


def acronym_candidates(blocks: list[tuple[str, str]]) -> list[dict]:
    contexts: dict[str, list[dict]] = {}
    for location, text in blocks:
        for sentence in split_sentences(text):
            for match in ACRONYM_RE.finditer(sentence):
                term = match.group(0)
                if term in ACRONYM_STOP or term.isdigit():
                    continue
                entries = contexts.setdefault(term, [])
                if len(entries) < 3:
                    entries.append({"location": location, "context": sentence})
    return [
        {
            "term": term,
            "occurrences_in_sampled_blocks": len(entries),
            "contexts": entries,
            "status": "unverified-candidate-not-a-definition",
        }
        for term, entries in sorted(contexts.items())
    ]


def figure_number(label: str, index: int) -> str:
    match = re.search(r"(?:Figure|Fig\.)\s*([0-9]+)", label, re.IGNORECASE)
    return match.group(1) if match else str(index)


def referencing_contexts(
    soup: BeautifulSoup,
    number: str,
    caption_node: Tag | None,
) -> list[str]:
    pattern = re.compile(FIGURE_REF_RE.format(number=re.escape(number)), re.IGNORECASE)
    contexts: list[str] = []
    for paragraph in soup.select("p.ltx_p, p"):
        if caption_node is not None and caption_node in paragraph.parents:
            continue
        text = normalize(paragraph.get_text(" ", strip=True))
        if text and pattern.search(text):
            contexts.append(text)
        if len(contexts) >= 4:
            break
    return contexts


def download_linked_asset(
    session: requests.Session,
    source_url: str,
    stem: Path,
    timeout: float,
    retries: int,
) -> tuple[Path, str]:
    response = request_with_retries(session, source_url, timeout, retries)
    response.raise_for_status()
    extension = infer_extension(source_url, response.headers.get("content-type"))
    destination = stem.with_suffix(extension)
    content = response.content
    response.close()
    destination.write_bytes(content)
    return destination, sha256_bytes(content)


def extract_figures(
    soup: BeautifulSoup,
    *,
    session: requests.Session,
    output_root: Path,
    paper_dir: Path,
    resolved_url: str,
    download_images: bool,
    timeout: float,
    retries: int,
) -> list[dict]:
    base_node = soup.select_one("base[href]")
    asset_base = (
        urljoin(resolved_url, base_node.get("href"))
        if base_node
        else urljoin(resolved_url, "./")
    )
    image_dir = paper_dir / "images"
    if download_images:
        image_dir.mkdir(parents=True, exist_ok=True)
    records: list[dict] = []
    for figure_index, node in enumerate(top_level_figures(soup), start=1):
        caption_node = direct_caption(node)
        label = caption_label(caption_node)
        caption = normalize(
            caption_node.get_text(" ", strip=True) if caption_node else ""
        )
        number = figure_number(label, figure_index)
        assets: list[dict] = []
        images = [
            item
            for item in node.find_all(["img", "svg"])
            if item.name == "img"
            or "ltx_picture" in (item.get("class") or [])
        ]
        for asset_index, image in enumerate(images, start=1):
            record = {
                "index": asset_index,
                "kind": "inline-svg" if image.name == "svg" else "linked-image",
                "source_url": "",
                "local_path": None,
                "sha256": None,
                "alt_text": normalize(
                    image.get("alt")
                    or image.get("aria-label")
                    or image.get("title")
                ),
                "status": "not-downloaded",
                "error": None,
            }
            stem = image_dir / f"figure-{figure_index:02d}-{asset_index:02d}"
            try:
                if image.name == "svg":
                    svg_id = image.get("id") or f"figure-{figure_index}-{asset_index}"
                    record["source_url"] = f"{resolved_url}#{svg_id}"
                    if download_images:
                        image["xmlns"] = (
                            image.get("xmlns") or "http://www.w3.org/2000/svg"
                        )
                        content = str(image).encode("utf-8")
                        destination = stem.with_suffix(".svg")
                        destination.write_bytes(content)
                        record["local_path"] = str(
                            destination.relative_to(output_root)
                        )
                        record["sha256"] = sha256_bytes(content)
                        record["status"] = "extracted"
                else:
                    raw_src = image.get("src") or image.get("data-src")
                    if not raw_src or raw_src.startswith("data:"):
                        record["status"] = "embedded-or-missing-source"
                    else:
                        source_url = urljoin(asset_base, raw_src)
                        record["source_url"] = source_url
                        if download_images:
                            destination, digest = download_linked_asset(
                                session,
                                source_url,
                                stem,
                                timeout,
                                retries,
                            )
                            record["local_path"] = str(
                                destination.relative_to(output_root)
                            )
                            record["sha256"] = digest
                            record["status"] = "downloaded"
            except Exception as exc:  # Preserve the rest of the evidence packet.
                record["status"] = "download-error"
                record["error"] = str(exc)
            assets.append(record)
        records.append(
            {
                "index": figure_index,
                "id": node.get("id"),
                "label": label,
                "caption": caption,
                "referencing_contexts": referencing_contexts(
                    soup, number, caption_node
                ),
                "assets": assets,
            }
        )
    return records


def paper_type_hint(title: str, abstract: str) -> str:
    text = f"{title} {abstract}".lower()
    if any(word in text for word in ("benchmark", "dataset", "evaluating")):
        return "benchmark-or-dataset"
    if any(word in text for word in ("verification", "symbolic", "compiler")):
        return "compiler-or-verification"
    if any(word in text for word in ("roofline", "speed-of-light", "profiling")):
        return "performance-analysis"
    if any(word in text for word in ("reinforcement learning", "fine-tun", "sft")):
        return "model-or-post-training"
    if any(word in text for word in ("agent", "search", "evolution")):
        return "agent-or-search"
    return "manual-review-required"


def parse_paper(
    *,
    arxiv_id: str,
    requested_ref: str,
    html_content: bytes,
    provider: str,
    resolved_url: str,
    output_root: Path,
    paper_dir: Path,
    session: requests.Session,
    download_images: bool,
    timeout: float,
    retries: int,
) -> dict:
    soup = BeautifulSoup(html_content, "html.parser")
    title = extract_title(soup, arxiv_id)
    abstract = extract_abstract(soup)
    introduction = section_paragraphs(soup, ("introduction",))
    conclusion = section_paragraphs(soup, ("conclusion",))
    limitations = section_paragraphs(
        soup, ("limitation", "discussion", "threat", "future work")
    )
    blocks: list[tuple[str, str]] = [("abstract", abstract)]
    blocks.extend(body_paragraph_blocks(soup))
    claims, definitions = candidate_sentences(blocks)
    figures = extract_figures(
        soup,
        session=session,
        output_root=output_root,
        paper_dir=paper_dir,
        resolved_url=resolved_url,
        download_images=download_images,
        timeout=timeout,
        retries=retries,
    )
    return {
        "arxiv_id": arxiv_id,
        "requested_ref": requested_ref,
        "title": title,
        "paper_type_hint": paper_type_hint(title, abstract),
        "provider": provider,
        "resolved_url": resolved_url,
        "retrieved_at": datetime.now(timezone.utc).isoformat(),
        "html_sha256": sha256_bytes(html_content),
        "abstract": abstract,
        "sections": extract_sections(soup),
        "introduction_paragraphs": introduction,
        "conclusion_paragraphs": conclusion,
        "limitations_or_discussion_paragraphs": limitations,
        "rhetorical_cues": rhetorical_cues(introduction),
        "claim_candidates": claims,
        "definition_candidates": definitions,
        "unverified_acronym_candidates": acronym_candidates(blocks),
        "figures": figures,
        "status": "ok",
        "warnings": [
            "All claim, definition, acronym, and paper-type fields are candidates.",
            "Verify exact source context before using them in prose.",
        ],
    }


def fetch_html(
    session: requests.Session,
    arxiv_ref: str,
    official_base_url: str,
    fallback_base_url: str | None,
    timeout: float,
    retries: int,
) -> tuple[bytes, str, str]:
    attempts = [("arxiv", f"{official_base_url.rstrip('/')}/{arxiv_ref}")]
    if fallback_base_url:
        attempts.append(("ar5iv", f"{fallback_base_url.rstrip('/')}/{arxiv_ref}"))
    errors: list[str] = []
    for provider, url in attempts:
        try:
            response = request_with_retries(session, url, timeout, retries)
            if response.status_code == 200 and response.content:
                content = response.content
                resolved = response.url
                response.close()
                return content, provider, resolved
            errors.append(f"{provider}: HTTP {response.status_code}")
            response.close()
        except Exception as exc:
            errors.append(f"{provider}: {exc}")
    raise RuntimeError("; ".join(errors))


def local_html_map(args: argparse.Namespace) -> dict[str, Path]:
    mapping: dict[str, Path] = {}
    if args.html_file:
        if len(args.id or []) != 1:
            raise SystemExit("--html-file requires exactly one --id")
        mapping[canonical_id(args.id[0])] = args.html_file
    if args.html_root:
        for path in sorted(args.html_root.glob("*/source.html")):
            try:
                arxiv_id = canonical_id(path.parent.name)
                if arxiv_id in mapping and mapping[arxiv_id] != path:
                    raise SystemExit(
                        f"--html-root contains multiple versions of {arxiv_id}; "
                        "extract them in separate runs"
                    )
                mapping[arxiv_id] = path
            except ValueError:
                continue
    return mapping


def collect_ids(args: argparse.Namespace, local: dict[str, Path]) -> list[str]:
    ids: list[str] = []
    if args.readme:
        ids.extend(ids_from_readme(args.readme))
    if args.id_file:
        ids.extend(canonical_id(ref) for ref in refs_from_id_file(args.id_file))
    ids.extend(canonical_id(value) for value in (args.id or []))
    ids.extend(local)
    unique = list(dict.fromkeys(ids))
    return unique[: args.limit] if args.limit is not None else unique


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--id",
        action="append",
        help="arXiv ID, optionally pinned as <id>vN; repeatable",
    )
    parser.add_argument("--readme", type=Path, help="Markdown containing arXiv URLs")
    parser.add_argument(
        "--id-file",
        type=Path,
        help="text file with one arXiv ID or versioned ID per line",
    )
    parser.add_argument("--html-file", type=Path, help="local HTML for one --id")
    parser.add_argument(
        "--html-root",
        type=Path,
        help="directory containing <arxiv-id>/source.html subdirectories",
    )
    parser.add_argument("--source-url", help="base URL for a local --html-file")
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--download-images", action="store_true")
    parser.add_argument("--limit", type=int)
    parser.add_argument("--overwrite", action="store_true")
    parser.add_argument("--timeout", type=float, default=30.0)
    parser.add_argument("--retries", type=int, default=3)
    parser.add_argument("--delay", type=float, default=0.5)
    parser.add_argument(
        "--official-base-url", default="https://arxiv.org/html"
    )
    parser.add_argument(
        "--fallback-base-url", default="https://ar5iv.labs.arxiv.org/html"
    )
    parser.add_argument("--no-fallback", action="store_true")
    args = parser.parse_args()

    local = local_html_map(args)
    ids = collect_ids(args, local)
    if not ids:
        raise SystemExit(
            "No papers found. Pass --id, --id-file, --readme, or --html-root."
        )

    output_root = args.output_dir.resolve()
    output_root.mkdir(parents=True, exist_ok=True)
    session = requests.Session()
    session.headers.update({"User-Agent": USER_AGENT})
    papers: list[dict] = []
    requested_refs: dict[str, str] = {}
    for arxiv_id, path in local.items():
        requested_refs.setdefault(arxiv_id, path.parent.name)
    if args.readme:
        for ref in refs_from_readme(args.readme):
            requested_refs.setdefault(canonical_id(ref), ref)
    if args.id_file:
        for ref in refs_from_id_file(args.id_file):
            requested_refs.setdefault(canonical_id(ref), ref)
    requested_refs.update(
        {canonical_id(value): value.strip() for value in (args.id or [])}
    )
    try:
        for index, arxiv_id in enumerate(ids, start=1):
            requested_ref = requested_refs.get(arxiv_id, arxiv_id)
            paper_dir = output_root / "papers" / safe_name(requested_ref)
            evidence_path = paper_dir / "evidence.json"
            print(f"[{index:03d}/{len(ids):03d}] {requested_ref}", flush=True)
            if evidence_path.exists() and not args.overwrite:
                papers.append(json.loads(evidence_path.read_text(encoding="utf-8")))
                continue
            paper_dir.mkdir(parents=True, exist_ok=True)
            try:
                if arxiv_id in local:
                    html_content = local[arxiv_id].read_bytes()
                    provider = "local-html"
                    resolved_url = (
                        args.source_url
                        or f"{args.official_base_url.rstrip('/')}/{arxiv_id}"
                    )
                else:
                    html_content, provider, resolved_url = fetch_html(
                        session,
                        requested_ref,
                        args.official_base_url,
                        None if args.no_fallback else args.fallback_base_url,
                        args.timeout,
                        args.retries,
                    )
                source_path = paper_dir / "source.html"
                source_path.write_bytes(html_content)
                evidence = parse_paper(
                    arxiv_id=arxiv_id,
                    requested_ref=requested_ref,
                    html_content=html_content,
                    provider=provider,
                    resolved_url=resolved_url,
                    output_root=output_root,
                    paper_dir=paper_dir,
                    session=session,
                    download_images=args.download_images,
                    timeout=args.timeout,
                    retries=args.retries,
                )
            except Exception as exc:
                evidence = {
                    "arxiv_id": arxiv_id,
                    "requested_ref": requested_ref,
                    "status": "error",
                    "error": str(exc),
                }
            evidence_path.write_text(
                json.dumps(evidence, ensure_ascii=False, indent=2),
                encoding="utf-8",
            )
            papers.append(evidence)
            if index != len(ids) and arxiv_id not in local:
                time.sleep(args.delay)
    finally:
        session.close()

    (output_root / "papers.json").write_text(
        json.dumps(papers, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    statuses = Counter(paper.get("status", "unknown") for paper in papers)
    summary = {
        "paper_count": len(papers),
        "statuses": dict(sorted(statuses.items())),
        "figure_count": sum(len(paper.get("figures", [])) for paper in papers),
        "asset_count": sum(
            len(figure.get("assets", []))
            for paper in papers
            for figure in paper.get("figures", [])
        ),
        "candidate_claim_count": sum(
            len(paper.get("claim_candidates", [])) for paper in papers
        ),
        "candidate_definition_count": sum(
            len(paper.get("definition_candidates", [])) for paper in papers
        ),
        "caveat": "Candidates require primary-source review before use.",
    }
    (output_root / "summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(json.dumps(summary, ensure_ascii=False))
    return 0 if statuses.get("error", 0) == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
