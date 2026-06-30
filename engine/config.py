"""
Global configuration for the Playbook Generator.
"""

from pathlib import Path

# -----------------------------------------------------------------------------
# Project Paths
# -----------------------------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent

ASSETS_DIR = PROJECT_ROOT / "assets"
DOCS_DIR = PROJECT_ROOT / "docs"
TEMPLATES_DIR = PROJECT_ROOT / "templates"
OUTPUT_DIR = PROJECT_ROOT / "playbook"

# -----------------------------------------------------------------------------
# Asset Paths
# -----------------------------------------------------------------------------

LOGOS_DIR = ASSETS_DIR / "logos"
DIAGRAMS_DIR = ASSETS_DIR / "diagrams"
COVER_DIR = ASSETS_DIR / "cover"
ICONS_DIR = ASSETS_DIR / "icons"
FONTS_DIR = ASSETS_DIR / "fonts"

# -----------------------------------------------------------------------------
# Output Files
# -----------------------------------------------------------------------------

HTML_OUTPUT = OUTPUT_DIR / "index.html"
PDF_OUTPUT = OUTPUT_DIR / "Enterprise-ERP-UI-Blueprint.pdf"

# -----------------------------------------------------------------------------
# Metadata
# -----------------------------------------------------------------------------

BOOK_TITLE = "Enterprise ERP UI Engineering Strategy & Execution Blueprint"
BOOK_SUBTITLE = "Founder Executive Edition 2026"

AUTHOR = "Sanjay Kr. Singh"

COMPANY = "Force Intellect"

VERSION = "2.0"

LANGUAGE = "en"

# -----------------------------------------------------------------------------
# PDF
# -----------------------------------------------------------------------------

PAGE_SIZE = "A4"

PRINT_BACKGROUND = True

MARGIN = {
    "top": "0mm",
    "right": "0mm",
    "bottom": "0mm",
    "left": "0mm"
}