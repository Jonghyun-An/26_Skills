# 26_Skills

Reusable Codex skills live here as canonical, versioned source packages. Each folder under `skills/` can be reviewed, installed locally, or installed from this GitHub repository without coupling it to another workspace.

## Layout

```text
26_Skills/
├── AGENTS.md
├── README.md
├── scripts/
│   └── validate_skills.py
└── skills/
    ├── README.md
    ├── install.sh
    └── <skill-name>/
        ├── SKILL.md
        ├── agents/openai.yaml
        └── references, scripts, assets (optional)
```

## Contract

- One folder is one independently installable skill.
- The repository copy is canonical; installed copies are disposable projections.
- Installation and validation are offline and dependency-free.
- Existing differing installations are never overwritten unless `--replace` is explicit.
- Secrets, local Codex state, caches, backups, and generated outputs stay untracked.

## Available skills

| Skill | Purpose |
|---|---|
| [`author-manual-dp-blueprints`](skills/author-manual-dp-blueprints/SKILL.md) | Derive narrow architecture decision points and hand-author mutually exclusive SVG candidates, comparisons, records, and sequential gates. |

## Install

From this checkout:

```bash
./skills/install.sh author-manual-dp-blueprints
./skills/install.sh author-manual-dp-blueprints --verify
```

Into a specific project-local Codex directory:

```bash
./skills/install.sh author-manual-dp-blueprints --target /path/to/project/.codex/skills
```

From GitHub, ask Codex to use `$skill-installer` with repository `Jonghyun-An/26_Skills` and path `skills/author-manual-dp-blueprints`. The package layout is compatible with the official GitHub skill installer.

See [`skills/README.md`](skills/README.md) for installation and contribution commands.
