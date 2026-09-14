#!/usr/bin/env python3
"""Render every mutable public summary from one program-current source.

The Program current state is the canonical public claim. Home cards, the
Research index, llms.txt, Program current-state/history blocks, and the all-note
index are derived views. ``--check`` fails when a committed view has drifted or
when a newer manifest entry exists than the declared current Research Note.
"""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path

import yaml

from publish_episode import frontmatter


ROOT = Path(__file__).resolve().parent.parent
START = "<!-- GENERATED: {name}:START -->"
END = "<!-- GENERATED: {name}:END -->"


@dataclass(frozen=True)
class Note:
    research_id: str
    slug: str
    date: str
    note_type: str
    title: dict[str, str]

    @property
    def episode(self) -> str:
        match = re.search(r"EP-\d+$", self.research_id)
        return match.group(0) if match else self.research_id


def load_yaml(path: Path) -> dict:
    data = yaml.safe_load(path.read_text(encoding="utf-8-sig"))
    if not isinstance(data, dict):
        raise ValueError(f"{path}: expected a YAML mapping")
    return data


def load_notes(manifest: dict) -> tuple[list[Note], dict[str, Note]]:
    notes: list[Note] = []
    by_id: dict[str, Note] = {}
    for entry in manifest.get("notes", []):
        research_id = str(entry["research_id"])
        localized: dict[str, str] = {}
        dates: set[str] = set()
        slugs: set[str] = set()
        for lang, rel_path in entry["views"].items():
            path = ROOT / str(rel_path)
            meta, _ = frontmatter(path.read_text(encoding="utf-8-sig"))
            localized[lang] = str(meta["title"])
            dates.add(str(meta["date"]))
            slugs.add(path.parent.name)
        if len(dates) != 1 or len(slugs) != 1:
            raise ValueError(f"{research_id}: language views disagree on date or slug")
        note = Note(
            research_id=research_id,
            slug=slugs.pop(),
            date=dates.pop(),
            note_type=str(entry["type"]),
            title=localized,
        )
        notes.append(note)
        by_id[research_id] = note
    return notes, by_id


def marker_pattern(name: str) -> re.Pattern[str]:
    return re.compile(
        re.escape(START.format(name=name)) + r".*?" + re.escape(END.format(name=name)),
        flags=re.DOTALL,
    )


def generated_block(name: str, body: str) -> str:
    return f"{START.format(name=name)}\n{body.rstrip()}\n{END.format(name=name)}"


def replace_block(path: Path, name: str, body: str, check: bool, stale: list[str]) -> None:
    text = path.read_text(encoding="utf-8-sig")
    pattern = marker_pattern(name)
    if not pattern.search(text):
        raise ValueError(f"{path.relative_to(ROOT)}: missing generated block {name!r}")
    updated = pattern.sub(lambda _: generated_block(name, body), text, count=1)
    if updated == text:
        return
    stale.append(str(path.relative_to(ROOT)))
    if not check:
        path.write_text(updated, encoding="utf-8", newline="\n")


def note_url(site: str, lang: str, note: Note, absolute: bool = False) -> str:
    path = f"/{lang}/research/{note.slug}/"
    return f"{site}{path}" if absolute else path


def program_url(site: str, lang: str, program_id: str, absolute: bool = False) -> str:
    path = f"/{lang}/programs/{program_id}/"
    return f"{site}{path}" if absolute else path


def render_program_current(program: dict, lang: str, note: Note) -> str:
    loc = program[lang]
    heading = "現在の公開結論" if lang == "ja" else "Current public state"
    boundary = "**証拠の境界：**" if lang == "ja" else "**Evidence boundary:**"
    link = (
        f"現在のResearch Note（{note.episode}）を読む →"
        if lang == "ja"
        else f"Read the current Research Note ({note.episode}) →"
    )
    return (
        f"## {heading}\n\n{loc['claim']}\n\n{boundary} {loc['evidence_boundary']}\n\n"
        f"**[{link}]({note_url('', lang, note)})**"
    )


def render_program_history(program: dict, lang: str, notes: list[Note], current: Note) -> str:
    heading = "公開中のResearch Note" if lang == "ja" else "Published Research Notes"
    lines = [f"## {heading}", ""]
    for index, note in enumerate(notes, start=1):
        label = f"{note.episode} — {note.title[lang]}"
        link = f"[[{lang}/research/{note.slug}/index|{label}]]"
        if note == current:
            latest = "最新" if lang == "ja" else "latest"
            link = f"**{link}（{latest}）**" if lang == "ja" else f"**{link} ({latest})**"
        lines.append(f"{index}. {link}")
    return "\n".join(lines)


def render_home(programs: list[dict], lang: str, by_id: dict[str, Note]) -> str:
    cards: list[str] = ['<div class="program-index">']
    for program in programs:
        loc = program[lang]
        note = by_id[program["current_research_id"]]
        overview = "研究概要" if lang == "ja" else "Program overview"
        latest = "最新Note" if lang == "ja" else "Current Note"
        cards.extend(
            [
                '  <article class="program-row">',
                "    <div>",
                f"      <h3>{loc['title']}</h3>",
                f"      <p>{loc['home_summary']}</p>",
                "    </div>",
                f'    <nav aria-label="{loc["title"]}">',
                f'      <a href="/{lang}/programs/{program["id"]}/">{overview}</a>',
                f'      <a href="{note_url("", lang, note)}">{latest}</a>',
                "    </nav>",
                "  </article>",
            ]
        )
    cards.append("</div>")
    return "\n".join(cards)


def render_research_index(programs: list[dict], lang: str, by_id: dict[str, Note]) -> str:
    sections: list[str] = []
    for program in programs:
        loc = program[lang]
        note = by_id[program["current_research_id"]]
        if lang == "ja":
            sections.extend(
                [
                    f"## {loc['title']}",
                    "",
                    f"**テーマ：** {loc['question']}",
                    "",
                    f"**現在地：** {loc['claim']}",
                    "",
                    f"**証拠の境界：** {loc['evidence_boundary']}",
                    "",
                    f"**[現在のResearch Note（{note.episode}）→]({note_url('', lang, note)})** — {note.note_type}",
                    "",
                    f"[研究の現在地と更新履歴を見る →]({program_url('', lang, program['id'])})",
                    "",
                ]
            )
        else:
            sections.extend(
                [
                    f"## {loc['title']}",
                    "",
                    f"**Question:** {loc['question']}",
                    "",
                    f"**Current state:** {loc['claim']}",
                    "",
                    f"**Evidence boundary:** {loc['evidence_boundary']}",
                    "",
                    f"**[Read the current Research Note ({note.episode}) →]({note_url('', lang, note)})** — {note.note_type}",
                    "",
                    f"[See the current state and revision history →]({program_url('', lang, program['id'])})",
                    "",
                ]
            )
    all_notes = (
        "[公開中のResearch Noteを時系列で見る →](/ja/research-notes/)"
        if lang == "ja"
        else "[Browse all published Research Notes by date →](/en/research-notes/)"
    )
    sections.append(all_notes)
    return "\n".join(sections)


def render_llms(programs: list[dict], notes: list[Note], by_id: dict[str, Note], site: str) -> str:
    lines = ["## Research areas", ""]
    assigned: set[str] = set()
    for program in programs:
        current = by_id[program["current_research_id"]]
        program_notes = [n for n in notes if n.research_id.startswith(program["research_id_prefix"])]
        assigned.update(n.research_id for n in program_notes)
        lines.extend(
            [
                f"### {program['en']['title']}",
                "",
                "Program overview:",
                f"- English: {program_url(site, 'en', program['id'], absolute=True)}",
                f"- Japanese: {program_url(site, 'ja', program['id'], absolute=True)}",
                "",
                f"Question: {program['en']['question']}",
                "",
                f"Current claim ({current.episode}): {program['en']['claim']}",
                "",
                f"Evidence boundary: {program['en']['evidence_boundary']}",
                "",
                "Published Research Notes:",
            ]
        )
        for note in program_notes:
            marker = " — CURRENT" if note == current else ""
            lines.extend(
                [
                    f"- {note.research_id} — {note.title['en']} ({note.note_type}){marker}",
                    f"  - English: {note_url(site, 'en', note, absolute=True)}",
                    f"  - Japanese: {note_url(site, 'ja', note, absolute=True)}",
                ]
            )
        lines.append("")

    unassigned = [n for n in notes if n.research_id not in assigned]
    if unassigned:
        lines.extend(["### Research instruments and other records", ""])
        for note in unassigned:
            lines.extend(
                [
                    f"- {note.research_id} — {note.title['en']} ({note.note_type})",
                    f"  - English: {note_url(site, 'en', note, absolute=True)}",
                    f"  - Japanese: {note_url(site, 'ja', note, absolute=True)}",
                ]
            )
        lines.append("")
    return "\n".join(lines)


def render_all_notes(lang: str, notes: list[Note]) -> str:
    if lang == "ja":
        title = "研究ログ"
        description = "公開中のResearch Noteを新しい順にたどる一覧。"
        intro = "ここは履歴の入口です。現在の結論を知りたい場合は、先に[研究分野ごとの現在地](/ja/research/)を読んでください。"
    else:
        title = "Research log"
        description = "All published Research Notes in reverse chronological order."
        intro = "This is the historical log. For current claims, start with the [research-area index](/en/research/)."
    ordered = sorted(enumerate(notes), key=lambda pair: (pair[1].date, pair[0]), reverse=True)
    lines = ["---", f"title: {title}", f"description: {description}", f"lang: {lang}", "---", "", intro, ""]
    current_date = None
    for _, note in ordered:
        if note.date != current_date:
            current_date = note.date
            lines.extend([f"## {current_date}", ""])
        lines.append(
            f"- **{note.research_id}** · {note.note_type} — "
            f"[{note.title[lang]}]({note_url('', lang, note)})"
        )
    lines.append("")
    return "\n".join(lines)


def validate_programs(programs: list[dict], notes: list[Note], by_id: dict[str, Note]) -> None:
    seen: set[str] = set()
    for program in programs:
        program_id = str(program["id"])
        if program_id in seen:
            raise ValueError(f"duplicate program id: {program_id}")
        seen.add(program_id)
        prefix = str(program["research_id_prefix"])
        matching = [n for n in notes if n.research_id.startswith(prefix)]
        if not matching:
            raise ValueError(f"{program_id}: no manifest notes match {prefix!r}")
        current_id = str(program["current_research_id"])
        if current_id not in by_id:
            raise ValueError(f"{program_id}: current note {current_id} is absent from manifest")
        if matching[-1].research_id != current_id:
            raise ValueError(
                f"{program_id}: current note is {current_id}, but newest matching manifest entry is "
                f"{matching[-1].research_id}"
            )
        for lang in ("ja", "en"):
            missing = {"title", "home_summary", "question", "claim", "evidence_boundary"} - set(program[lang])
            if missing:
                raise ValueError(f"{program_id}/{lang}: missing {sorted(missing)}")


def sync(check: bool) -> int:
    state = load_yaml(ROOT / "program-current.yaml")
    manifest = load_yaml(ROOT / "publication-manifest.yaml")
    programs = state.get("programs")
    if not isinstance(programs, list):
        raise ValueError("program-current.yaml: programs must be a list")
    notes, by_id = load_notes(manifest)
    validate_programs(programs, notes, by_id)
    stale: list[str] = []

    for lang in ("ja", "en"):
        replace_block(ROOT / "content" / lang / "index.md", "program-cards", render_home(programs, lang, by_id), check, stale)
        replace_block(ROOT / "content" / lang / "research" / "index.md", "research-current", render_research_index(programs, lang, by_id), check, stale)
        for program in programs:
            note = by_id[program["current_research_id"]]
            program_notes = [n for n in notes if n.research_id.startswith(program["research_id_prefix"])]
            path = ROOT / "content" / lang / "programs" / program["id"] / "index.md"
            replace_block(path, "program-current", render_program_current(program, lang, note), check, stale)
            replace_block(path, "program-history", render_program_history(program, lang, program_notes, note), check, stale)
        log_path = ROOT / "content" / lang / "research-notes" / "index.md"
        expected = render_all_notes(lang, notes)
        actual = log_path.read_text(encoding="utf-8-sig") if log_path.exists() else ""
        if actual != expected:
            stale.append(str(log_path.relative_to(ROOT)))
            if not check:
                log_path.parent.mkdir(parents=True, exist_ok=True)
                log_path.write_text(expected, encoding="utf-8", newline="\n")

    replace_block(
        ROOT / "quartz" / "static" / "llms.txt",
        "research-current",
        render_llms(programs, notes, by_id, str(state["site_url"]).rstrip("/")),
        check,
        stale,
    )

    if stale and check:
        print("Derived current-state views are stale:")
        print("\n".join(f"- {path}" for path in sorted(set(stale))))
        print("Run: python scripts/sync_current_state.py")
        return 1
    action = "checked" if check else "updated"
    print(f"Current-state views {action}: {len(set(stale))} file(s) changed")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="fail instead of writing when a derived view is stale")
    args = parser.parse_args()
    try:
        return sync(args.check)
    except (KeyError, TypeError, ValueError, yaml.YAMLError) as exc:
        print(f"Current-state sync failed: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
