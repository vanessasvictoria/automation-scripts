#!/usr/bin/env python3
"""
Batch rename files in a folder with a consistent prefix.

Examples:
  python3 src/rename_files.py --path "./downloads" --prefix "basel_" --dry-run
  python3 src/rename_files.py --path "./downloads" --prefix "basel_"
"""

from __future__ import annotations

import argparse
from pathlib import Path


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Batch rename files in a folder by adding a prefix.")
    p.add_argument("--path", required=True, help="Folder containing files to rename")
    p.add_argument("--prefix", required=True, help="Prefix to add to each filename (e.g., basel_)")
    p.add_argument("--dry-run", action="store_true", help="Show changes without renaming")
    p.add_argument("--include-hidden", action="store_true", help="Include dotfiles like .DS_Store")
    return p.parse_args()


def main() -> None:
    args = parse_args()
    folder = Path(args.path).expanduser().resolve()

    if not folder.exists() or not folder.is_dir():
        raise SystemExit(f"Error: '{folder}' is not a valid folder.")

    files = sorted([f for f in folder.iterdir() if f.is_file()])

    if not args.include_hidden:
        files = [f for f in files if not f.name.startswith(".")]

    if not files:
        print("No files found.")
        return

    planned = []
    for f in files:
        if f.name.startswith(args.prefix):
            continue  # already prefixed
        new_name = args.prefix + f.name
        planned.append((f, f.with_name(new_name)))

    if not planned:
        print("Nothing to rename (files already have the prefix?).")
        return

    print(f"Folder: {folder}")
    print(f"Planned renames ({len(planned)}):")
    for old, new in planned:
        print(f"  {old.name}  ->  {new.name}")

    if args.dry_run:
        print("\nDry run: no files were renamed.")
        return

    # Safety check: avoid overwriting existing files
    collisions = [new for _, new in planned if new.exists()]
    if collisions:
        print("\nERROR: These target filenames already exist:")
        for c in collisions:
            print(f"  {c.name}")
        print("Aborting to avoid overwriting.")
        return

    for old, new in planned:
        old.rename(new)

    print("\nDone.")


if __name__ == "__main__":
    main()
