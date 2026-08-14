#!/usr/bin/env python3
"""Validate canonical Codex skill packages without third-party dependencies."""

from __future__ import annotations

import argparse
import ast
import re
import sys
from pathlib import Path


NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
LINK_RE = re.compile(r"\[[^]]+\]\(([^)]+)\)")
STRING_FIELD_RE = re.compile(r'^\s+[a-z_]+:\s+".*"\s*$')


def parse_scalar(raw: str) -> str:
    value = raw.strip()
    if not value:
        return ""
    if value[0] in {'"', "'"}:
        parsed = ast.literal_eval(value)
        if not isinstance(parsed, str):
            raise ValueError("frontmatter values must be strings")
        return parsed
    return value


def parse_frontmatter(skill_md: Path) -> dict[str, str]:
    lines = skill_md.read_text(encoding="utf-8").splitlines()
    if not lines or lines[0] != "---":
        raise ValueError("SKILL.md must start with YAML frontmatter")
    try:
        end = lines.index("---", 1)
    except ValueError as exc:
        raise ValueError("SKILL.md frontmatter is not closed") from exc

    fields: dict[str, str] = {}
    for line in lines[1:end]:
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if ":" not in line or line[:1].isspace():
            raise ValueError(f"unsupported frontmatter line: {line!r}")
        key, raw = line.split(":", 1)
        key = key.strip()
        if key in fields:
            raise ValueError(f"duplicate frontmatter key: {key}")
        fields[key] = parse_scalar(raw)

    if set(fields) != {"name", "description"}:
        raise ValueError("frontmatter must contain only name and description")
    return fields


def validate_links(skill_dir: Path) -> list[str]:
    errors: list[str] = []
    root = skill_dir.resolve()
    for markdown in sorted(skill_dir.rglob("*.md")):
        for target in LINK_RE.findall(markdown.read_text(encoding="utf-8")):
            if "://" in target or target.startswith("#"):
                continue
            clean_target = target.split("#", 1)[0]
            resolved = (markdown.parent / clean_target).resolve()
            if not resolved.is_relative_to(root):
                errors.append(f"{markdown}: link leaves the skill folder: {target}")
            elif not resolved.exists():
                errors.append(f"{markdown}: missing link target: {target}")
    return errors


def validate_openai_yaml(skill_dir: Path, name: str) -> list[str]:
    path = skill_dir / "agents" / "openai.yaml"
    if not path.exists():
        return []

    errors: list[str] = []
    lines = path.read_text(encoding="utf-8").splitlines()
    if not lines or lines[0] != "interface:":
        errors.append(f"{path}: expected interface as the first top-level key")
        return errors

    fields: dict[str, str] = {}
    for line in lines[1:]:
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if not STRING_FIELD_RE.match(line):
            errors.append(f"{path}: interface string values must be quoted: {line!r}")
            continue
        key, raw = line.strip().split(":", 1)
        fields[key] = parse_scalar(raw)

    for required in ("display_name", "short_description", "default_prompt"):
        if not fields.get(required):
            errors.append(f"{path}: missing interface.{required}")
    short = fields.get("short_description", "")
    if short and not 25 <= len(short) <= 64:
        errors.append(f"{path}: short_description must be 25-64 characters")
    prompt = fields.get("default_prompt", "")
    if prompt and f"${name}" not in prompt:
        errors.append(f"{path}: default_prompt must mention ${name}")
    return errors


def validate_skill(skill_dir: Path) -> list[str]:
    errors: list[str] = []
    if not skill_dir.is_dir():
        return [f"{skill_dir}: not a directory"]
    if skill_dir.is_symlink():
        errors.append(f"{skill_dir}: skill directories must not be symlinks")

    skill_md = skill_dir / "SKILL.md"
    if not skill_md.is_file():
        return [f"{skill_dir}: missing SKILL.md"]
    if (skill_dir / "README.md").exists():
        errors.append(f"{skill_dir}: README.md belongs at repository level")

    try:
        fields = parse_frontmatter(skill_md)
    except (ValueError, SyntaxError) as exc:
        return [f"{skill_md}: {exc}"]

    name = fields["name"]
    if not NAME_RE.fullmatch(name) or len(name) > 63:
        errors.append(f"{skill_md}: invalid skill name: {name!r}")
    if name != skill_dir.name:
        errors.append(f"{skill_md}: name must match folder {skill_dir.name!r}")
    if not fields["description"].strip():
        errors.append(f"{skill_md}: description must not be empty")
    if len(skill_md.read_text(encoding="utf-8").splitlines()) > 500:
        errors.append(f"{skill_md}: keep SKILL.md at or below 500 lines")

    for path in skill_dir.rglob("*"):
        if path.is_symlink():
            errors.append(f"{path}: bundled resources must not be symlinks")
        if path.name == "__pycache__" or path.suffix in {".pyc", ".pyo"}:
            errors.append(f"{path}: generated cache file is not allowed")

    errors.extend(validate_links(skill_dir))
    errors.extend(validate_openai_yaml(skill_dir, name))
    return errors


def discover(repo_root: Path) -> list[Path]:
    skills_root = repo_root / "skills"
    return sorted(
        path
        for path in skills_root.iterdir()
        if path.is_dir() and not path.name.startswith(".")
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("paths", nargs="*", type=Path, help="skill folders to validate")
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parent.parent
    skill_dirs = args.paths or discover(repo_root)
    if not skill_dirs:
        print("PASS no skill packages found")
        return 0

    failed = False
    for skill_dir in skill_dirs:
        errors = validate_skill(skill_dir)
        if errors:
            failed = True
            for error in errors:
                print(f"FAIL {error}", file=sys.stderr)
        else:
            print(f"PASS {skill_dir}")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())

