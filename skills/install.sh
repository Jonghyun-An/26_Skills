#!/usr/bin/env bash
set -euo pipefail

script_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)"
repo_root="$(cd -- "$script_dir/.." && pwd -P)"
validator="$repo_root/scripts/validate_skills.py"

usage() {
  cat <<'EOF'
Usage:
  ./skills/install.sh --list
  ./skills/install.sh <skill-name> [<skill-name> ...] [options]
  ./skills/install.sh --all [options]

Options:
  --target DIR  Install into DIR instead of ${CODEX_HOME}/skills or ${HOME}/.codex/skills
  --verify      Compare source and installed copies without changing files
  --replace     Back up and replace a differing installed copy
  --all         Select every tracked skill
  --list        List tracked skills
  -h, --help    Show this help
EOF
}

die() {
  printf 'ERROR: %s\n' "$*" >&2
  exit 1
}

list_skills() {
  local found=0
  local path
  while IFS= read -r path; do
    found=1
    basename -- "$path"
  done < <(find "$script_dir" -mindepth 1 -maxdepth 1 -type d ! -name '.*' -exec test -f '{}/SKILL.md' ';' -print | sort)
  if [[ "$found" -eq 0 ]]; then
    printf 'No skills found.\n'
  fi
}

canonicalize() {
  python3 - "$1" <<'PY'
import os
import sys
print(os.path.realpath(os.path.abspath(sys.argv[1])))
PY
}

target=""
verify=0
replace=0
select_all=0
list_only=0
declare -a names=()

while (($#)); do
  case "$1" in
    --target)
      (($# >= 2)) || die "--target requires a directory"
      target="$2"
      shift 2
      ;;
    --verify)
      verify=1
      shift
      ;;
    --replace)
      replace=1
      shift
      ;;
    --all)
      select_all=1
      shift
      ;;
    --list)
      list_only=1
      shift
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    --*)
      die "unknown option: $1"
      ;;
    *)
      names+=("$1")
      shift
      ;;
  esac
done

if [[ "$list_only" -eq 1 ]]; then
  [[ "$select_all" -eq 0 && "${#names[@]}" -eq 0 && "$verify" -eq 0 && "$replace" -eq 0 && -z "$target" ]] || die "--list cannot be combined with install options"
  list_skills
  exit 0
fi

[[ "$select_all" -eq 0 || "${#names[@]}" -eq 0 ]] || die "use skill names or --all, not both"
[[ "$verify" -eq 0 || "$replace" -eq 0 ]] || die "--verify and --replace are mutually exclusive"

if [[ "$select_all" -eq 1 ]]; then
  mapfile -t names < <(list_skills | grep -v '^No skills found\.$')
fi
[[ "${#names[@]}" -gt 0 ]] || die "select at least one skill or use --all"

if [[ -z "$target" ]]; then
  if [[ -n "${CODEX_HOME:-}" ]]; then
    target="$CODEX_HOME/skills"
  elif [[ -n "${HOME:-}" ]]; then
    target="$HOME/.codex/skills"
  else
    die "HOME and CODEX_HOME are unset; provide --target"
  fi
fi

target="$(canonicalize "$target")"
repo_root="$(canonicalize "$repo_root")"
[[ "$target" != "/" ]] || die "refusing filesystem root as target"
[[ "$target" != "$repo_root" && "$target" != "$repo_root/"* ]] || die "refusing repository source tree as target"

if [[ "$verify" -eq 1 ]]; then
  [[ -d "$target" ]] || die "verification target does not exist: $target"
else
  mkdir -p -- "$target"
fi

declare -A seen=()
for name in "${names[@]}"; do
  [[ "$name" =~ ^[a-z0-9]+(-[a-z0-9]+)*$ ]] || die "invalid skill name: $name"
  [[ -z "${seen[$name]:-}" ]] || die "duplicate skill name: $name"
  seen[$name]=1

  source_dir="$script_dir/$name"
  destination="$target/$name"
  [[ -f "$source_dir/SKILL.md" ]] || die "unknown skill: $name"
  python3 "$validator" "$source_dir"

  if [[ "$verify" -eq 1 ]]; then
    [[ -d "$destination" ]] || die "not installed: $destination"
    diff -qr -- "$source_dir" "$destination" >/dev/null || die "installed copy differs: $destination"
    printf 'VERIFIED %s\n' "$destination"
    continue
  fi

  if [[ -d "$destination" ]] && diff -qr -- "$source_dir" "$destination" >/dev/null; then
    printf 'UNCHANGED %s\n' "$destination"
    continue
  fi
  if [[ -e "$destination" && "$replace" -ne 1 ]]; then
    die "destination differs; rerun with --replace: $destination"
  fi

  stage_root="$(mktemp -d "$target/.skill-install.XXXXXX")"
  stage_dir="$stage_root/$name"
  cleanup_stage() {
    rm -rf -- "$stage_root"
  }
  trap cleanup_stage EXIT
  cp -a -- "$source_dir" "$stage_dir"
  diff -qr -- "$source_dir" "$stage_dir" >/dev/null || die "staged copy verification failed: $name"

  if [[ -e "$destination" ]]; then
    timestamp="$(date +%Y%m%d-%H%M%S)"
    backup="$destination.backup-$timestamp"
    [[ ! -e "$backup" ]] || backup="$backup-$$"
    mv -- "$destination" "$backup"
    if ! mv -- "$stage_dir" "$destination"; then
      mv -- "$backup" "$destination"
      die "replacement failed; original restored: $destination"
    fi
    printf 'REPLACED %s\n' "$destination"
    printf 'BACKUP %s\n' "$backup"
  else
    mv -- "$stage_dir" "$destination"
    printf 'INSTALLED %s\n' "$destination"
  fi

  rm -rf -- "$stage_root"
  trap - EXIT
done

