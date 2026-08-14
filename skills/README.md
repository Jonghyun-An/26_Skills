# Skill packages

Every direct child directory of `skills/` is a standalone Codex skill. A package requires `SKILL.md`; `agents/openai.yaml` and bundled `references/`, `scripts/`, or `assets/` are optional.

## Catalog

- [`author-manual-dp-blueprints`](author-manual-dp-blueprints/SKILL.md) — architecture authority axes, hand-authored A/B SVG blueprints, trade-off records, and sequential validation gates.

Repository tooling will support these operations:

```bash
./skills/install.sh --list
./skills/install.sh <skill-name>
./skills/install.sh <skill-name> --verify
./skills/install.sh --all
python3 scripts/validate_skills.py
```

Use `--target <skills-directory>` for a project-local installation. Without it, the installer targets `${CODEX_HOME}/skills` or falls back to `${HOME}/.codex/skills`.

The installer is idempotent for an identical copy. A differing destination is refused by default; `--replace` creates a sibling `.backup-YYYYMMDD-HHMMSS` before replacement. Use `--verify` for a read-only recursive comparison.

## Add a skill

1. Create `skills/<skill-name>/SKILL.md` with only `name` and `description` in YAML frontmatter.
2. Add `agents/openai.yaml` when UI metadata is useful.
3. Keep detailed optional material in one-level `references/`, reusable deterministic code in `scripts/`, and output resources in `assets/`.
4. Add the skill to the root README index.
5. Run repository validation and installer scenarios before committing.
