#!/usr/bin/env python3
"""npm-style version bump + CHANGELOG sync for the cgz marketplace.

Usage:
    python scripts/bump.py <plugin> --patch|--minor|--major --note "..."
    python scripts/bump.py --release
    python scripts/bump.py --status

See CONTRIBUTING.md `## 版本与发布（Releasing）` for the full flow.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MARKETPLACE = ROOT / ".claude-plugin" / "marketplace.json"
CHANGELOG = ROOT / "CHANGELOG.md"

KIND_RANK = {"patch": 0, "minor": 1, "major": 2}
UNRELEASED_HEADING = "## [Unreleased]"
UNRELEASED_PLACEHOLDER = (
    "<!-- 下一版的改动写这里。release 时移到新版本号下，并补 [Unreleased] 空段。 -->"
)


def parse_version(v: str) -> tuple[int, int, int]:
    parts = v.split(".")
    if len(parts) != 3 or not all(p.isdigit() for p in parts):
        raise ValueError(f"Invalid SemVer: {v}")
    return int(parts[0]), int(parts[1]), int(parts[2])


def format_version(t: tuple[int, int, int]) -> str:
    return ".".join(str(x) for x in t)


def bump_version(v: str, kind: str) -> str:
    major, minor, patch = parse_version(v)
    if kind == "major":
        return format_version((major + 1, 0, 0))
    if kind == "minor":
        return format_version((major, minor + 1, 0))
    if kind == "patch":
        return format_version((major, minor, patch + 1))
    raise ValueError(f"Unknown bump kind: {kind}")


def semver_lt(a: str, b: str) -> bool:
    return parse_version(a) < parse_version(b)


def load_marketplace() -> dict:
    return json.loads(MARKETPLACE.read_text(encoding="utf-8"))


INLINE_ARRAY_KEYS = ("keywords", "skills")


def _compact_inline_arrays(text: str) -> str:
    """Collapse short string arrays back to a single line.

    json.dumps(indent=2) expands every array to multi-line. The original
    marketplace.json keeps `keywords` and `skills` inline; preserve that
    so the diff for a version bump stays surgical.
    """
    for key in INLINE_ARRAY_KEYS:
        pattern = re.compile(
            rf'"{re.escape(key)}":\s*\[\n((?:[ \t]+"[^"]*",?\n)+)[ \t]*\]'
        )

        def collapse(match: re.Match) -> str:
            items = re.findall(r'"[^"]*"', match.group(1))
            return f'"{key}": [{", ".join(items)}]'

        text = pattern.sub(collapse, text)
    return text


def save_marketplace(data: dict) -> None:
    text = json.dumps(data, ensure_ascii=False, indent=2)
    text = _compact_inline_arrays(text)
    MARKETPLACE.write_text(text + "\n", encoding="utf-8")


def find_plugin(data: dict, name: str) -> dict:
    for p in data["plugins"]:
        if p["name"] == name:
            return p
    available = ", ".join(p["name"] for p in data["plugins"])
    sys.exit(f"Plugin not found: {name}\nAvailable: {available}")


def last_released_version(changelog: str) -> str:
    matches = re.findall(r"^## \[(\d+\.\d+\.\d+)\]", changelog, re.MULTILINE)
    return matches[0] if matches else "0.0.0"


def find_unreleased_bounds(lines: list[str]) -> tuple[int, int]:
    start = -1
    for i, line in enumerate(lines):
        if line.strip() == UNRELEASED_HEADING:
            start = i
            break
    if start < 0:
        sys.exit("CHANGELOG.md missing `## [Unreleased]` heading.")
    end = len(lines)
    for i in range(start + 1, len(lines)):
        if lines[i].startswith("## "):
            end = i
            break
        if lines[i].rstrip() == "---":
            for j in range(i + 1, min(i + 6, len(lines))):
                if lines[j].startswith("## "):
                    end = i
                    break
            if end != len(lines):
                break
    return start, end


def append_unreleased_bullet(changelog: str, bullet: str) -> str:
    lines = changelog.split("\n")
    start, end = find_unreleased_bounds(lines)
    insert_at = end
    while insert_at > start + 1 and not lines[insert_at - 1].strip():
        insert_at -= 1
    prefix = lines[:insert_at]
    suffix = lines[insert_at:]
    new_block: list[str] = []
    if prefix and prefix[-1].strip() and not prefix[-1].lstrip().startswith("-"):
        new_block.append("")
    new_block.append(bullet)
    return "\n".join(prefix + new_block + suffix)


def parse_unreleased_bullets(changelog: str) -> list[dict]:
    lines = changelog.split("\n")
    start, end = find_unreleased_bounds(lines)
    pattern = re.compile(
        r"^-\s+\*\*([\w-]+)\*\*\s+`([\d.]+)\s*(?:→|->)\s*([\d.]+)`\s*\((patch|minor|major)\)\s*[—\-]+\s*(.+)$"
    )
    bumps: list[dict] = []
    for line in lines[start + 1 : end]:
        m = pattern.match(line)
        if m:
            bumps.append(
                {
                    "plugin": m.group(1),
                    "old": m.group(2),
                    "new": m.group(3),
                    "kind": m.group(4),
                    "note": m.group(5).strip(),
                }
            )
    return bumps


def extract_unreleased_body(lines: list[str], start: int, end: int) -> list[str]:
    body: list[str] = []
    in_block_comment = False
    for line in lines[start + 1 : end]:
        stripped = line.strip()
        if stripped == UNRELEASED_PLACEHOLDER:
            continue
        if in_block_comment:
            if stripped.endswith("-->"):
                in_block_comment = False
            continue
        if stripped.startswith("<!--") and stripped.endswith("-->"):
            continue
        if stripped.startswith("<!--"):
            in_block_comment = True
            continue
        body.append(line)
    while body and not body[0].strip():
        body.pop(0)
    while body and not body[-1].strip():
        body.pop()
    return body


def cmd_bump(args: argparse.Namespace) -> None:
    data = load_marketplace()
    plugin = find_plugin(data, args.plugin)
    old_version = plugin["version"]
    new_version = bump_version(old_version, args.kind)
    plugin["version"] = new_version

    changelog = CHANGELOG.read_text(encoding="utf-8")
    last_released = last_released_version(changelog)
    target_marketplace = bump_version(last_released, args.kind)
    if semver_lt(data["metadata"]["version"], target_marketplace):
        data["metadata"]["version"] = target_marketplace

    save_marketplace(data)

    bullet = f"- **{args.plugin}** `{old_version} → {new_version}` ({args.kind}) — {args.note}"
    new_changelog = append_unreleased_bullet(changelog, bullet)
    CHANGELOG.write_text(new_changelog, encoding="utf-8")

    print(f"Bumped {args.plugin}: {old_version} → {new_version} ({args.kind})")
    print(f"Marketplace metadata.version: {data['metadata']['version']}")
    print()
    print("CHANGELOG: bullet appended under [Unreleased].")
    print()
    print("Next:")
    print("  git add .claude-plugin/marketplace.json CHANGELOG.md")
    print(
        f"  git commit -m \"bump: {args.plugin} {args.kind} ({old_version} → {new_version})\""
    )


def cmd_release(args: argparse.Namespace) -> None:
    data = load_marketplace()
    changelog = CHANGELOG.read_text(encoding="utf-8")
    bumps = parse_unreleased_bullets(changelog)
    if not bumps:
        sys.exit("Nothing in [Unreleased]. Bump at least one plugin first.")

    new_version = data["metadata"]["version"]
    today = date.today().isoformat()

    lines = changelog.split("\n")
    start, end = find_unreleased_bounds(lines)
    body = extract_unreleased_body(lines, start, end)

    new_unreleased_section = [
        UNRELEASED_HEADING,
        "",
        UNRELEASED_PLACEHOLDER,
        "",
        "---",
        "",
    ]
    new_version_section = [f"## [{new_version}] — {today}", ""]
    new_version_section.extend(body)
    if new_version_section[-1].strip():
        new_version_section.append("")

    new_lines = lines[:start] + new_unreleased_section + new_version_section + lines[end:]
    CHANGELOG.write_text("\n".join(new_lines), encoding="utf-8")

    print(f"Released v{new_version} ({today}).")
    print(f"Bumps in this release: {len(bumps)}")
    for b in bumps:
        print(
            f"  - {b['plugin']:25s} {b['old']} → {b['new']:8s} ({b['kind']}) — {b['note']}"
        )
    print()
    print("Next:")
    print("  git add CHANGELOG.md .claude-plugin/marketplace.json")
    print(f'  git commit -m "release: v{new_version}"')
    print(f"  git tag v{new_version}")
    print("  git push origin main --tags")


def cmd_status(args: argparse.Namespace) -> None:
    data = load_marketplace()
    changelog = CHANGELOG.read_text(encoding="utf-8")
    bumps = parse_unreleased_bullets(changelog)
    last_released = last_released_version(changelog)

    print(
        f"Marketplace: {data['metadata']['version']} (last released: {last_released})"
    )
    print()
    print("Plugins:")
    for p in data["plugins"]:
        print(f"  {p['name']:25s} {p['version']}")
    print()
    print(f"Pending bumps in [Unreleased]: {len(bumps)}")
    for b in bumps:
        print(
            f"  - {b['plugin']:25s} {b['old']} → {b['new']:8s} ({b['kind']}) — {b['note']}"
        )


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Bump plugin versions and sync CHANGELOG (npm-style).",
        epilog=(
            "Examples:\n"
            "  python scripts/bump.py focused-discussion --minor --note 'Added X'\n"
            "  python scripts/bump.py cgz-init --patch --note 'Fix scan order'\n"
            "  python scripts/bump.py --release\n"
            "  python scripts/bump.py --status"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("plugin", nargs="?", help="Plugin name (must exist in marketplace.json)")
    parser.add_argument("--patch", action="store_const", dest="kind", const="patch")
    parser.add_argument("--minor", action="store_const", dest="kind", const="minor")
    parser.add_argument("--major", action="store_const", dest="kind", const="major")
    parser.add_argument("--note", help="One-line note for the CHANGELOG entry")
    parser.add_argument("--release", action="store_true", help="Cut [Unreleased] into a new version section")
    parser.add_argument("--status", action="store_true", help="Show current versions and pending bumps")
    args = parser.parse_args()

    if args.release:
        cmd_release(args)
        return
    if args.status:
        cmd_status(args)
        return
    if args.plugin and args.kind:
        if not args.note:
            parser.error("--note is required when bumping a plugin")
        cmd_bump(args)
        return
    parser.print_help()
    sys.exit(1)


if __name__ == "__main__":
    main()
