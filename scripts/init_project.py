"""Turn the template into a project: rename ``myproject`` everywhere, once.

Usage::

    python3 scripts/init_project.py <name> [--author "Your Name"]

``<name>`` is the Python package name: lowercase letters, digits and underscores. The script
rewrites every tracked text file, renames ``src/myproject`` and deletes itself.
"""

import argparse
import re
import subprocess
import sys
from pathlib import Path

PLACEHOLDER = "myproject"
NAME_RE = re.compile(r"[a-z][a-z0-9_]*")


def tracked_files(root: Path) -> list[Path]:
    out = subprocess.run(
        ["git", "ls-files"], cwd=root, check=True, capture_output=True, text=True
    ).stdout
    return [root / line for line in out.splitlines() if line]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n", 1)[0])
    parser.add_argument("name")
    parser.add_argument("--author")
    args = parser.parse_args()
    if not NAME_RE.fullmatch(args.name):
        print(f"{args.name!r}: use lowercase letters, digits and underscores", file=sys.stderr)
        return 2
    root = Path(__file__).resolve().parents[1]
    this = Path(__file__).resolve()
    for path in tracked_files(root):
        if path.resolve() == this or not path.is_file():
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        new = text.replace(PLACEHOLDER, args.name)
        if args.author:
            new = new.replace("Your Name", args.author)
        if new != text:
            path.write_text(new, encoding="utf-8")
    (root / "src" / PLACEHOLDER).rename(root / "src" / args.name)
    this.unlink()
    print(f"Renamed to {args.name}. Next: uv lock && make setup && make check, then commit.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
