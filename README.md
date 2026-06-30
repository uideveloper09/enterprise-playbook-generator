# 🚀 Enterprise Playbook Generator

An enterprise-grade Playbook Generator that converts Markdown documents into beautifully designed HTML and production-ready PDF playbooks using Python and Puppeteer.

---

## ✨ Features

- 📖 Markdown to HTML conversion
- 📄 Professional PDF generation
- 🎨 Enterprise cover page
- 📑 Automatic Table of Contents
- 🖼️ Diagram and image support
- 📊 Tables and callout blocks
- 📌 Page numbering and footer
- 🖨️ Print-ready A4 layout
- ⚡ Puppeteer-powered PDF rendering
- 🏢 Enterprise documentation structure

---

## 📁 Project Structure

```text
playbook-generator/
│
├── assets/                  # Logos, cover, diagrams, icons
├── docs/                    # Markdown chapters
├── engine/                  # Core engine modules
├── overrides/               # MkDocs overrides
├── playbook/                # Generated HTML & PDF
├── templates/               # HTML templates
│
├── generate_playbook.py     # Main entry point
├── generate_playbook_pdf.py # Markdown → HTML
├── generate_pdf.js          # HTML → PDF
│
├── package.json
├── requirements.txt
├── mkdocs.yml
└── README.md
```

---

## ⚙️ Requirements

- Python 3.11+
- Node.js 20+
- Google Chrome / Chromium
- Puppeteer

---

## 📦 Installation

### Clone Repository

```bash
git clone https://github.com/uideveloper09/enterprise-playbook-generator.git

cd enterprise-playbook-generator
```

### Install Python Dependencies

```bash
pip install -r requirements.txt
```

### Install Node Packages

```bash
npm install
```

---

## 🚀 Usage

Generate HTML

```bash
python generate_playbook_pdf.py
```

Generate PDF

```bash
node generate_pdf.js
```

Or run everything together

```bash
python generate_playbook.py
```

---

## 📄 Output

Generated files are stored in:

```text
playbook/

├── playbook.html
└── Enterprise-ERP-UI-Blueprint.pdf
```

---

## 🏗️ Technology Stack

- Python
- JavaScript
- Puppeteer
- HTML5
- CSS3
- Markdown
- MkDocs

---

## 🎯 Roadmap

- [ ] Intelligent pagination engine
- [ ] Smart page-break optimization
- [ ] Multiple PDF themes
- [ ] Custom templates
- [ ] CLI support
- [ ] Docker support
- [ ] CI/CD pipeline
- [ ] Plugin architecture

---

## 🤝 Contributing

Contributions, issues, and feature requests are welcome.

Please open an issue before submitting large changes.

---

## 📜 License

MIT License

---

## 👨‍💻 Author

**Sanjay Kr. Singh**

Tech Lead • Frontend Architect

React • Next.js • TypeScript • UI Engineering • Enterprise Architecture

GitHub:
https://github.com/uideveloper09

---

## ⭐ Support

If you find this project useful, please consider giving it a ⭐ on GitHub.
