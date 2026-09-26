#!/usr/bin/env python3
"""Create the standard workspace folders for doc-translator-zh."""

import argparse
import os
import subprocess
import sys
from pathlib import Path


def run_command(cmd, cwd=None):
    """Run a shell command and return (returncode, stdout, stderr)."""
    result = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
    return result.returncode, result.stdout, result.stderr


def main():
    parser = argparse.ArgumentParser(description="Create doc-translator-zh workspace folders.")
    parser.add_argument("--root", required=True, help="Workspace root directory")
    parser.add_argument("--clean", action="store_true", help="Remove existing workspace first")
    parser.add_argument("--git-init", action="store_true", help="Initialize a git repo in the workspace if not already one")
    args = parser.parse_args()

    root = Path(args.root).resolve()

    if args.clean and root.exists():
        import shutil
        shutil.rmtree(root)

    for sub in ("input", "output", "script"):
        (root / sub).mkdir(parents=True, exist_ok=True)

    git_initialized = False
    if args.git_init:
        git_dir = root / ".git"
        if not git_dir.exists():
            rc, stdout, stderr = run_command(["git", "init"], cwd=root)
            if rc == 0:
                git_initialized = True
                # Create a basic .gitignore to ignore temporary pdf page images
                gitignore = root / ".gitignore"
                if not gitignore.exists():
                    gitignore.write_text("output/pdf_pages/\n", encoding="utf-8")
            else:
                print(f"Warning: git init failed: {stderr}", file=sys.stderr)
        else:
            git_initialized = True  # already a git repo

    result = {
        "workspace": str(root),
        "input": str(root / "input"),
        "output": str(root / "output"),
        "script": str(root / "script"),
        "git_initialized": git_initialized,
    }

    for key, path in result.items():
        print(f"{key}: {path}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
