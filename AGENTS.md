# AGENTS.md — Canonical Skill Workspace

## Mission

This repository is the canonical, versioned source for reusable Codex skills. Keep each skill independently installable from its folder and keep repository tooling generic across all skills.

## Source layout

- `skills/<skill-name>/SKILL.md` is the required entrypoint for each skill.
- `skills/<skill-name>/agents/openai.yaml` contains optional UI metadata.
- `skills/<skill-name>/scripts/`, `references/`, and `assets/` are optional bundled resources.
- `skills/install.sh` installs or verifies one or all tracked skills.
- `scripts/validate_skills.py` validates repository skill packages without third-party dependencies.

Do not put a README or installation guide inside an individual skill folder. Repository-level usage belongs in `README.md` or `skills/README.md`.

## Change workflow

1. Add or update one skill folder.
2. Keep `SKILL.md` frontmatter limited to `name` and `description`.
3. Keep the folder name identical to the frontmatter `name`.
4. Update `agents/openai.yaml` when skill behavior or invocation changes.
5. Run repository validation and a clean local install/verify scenario.
6. Commit small, reviewable units with concise conventional messages.

## Safety and hygiene

- Treat this repository as source, never as an installation destination.
- Never commit `.codex/`, `.omx/`, virtual environments, caches, installer staging directories, backups, credentials, or generated artifacts.
- Installer replacement must be explicit and must preserve a recoverable timestamped backup.
- Canonicalize target paths before safety checks; reject filesystem root and the repository source tree as targets.
- Do not add network dependencies to local validation or installation.

## Required verification

Before committing or pushing, run:

```bash
python3 scripts/validate_skills.py
bash -n skills/install.sh
git diff --check
git status --short --branch
git remote -v
```

For a changed skill, also exercise new install, idempotent install, drift refusal, replacement/backup, and `--verify` in a temporary target.

