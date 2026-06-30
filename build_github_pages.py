from __future__ import annotations

import os
import shutil
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parent
SITE_DIR = ROOT / "_site"
ASSETS_DIR = ROOT / "assets"
PLAYBOOK_HTML = ROOT / "playbook" / "playbook.html"
PLAYBOOK_PDF = ROOT / "playbook" / "Enterprise-ERP-UI-Blueprint.pdf"


def main() -> None:
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


if __name__ == "__main__":
    main()
