#!/usr/bin/env python3
"""Package Yuzhoujun Fig2Edit for GitHub releases or direct sharing."""

from __future__ import annotations

import shutil
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist"
PACKAGE_NAME = "yuzhoujun-fig2edit"

EXCLUDED_DIRS = {
    ".git",
    "__pycache__",
    ".pytest_cache",
    "dist",
}

EXCLUDED_SUFFIXES = {
    ".pyc",
    ".DS_Store",
}

EXCLUDED_FILES = {
    # Iteration artifacts kept locally for audit, but not shipped as public API.
    "build_zebrafish_case_outputs.py",
    "build_zebrafish_clean_v2.py",
    "build_zebrafish_commercial_quality_package.py",
    "build_zebrafish_editable_outputs.py",
    "build_zebrafish_editable_overlay_v5.py",
    "build_zebrafish_hybrid_editable_v6.py",
    "build_zebrafish_integrated_clean_editable_v7.py",
    "build_zebrafish_professional_editable.py",
    "build_zebrafish_verified_v3.py",
    "build_four_panel_highres_editable.py",
}


def should_include(path: Path) -> bool:
    rel = path.relative_to(ROOT)
    if any(part in EXCLUDED_DIRS for part in rel.parts):
        return False
    if path.name in EXCLUDED_SUFFIXES:
        return False
    if path.suffix in EXCLUDED_SUFFIXES:
        return False
    if path.name in EXCLUDED_FILES:
        return False
    return True


def copy_tree(target: Path) -> None:
    for path in ROOT.rglob("*"):
        if not should_include(path):
            continue
        rel = path.relative_to(ROOT)
        dest = target / rel
        if path.is_dir():
            dest.mkdir(parents=True, exist_ok=True)
        else:
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(path, dest)


def main() -> int:
    if DIST.exists():
        shutil.rmtree(DIST)
    DIST.mkdir(parents=True)

    package_root = DIST / PACKAGE_NAME
    package_root.mkdir()
    copy_tree(package_root)

    archive_base = DIST / f"{PACKAGE_NAME}-full"
    archive_path = shutil.make_archive(str(archive_base), "zip", DIST, PACKAGE_NAME)

    prompt_src = ROOT / "fig2edit-prompt.md"
    prompt_dest = DIST / "fig2edit-prompt.md"
    if prompt_src.exists():
        shutil.copy2(prompt_src, prompt_dest)

    print(f"Full package: {archive_path}")
    if prompt_dest.exists():
        print(f"Prompt-only:  {prompt_dest}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
