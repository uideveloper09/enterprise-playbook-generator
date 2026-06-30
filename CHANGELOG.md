# Changelog

## 2026-06-30 — Repository Stabilization for CTO Review

### Files Modified

| File | Reason | Impact |
|------|--------|--------|
| `generate_playbook.py` | Replaced broken stub with official validated entry point | `python generate_playbook.py` is now the supported build command |
| `generate_playbook_pdf.py` | Added build validation, exit codes, improved PDF errors, removed dead helpers | Safer builds; clearer failures; no HTML/PDF design changes |
| `generate_pdf.js` | Added actionable error messages and output checks | Easier PDF troubleshooting |
| `build_github_pages.py` | Added pre-build validation and exit codes | CI/local Pages build fails fast on missing inputs |
| `README.md` | Rewrote documentation to match actual behavior | Removes inaccurate claims; improves CTO/onboarding clarity |
| `LICENSE` | Added MIT license file | Legal/open-source readiness |
| `.gitignore` | Expanded ignore rules | Cleaner working tree |
| `package.json` | Removed unused `pdf-lib`, added metadata and script | Smaller dependency surface |
| `mkdocs.yml` | Fixed broken logo paths and removed missing asset references | Optional MkDocs preview can start without missing-file errors |

### Impact Summary

- Build pipeline is now explicit, validated, and logged
- Repository documentation matches the real implementation
- No architecture rewrite
- No HTML redesign
- No PDF redesign
- No feature removal from the generated playbook

### Remaining Technical Debt

- `generate_playbook_pdf.py` remains a large monolithic file
- `engine/` contains unused legacy scaffold files
- Custom Markdown parser does not render ordered lists correctly
- Chapter layout metadata is still hardcoded in Python
- `index.md` and `00-cover.md` content is not fully driven by Markdown
- GitHub Pages deploy is HTML-only; PDF is not published by CI
- No automated test suite yet
- Preface stat "90 Key Diagrams" is still inaccurate in generated HTML

### Future Improvements

- CI job to publish PDF artifacts on release
- Snapshot tests for HTML output
- Ordered-list support in Markdown parser
- Optional quiet mode for `generate_pdf.js` console output
- Screenshots added to README
- Resolve public "Confidential" labeling for published Pages site
