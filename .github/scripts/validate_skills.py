"""
Validate every skill under skills/ against the Agent Skills specification.

Reference: https://agentskills.io/specification

Checks per skill directory:
  - SKILL.md exists
  - YAML frontmatter present and parseable
  - name: required, 1-64 chars, lowercase a-z / 0-9 / hyphens, no leading/trailing
    hyphen, no consecutive hyphens, must equal parent directory name
  - description: required, 1-1024 chars
  - body length: warns if > 500 lines (spec recommendation)
  - reserved fields type-checked when present (license/compatibility/metadata)

Exit 0 if all skills valid, exit 1 otherwise.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

import yaml


SKILLS_DIR = Path("skills")
NAME_PATTERN = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
NAME_MAX = 64
DESCRIPTION_MAX = 1024
BODY_LINE_SOFT_LIMIT = 500
COMPATIBILITY_MAX = 500


def parse_frontmatter(text: str) -> tuple[dict, str] | None:
    if not text.startswith("---"):
        return None
    parts = text.split("---", 2)
    if len(parts) < 3:
        return None
    try:
        meta = yaml.safe_load(parts[1]) or {}
    except yaml.YAMLError:
        return None
    if not isinstance(meta, dict):
        return None
    return meta, parts[2]


def validate_skill(skill_dir: Path) -> list[str]:
    errors: list[str] = []
    skill_name = skill_dir.name
    skill_md = skill_dir / "SKILL.md"

    if not skill_md.exists():
        return [f"{skill_name}: missing SKILL.md"]

    parsed = parse_frontmatter(skill_md.read_text(encoding="utf-8"))
    if parsed is None:
        return [f"{skill_name}: missing or malformed YAML frontmatter"]
    meta, body = parsed

    # name
    name = meta.get("name")
    if not name:
        errors.append(f"{skill_name}: frontmatter 'name' is required")
    elif not isinstance(name, str):
        errors.append(f"{skill_name}: 'name' must be a string")
    else:
        if len(name) > NAME_MAX:
            errors.append(f"{skill_name}: 'name' longer than {NAME_MAX} chars")
        if not NAME_PATTERN.match(name):
            errors.append(
                f"{skill_name}: 'name' must be lowercase kebab-case "
                f"(a-z, 0-9, hyphens, no leading/trailing or consecutive hyphens). Got: {name!r}"
            )
        if name != skill_name:
            errors.append(
                f"{skill_name}: 'name' ({name!r}) must equal parent directory name ({skill_name!r})"
            )

    # description
    desc = meta.get("description")
    if not desc:
        errors.append(f"{skill_name}: frontmatter 'description' is required")
    elif not isinstance(desc, str):
        errors.append(f"{skill_name}: 'description' must be a string")
    elif len(desc) > DESCRIPTION_MAX:
        errors.append(
            f"{skill_name}: 'description' longer than {DESCRIPTION_MAX} chars (got {len(desc)})"
        )

    # optional but type-checked
    if "license" in meta and not isinstance(meta["license"], str):
        errors.append(f"{skill_name}: 'license' must be a string")
    if "compatibility" in meta:
        comp = meta["compatibility"]
        if not isinstance(comp, str):
            errors.append(f"{skill_name}: 'compatibility' must be a string")
        elif len(comp) > COMPATIBILITY_MAX:
            errors.append(
                f"{skill_name}: 'compatibility' longer than {COMPATIBILITY_MAX} chars"
            )
    if "metadata" in meta and not isinstance(meta["metadata"], dict):
        errors.append(f"{skill_name}: 'metadata' must be a mapping")

    # body length soft check
    body_lines = body.count("\n")
    if body_lines > BODY_LINE_SOFT_LIMIT:
        errors.append(
            f"{skill_name}: SKILL.md body has {body_lines} lines "
            f"(>{BODY_LINE_SOFT_LIMIT}). Split detail into references/ per spec."
        )

    return errors


def main() -> int:
    if not SKILLS_DIR.exists():
        print(f"ERROR: '{SKILLS_DIR}/' directory not found", file=sys.stderr)
        return 1

    skill_dirs = sorted(d for d in SKILLS_DIR.iterdir() if d.is_dir())
    if not skill_dirs:
        print(f"ERROR: no skills found under '{SKILLS_DIR}/'", file=sys.stderr)
        return 1

    all_errors: list[str] = []
    for skill_dir in skill_dirs:
        all_errors.extend(validate_skill(skill_dir))

    if all_errors:
        print("Validation failed:\n", file=sys.stderr)
        for err in all_errors:
            print(f"  - {err}", file=sys.stderr)
        return 1

    print(f"OK: {len(skill_dirs)} skill(s) valid")
    for d in skill_dirs:
        print(f"  - {d.name}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
