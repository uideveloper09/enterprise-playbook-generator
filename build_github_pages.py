from __future__ import annotations

import os
import shutil
import subprocess
import sys
from pathlib import Path

from generate_playbook_pdf import collect_build_issues


ROOT = Path(__file__).resolve().parent
SITE_DIR = ROOT / "_site"
ASSETS_DIR = ROOT / "assets"
PLAYBOOK_HTML = ROOT / "playbook" / "playbook.html"
PLAYBOOK_PDF = ROOT / "playbook" / "Enterprise-ERP-UI-Blueprint.pdf"


def main() -> int:
    issues = collect_build_issues(require_node=False)
    if issues:
        for issue in issues:
            print(f"Error: {issue}", file=sys.stderr)
        return 1

    env = os.environ.copy()
    env["PLAYBOOK_ASSETS_BASE"] = "assets"
    env["PLAYBOOK_HTML_ONLY"] = "1"

    subprocess.run(["python", "generate_playbook_pdf.py"], cwd=ROOT, check=True, env=env)

    if SITE_DIR.exists():
        shutil.rmtree(SITE_DIR)

    SITE_DIR.mkdir()
    (SITE_DIR / ".nojekyll").touch()
    shutil.copytree(ASSETS_DIR, SITE_DIR / "assets")
    shutil.copy(PLAYBOOK_HTML, SITE_DIR / "index.html")

    if PLAYBOOK_PDF.exists():
        shutil.copy(PLAYBOOK_PDF, SITE_DIR / "Enterprise-ERP-UI-Blueprint.pdf")

    print(f"GitHub Pages site built: {SITE_DIR}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
