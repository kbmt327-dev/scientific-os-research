#!/usr/bin/env python3
"""Create a non-copying public-note skeleton and validate publishable notes."""

from __future__ import annotations

import argparse
import hashlib
import re
from pathlib import Path

import yaml


TYPES = {"Finding", "Protocol", "Method", "Replication", "Negative Result", "Dataset", "Benchmark"}
PUBLICATION_STATES = {"draft", "candidate", "publishable"}
COMMON_SECTIONS = {
    "Summary", "Research question", "Why this matters", "Method", "What changed",
    "What failed", "Evidence boundary", "UNKNOWN", "Falsification targets", "Reproduce",
    "Evidence / Artifacts", "External audit", "Next experiment",
}
COMMON_SECTIONS_JA = {
    "要約", "研究質問", "なぜ重要か", "方法", "何が変わったか",
    "何が失敗したか", "証拠境界", "UNKNOWN", "反証条件", "再現",
    "証拠 / Artifacts", "外部監査", "次の実験",
}
PAIR_FIELDS = ("research_id", "type", "source_episode", "source_episode_sha256")


def frontmatter(text: str) -> tuple[dict, str]:
    match = re.match(r"\A---\s*\n(.*?)\n---\s*\n", text, flags=re.DOTALL)
    if not match:
        raise ValueError("missing YAML frontmatter")
    data = yaml.safe_load(match.group(1))
    if not isinstance(data, dict):
        raise ValueError("frontmatter must be a mapping")
    return data, text[match.end():]


def validate_note(path: Path) -> list[str]:
    errors: list[str] = []
    try:
        meta, body = frontmatter(path.read_text(encoding="utf-8-sig"))
    except Exception as exc:
        return [f"{path}: {exc}"]
    required = {"research_id", "lang", "title", "date", "domain", "type", "status", "evidence", "review", "replication", "claim_scope", "source_episode", "source_episode_sha256", "publication"}
    missing = sorted(required - set(meta))
    if missing:
        errors.append(f"missing frontmatter: {', '.join(missing)}")
    if meta.get("type") not in TYPES:
        errors.append(f"unsupported research type: {meta.get('type')!r}")
    if meta.get("lang") not in {"en", "ja"}:
        errors.append("lang must be en or ja")
    if "translation_of" in meta:
        errors.append("translation_of is not allowed; language views share research_id")
    if not isinstance(meta.get("evidence"), dict) or not all(meta["evidence"].get(k) for k in ("class", "source")):
        errors.append("evidence.class and evidence.source are required")
    review_fields = {
        "editorial_reviewed", "scientific_reviewed",
        "domain_expert_reviewed", "peer_reviewed",
    }
    if not isinstance(meta.get("review"), dict) or not review_fields.issubset(meta["review"]):
        errors.append("review must separate editorial, scientific, domain-expert, and peer review")
    elif any(not isinstance(meta["review"][field], bool) for field in review_fields):
        errors.append("all review fields must be boolean")
    if not isinstance(meta.get("replication"), dict) or not all(k in meta["replication"] for k in ("independent", "failed")):
        errors.append("replication.independent and replication.failed are required")
    publication = meta.get("publication")
    if not isinstance(publication, dict) or publication.get("status") not in PUBLICATION_STATES:
        errors.append("publication.status must be draft, candidate, or publishable")
    if re.search(r"[A-Za-z]:[\\/]", str(meta.get("source_episode", ""))):
        errors.append("source_episode must be an opaque public identifier, not a local path")
    sections = set(re.findall(r"^##\s+(.+?)\s*$", body, flags=re.MULTILINE))
    language = str(meta.get("lang", "en")).lower()
    required_sections = set(COMMON_SECTIONS_JA if language.startswith("ja") else COMMON_SECTIONS)
    if meta.get("type") == "Finding":
        required_sections.add("結果" if language.startswith("ja") else "Results")
        required_sections.update(
            {"発見", "Key figure", "この研究が示すこと", "この研究が示さないこと"}
            if language.startswith("ja")
            else {"The finding", "Key figure", "What this research shows", "What this research does not show"}
        )
    elif meta.get("type") == "Method":
        required_sections.update(
            {"Method", "Key figure", "このMethodが確立すること", "このMethodが確立しないこと"}
            if language.startswith("ja")
            else {"The method", "Key figure", "What this method establishes", "What this method does not establish"}
        )
    elif meta.get("type") == "Protocol":
        required_sections.update(
            {"問い", "Key figure", "このProtocolが確立すること", "このProtocolが確立しないこと"}
            if language.startswith("ja")
            else {"The question", "Key figure", "What this protocol establishes", "What this protocol does not establish"}
        )
    missing_sections = sorted(required_sections - sections)
    if missing_sections:
        errors.append(f"missing sections: {', '.join(missing_sections)}")
    result_claim = r"\b(confirmatory result|we found|demonstrates an effect)\b|確証的な結果|効果を示した|効果を実証"
    if meta.get("type") == "Protocol" and re.search(result_claim, body, flags=re.IGNORECASE):
        errors.append("protocol contains result-like claim requiring manual review")
    return [f"{path}: {error}" for error in errors]


def validate_tree(root: Path) -> int:
    notes = sorted(root.glob("en/research/*/index.md")) + sorted(root.glob("ja/research/*/index.md"))
    errors = [error for note in notes for error in validate_note(note)]
    pairs: dict[str, dict[str, tuple[Path, dict]]] = {}
    for note in notes:
        try:
            meta, _ = frontmatter(note.read_text(encoding="utf-8-sig"))
        except Exception:
            continue
        research_id = str(meta.get("research_id", ""))
        lang = str(meta.get("lang", ""))
        if research_id and lang:
            if lang in pairs.setdefault(research_id, {}):
                errors.append(f"{note}: duplicate research_id {research_id!r} for lang {lang!r}")
            pairs[research_id][lang] = (note, meta)
    for research_id, views in sorted(pairs.items()):
        if set(views) != {"en", "ja"}:
            errors.append(f"{research_id}: expected en and ja views, found {sorted(views)}")
            continue
        en_meta = views["en"][1]
        ja_meta = views["ja"][1]
        for field in PAIR_FIELDS:
            if en_meta.get(field) != ja_meta.get(field):
                errors.append(f"{research_id}: language views disagree on {field}")
    manifest_path = root.parent / "publication-manifest.yaml"
    if manifest_path.exists():
        manifest = yaml.safe_load(manifest_path.read_text(encoding="utf-8-sig"))
        manifest_notes = manifest.get("notes", []) if isinstance(manifest, dict) else []
        manifest_ids: set[str] = set()
        for entry in manifest_notes:
            research_id = str(entry.get("research_id", ""))
            if not research_id:
                errors.append(f"{manifest_path}: entry missing research_id")
                continue
            if research_id in manifest_ids:
                errors.append(f"{manifest_path}: duplicate research_id {research_id}")
            manifest_ids.add(research_id)
            views = entry.get("views")
            if not isinstance(views, dict) or set(views) != {"en", "ja"}:
                errors.append(f"{manifest_path}: {research_id} must declare en and ja views")
                continue
            for lang, public_path in views.items():
                path = root.parent / str(public_path)
                if not path.exists():
                    errors.append(f"{manifest_path}: missing {lang} view for {research_id}: {public_path}")
                    continue
                meta, _ = frontmatter(path.read_text(encoding="utf-8-sig"))
                if meta.get("research_id") != research_id or meta.get("lang") != lang:
                    errors.append(f"{manifest_path}: {public_path} identity or lang does not match {research_id}/{lang}")
                for field in ("type", "source_episode", "source_episode_sha256"):
                    if entry.get(field) != meta.get(field):
                        errors.append(f"{manifest_path}: {research_id} disagrees with {public_path} on {field}")
        if manifest_ids != set(pairs):
            errors.append(
                f"{manifest_path}: manifest/research-note IDs differ; "
                f"missing={sorted(set(pairs) - manifest_ids)}, extra={sorted(manifest_ids - set(pairs))}"
            )
    if errors:
        print("Publication validation failed:")
        print("\n".join(errors))
        return 1
    print(f"Publication validation passed: {len(notes)} Research Notes")
    return 0


def project(source: Path, output: Path, note_type: str, lang: str) -> int:
    text = source.read_text(encoding="utf-8-sig")
    meta, _ = frontmatter(text)
    source_id = meta.get("episode_id") or meta.get("id")
    domain = str(meta.get("domain", "UNKNOWN")).upper().replace(" ", "-")
    if not source_id:
        raise SystemExit("source Episode lacks episode_id/id")
    digest = hashlib.sha256(source.read_bytes()).hexdigest()
    public_id = f"{domain}-{source_id}"
    skeleton = f'''---
research_id: {public_id}
lang: {lang}
title: TODO
date: {meta.get("date") or meta.get("created_at") or "TODO"}
domain: {meta.get("domain", "UNKNOWN")}
type: {note_type}
status: Draft
evidence:
  class: TODO
  source: TODO
review:
  editorial_reviewed: false
  scientific_reviewed: false
  domain_expert_reviewed: false
  peer_reviewed: false
replication:
  independent: 0
  failed: 0
claim_scope: TODO
source_episode: {domain}/{source_id}
source_episode_sha256: {digest}
publication:
  status: draft
---

# TODO

## Summary

## Research question

## Why this matters

## Method

## Results

## What changed

## What failed

## Evidence boundary

## UNKNOWN

## Falsification targets

## Reproduce

Reproduction package: not yet public.

## Evidence / Artifacts

## External audit

- Independent replications: 0
- Failed replications: 0
- Confirmed bugs: 0
- Open critiques: 0

## Next experiment
'''
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(skeleton, encoding="utf-8")
    print(f"Created draft projection without copying Episode body: {output}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)
    check = sub.add_parser("validate")
    check.add_argument("content", nargs="?", default="content")
    make = sub.add_parser("project")
    make.add_argument("source")
    make.add_argument("output")
    make.add_argument("--type", required=True, choices=sorted(TYPES))
    make.add_argument("--lang", choices=("en", "ja"), default="en")
    args = parser.parse_args()
    if args.command == "validate":
        return validate_tree(Path(args.content))
    return project(Path(args.source), Path(args.output), args.type, args.lang)


if __name__ == "__main__":
    raise SystemExit(main())
