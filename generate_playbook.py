#!/usr/bin/env python3
"""Official entry point for the Enterprise Playbook Generator."""

from __future__ import annotations

import os
import sys

from generate_playbook_pdf import (
    HTML_OUTPUT,
    PDF_OUTPUT,
    collect_build_issues,
    generate_pdf,
    write_html,
)


def _configure_console() -> None:
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            try:
                stream.reconfigure(encoding="utf-8")
            except (OSError, ValueError):
                pass


def _divider() -> None:
    print("-" * 48)


def _success(label: str) -> None:
    print(f"✓ {label}")


def _failure(message: str) -> None:
    print(f"✗ {message}")


def main() -> int:
    _configure_console()
    html_only = os.environ.get("PLAYBOOK_HTML_ONLY", "").lower() in {"1", "true", "yes"}

    _divider()
    print("Enterprise Playbook Generator")
    print()
    print("Checking project...")

    issues = collect_build_issues(require_node=not html_only)
    if issues:
        for issue in issues:
            _failure(issue)
        print()
        print("Build failed.")
        _divider()
        return 1

    _success("docs")
    _success("assets")
    _success("playbook")
    _success("generate_playbook_pdf.py")
    _success("generate_pdf.js")

    print()
    print("Generating HTML...")
    try:
        write_html(quiet=True)
    except OSError as exc:
        _failure(
            f"HTML generation failed.\n"
            f"  Why: {exc}\n"
            "  Fix: verify write permissions for the playbook/ folder."
        )
        print()
        print("Build failed.")
        _divider()
        return 1

    _success(HTML_OUTPUT.name)

    if html_only:
        print()
        print("Completed Successfully")
        _divider()
        return 0

    print()
    print("Generating PDF...")
    try:
        generate_pdf()
    except (OSError, RuntimeError, FileNotFoundError) as exc:
        _failure(str(exc))
        print()
        print("Build failed.")
        _divider()
        return 1

    _success(PDF_OUTPUT.name)
    print()
    print("Completed Successfully")
    _divider()
    return 0


if __name__ == "__main__":
    sys.exit(main())
