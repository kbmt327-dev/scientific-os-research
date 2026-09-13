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
    required = {"id", "title", "date", "domain", "type", "status", "evidence", "review", "replication", "claim_scope", "source_episode", "publication"}
    missing = sorted(required - set(meta))
    if missing:
        errors.append(f"missing frontmatter: {', '.join(missing)}")
    if meta.get("type") not in TYPES:
        errors.append(f"unsupported research type: {meta.get('type')!r}")
    if not isinstance(meta.get("evidence"), dict) or not all(meta["evidence"].get(k) for k in ("class", "source")):
        errors.append("evidence.class and evidence.source are required")
    if not isinstance(meta.get("review"), dict) or "peer_reviewed" not in meta["review"] or "human_reviewed" not in meta["review"]:
        errors.append("review.peer_reviewed and review.human_reviewed are required")
    if not isinstance(meta.get("replication"), dict) or not all(k in meta["replication"] for k in ("independent", "failed")):
        errors.append("replication.independent and replication.failed are required")
    publication = meta.get("publication")
    if not isinstance(publication, dict) or publication.get("status") not in PUBLICATION_STATES:
        errors.append("publication.status must be draft, candidate, or publishable")
    if re.search(r"[A-Za-z]:[\\/]", str(meta.get("source_episode", ""))):
        errors.append("source_episode must be an opaque public identifier, not a local path")
    sections = set(re.findall(r"^##\s+(.+?)\s*$", body, flags=re.MULTILINE))
    required_sections = set(COMMON_SECTIONS)
    if meta.get("type") == "Finding":
        required_sections.add("Results")
    missing_sections = sorted(required_sections - sections)
    if missing_sections:
        errors.append(f"missing sections: {', '.join(missing_sections)}")
    if meta.get("type") == "Protocol" and re.search(r"\b(confirmatory result|we found|demonstrates an effect)\b", body, flags=re.IGNORECASE):
        errors.append("protocol contains result-like claim requiring manual review")
    return [f"{path}: {error}" for error in errors]


def validate_tree(root: Path) -> int:
    notes = sorted(root.glob("research/*/index.md"))
    errors = [error for note in notes for error in validate_note(note)]
    if errors:
        print("Publication validation failed:")
        print("\n".join(errors))
        return 1
    print(f"Publication validation passed: {len(notes)} Research Notes")
    return 0


def project(source: Path, output: Path, note_type: str) -> int:
    text = source.read_text(encoding="utf-8-sig")
    meta, _ = frontmatter(text)
    source_id = meta.get("episode_id") or meta.get("id")
    domain = str(meta.get("domain", "UNKNOWN")).upper().replace(" ", "-")
    if not source_id:
        raise SystemExit("source Episode lacks episode_id/id")
    digest = hashlib.sha256(source.read_bytes()).hexdigest()
    public_id = f"{domain}-{source_id}"
    skeleton = f'''---
id: {public_id}
title: TODO
date: {meta.get("date") or meta.get("created_at") or "TODO"}
domain: {meta.get("domain", "UNKNOWN")}
type: {note_type}
status: Draft
evidence:
  class: TODO
  source: TODO
review:
  peer_reviewed: false
  human_reviewed: false
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
    args = parser.parse_args()
    if args.command == "validate":
        return validate_tree(Path(args.content))
    return project(Path(args.source), Path(args.output), args.type)


if __name__ == "__main__":
    raise SystemExit(main())

