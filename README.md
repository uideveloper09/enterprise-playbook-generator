# Enterprise Playbook Generator

Converts Markdown chapters into a premium HTML playbook and a print-ready A4 PDF for the Force Intellect Enterprise ERP UI Engineering Blueprint.

**Live playbook:** [playbook.bitcraftly.com](https://playbook.bitcraftly.com/)

**Repository:** [github.com/uideveloper09/enterprise-playbook-generator](https://github.com/uideveloper09/enterprise-playbook-generator)

---

## Overview

This project is a focused publishing pipeline for a single executive playbook. It reads chapter Markdown from `docs/`, applies the existing premium layout in `generate_playbook_pdf.py`, writes `playbook/index.html`, and exports `playbook/Enterprise-ERP-UI-Blueprint.pdf` with Puppeteer.

The generator is intentionally monolithic. The current HTML and PDF designs are preserved.

---

## Architecture

```text
docs/*.md
    ↓
generate_playbook.py          ← official entry point
    ↓
generate_playbook_pdf.py      ← Markdown → HTML
    ↓
playbook/index.html
    ↓
generate_pdf.js + Puppeteer ← HTML → PDF
    ↓
playbook/Enterprise-ERP-UI-Blueprint.pdf
```

GitHub Pages uses a separate HTML-only path:

```text
build_github_pages.py → _site/ → gh-pages branch
```

Optional Markdown preview:

```text
mkdocs.yml → mkdocs serve
```

---

## Folder Structure

```text
playbook-generator/
├── assets/
│   ├── brand/                 # Logo
│   ├── cover/                 # Cover background
│   └── diagrams/              # Chapter diagrams
├── docs/                      # Markdown source chapters
├── engine/                    # Legacy scaffold (not used by the active build)
├── playbook/                  # Generated HTML and PDF output
├── .github/workflows/         # GitHub Pages deployment
├── generate_playbook.py       # Official build entry point
├── generate_playbook_pdf.py   # HTML generator
├── generate_pdf.js            # PDF exporter
├── build_github_pages.py      # GitHub Pages site builder
├── package.json               # Node dependencies for Puppeteer
├── requirements.txt           # Optional MkDocs dependencies
├── mkdocs.yml                 # Optional MkDocs site config
├── LICENSE
└── README.md
```

---

## Requirements

- Python 3.11+
- Node.js 20+
- npm
- Chromium via Puppeteer (installed by `npm install`)

Python standard library is sufficient for the HTML/PDF build. `requirements.txt` is only needed if you want to preview chapters with MkDocs.

---

## Installation

```bash
git clone https://github.com/uideveloper09/enterprise-playbook-generator.git
cd enterprise-playbook-generator
npm install
```

Optional MkDocs preview:

```bash
pip install -r requirements.txt
```

---

## Usage

### Full build (recommended)

```bash
python generate_playbook.py
```

### HTML only

```bash
set PLAYBOOK_HTML_ONLY=1
python generate_playbook.py
```

On macOS/Linux:

```bash
PLAYBOOK_HTML_ONLY=1 python generate_playbook.py
```

### Direct scripts

```bash
python generate_playbook_pdf.py
node generate_pdf.js
```

### GitHub Pages site

```bash
python build_github_pages.py
```

Preview from `_site/index.html`.

---

## Live Deployment (`playbook.bitcraftly.com`)

The playbook is published to **[playbook.bitcraftly.com](https://playbook.bitcraftly.com/)** via GitHub Pages on the `gh-pages` branch.

This uses a **subdomain only**. It does **not** change [bitcraftly.com](https://bitcraftly.com/) DNS or hosting.

### DNS (one-time, at your domain provider)

| Type | Name | Value |
|------|------|-------|
| CNAME | `playbook` | `uideveloper09.github.io` |

Do **not** add or change apex (`@`) records for `bitcraftly.com`.

### GitHub (one-time)

1. **[Settings → Pages](https://github.com/uideveloper09/enterprise-playbook-generator/settings/pages)** → Source: **Deploy from branch** → `gh-pages` / root
2. **Custom domain:** `playbook.bitcraftly.com`
3. Enable **Enforce HTTPS** after DNS propagates

Every push to `main` runs **Deploy GitHub Pages** and updates the live site.

---

## Build Pipeline

| Step | Command / File | Output |
|------|----------------|--------|
| 1. Validate | `generate_playbook.py` | Checks docs, assets, scripts, markdown, diagrams |
| 2. HTML | `generate_playbook_pdf.py` | `playbook/index.html` |
| 3. PDF | `generate_pdf.js` | `playbook/Enterprise-ERP-UI-Blueprint.pdf` |

The build stops on the first error and returns a non-zero exit code.

Example success output:

```text
------------------------------------------------
Enterprise Playbook Generator

Checking project...

✓ docs
✓ assets
✓ playbook
✓ generate_playbook_pdf.py
✓ generate_pdf.js

Generating HTML...
✓ index.html

Generating PDF...
✓ Enterprise-ERP-UI-Blueprint.pdf

Completed Successfully
------------------------------------------------
```

---

## Output

```text
playbook/
├── index.html
└── Enterprise-ERP-UI-Blueprint.pdf
```

Current playbook scope:

- Cover page
- Blueprint overview / preface
- Chapters 01–15
- Visual reference diagrams
- Footer with repository link

---

## Screenshots

| Preview | Path |
|---------|------|
| Cover page | _Add screenshot here_ |
| Chapter page | _Add screenshot here_ |
| PDF export | _Add screenshot here_ |
| GitHub Pages | _Add screenshot here_ |

---

## GitHub Pages Deployment

The repository includes `.github/workflows/deploy-pages.yml`.

**Live URL:** https://playbook.bitcraftly.com/

1. Enable **Settings → Actions → General → Workflow permissions → Read and write**
2. Add DNS **CNAME**: `playbook` → `uideveloper09.github.io` (subdomain only — [bitcraftly.com](https://bitcraftly.com/) is unaffected)
3. Enable **Settings → Pages → Deploy from branch → `gh-pages` / root**
4. Set **Custom domain** to `playbook.bitcraftly.com` and enable **Enforce HTTPS**
5. Push to `main` or run the workflow manually

The CI workflow publishes HTML only. PDF generation remains a local build step.

---

## Roadmap

- [x] Official `generate_playbook.py` entry point
- [x] Build validation and error reporting
- [x] GitHub Pages deployment
- [x] MIT License
- [ ] Automated PDF artifact in CI
- [ ] Ordered-list rendering in custom Markdown parser
- [ ] Data-driven chapter configuration
- [ ] Automated tests and snapshot checks
- [ ] Docker-based reproducible PDF build

---

## Contributing

Issues and improvement suggestions are welcome. Please open an issue before large changes.

---

## License

MIT License. See [LICENSE](LICENSE).

---

## Author

**Sanjay Kr. Singh**  
Tech Lead · Frontend Architect  
https://github.com/uideveloper09
