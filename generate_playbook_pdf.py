from __future__ import annotations

import html
import os
import re
import subprocess
from pathlib import Path
from typing import Callable
from urllib.parse import quote


ROOT = Path(__file__).resolve().parent
GITHUB_REPO_URL = "https://github.com/uideveloper09/enterprise-playbook-generator"
GITHUB_PAGES_URL = "https://uideveloper09.github.io/enterprise-playbook-generator/"
ASSETS_BASE = os.environ.get("PLAYBOOK_ASSETS_BASE", "../assets").rstrip("/") + "/"
DOCS_DIR = ROOT / "docs"
PLAYBOOK_DIR = ROOT / "playbook"
HTML_OUTPUT = PLAYBOOK_DIR / "playbook.html"
COVER_BACKGROUND = ROOT / "assets" / "cover" / "cover-background.png"
BRAND_LOGO = ROOT / "assets" / "brand" / "force-logo.png"
DIAGRAMS_DIR = ROOT / "assets" / "diagrams"
GENERATE_COVER_ONLY = False
ACTIVE_PAGES = {
    "00-cover.md",
    "index.md",
    "01-executive-summary.md",
    "02-business-strategy.md",
    "03-product-strategy.md",
    "04-ui-engineering-vision.md",
    "05-engineering-leadership.md",
    "06-ui-engineering-organization.md",
    "07-enterprise-frontend-architecture.md",
    "08-design-system.md",
    "09-enterprise-component-library.md",
    "10-engineering-standards.md",
    "11-engineering-delivery-model.md",
    "12-engineering-excellence-framework.md",
    "13-ai-augmented-engineering.md",
    "14-90-day-execution-plan.md",
    "15-future-vision.md",
}

BLUEPRINT_CHAPTERS = [
    ("01", "Executive Summary"),
    ("02", "Business Strategy"),
    ("03", "Product Strategy"),
    ("04", "UI Engineering Vision"),
    ("05", "Engineering Leadership"),
    ("06", "UI Engineering Organization"),
    ("07", "Enterprise Frontend Architecture"),
    ("08", "Design System Strategy"),
    ("09", "Enterprise Component Library"),
    ("10", "Engineering Standards"),
    ("11", "Engineering Delivery Model"),
    ("12", "Engineering Excellence Framework"),
    ("13", "AI-Augmented Engineering"),
    ("14", "90-Day Transformation Roadmap"),
    ("15", "Future Vision"),
]

AUDIENCE_ROLES = [
    "Founder",
    "Chief Executive Officer (CEO)",
    "Chief Technology Officer (CTO)",
    "Engineering Director",
    "Product Leadership",
    "Solution Architects",
    "Engineering Managers",
    "Technical Leads",
]

GUIDING_PRINCIPLES = [
    "Business-Driven Engineering",
    "Platform Thinking",
    "Scalable Architecture",
    "Engineering Excellence",
    "Reusability by Design",
    "Security by Default",
    "Continuous Improvement",
    "Sustainable Product Development",
]

CHAPTER_ONE_DIAGRAMS = [
    ("UI engineering strategy infographic diagram.png", "UI Engineering Strategy Overview"),
]

CHAPTER_TWO_INLINE_DIAGRAM = (
    "UI engineering goals & objectives diagram.png",
    "UI Engineering Goals & Objectives Diagram",
)

CHAPTER_THREE_INLINE_DIAGRAM = (
    "UI engineering lifecycle diagram.png",
    "UI Engineering Lifecycle Diagram",
)

CHAPTER_FOUR_INLINE_DIAGRAM = (
    "UI engineering vision infographic diagram.png",
    "UI Engineering Vision Diagram",
)

CHAPTER_FOUR_SECOND_INLINE_DIAGRAM = (
    "UI engineering principles infographic.png",
    "UI Engineering Principles Infographic",
)

CHAPTER_FIVE_INLINE_DIAGRAM = (
    "UI Engineering Maturity Model diagram.png",
    "UI Engineering Maturity Model",
)

CHAPTER_SIX_INLINE_DIAGRAM = (
    "UI engineering lifecycle overview diagram.png",
    "UI Engineering Lifecycle Overview",
)

CHAPTER_SEVEN_INLINE_DIAGRAM = (
    "Enterprise frontend architecture diagram.png",
    "Enterprise Frontend Architecture Diagram",
)

CHAPTER_EIGHT_INLINE_DIAGRAM = (
    "Design system architecture overview.png",
    "Design System Architecture Overview",
)

CHAPTER_NINE_INLINE_DIAGRAM = (
    "Enterprise component library diagram.png",
    "Enterprise Component Library Structure",
)

CHAPTER_TEN_INLINE_DIAGRAM = (
    "UI engineering standards overview chart.png",
    "UI Engineering Standards Overview",
)

CHAPTER_ELEVEN_INLINE_DIAGRAM = (
    "UI engineering delivery model infographic.png",
    "UI Engineering Delivery Model",
)

CHAPTER_TWELVE_INLINE_DIAGRAM = (
    "Engineering excellence framework infographic.png",
    "Engineering Excellence Framework",
)

CHAPTER_THIRTEEN_INLINE_DIAGRAM = (
    "AI-assisted UI engineering workflow.png",
    "AI-Augmented UI Engineering Workflow",
)

CHAPTER_FOURTEEN_INLINE_DIAGRAM = (
    "modern infographic features-90.png",
    "90-Day UI Engineering Transformation Roadmap",
)

CHAPTER_FIFTEEN_INLINE_DIAGRAM = (
    "UI engineering strategy infographic.png",
    "UI Engineering Strategy Framework",
)


def read_md(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def strip_frontmatter(markdown: str) -> str:
    lines = markdown.splitlines()

    if lines and lines[0].strip() == "---":
        for index, line in enumerate(lines[1:], start=1):
            if line.strip() == "---":
                return "\n".join(lines[index + 1 :]).strip()

    return markdown.strip()


def unwrap_outer_code_fence(markdown: str) -> str:
    lines = markdown.strip().splitlines()

    if len(lines) >= 2 and lines[0].strip().startswith("```") and lines[-1].strip() == "```":
        return "\n".join(lines[1:-1]).strip()

    return markdown.strip()


def inline_markdown(text: str) -> str:
    escaped = html.escape(text)
    escaped = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", escaped)
    escaped = re.sub(r"\*(.+?)\*", r"<em>\1</em>", escaped)
    escaped = re.sub(r"`(.+?)`", r"<code>\1</code>", escaped)
    return escaped


def is_table_separator(line: str) -> bool:
    cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
    return bool(cells) and all(re.fullmatch(r":?-{3,}:?", cell or "") for cell in cells)


def render_table(lines: list[str]) -> str:
    rows = [[cell.strip() for cell in line.strip().strip("|").split("|")] for line in lines]
    header = rows[0]
    body = rows[2:] if len(rows) > 1 and is_table_separator(lines[1]) else rows[1:]

    output = ["<table>", "<thead><tr>"]
    output.extend(f"<th>{inline_markdown(cell)}</th>" for cell in header)
    output.append("</tr></thead>")

    if body:
        output.append("<tbody>")
        for row in body:
            output.append("<tr>")
            output.extend(f"<td>{inline_markdown(cell)}</td>" for cell in row)
            output.append("</tr>")
        output.append("</tbody>")

    output.append("</table>")
    return "\n".join(output)


def markdown_to_html(markdown: str) -> str:
    lines = strip_frontmatter(unwrap_outer_code_fence(markdown)).splitlines()
    output: list[str] = []
    paragraph: list[str] = []
    list_items: list[str] = []
    table_lines: list[str] = []
    in_code_block = False
    code_lines: list[str] = []

    def flush_paragraph() -> None:
        if paragraph:
            output.append(f"<p>{inline_markdown(' '.join(paragraph))}</p>")
            paragraph.clear()

    def flush_list() -> None:
        if list_items:
            output.append("<ul>")
            output.extend(f"<li>{inline_markdown(item)}</li>" for item in list_items)
            output.append("</ul>")
            list_items.clear()

    def flush_table() -> None:
        if table_lines:
            output.append(render_table(table_lines))
            table_lines.clear()

    for raw_line in lines:
        line = raw_line.rstrip()
        stripped = line.strip()

        if stripped.startswith("```"):
            flush_paragraph()
            flush_list()
            flush_table()
            if in_code_block:
                output.append(f"<pre><code>{html.escape(chr(10).join(code_lines))}</code></pre>")
                code_lines.clear()
                in_code_block = False
            else:
                in_code_block = True
            continue

        if in_code_block:
            code_lines.append(line)
            continue

        if not stripped:
            flush_paragraph()
            flush_list()
            flush_table()
            continue

        if stripped.startswith("|") and stripped.endswith("|"):
            flush_paragraph()
            flush_list()
            table_lines.append(stripped)
            continue

        flush_table()

        if stripped == "---":
            flush_paragraph()
            flush_list()
            output.append("<hr>")
            continue

        if stripped.startswith("<") and stripped.endswith(">"):
            flush_paragraph()
            flush_list()
            output.append(stripped)
            continue

        heading = re.match(r"^(#{1,6})\s+(.+)$", stripped)
        if heading:
            flush_paragraph()
            flush_list()
            level = len(heading.group(1))
            output.append(f"<h{level}>{inline_markdown(heading.group(2))}</h{level}>")
            continue

        bullet = re.match(r"^[-*]\s+(.+)$", stripped)
        if bullet:
            flush_paragraph()
            list_items.append(bullet.group(1))
            continue

        quote = re.match(r"^>\s?(.+)$", stripped)
        if quote:
            flush_paragraph()
            flush_list()
            output.append(f"<blockquote>{inline_markdown(quote.group(1))}</blockquote>")
            continue

        paragraph.append(stripped)

    flush_paragraph()
    flush_list()
    flush_table()

    if in_code_block:
        output.append(f"<pre><code>{html.escape(chr(10).join(code_lines))}</code></pre>")

    return "\n".join(output)


def ordered_markdown_files() -> list[Path]:
    files = sorted(DOCS_DIR.glob("*.md"))
    cover = [path for path in files if path.name == "00-cover.md"]
    overview = [path for path in files if path.name == "index.md"]
    chapters = [path for path in files if path not in cover and path not in overview]
    return cover + overview + chapters


def chapter_label(path: Path) -> str:
    if path.name == "index.md":
        return "Blueprint Overview"

    label = path.stem.replace("-", " ").title()
    return label


def overview_body(markdown: str) -> str:
    body = strip_frontmatter(unwrap_outer_code_fence(markdown))
    marker = "# About This Blueprint"

    if marker in body:
        return body[body.index(marker) :].strip()

    return body


def asset_src(relative_path: str) -> str:
    return f"{ASSETS_BASE}{relative_path}"


def diagram_src(filename: str) -> str:
    return asset_src(f"diagrams/{quote(filename)}")


def chapter_diagrams_html(filenames: list[tuple[str, str]]) -> str:
    blocks = []

    for filename, caption in filenames:
        block = visual_reference_html(filename, caption)
        if block:
            blocks.append(block)

    return "\n".join(blocks)


def visual_reference_html(filename: str, caption: str) -> str:
    path = DIAGRAMS_DIR / filename
    if not path.exists():
        return ""

    return (
        '<div class="visual-reference">\n'
        '<div class="visual-reference-bar">Visual Reference</div>\n'
        '<figure class="visual-reference-figure">\n'
        f'<img src="{diagram_src(filename)}" alt="{html.escape(caption)}">\n'
        "</figure>\n"
        f'<p class="visual-reference-caption"><span aria-hidden="true">◆</span> {html.escape(caption)}</p>\n'
        "</div>\n"
    )


def inject_html_after_heading(
    body_html: str,
    heading_text: str,
    injection: str,
    level: int = 2,
) -> str:
    needle = f"<h{level}>{html.escape(heading_text)}</h{level}>"
    if needle in body_html and injection:
        return body_html.replace(needle, f"{needle}\n{injection}", 1)
    return body_html


def chapter_header_html(chapter_number: int, chapter_title: str) -> str:
    number = f"{chapter_number:02d}"
    logo_html = ""

    if BRAND_LOGO.exists():
        logo_html = (
            '<img class="chapter-header-logo" src="'
            f'{asset_src("brand/force-logo.png")}" '
            'alt="Force Intellect">\n'
        )

    return (
        '<header class="chapter-header">\n'
        f'<span class="chapter-header-watermark">{number}</span>\n'
        f"{logo_html}"
        '<div class="chapter-header-copy">\n'
        f'<span class="chapter-header-badge">Chapter {number}</span>\n'
        f'<h1 class="chapter-header-title">{html.escape(chapter_title)}</h1>\n'
        '<span class="chapter-header-line" aria-hidden="true"></span>\n'
        "</div>\n"
        "</header>\n"
    )


def page_topbar_html(title: str, page_number: int) -> str:
    return (
        '<header class="page-topbar">\n'
        f'<span class="page-topbar-title">{html.escape(title)}</span>\n'
        f'<span class="page-topbar-number">{page_number:02d}</span>\n'
        '</header>\n'
    )


def page_footer_html() -> str:
    return (
        '<footer class="page-footer">\n'
        '<div class="page-footer-inner">\n'
        '<div class="page-footer-brand">\n'
        '<span class="page-footer-accent" aria-hidden="true"></span>\n'
        '<div class="page-footer-copy">\n'
        '<strong>Enterprise ERP UI Blueprint</strong>\n'
        '<span>Force Intellect · Founder Executive Edition 2026</span>\n'
        f'<a class="page-footer-github" href="{GITHUB_REPO_URL}">'
        "github.com/uideveloper09/enterprise-playbook-generator</a>\n"
        "</div>\n"
        "</div>\n"
        '<span class="page-footer-label">Strategic Playbook</span>\n'
        '<span class="page-footer-badge">Confidential</span>\n'
        "</div>\n"
        "</footer>\n"
    )


def preface_card(title: str, icon_class: str, body_html: str) -> str:
    return (
        '<article class="preface-card">\n'
        f'<div class="preface-card-head"><span class="preface-icon {icon_class}"></span>'
        f"<h3>{html.escape(title)}</h3></div>\n"
        f'<div class="preface-card-body">{body_html}</div>\n'
        "</article>\n"
    )


def preface_page_html() -> str:
    audience_pills = "".join(f"<span>{html.escape(role)}</span>" for role in AUDIENCE_ROLES)
    principles = "".join(f"<li>{html.escape(item)}</li>" for item in GUIDING_PRINCIPLES)
    scope_items = "".join(
        f'<li><strong>{num}</strong><span>{html.escape(title)}</span></li>'
        for num, title in BLUEPRINT_CHAPTERS
    )

    purpose_body = (
        "<p>This blueprint presents a comprehensive engineering strategy for designing, "
        "developing, and scaling a modern Enterprise ERP Frontend Platform.</p>"
        "<p>It establishes a practical framework covering engineering leadership, frontend "
        "architecture, design systems, delivery excellence, governance, AI-enabled development, "
        "and long-term platform evolution.</p>"
        "<p>Rather than focusing solely on technologies, this document defines the engineering "
        "principles, organizational practices, and execution models required to build sustainable "
        "enterprise software.</p>"
    )

    info_body = (
        '<dl class="preface-info">'
        "<dt>Organization</dt><dd>Force Intellect</dd>"
        "<dt>Edition</dt><dd>Founder Executive Edition 2026</dd>"
        "<dt>Author</dt><dd>Sanjay Kr. Singh</dd>"
        "<dt>Role</dt><dd>Tech Lead · Frontend Architect</dd>"
        '<dt>Classification</dt><dd><span class="preface-badge preface-badge-green">Confidential</span></dd>'
        '<dt>Status</dt><dd><span class="preface-badge preface-badge-gold">Leadership Review Draft</span></dd>'
        "</dl>"
    )

    read_body = (
        "<p>This document is intended to be read sequentially. Each chapter builds upon the "
        "previous one, progressing from business strategy to engineering leadership, platform "
        "architecture, governance, delivery excellence, AI-enabled engineering, organizational "
        "transformation, and long-term engineering vision.</p>"
        '<div class="preface-callout">Individual chapters may also be referenced independently '
        "when defining engineering standards, evaluating architecture, planning organizational "
        "improvements, or supporting executive decision-making.</div>"
    )

    left_column = (
        preface_card("Document Purpose", "preface-icon-purple", purpose_body)
        + preface_card("Document Information", "preface-icon-orange", info_body)
        + preface_card("Guiding Principles", "preface-icon-gold", f"<ul>{principles}</ul>")
    )

    right_column = (
        preface_card("Intended Audience", "preface-icon-violet", f'<div class="preface-pills">{audience_pills}</div>')
        + preface_card("Blueprint Scope", "preface-icon-green", f'<ol class="preface-scope">{scope_items}</ol>')
        + preface_card("How to Read This Blueprint", "preface-icon-blue", read_body)
    )

    return (
        '<section class="chapter content-page preface-page" data-source="index.md" '
        'data-label="Blueprint Overview">\n'
        '<header class="preface-hero">\n'
        '<div class="preface-hero-top">\n'
        '<span class="preface-kicker">A Strategic Playbook · Confidential</span>\n'
        '<span class="preface-edition">Founder Executive Edition 2026</span>\n'
        "</div>\n"
        "<h1>Enterprise ERP UI Engineering Strategy &amp; Execution Blueprint</h1>\n"
        '<div class="preface-metrics">\n'
        "<div><strong>15</strong><span>Chapters</span></div>\n"
        "<div><strong>8</strong><span>Core Principles</span></div>\n"
        "<div><strong>90</strong><span>Key Diagrams</span></div>\n"
        "<div><strong>8+</strong><span>Audience Roles</span></div>\n"
        "<div><strong>2026</strong><span>Edition</span></div>\n"
        "</div>\n"
        "</header>\n"
        f'<div class="preface-grid">{left_column}{right_column}</div>\n'
        f"{page_footer_html()}"
        "</section>"
    )


def overview_page_html(markdown: str) -> str:
    return preface_page_html()


def chapter_body(markdown: str, marker: str = "# Executive Context") -> str:
    body = strip_frontmatter(unwrap_outer_code_fence(markdown))

    if marker in body:
        return body[body.index(marker) :].strip()

    return body


def chapter_page_html(
    chapter_number: int,
    title: str,
    source_file: str,
    label: str,
    kicker: str,
    quote: str,
    stats: list[tuple[str, str, str]],
    pillars: list[tuple[str, str, str, str]],
    diagrams: list[tuple[str, str]],
    markdown: str,
    body_marker: str = "# Executive Context",
    body_post_process: Callable[[str], str] | None = None,
) -> str:
    stats_html = "".join(
        f'<article class="chapter-01-stat chapter-01-stat-{modifier}">'
        f'<span class="chapter-01-stat-value">{html.escape(value)}</span>'
        f'<span class="chapter-01-stat-label">{html.escape(stat_label)}</span></article>'
        for value, stat_label, modifier in stats
    )
    pillars_html = "".join(
        f'<article class="chapter-01-pillar chapter-01-pillar-{modifier}">'
        f'<span class="chapter-01-pillar-num">{html.escape(num)}</span>'
        f"<strong>{html.escape(pillar_title)}</strong>"
        f"<p>{html.escape(description)}</p></article>"
        for num, pillar_title, description, modifier in pillars
    )

    body_html = markdown_to_html(chapter_body(markdown, body_marker))
    if body_post_process:
        body_html = body_post_process(body_html)

    return (
        f'<section class="chapter content-page overview-page chapter-page chapter-{chapter_number:02d}-page" '
        f'data-source="{html.escape(source_file)}" data-label="{html.escape(label)}">\n'
        f"{chapter_header_html(chapter_number, title)}"
        '<div class="chapter-01-content">\n'
        '<div class="chapter-01-lead">\n'
        '<div class="chapter-01-lead-head">\n'
        '<span class="chapter-01-lead-icon" aria-hidden="true"></span>\n'
        f'<p class="chapter-01-kicker">{html.escape(kicker)}</p>\n'
        "</div>\n"
        f'<blockquote class="chapter-01-quote"><em>{html.escape(quote)}</em></blockquote>\n'
        "</div>\n"
        '<section class="chapter-01-block">\n'
        '<div class="chapter-01-block-head">\n'
        '<span class="chapter-01-block-icon chapter-01-block-icon-blue" aria-hidden="true"></span>\n'
        "<h3>Chapter Highlights</h3>\n"
        "</div>\n"
        f'<div class="chapter-01-stats">{stats_html}</div>\n'
        "</section>\n"
        f"{chapter_diagrams_html(diagrams)}\n"
        '<section class="chapter-01-block">\n'
        '<div class="chapter-01-block-head">\n'
        '<span class="chapter-01-block-icon chapter-01-block-icon-gold" aria-hidden="true"></span>\n'
        "<h3>Strategic Pillars</h3>\n"
        "</div>\n"
        f'<div class="chapter-01-pillars">{pillars_html}</div>\n'
        "</section>\n"
        '<div class="chapter-01-body">\n'
        f"{body_html}\n"
        "</div>\n"
        "</div>\n"
        f"{page_footer_html()}"
        "</section>"
    )


def chapter_one_html(markdown: str) -> str:
    return chapter_page_html(
        chapter_number=1,
        title="Executive Summary",
        source_file="01-executive-summary.md",
        label="Chapter 01 Executive Summary",
        kicker="Opening Perspective",
        quote=(
            "Enterprise software is built through disciplined engineering, not individual "
            "technical excellence. Sustainable products emerge when business strategy, product "
            "vision, architecture, engineering culture, and execution operate as one integrated system."
        ),
        stats=[
            ("8", "Business Objectives", "objectives"),
            ("5", "Engineering Principles", "principles"),
            ("3", "Priority Horizons", "horizons"),
        ],
        pillars=[
            ("01", "Align", "Engineering investments with business priorities.", "align"),
            ("02", "Standardize", "Architecture, quality, and reusable platforms.", "standardize"),
            ("03", "Scale", "Culture, governance, and AI-enabled delivery.", "scale"),
        ],
        diagrams=CHAPTER_ONE_DIAGRAMS,
        markdown=markdown,
    )


def chapter_two_body_post_process(body_html: str) -> str:
    filename, caption = CHAPTER_TWO_INLINE_DIAGRAM
    diagram = visual_reference_html(filename, caption)
    return inject_html_after_heading(body_html, "Customer Value", diagram)


def chapter_two_html(markdown: str) -> str:
    return chapter_page_html(
        chapter_number=2,
        title="Business Strategy",
        source_file="02-business-strategy.md",
        label="Chapter 02 Business Strategy",
        kicker="Strategic Context",
        quote=(
            "Technology creates capabilities. Business strategy determines where those capabilities "
            "create value. Sustainable engineering organizations align every technical investment "
            "with measurable business outcomes."
        ),
        stats=[
            ("8", "Business Objectives", "objectives"),
            ("5", "Strategic Principles", "principles"),
            ("8", "Success Indicators", "horizons"),
        ],
        pillars=[
            ("01", "Value", "Every capability must solve a genuine customer problem.", "align"),
            ("02", "Excellence", "Technology should simplify operations and improve efficiency.", "standardize"),
            ("03", "Platform", "Build a unified business platform, not isolated modules.", "scale"),
        ],
        diagrams=[],
        markdown=markdown,
        body_post_process=chapter_two_body_post_process,
    )


def chapter_three_body_post_process(body_html: str) -> str:
    filename, caption = CHAPTER_THREE_INLINE_DIAGRAM
    diagram = visual_reference_html(filename, caption)
    return inject_html_after_heading(body_html, "Solve Business Problems", diagram)


def chapter_three_html(markdown: str) -> str:
    return chapter_page_html(
        chapter_number=3,
        title="UI Product Strategy",
        source_file="03-product-strategy.md",
        label="Chapter 03 UI Product Strategy",
        kicker="Product Context",
        quote=(
            "Successful products are built through disciplined strategy, thoughtful prioritization, "
            "and continuous alignment between customer needs, business goals, and engineering execution."
        ),
        stats=[
            ("8", "Business Objectives", "objectives"),
            ("5", "Product Principles", "principles"),
            ("10", "Lifecycle Stages", "horizons"),
        ],
        pillars=[
            ("01", "Discover", "Business discovery and structured requirement analysis.", "align"),
            ("02", "Plan", "Roadmap prioritization aligned with customer and business value.", "standardize"),
            ("03", "Deliver", "Design, build, release, and continuously improve the platform.", "scale"),
        ],
        diagrams=[],
        markdown=markdown,
        body_post_process=chapter_three_body_post_process,
    )


def chapter_four_body_post_process(body_html: str) -> str:
    vision = visual_reference_html(*CHAPTER_FOUR_INLINE_DIAGRAM)
    principles = visual_reference_html(*CHAPTER_FOUR_SECOND_INLINE_DIAGRAM)
    diagrams = f"{vision}\n{principles}"
    return inject_html_after_heading(body_html, "Standardization", diagrams)


def chapter_four_html(markdown: str) -> str:
    return chapter_page_html(
        chapter_number=4,
        title="UI Engineering Vision",
        source_file="04-ui-engineering-vision.md",
        label="Chapter 04 UI Engineering Vision",
        kicker="Vision Context",
        quote=(
            "Modern UI Engineering is not about building screens. It is about building a scalable "
            "engineering platform that enables exceptional user experiences, consistent product "
            "delivery, and sustainable business growth."
        ),
        stats=[
            ("8", "Business Objectives", "objectives"),
            ("6", "Strategic Objectives", "principles"),
            ("12", "Engineering Responsibilities", "horizons"),
        ],
        pillars=[
            ("01", "Standardize", "Common engineering standards across every ERP module.", "align"),
            ("02", "Reuse", "Shared platform assets that reduce duplication and accelerate delivery.", "standardize"),
            ("03", "Scale", "Architecture, performance, and quality built for long-term growth.", "scale"),
        ],
        diagrams=[],
        markdown=markdown,
        body_post_process=chapter_four_body_post_process,
    )


def chapter_five_body_post_process(body_html: str) -> str:
    diagram = visual_reference_html(*CHAPTER_FIVE_INLINE_DIAGRAM)
    return inject_html_after_heading(body_html, "Drive Continuous Improvement", diagram)


def chapter_five_html(markdown: str) -> str:
    return chapter_page_html(
        chapter_number=5,
        title="UI Engineering Leadership",
        source_file="05-engineering-leadership.md",
        label="Chapter 05 UI Engineering Leadership",
        kicker="Leadership Context",
        quote=(
            "Engineering leadership is measured not by the authority it holds, but by the clarity "
            "of its vision, the strength of its teams, and the quality of the engineering culture "
            "it creates."
        ),
        stats=[
            ("8", "Business Objectives", "objectives"),
            ("5", "Leadership Responsibilities", "principles"),
            ("8", "Success Indicators", "horizons"),
        ],
        pillars=[
            ("01", "Direct", "Establish technical vision, standards, and architectural direction.", "align"),
            ("02", "Develop", "Invest in mentoring, growth, and knowledge sharing.", "standardize"),
            ("03", "Govern", "Reviews, metrics, and continuous improvement at scale.", "scale"),
        ],
        diagrams=[],
        markdown=markdown,
        body_post_process=chapter_five_body_post_process,
    )


def chapter_six_body_post_process(body_html: str) -> str:
    diagram = visual_reference_html(*CHAPTER_SIX_INLINE_DIAGRAM)
    return inject_html_after_heading(body_html, "Cross-Functional Collaboration", diagram)


def chapter_six_html(markdown: str) -> str:
    return chapter_page_html(
        chapter_number=6,
        title="UI Engineering Organization",
        source_file="06-ui-engineering-organization.md",
        label="Chapter 06 UI Engineering Organization",
        kicker="Organizational Context",
        quote=(
            "Scalable products are built by scalable organizations. Clear ownership, disciplined "
            "collaboration, and consistent engineering practices enable teams to deliver sustainable "
            "business value."
        ),
        stats=[
            ("8", "Business Objectives", "objectives"),
            ("4", "Organizational Principles", "principles"),
            ("6", "Core Team Roles", "horizons"),
        ],
        pillars=[
            ("01", "Own", "Clear ownership for every feature, module, and decision.", "align"),
            ("02", "Collaborate", "Intentional cross-functional communication and shared goals.", "standardize"),
            ("03", "Standardize", "Common practices that create consistency across teams.", "scale"),
        ],
        diagrams=[],
        markdown=markdown,
        body_post_process=chapter_six_body_post_process,
    )


def chapter_seven_body_post_process(body_html: str) -> str:
    diagram = visual_reference_html(*CHAPTER_SEVEN_INLINE_DIAGRAM)
    return inject_html_after_heading(body_html, "Modularity", diagram)


def chapter_seven_html(markdown: str) -> str:
    return chapter_page_html(
        chapter_number=7,
        title="Enterprise Frontend Architecture",
        source_file="07-enterprise-frontend-architecture.md",
        label="Chapter 07 Enterprise Frontend Architecture",
        kicker="Architecture Context",
        quote=(
            "Architecture is a long-term business investment. Well-designed systems enable "
            "organizations to innovate faster, scale confidently, and deliver consistent value "
            "over time."
        ),
        stats=[
            ("8", "Business Objectives", "objectives"),
            ("7", "Architectural Principles", "principles"),
            ("5", "Platform Layers", "horizons"),
        ],
        pillars=[
            ("01", "Modular", "Independent modules that support parallel development.", "align"),
            ("02", "Reusable", "Shared platform capabilities across every business module.", "standardize"),
            ("03", "Scalable", "Architecture built for growth, stability, and maintainability.", "scale"),
        ],
        diagrams=[],
        markdown=markdown,
        body_post_process=chapter_seven_body_post_process,
    )


def chapter_eight_body_post_process(body_html: str) -> str:
    diagram = visual_reference_html(*CHAPTER_EIGHT_INLINE_DIAGRAM)
    return inject_html_after_heading(body_html, "Simplicity", diagram)


def chapter_eight_html(markdown: str) -> str:
    return chapter_page_html(
        chapter_number=8,
        title="Design System Strategy",
        source_file="08-design-system.md",
        label="Chapter 08 Design System Strategy",
        kicker="Design System Context",
        quote=(
            "A Design System is the operational foundation of modern product development. It creates "
            "a shared language between Design, Product, and Engineering, enabling consistent user "
            "experiences and predictable software delivery."
        ),
        stats=[
            ("8", "Business Objectives", "objectives"),
            ("5", "Design Principles", "principles"),
            ("5", "Architecture Layers", "horizons"),
        ],
        pillars=[
            ("01", "Consistent", "Predictable layouts, patterns, and workflows across modules.", "align"),
            ("02", "Reusable", "Tokens, components, and patterns as the default strategy.", "standardize"),
            ("03", "Accessible", "Inclusive design integrated into every interface decision.", "scale"),
        ],
        diagrams=[],
        markdown=markdown,
        body_post_process=chapter_eight_body_post_process,
    )


def chapter_nine_body_post_process(body_html: str) -> str:
    diagram = visual_reference_html(*CHAPTER_NINE_INLINE_DIAGRAM)
    return inject_html_after_heading(body_html, "Foundation Components", diagram)


def chapter_nine_html(markdown: str) -> str:
    return chapter_page_html(
        chapter_number=9,
        title="Enterprise Component Library",
        source_file="09-enterprise-component-library.md",
        label="Chapter 09 Enterprise Component Library",
        kicker="Component Library Context",
        quote=(
            "A Component Library is more than a collection of reusable UI elements. It is an "
            "engineering platform that standardizes implementation, accelerates product delivery, "
            "and preserves consistency across every application."
        ),
        stats=[
            ("8", "Business Objectives", "objectives"),
            ("5", "Engineering Principles", "principles"),
            ("10", "Component Categories", "horizons"),
        ],
        pillars=[
            ("01", "Reuse", "Production-ready components adopted across every product.", "align"),
            ("02", "Compose", "Complex interfaces built from smaller building blocks.", "standardize"),
            ("03", "Govern", "Documentation, versioning, and quality at platform scale.", "scale"),
        ],
        diagrams=[],
        markdown=markdown,
        body_post_process=chapter_nine_body_post_process,
    )


def chapter_ten_body_post_process(body_html: str) -> str:
    diagram = visual_reference_html(*CHAPTER_TEN_INLINE_DIAGRAM)
    return inject_html_after_heading(body_html, "Maintainability", diagram)


def chapter_ten_html(markdown: str) -> str:
    return chapter_page_html(
        chapter_number=10,
        title="UI Engineering Standards",
        source_file="10-engineering-standards.md",
        label="Chapter 10 UI Engineering Standards",
        kicker="Standards Context",
        quote=(
            "Engineering standards are not created to restrict developers. They exist to create "
            "consistency, reduce unnecessary complexity, and enable teams to deliver reliable "
            "software at scale."
        ),
        stats=[
            ("8", "Business Objectives", "objectives"),
            ("5", "Core Principles", "principles"),
            ("7", "Standard Domains", "horizons"),
        ],
        pillars=[
            ("01", "Consistent", "Common patterns, structures, and naming across repositories.", "align"),
            ("02", "Readable", "Code that is easy to review, extend, and maintain.", "standardize"),
            ("03", "Reliable", "Quality, testing, and documentation built into every delivery.", "scale"),
        ],
        diagrams=[],
        markdown=markdown,
        body_post_process=chapter_ten_body_post_process,
    )


def chapter_eleven_body_post_process(body_html: str) -> str:
    diagram = visual_reference_html(*CHAPTER_ELEVEN_INLINE_DIAGRAM)
    return inject_html_after_heading(body_html, "Incremental Delivery", diagram)


def chapter_eleven_html(markdown: str) -> str:
    return chapter_page_html(
        chapter_number=11,
        title="UI Engineering Delivery Model",
        source_file="11-engineering-delivery-model.md",
        label="Chapter 11 UI Engineering Delivery Model",
        kicker="Delivery Context",
        quote=(
            "Consistent engineering delivery is achieved through disciplined execution, clear ownership, "
            "predictable processes, and continuous feedback. A successful delivery model enables teams "
            "to move quickly without compromising quality."
        ),
        stats=[
            ("8", "Business Objectives", "objectives"),
            ("5", "Delivery Principles", "principles"),
            ("10", "Delivery Stages", "horizons"),
        ],
        pillars=[
            ("01", "Plan", "Predictable planning aligned with customer and business value.", "align"),
            ("02", "Build", "Incremental delivery with quality embedded at every step.", "standardize"),
            ("03", "Improve", "Release, monitor, and refine through continuous feedback.", "scale"),
        ],
        diagrams=[],
        markdown=markdown,
        body_post_process=chapter_eleven_body_post_process,
    )


def chapter_twelve_body_post_process(body_html: str) -> str:
    diagram = visual_reference_html(*CHAPTER_TWELVE_INLINE_DIAGRAM)
    return inject_html_after_heading(body_html, "Quality Engineering", diagram, level=1)


def chapter_twelve_html(markdown: str) -> str:
    return chapter_page_html(
        chapter_number=12,
        title="Engineering Excellence Framework",
        source_file="12-engineering-excellence-framework.md",
        label="Chapter 12 Engineering Excellence Framework",
        kicker="Excellence Context",
        quote=(
            "Engineering excellence is achieved through disciplined execution, measurable quality, "
            "operational reliability, and a commitment to continuous improvement. It is not a "
            "milestone—it is an organizational capability."
        ),
        stats=[
            ("8", "Business Objectives", "objectives"),
            ("8", "Excellence Pillars", "principles"),
            ("5", "Core Outcomes", "horizons"),
        ],
        pillars=[
            ("01", "Quality", "Build right from the start with measurable standards.", "align"),
            ("02", "Perform", "Optimize for speed, reliability, and operational stability.", "standardize"),
            ("03", "Improve", "Learn, measure, and refine through continuous feedback.", "scale"),
        ],
        diagrams=[],
        markdown=markdown,
        body_post_process=chapter_twelve_body_post_process,
    )


def chapter_thirteen_body_post_process(body_html: str) -> str:
    diagram = visual_reference_html(*CHAPTER_THIRTEEN_INLINE_DIAGRAM)
    return inject_html_after_heading(body_html, "Development", diagram)


def chapter_thirteen_html(markdown: str) -> str:
    return chapter_page_html(
        chapter_number=13,
        title="AI-Augmented Engineering",
        source_file="13-ai-augmented-engineering.md",
        label="Chapter 13 AI-Augmented Engineering",
        kicker="AI Engineering Context",
        quote=(
            "Artificial Intelligence should enhance engineering capability, not replace engineering "
            "judgment. The strongest engineering organizations use AI to improve productivity while "
            "preserving architectural discipline, code quality, and human accountability."
        ),
        stats=[
            ("8", "Business Objectives", "objectives"),
            ("4", "Engineering Principles", "principles"),
            ("6", "AI Lifecycle Stages", "horizons"),
        ],
        pillars=[
            ("01", "Accountable", "Human ownership of architecture, quality, and decisions.", "align"),
            ("02", "Secure", "AI adoption governed by security and engineering discipline.", "standardize"),
            ("03", "Augment", "AI that accelerates design, build, test, and documentation.", "scale"),
        ],
        diagrams=[],
        markdown=markdown,
        body_post_process=chapter_thirteen_body_post_process,
    )


def chapter_fourteen_body_post_process(body_html: str) -> str:
    diagram = visual_reference_html(*CHAPTER_FOURTEEN_INLINE_DIAGRAM)
    return inject_html_after_heading(body_html, "Engineering Assessment", diagram)


def chapter_fourteen_html(markdown: str) -> str:
    return chapter_page_html(
        chapter_number=14,
        title="90-Day Transformation Roadmap",
        source_file="14-90-day-execution-plan.md",
        label="Chapter 14 90-Day Transformation Roadmap",
        kicker="Transformation Context",
        quote=(
            "Transformation is achieved through disciplined execution. Small, well-planned improvements "
            "delivered consistently create stronger engineering organizations than large initiatives "
            "executed without structure."
        ),
        stats=[
            ("8", "Business Objectives", "objectives"),
            ("3", "Execution Phases", "principles"),
            ("90", "Day Roadmap", "horizons"),
        ],
        pillars=[
            ("01", "Assess", "Foundation phase: standards, alignment, and quick wins.", "align"),
            ("02", "Standardize", "Acceleration phase: design system and delivery improvements.", "standardize"),
            ("03", "Scale", "Optimization phase: platform, AI, and governance at scale.", "scale"),
        ],
        diagrams=[],
        markdown=markdown,
        body_post_process=chapter_fourteen_body_post_process,
    )


def chapter_fifteen_body_post_process(body_html: str) -> str:
    diagram = visual_reference_html(*CHAPTER_FIFTEEN_INLINE_DIAGRAM)
    return inject_html_after_heading(body_html, "Engineering Maturity", diagram, level=1)


def chapter_fifteen_html(markdown: str) -> str:
    return chapter_page_html(
        chapter_number=15,
        title="Future Vision",
        source_file="15-future-vision.md",
        label="Chapter 15 Future Vision",
        kicker="Future Context",
        quote=(
            "The long-term success of an engineering organization is determined not by the technologies "
            "it adopts today, but by the engineering capabilities it continues to build over time."
        ),
        stats=[
            ("8", "Business Objectives", "objectives"),
            ("5", "Strategy Levels", "principles"),
            ("5", "Vision Horizons", "horizons"),
        ],
        pillars=[
            ("01", "Vision", "Long-term direction for platform, culture, and capability.", "align"),
            ("02", "Evolve", "Continuous platform innovation and engineering maturity.", "standardize"),
            ("03", "Sustain", "Leadership, measurement, and lasting organizational growth.", "scale"),
        ],
        diagrams=[],
        markdown=markdown,
        body_post_process=chapter_fifteen_body_post_process,
    )


def build_html() -> str:
    sections = []

    for path in ordered_markdown_files():
        if path.name == "00-cover.md" and COVER_BACKGROUND.exists() and BRAND_LOGO.exists():
            sections.append(
                f'<section class="chapter cover-page" data-source="{html.escape(path.name)}" '
                'aria-label="Frontend Engineering Playbook cover">\n'
                '<div class="cover-page-frame" aria-hidden="true"></div>\n'
                '<div class="cover-art">\n'
                f'<img src="{asset_src("cover/cover-background.png")}" alt="" aria-hidden="true">\n'
                '</div>\n'
                '<div class="cover-content">\n'
                '<div class="cover-panel">\n'
                '<header class="cover-brand">\n'
                '<div class="cover-logo-box">\n'
                f'<img class="cover-logo" src="{asset_src("brand/force-logo.png")}" alt="Force Intellect">\n'
                '</div>\n'
                '</header>\n'
                '<div class="cover-headline">\n'
                '<p class="cover-eyebrow">Enterprise ERP · UI Engineering</p>\n'
                '<h1 class="cover-title">\n'
                '<span class="cover-title-line">Frontend</span>\n'
                '<span class="cover-title-line cover-title-em">Engineering</span>\n'
                '<span class="cover-title-line cover-title-em">Playbook</span>\n'
                '</h1>\n'
                '<p class="cover-subtitle">Building a World-Class UI Engineering Organization for Enterprise ERP</p>\n'
                '<div class="cover-tags">\n'
                '<span>Architecture</span><span>Design Systems</span><span>Delivery</span>\n'
                '</div>\n'
                '<div class="cover-edition"><span class="cover-edition-icon"></span>Founder Edition 2026</div>\n'
                '</div>\n'
                '<footer class="cover-author">\n'
                '<span class="cover-author-label">Prepared by</span>\n'
                '<strong>Sanjay Kr. Singh</strong>\n'
                '<span class="cover-author-role">Tech Lead · Frontend Architect</span>\n'
                '</footer>\n'
                '</div>\n'
                '</div>\n'
                '</section>'
            )
            continue

        if GENERATE_COVER_ONLY:
            continue

        if path.name not in ACTIVE_PAGES:
            continue

        markdown = read_md(path)

        if path.name == "index.md":
            sections.append(preface_page_html())
            continue

        if path.name == "01-executive-summary.md":
            sections.append(chapter_one_html(markdown))
            continue

        if path.name == "02-business-strategy.md":
            sections.append(chapter_two_html(markdown))
            continue

        if path.name == "03-product-strategy.md":
            sections.append(chapter_three_html(markdown))
            continue

        if path.name == "04-ui-engineering-vision.md":
            sections.append(chapter_four_html(markdown))
            continue

        if path.name == "05-engineering-leadership.md":
            sections.append(chapter_five_html(markdown))
            continue

        if path.name == "06-ui-engineering-organization.md":
            sections.append(chapter_six_html(markdown))
            continue

        if path.name == "07-enterprise-frontend-architecture.md":
            sections.append(chapter_seven_html(markdown))
            continue

        if path.name == "08-design-system.md":
            sections.append(chapter_eight_html(markdown))
            continue

        if path.name == "09-enterprise-component-library.md":
            sections.append(chapter_nine_html(markdown))
            continue

        if path.name == "10-engineering-standards.md":
            sections.append(chapter_ten_html(markdown))
            continue

        if path.name == "11-engineering-delivery-model.md":
            sections.append(chapter_eleven_html(markdown))
            continue

        if path.name == "12-engineering-excellence-framework.md":
            sections.append(chapter_twelve_html(markdown))
            continue

        if path.name == "13-ai-augmented-engineering.md":
            sections.append(chapter_thirteen_html(markdown))
            continue

        if path.name == "14-90-day-execution-plan.md":
            sections.append(chapter_fourteen_html(markdown))
            continue

        if path.name == "15-future-vision.md":
            sections.append(chapter_fifteen_html(markdown))
            continue

        sections.append(
            f'<section class="chapter content-page" data-source="{html.escape(path.name)}" '
            f'data-label="{html.escape(chapter_label(path))}">\n'
            '<div class="page-watermark">FI</div>\n'
            '<header class="page-header">\n'
            f'<img src="{asset_src("brand/force-logo.png")}" alt="Force Intellect">\n'
            '<span>Frontend Engineering Playbook</span>\n'
            '</header>\n'
            '<div class="chapter-shell">\n'
            '<div class="chapter-ribbon">Force Intellect Playbook</div>\n'
            f"{markdown_to_html(markdown)}\n"
            "</div>\n"
            f"{page_footer_html()}"
            "</section>"
        )

    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Enterprise ERP UI Engineering Strategy & Execution Blueprint</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@500;600;700;800&display=swap" rel="stylesheet">
  <style>
    :root {{
      --ink: #182236;
      --muted: #5d6b82;
      --blue: #082f8f;
      --blue-dark: #061f63;
      --blue-soft: #eef4ff;
      --line: #d7e0ee;
      --paper: #ffffff;
      --canvas: #eef2f7;
      --gold: #d9a441;
      --page-frame-inset: 6mm;
      --page-gutter-left: var(--page-frame-inset);
      --page-gutter-right: var(--page-frame-inset);
      --cover-gutter-left: 14mm;
      --cover-gutter-right: 8mm;
    }}
    @page {{ size: A4; margin: 0; }}
    @page cover {{ size: A4; margin: 0; }}
    * {{ box-sizing: border-box; }}
    html {{
      background: var(--canvas);
    }}
    body {{
      margin: 0;
      color: var(--ink);
      background: var(--canvas);
      font-family: "Segoe UI", Arial, Helvetica, sans-serif;
      font-size: 10.8pt;
      line-height: 1.62;
    }}
    .chapter {{
      position: relative;
      break-after: page;
      page-break-after: always;
      background: var(--paper);
    }}
    .cover-page {{
      page: cover;
      width: 210mm;
      height: 297mm;
      overflow: hidden;
      background: #ffffff;
    }}
    .cover-page-frame {{
      position: absolute;
      inset: 6mm;
      z-index: 3;
      border: 1px solid #d5e0f2;
      border-radius: 2mm;
      pointer-events: none;
    }}
    .cover-page-frame::before {{
      content: "";
      position: absolute;
      top: 0;
      left: 0;
      right: 0;
      height: 1.4mm;
      border-radius: 2mm 2mm 0 0;
      background: linear-gradient(90deg, var(--blue-dark), var(--blue), #3b7bd6);
    }}
    .cover-page-frame::after {{
      content: "";
      position: absolute;
      left: 6mm;
      bottom: 6mm;
      width: 18mm;
      height: 0.35mm;
      background: linear-gradient(90deg, var(--gold), transparent);
      border-radius: 999px;
    }}
    .cover-art {{
      position: absolute;
      inset: 0;
      width: 100%;
      height: 100%;
      min-height: 297mm;
      overflow: hidden;
      pointer-events: none;
    }}
    .cover-art img {{
      position: absolute;
      top: 0;
      right: 0;
      height: 100%;
      min-height: 297mm;
      width: auto;
      max-width: none;
      display: block;
      object-fit: cover;
      object-position: right center;
    }}
    .cover-content {{
      position: relative;
      z-index: 2;
      width: 100%;
      height: 100%;
      padding: 14mm var(--cover-gutter-right) 14mm var(--cover-gutter-left);
      font-family: "Plus Jakarta Sans", "Segoe UI", Arial, sans-serif;
    }}
    .cover-panel {{
      position: relative;
      width: 118mm;
      height: 100%;
      display: flex;
      flex-direction: column;
      padding: 4mm 5mm 0 0;
    }}
    .cover-panel::before {{
      content: "";
      position: absolute;
      inset: 0 -6mm 0 -16mm;
      background: linear-gradient(90deg, rgba(255, 255, 255, 0.55), rgba(255, 255, 255, 0.08) 72%, transparent);
      pointer-events: none;
    }}
    .cover-brand {{
      margin-bottom: 4mm;
    }}
    .cover-logo-box {{
      display: inline-block;
      padding: 3mm 4.5mm;
      background: #ffffff;
      border-radius: 2mm;
      box-shadow: 0 3px 12px rgba(8, 47, 143, 0.14);
    }}
    .cover-logo {{
      display: block;
      width: 54mm;
      max-height: 13mm;
      object-fit: contain;
      object-position: left center;
    }}
    .cover-brand,
    .cover-headline,
    .cover-author {{
      position: relative;
      z-index: 1;
    }}
    .cover-headline {{
      margin-top: auto;
      margin-bottom: auto;
      padding: 6mm 0 4mm;
    }}
    .cover-eyebrow {{
      margin: 0 0 4mm;
      color: var(--blue);
      font-size: 7pt;
      font-weight: 800;
      letter-spacing: 0.28em;
      text-transform: uppercase;
    }}
    .cover-title {{
      margin: 0;
      padding: 0;
      border: 0;
      display: flex;
      flex-direction: column;
      gap: 0.5mm;
    }}
    .cover-title-line {{
      display: block;
      color: #1a3366;
      font-size: 19pt;
      line-height: 1;
      font-weight: 700;
      letter-spacing: -0.02em;
      text-transform: uppercase;
    }}
    .cover-title-em {{
      color: var(--blue-dark);
      font-size: 34pt;
      line-height: 0.94;
      font-weight: 800;
      letter-spacing: -0.04em;
    }}
    .cover-subtitle {{
      max-width: 92mm;
      margin: 7mm 0 5mm;
      color: #2a3850;
      font-size: 10.6pt;
      line-height: 1.52;
      font-weight: 600;
    }}
    .cover-tags {{
      display: flex;
      flex-wrap: wrap;
      gap: 2mm;
      margin-bottom: 6mm;
    }}
    .cover-tags span {{
      display: inline-flex;
      align-items: center;
      min-height: 7mm;
      padding: 0 3.2mm;
      border-radius: 999px;
      color: #24416f;
      background: rgba(255, 255, 255, 0.88);
      border: 1px solid #d7e4f7;
      font-size: 6.6pt;
      font-weight: 800;
      letter-spacing: 0.08em;
      text-transform: uppercase;
    }}
    .cover-edition {{
      display: inline-flex;
      align-items: center;
      gap: 3mm;
      min-height: 11mm;
      padding: 0 7mm 0 4mm;
      border-radius: 999px;
      color: #ffffff;
      background: linear-gradient(135deg, #04184f 0%, var(--blue-dark) 35%, var(--blue) 100%);
      border: 1px solid rgba(255, 255, 255, 0.2);
      box-shadow:
        0 16px 36px rgba(8, 47, 143, 0.32),
        inset 0 1px 0 rgba(255, 255, 255, 0.2);
      font-size: 8.2pt;
      font-weight: 800;
      letter-spacing: 0.16em;
      text-transform: uppercase;
    }}
    .cover-edition-icon {{
      width: 5mm;
      height: 5mm;
      border-radius: 50%;
      background: linear-gradient(135deg, var(--gold), #f0d080);
      box-shadow: 0 0 0 1mm rgba(255, 255, 255, 0.35);
      flex-shrink: 0;
    }}
    .cover-author {{
      display: flex;
      flex-direction: column;
      gap: 1mm;
      width: 100%;
      padding-bottom: 2mm;
    }}
    .cover-author-label {{
      color: #7a8799;
      font-size: 6.5pt;
      font-weight: 600;
      letter-spacing: 0.08em;
      text-transform: uppercase;
    }}
    .cover-author strong {{
      color: var(--blue-dark);
      font-size: 11pt;
      line-height: 1.2;
      font-weight: 700;
    }}
    .cover-author-role {{
      color: #4a5568;
      font-size: 8pt;
      font-weight: 500;
    }}
    .preface-page {{
      padding: 0;
      background: #ffffff;
      font-family: "Plus Jakarta Sans", "Segoe UI", Arial, sans-serif;
    }}
    .content-page.preface-page {{
      padding: 0;
      min-height: 297mm;
      background: #ffffff;
    }}
    .content-page.preface-page::before {{
      display: none;
    }}
    .content-page.preface-page .cover-page-frame {{
      display: none;
    }}
    .content-page.preface-page::after {{
      display: none;
    }}
    .content-page.chapter-page {{
      padding: 0;
      min-height: 297mm;
      background: #ffffff;
      font-family: "Plus Jakarta Sans", "Segoe UI", Arial, sans-serif;
    }}
    .content-page.chapter-page::before {{
      display: none;
    }}
    .content-page.chapter-page .cover-page-frame {{
      display: none;
    }}
    .overview-page.chapter-page {{
      padding: 0;
    }}
    .chapter-page .chapter-header {{
      width: 100%;
      margin: 0 0 6mm;
      padding: 5mm var(--page-gutter-right) 6mm var(--page-gutter-left);
      border-radius: 0;
    }}
    .chapter-page .chapter-header-logo {{
      right: var(--page-gutter-right);
    }}
    .chapter-page .chapter-header-watermark {{
      right: calc(var(--page-gutter-right) + 2mm);
    }}
    .chapter-01-content {{
      margin: 0 var(--page-gutter-right) 14mm var(--page-gutter-left);
    }}
    .chapter-01-lead {{
      position: relative;
      margin-bottom: 4.5mm;
      padding: 3.5mm 0 4mm;
      border-radius: 2mm;
      background: #ffffff;
      border: 1px solid #e3ebf7;
      box-shadow: 0 3px 14px rgba(8, 47, 143, 0.06);
      overflow: hidden;
    }}
    .chapter-01-lead::before {{
      content: "";
      position: absolute;
      top: 0;
      left: 0;
      width: 100%;
      height: 0.6mm;
      background: linear-gradient(90deg, var(--gold), #f0d080 40%, var(--blue) 100%);
    }}
    .chapter-01-lead-head {{
      display: flex;
      align-items: center;
      gap: 2mm;
      margin-bottom: 2.5mm;
      padding: 0 3mm;
    }}
    .chapter-01-lead-icon {{
      width: 5.5mm;
      height: 5.5mm;
      border-radius: 50%;
      background: linear-gradient(135deg, #7c3aed, #6366f1);
      flex-shrink: 0;
    }}
    .chapter-01-kicker {{
      margin: 0;
      color: var(--blue-dark);
      font-size: 6.4pt;
      font-weight: 800;
      letter-spacing: 0.14em;
      text-transform: uppercase;
    }}
    .chapter-01-quote {{
      position: relative;
      margin: 0 3mm;
      padding: 0.5mm 0 0.5mm 4.5mm;
      border: 0;
      border-left: 0.65mm solid var(--gold);
      background: transparent;
      color: #1e293b;
      font-size: 9pt;
      line-height: 1.58;
      font-style: italic;
    }}
    .chapter-01-quote em {{
      font-style: italic;
    }}
    .chapter-01-block {{
      margin-bottom: 4.5mm;
      padding: 3mm 0 3.5mm;
      border-radius: 2mm;
      background: #ffffff;
      border: 1px solid #e3ebf7;
      box-shadow: 0 2px 12px rgba(8, 47, 143, 0.05);
    }}
    .chapter-01-block-head {{
      display: flex;
      align-items: center;
      gap: 2.2mm;
      margin-bottom: 3mm;
      padding: 0 3mm 2mm;
      border-bottom: 1px solid #edf2f7;
    }}
    .chapter-01-block-head h3 {{
      margin: 0;
      padding: 0;
      border: 0;
      color: var(--blue-dark);
      font-size: 6.8pt;
      font-weight: 800;
      letter-spacing: 0.12em;
      text-transform: uppercase;
    }}
    .chapter-01-block-icon {{
      width: 5mm;
      height: 5mm;
      border-radius: 50%;
      flex-shrink: 0;
    }}
    .chapter-01-block-icon-blue {{
      background: linear-gradient(135deg, var(--blue-dark), var(--blue));
    }}
    .chapter-01-block-icon-gold {{
      background: linear-gradient(135deg, #d97706, var(--gold));
    }}
    .chapter-01-stats {{
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 2.2mm;
      padding: 0 3mm;
    }}
    .chapter-01-stat {{
      position: relative;
      padding: 3mm 2mm 2.8mm;
      border-radius: 1.8mm;
      background: linear-gradient(180deg, #fafbfd 0%, #ffffff 100%);
      border: 1px solid #e8eef6;
      text-align: center;
      overflow: hidden;
    }}
    .chapter-01-stat-objectives {{
      border-top: 0.65mm solid var(--blue);
    }}
    .chapter-01-stat-principles {{
      border-top: 0.65mm solid var(--gold);
    }}
    .chapter-01-stat-horizons {{
      border-top: 0.65mm solid #0d9488;
    }}
    .chapter-01-stat-value {{
      display: block;
      color: var(--blue-dark);
      font-size: 16pt;
      line-height: 1;
      font-weight: 800;
      letter-spacing: -0.03em;
    }}
    .chapter-01-stat-principles .chapter-01-stat-value {{
      color: #92400e;
    }}
    .chapter-01-stat-horizons .chapter-01-stat-value {{
      color: #0f766e;
    }}
    .chapter-01-stat-label {{
      display: block;
      margin-top: 1.2mm;
      color: #64748b;
      font-size: 5.8pt;
      font-weight: 700;
      letter-spacing: 0.07em;
      text-transform: uppercase;
      line-height: 1.25;
    }}
    .chapter-page .chapter-diagram {{
      margin-bottom: 4.5mm;
      border-radius: 2mm;
      border: 1px solid #e3ebf7;
      background: #ffffff;
      box-shadow: 0 3px 14px rgba(8, 47, 143, 0.06);
      overflow: hidden;
    }}
    .chapter-page .chapter-diagram img {{
      display: block;
      width: 100%;
      height: auto;
    }}
    .chapter-page .chapter-diagram figcaption {{
      padding: 2mm 3mm;
      background: linear-gradient(90deg, var(--blue-dark), var(--blue));
      color: rgba(255, 255, 255, 0.92);
      font-size: 5.8pt;
      font-weight: 700;
      letter-spacing: 0.12em;
      text-transform: uppercase;
      text-align: center;
    }}
    .visual-reference {{
      margin: 3mm 0 4.5mm;
      border-radius: 2mm;
      overflow: hidden;
      background: #ffffff;
      border: 1px solid #e3ebf7;
      box-shadow: 0 3px 14px rgba(8, 47, 143, 0.06);
      break-inside: avoid;
      page-break-inside: avoid;
    }}
    .visual-reference + .visual-reference {{
      margin-top: 2mm;
    }}
    .visual-reference-bar {{
      min-height: 5.5mm;
      padding: 0 3mm;
      display: flex;
      align-items: center;
      background: linear-gradient(90deg, var(--blue-dark), var(--blue), #0d9488);
      color: rgba(255, 255, 255, 0.94);
      font-size: 5.6pt;
      font-weight: 800;
      letter-spacing: 0.14em;
      text-transform: uppercase;
    }}
    .visual-reference-figure {{
      margin: 0;
      padding: 0;
      background: #ffffff;
    }}
    .visual-reference-figure img {{
      display: block;
      width: 100%;
      height: auto;
    }}
    .visual-reference-caption {{
      margin: 0;
      min-height: 6mm;
      padding: 0 3mm;
      display: flex;
      align-items: center;
      gap: 1mm;
      border-top: 1px solid #edf2f7;
      background: linear-gradient(180deg, #f8fafc 0%, #ffffff 100%);
      color: var(--blue-dark);
      font-size: 5.8pt;
      font-weight: 700;
      letter-spacing: 0.03em;
      line-height: 1;
      white-space: nowrap;
    }}
    .visual-reference-caption span {{
      color: var(--gold);
      flex-shrink: 0;
    }}
    .chapter-01-pillars {{
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 2.2mm;
      padding: 0 3mm;
    }}
    .chapter-01-pillar {{
      position: relative;
      padding: 3mm 2.8mm 2.8mm;
      border-radius: 1.8mm;
      background: #fafbfd;
      border: 1px solid #e8eef6;
    }}
    .chapter-01-pillar-align {{
      border-left: 0.65mm solid var(--blue);
    }}
    .chapter-01-pillar-standardize {{
      border-left: 0.65mm solid var(--gold);
    }}
    .chapter-01-pillar-scale {{
      border-left: 0.65mm solid #0d9488;
    }}
    .chapter-01-pillar-num {{
      display: inline-flex;
      align-items: center;
      justify-content: center;
      min-width: 6mm;
      height: 5.5mm;
      margin-bottom: 1.8mm;
      padding: 0 1.5mm;
      border-radius: 999px;
      background: rgba(8, 47, 143, 0.08);
      color: var(--blue-dark);
      font-size: 5.4pt;
      font-weight: 800;
      letter-spacing: 0.06em;
    }}
    .chapter-01-pillar-standardize .chapter-01-pillar-num {{
      background: rgba(217, 164, 65, 0.14);
      color: #92400e;
    }}
    .chapter-01-pillar-scale .chapter-01-pillar-num {{
      background: rgba(13, 148, 136, 0.12);
      color: #0f766e;
    }}
    .chapter-01-pillars strong {{
      display: block;
      color: var(--blue-dark);
      font-size: 8.8pt;
      font-weight: 800;
      margin-bottom: 1mm;
    }}
    .chapter-01-pillars p {{
      margin: 0;
      color: #475569;
      font-size: 7pt;
      line-height: 1.45;
      font-weight: 500;
    }}
    .chapter-01-body {{
      position: relative;
      z-index: 2;
      padding: 3.5mm 3mm 1mm;
      border-radius: 2mm;
      background: #ffffff;
      border: 1px solid #e3ebf7;
      box-shadow: 0 2px 12px rgba(8, 47, 143, 0.04);
    }}
    .chapter-01-body h1 {{
      max-width: none;
      margin: 5mm 0 3mm;
      padding: 0 0 0 3mm;
      border: 0;
      border-left: 0.65mm solid var(--blue);
      color: var(--blue-dark);
      font-size: 9.5pt;
      font-weight: 800;
      letter-spacing: 0.08em;
      text-transform: uppercase;
      line-height: 1.2;
    }}
    .chapter-01-body h1::after {{
      display: none;
    }}
    .chapter-01-body h1:first-child {{
      margin-top: 0;
    }}
    .chapter-01-body h2 {{
      margin: 3.5mm 0 2mm;
      padding: 1.8mm 2.5mm 1.8mm 4mm;
      border-radius: 1.5mm;
      background: #f8fafc;
      border: 1px solid #edf2f7;
      color: #1e3a5f;
      font-size: 8.8pt;
      font-weight: 800;
    }}
    .chapter-01-body h2::before {{
      top: 50%;
      transform: translateY(-50%);
      height: 50%;
      background: var(--gold);
    }}
    .chapter-01-body h3 {{
      margin: 3mm 0 1.5mm;
      color: #24416f;
      font-size: 8.4pt;
      font-weight: 800;
    }}
    .chapter-01-body p {{
      margin: 0 0 2.2mm;
      color: #334155;
      font-size: 8.6pt;
      line-height: 1.52;
    }}
    .chapter-01-body ul {{
      margin: 1mm 0 3.5mm;
      padding: 2.2mm 2.8mm;
      border-radius: 1.5mm;
      background: #f8fafc;
      border: 1px solid #edf2f7;
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 1mm 3mm;
    }}
    .chapter-01-body li {{
      margin: 0;
      padding-left: 4.5mm;
      color: #334155;
      font-size: 8.2pt;
      line-height: 1.4;
    }}
    .chapter-01-body li::before {{
      top: 0.5em;
      width: 1.8mm;
      height: 1.8mm;
      background: var(--blue);
      box-shadow: none;
    }}
    .chapter-01-body hr {{
      height: 0;
      border: 0;
      margin: 4mm 0;
      border-top: 1px dashed #dbe3ef;
    }}
    .chapter-01-body blockquote {{
      margin: 2.5mm 0;
      padding: 2.5mm 3mm;
      border-left: 0.6mm solid var(--gold);
      border-radius: 0 1.5mm 1.5mm 0;
      background: #fffbeb;
      color: #78350f;
      font-size: 8.2pt;
      box-shadow: none;
    }}
    .page-footer {{
      position: absolute;
      left: 0;
      right: 0;
      bottom: 0;
      z-index: 4;
      background: linear-gradient(180deg, #f8fafc 0%, #f1f5f9 100%);
      border-top: 0.25mm solid #e2e8f0;
    }}
    .page-footer-inner {{
      display: grid;
      grid-template-columns: 1fr auto auto;
      align-items: center;
      gap: 4mm;
      min-height: 10mm;
      padding: 2.5mm var(--page-gutter-right) 2.8mm var(--page-gutter-left);
    }}
    .page-footer-brand {{
      display: flex;
      align-items: center;
      gap: 2.5mm;
      min-width: 0;
    }}
    .page-footer-accent {{
      width: 0.7mm;
      height: 5mm;
      border-radius: 999px;
      background: linear-gradient(180deg, var(--gold) 0%, #e8c46a 100%);
      flex-shrink: 0;
    }}
    .page-footer-copy {{
      display: flex;
      flex-direction: column;
      gap: 0.5mm;
      min-width: 0;
    }}
    .page-footer-copy strong {{
      color: var(--blue-dark);
      font-size: 6.4pt;
      font-weight: 800;
      letter-spacing: 0.1em;
      text-transform: uppercase;
      line-height: 1.15;
    }}
    .page-footer-copy span {{
      color: #94a3b8;
      font-size: 5.6pt;
      font-weight: 500;
      letter-spacing: 0.03em;
      line-height: 1.2;
    }}
    .page-footer-github {{
      color: var(--blue);
      font-size: 5.4pt;
      font-weight: 600;
      letter-spacing: 0.02em;
      line-height: 1.2;
      text-decoration: none;
    }}
    .page-footer-github:hover {{
      text-decoration: underline;
    }}
    .page-footer-label {{
      color: #64748b;
      font-size: 5.6pt;
      font-weight: 600;
      letter-spacing: 0.12em;
      text-transform: uppercase;
      white-space: nowrap;
    }}
    .page-footer-badge {{
      display: inline-flex;
      align-items: center;
      min-height: 5.2mm;
      padding: 0 3mm;
      border-radius: 999px;
      background: rgba(255, 255, 255, 0.72);
      border: 0.25mm solid #e2e8f0;
      color: #64748b;
      font-size: 5.4pt;
      font-weight: 700;
      letter-spacing: 0.14em;
      text-transform: uppercase;
      white-space: nowrap;
      box-shadow: 0 1px 2px rgba(15, 23, 42, 0.04);
    }}
    .preface-page::before,
    .preface-page::after {{
      display: none;
    }}
    .preface-hero {{
      position: relative;
      z-index: 2;
      width: 100%;
      margin: 0;
      padding: 5mm var(--page-gutter-right) 4.5mm var(--page-gutter-left);
      border-radius: 0;
      background: linear-gradient(135deg, #04184f 0%, #061f63 52%, #0a3080 100%);
      color: #ffffff;
    }}
    .preface-hero-top {{
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 4mm;
      margin-bottom: 3mm;
    }}
    .preface-kicker {{
      color: var(--gold);
      font-size: 6pt;
      font-weight: 800;
      letter-spacing: 0.18em;
      text-transform: uppercase;
    }}
    .preface-edition {{
      display: inline-flex;
      align-items: center;
      min-height: 6mm;
      padding: 0 3mm;
      border-radius: 999px;
      background: rgba(255, 255, 255, 0.12);
      border: 0.3mm solid rgba(255, 255, 255, 0.22);
      color: #ffffff;
      font-size: 5.6pt;
      font-weight: 700;
      letter-spacing: 0.1em;
      text-transform: uppercase;
      white-space: nowrap;
    }}
    .preface-hero h1 {{
      margin: 0 0 4mm;
      padding: 0;
      border: 0;
      max-width: 118mm;
      color: #ffffff;
      font-size: 17pt;
      line-height: 1.08;
      font-weight: 800;
      letter-spacing: -0.02em;
    }}
    .preface-metrics {{
      display: grid;
      grid-template-columns: repeat(5, 1fr);
      gap: 0;
      padding-top: 3mm;
      border-top: 0.3mm solid rgba(255, 255, 255, 0.16);
    }}
    .preface-metrics > div {{
      position: relative;
      padding: 0 2mm;
      text-align: center;
    }}
    .preface-metrics > div + div::before {{
      content: "";
      position: absolute;
      left: 0;
      top: 0.5mm;
      bottom: 0.5mm;
      width: 0.3mm;
      background: rgba(255, 255, 255, 0.18);
    }}
    .preface-metrics strong {{
      display: block;
      color: var(--gold);
      font-size: 14pt;
      line-height: 1;
      font-weight: 800;
    }}
    .preface-metrics span {{
      display: block;
      margin-top: 1mm;
      color: rgba(255, 255, 255, 0.88);
      font-size: 5.4pt;
      font-weight: 700;
      letter-spacing: 0.1em;
      text-transform: uppercase;
    }}
    .preface-grid {{
      position: relative;
      z-index: 2;
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 3mm;
      margin: 0 var(--page-gutter-right) 0 var(--page-gutter-left);
      padding: 4mm 0 14mm;
      background: #ffffff;
    }}
    .preface-card {{
      break-inside: avoid;
      page-break-inside: avoid;
      border-radius: 2mm;
      background: #ffffff;
      border: 0.3mm solid #dce7fb;
      box-shadow: 0 2px 10px rgba(8, 47, 143, 0.06);
      overflow: hidden;
    }}
    .preface-card-head {{
      display: flex;
      align-items: center;
      gap: 2.5mm;
      padding: 2.8mm 3.5mm 2.2mm;
      border-bottom: 0.3mm solid #edf2fb;
    }}
    .preface-card-head h3 {{
      margin: 0;
      padding: 0;
      border: 0;
      color: var(--blue-dark);
      font-size: 6.6pt;
      font-weight: 800;
      letter-spacing: 0.12em;
      text-transform: uppercase;
    }}
    .preface-icon {{
      width: 6mm;
      height: 6mm;
      border-radius: 50%;
      flex-shrink: 0;
      background-repeat: no-repeat;
      background-position: center;
      background-size: 58%;
    }}
    .preface-icon-purple {{
      background-color: #7c3aed;
      background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' fill='white' viewBox='0 0 24 24'%3E%3Cpath d='M6 2h9l5 5v15a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2zm8 1.5V8h4.5'/%3E%3C/svg%3E");
    }}
    .preface-icon-orange {{
      background-color: #ea580c;
      background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' fill='white' viewBox='0 0 24 24'%3E%3Cpath d='M12 2a10 10 0 1 0 0 20 10 10 0 0 0 0-20zm1 5v5l4 2'/%3E%3C/svg%3E");
    }}
    .preface-icon-gold {{
      background-color: #d97706;
      background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' fill='white' viewBox='0 0 24 24'%3E%3Cpath d='M12 2l2.4 7.4H22l-6 4.6 2.3 7L12 17.8 5.7 21.1 8 14 2 9.4h7.6z'/%3E%3C/svg%3E");
    }}
    .preface-icon-violet {{
      background-color: #6366f1;
      background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' fill='white' viewBox='0 0 24 24'%3E%3Cpath d='M12 12a4 4 0 1 0-4-4 4 4 0 0 0 4 4zm0 2c-4.4 0-8 2.2-8 5v1h16v-1c0-2.8-3.6-5-8-5z'/%3E%3C/svg%3E");
    }}
    .preface-icon-green {{
      background-color: #059669;
      background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' fill='white' viewBox='0 0 24 24'%3E%3Cpath d='M4 6h16v2H4V6zm0 5h16v2H4v-2zm0 5h16v2H4v-2z'/%3E%3C/svg%3E");
    }}
    .preface-icon-blue {{
      background-color: #2563eb;
      background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' fill='white' viewBox='0 0 24 24'%3E%3Cpath d='M10 4a6 6 0 1 0 4.9 9.5l4.8 4.8 1.4-1.4-4.8-4.8A6 6 0 0 0 10 4zm0 2a4 4 0 1 1-4 4 4 4 0 0 1 4-4z'/%3E%3C/svg%3E");
    }}
    .preface-card-body {{
      padding: 2.8mm 3.5mm 3.2mm;
      color: #334155;
      font-size: 6.8pt;
      line-height: 1.45;
    }}
    .preface-card-body p {{
      margin: 0 0 2mm;
    }}
    .preface-card-body p:last-child {{
      margin-bottom: 0;
    }}
    .preface-card-body ul {{
      margin: 0;
      padding: 0;
      list-style: none;
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 1mm 3mm;
    }}
    .preface-card-body ul li {{
      position: relative;
      padding-left: 3mm;
    }}
    .preface-card-body ul li::before {{
      content: "";
      position: absolute;
      left: 0;
      top: 1.6mm;
      width: 1.2mm;
      height: 1.2mm;
      border-radius: 50%;
      background: var(--blue);
    }}
    .preface-info {{
      margin: 0;
      display: grid;
      grid-template-columns: auto 1fr;
      gap: 1.2mm 3mm;
      align-items: center;
    }}
    .preface-info dt {{
      margin: 0;
      color: #64748b;
      font-size: 6.2pt;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.06em;
    }}
    .preface-info dd {{
      margin: 0;
      color: #1e293b;
      font-size: 6.8pt;
      font-weight: 600;
    }}
    .preface-badge {{
      display: inline-flex;
      align-items: center;
      min-height: 5mm;
      padding: 0 2.5mm;
      border-radius: 999px;
      font-size: 5.8pt;
      font-weight: 700;
      letter-spacing: 0.04em;
    }}
    .preface-badge-green {{
      color: #166534;
      background: #dcfce7;
      border: 0.3mm solid #bbf7d0;
    }}
    .preface-badge-gold {{
      color: #92400e;
      background: #fef3c7;
      border: 0.3mm solid #fde68a;
    }}
    .preface-pills {{
      display: flex;
      flex-wrap: wrap;
      gap: 1.5mm;
    }}
    .preface-pills span {{
      display: inline-flex;
      align-items: center;
      min-height: 5.5mm;
      padding: 0 2.5mm;
      border-radius: 999px;
      background: #eef4ff;
      border: 0.3mm solid #dbeafe;
      color: #1e40af;
      font-size: 5.8pt;
      font-weight: 600;
      line-height: 1.2;
    }}
    .preface-pills span:nth-child(even) {{
      background: #f5f3ff;
      border-color: #e9d5ff;
      color: #5b21b6;
    }}
    .preface-scope {{
      margin: 0;
      padding: 0;
      list-style: none;
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 1mm 2.5mm;
      counter-reset: scope;
    }}
    .preface-scope li {{
      display: flex;
      align-items: baseline;
      gap: 1.5mm;
      font-size: 6.2pt;
      line-height: 1.35;
    }}
    .preface-scope li strong {{
      color: var(--blue);
      font-size: 6.4pt;
      font-weight: 800;
      min-width: 4mm;
    }}
    .preface-scope li span {{
      color: #334155;
      font-weight: 600;
    }}
    .preface-callout {{
      margin-top: 2.5mm;
      padding: 2.5mm 3mm;
      border-radius: 1.5mm;
      background: #eef6ff;
      border: 0.3mm solid #dbeafe;
      color: #1e3a5f;
      font-size: 6.4pt;
      line-height: 1.45;
    }}
    .overview-page {{
      padding: 14mm 14mm 16mm;
      font-family: "Plus Jakarta Sans", "Segoe UI", Arial, sans-serif;
    }}
    .overview-page::before {{
      display: none;
    }}
    .overview-page::after {{
      display: none;
    }}
    .page-topbar {{
      position: relative;
      z-index: 2;
      display: flex;
      flex-direction: column;
      align-items: flex-end;
      gap: 1mm;
      margin-bottom: 7mm;
      padding-bottom: 3.5mm;
      border-bottom: 0.35mm solid #e3ebf7;
      text-align: right;
    }}
    .page-topbar-title {{
      color: var(--blue-dark);
      font-size: 8.6pt;
      font-weight: 800;
      letter-spacing: 0.14em;
      text-transform: uppercase;
    }}
    .page-topbar-number {{
      color: #94a3b8;
      font-size: 22pt;
      font-weight: 800;
      line-height: 1;
      letter-spacing: -0.03em;
    }}
    .chapter-header {{
      position: relative;
      z-index: 2;
      margin-bottom: 6mm;
      padding: 5mm 6mm 6mm;
      border-radius: 2mm;
      overflow: hidden;
      background: linear-gradient(135deg, #04184f 0%, #061f63 52%, #0a3080 100%);
    }}
    .chapter-header-watermark {{
      position: absolute;
      right: 5mm;
      top: 50%;
      transform: translateY(-46%);
      color: rgba(255, 255, 255, 0.1);
      font-size: 54pt;
      font-weight: 800;
      line-height: 1;
      letter-spacing: -0.05em;
      pointer-events: none;
    }}
    .chapter-header-logo {{
      position: absolute;
      top: 4mm;
      right: 5mm;
      z-index: 2;
      width: 36mm;
      max-height: 9mm;
      object-fit: contain;
      object-position: right center;
      filter: brightness(1.08);
    }}
    .chapter-header-copy {{
      position: relative;
      z-index: 1;
      max-width: 72%;
    }}
    .chapter-header-badge {{
      display: inline-flex;
      align-items: center;
      min-height: 6.5mm;
      padding: 0 3.5mm;
      border: 0.35mm solid var(--gold);
      border-radius: 999px;
      color: var(--gold);
      font-size: 6.4pt;
      font-weight: 800;
      letter-spacing: 0.2em;
      text-transform: uppercase;
    }}
    .chapter-header-title {{
      margin: 3mm 0 3.5mm;
      padding: 0;
      border: 0;
      color: #ffffff;
      font-size: 23pt;
      line-height: 1.05;
      font-weight: 800;
      letter-spacing: -0.02em;
    }}
    .chapter-header-line {{
      display: block;
      width: 30mm;
      height: 0.55mm;
      border-radius: 999px;
      background: linear-gradient(90deg, var(--gold) 0%, #4fd1c5 100%);
    }}
    .overview-hero {{
      position: relative;
      z-index: 2;
      margin-bottom: 6mm;
    }}
    .overview-kicker {{
      margin: 0 0 3mm;
      color: var(--blue);
      font-size: 7pt;
      font-weight: 800;
      letter-spacing: 0.24em;
      text-transform: uppercase;
    }}
    .overview-hero h1 {{
      margin: 0 0 5mm;
      padding: 0;
      border: 0;
      color: var(--blue-dark);
      font-size: 26pt;
      line-height: 1;
      font-weight: 800;
      letter-spacing: -0.03em;
    }}
    .overview-quote {{
      position: relative;
      margin: 0;
      padding: 4.5mm 5mm 4.5mm 6mm;
      border-left: 0.9mm solid var(--gold);
      border-radius: 0 2mm 2mm 0;
      background: linear-gradient(90deg, #f8fbff 0%, #ffffff 100%);
      color: #24324a;
      font-size: 9.6pt;
      line-height: 1.5;
      overflow: hidden;
    }}
    .overview-quote::before {{
      content: "“";
      position: absolute;
      left: 2mm;
      top: -1mm;
      color: rgba(217, 164, 65, 0.18);
      font-size: 34pt;
      line-height: 1;
      font-weight: 800;
    }}
    .overview-stats {{
      position: relative;
      z-index: 2;
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 3mm;
      margin-bottom: 8mm;
    }}
    .overview-stats div {{
      padding: 3mm;
      border-radius: 2.5mm;
      background: #ffffff;
      border: 0.35mm solid #dce7fb;
      box-shadow: 0 2px 8px rgba(8, 47, 143, 0.06);
      text-align: center;
    }}
    .overview-stats strong {{
      display: block;
      color: var(--blue);
      font-size: 16pt;
      line-height: 1;
      font-weight: 800;
    }}
    .overview-stats span {{
      display: block;
      margin-top: 1.5mm;
      color: #5d6b82;
      font-size: 6.8pt;
      font-weight: 700;
      letter-spacing: 0.08em;
      text-transform: uppercase;
    }}
    .overview-body {{
      position: relative;
      z-index: 2;
    }}
    .overview-body h1:first-child {{
      margin-top: 0;
    }}
    .chapter-diagram {{
      position: relative;
      z-index: 2;
      margin: 0 0 6mm;
      border-radius: 2.5mm;
      overflow: hidden;
      border: 0.35mm solid #dce7fb;
      box-shadow: 0 2px 10px rgba(8, 47, 143, 0.08);
      break-inside: avoid;
      page-break-inside: avoid;
    }}
    .chapter-diagram img {{
      display: block;
      width: 100%;
      height: auto;
    }}
    .chapter-pillars {{
      position: relative;
      z-index: 2;
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 3mm;
      margin-bottom: 6mm;
    }}
    .chapter-pillars div {{
      padding: 3.5mm 3mm;
      border-radius: 2.5mm;
      background: #ffffff;
      border: 0.35mm solid #dce7fb;
      border-top: 0.8mm solid var(--blue);
      box-shadow: 0 2px 8px rgba(8, 47, 143, 0.06);
    }}
    .chapter-pillars strong {{
      display: block;
      color: var(--blue-dark);
      font-size: 9.6pt;
      font-weight: 800;
      margin-bottom: 1.5mm;
    }}
    .chapter-pillars p {{
      margin: 0;
      color: #4a5568;
      font-size: 7.8pt;
      line-height: 1.45;
      font-weight: 500;
    }}
    .content-page {{
      width: 210mm;
      min-height: 297mm;
      margin: 0 auto;
      overflow: hidden;
      padding: 20mm 18mm 14mm;
    }}
    .content-page::before {{
      content: "";
      position: absolute;
      top: 0;
      left: 0;
      width: 100%;
      height: 7mm;
      background: linear-gradient(90deg, var(--blue-dark), var(--blue), #2c75d6);
    }}
    .content-page::after {{
      display: none;
    }}
    .page-watermark {{
      position: absolute;
      right: -10mm;
      top: 22mm;
      color: rgba(8, 47, 143, 0.035);
      font-size: 84pt;
      font-weight: 800;
      letter-spacing: -0.08em;
      pointer-events: none;
    }}
    .page-header {{
      position: relative;
      z-index: 2;
      display: flex;
      align-items: center;
      justify-content: space-between;
      margin-bottom: 10mm;
      padding-bottom: 4mm;
      border-bottom: 1px solid var(--line);
    }}
    .page-header img {{
      width: 44mm;
      max-height: 12mm;
      object-fit: contain;
      object-position: left center;
    }}
    .page-header span {{
      color: #718096;
      font-size: 7.8pt;
      font-weight: 800;
      letter-spacing: 0.14em;
      text-transform: uppercase;
    }}
    .chapter-shell {{
      position: relative;
      z-index: 1;
    }}
    .chapter-ribbon {{
      display: inline-block;
      margin-bottom: 10mm;
      padding: 3.2mm 6mm;
      border-radius: 999px;
      color: var(--blue-dark);
      background: linear-gradient(90deg, var(--blue-soft), #ffffff);
      border: 1px solid #dce7fb;
      font-size: 8pt;
      font-weight: 800;
      letter-spacing: 0.12em;
      text-transform: uppercase;
    }}
    .chapter-01 {{
      padding-top: 17mm;
      background:
        radial-gradient(circle at 100% 0, rgba(10, 75, 194, 0.1), transparent 32%),
        linear-gradient(180deg, #ffffff 0%, #ffffff 68%, #f8fbff 100%);
    }}
    .chapter-01::before {{
      height: 5mm;
      background: linear-gradient(90deg, var(--blue-dark), var(--blue));
    }}
    .chapter-01-art {{
      position: absolute;
      top: 19mm;
      right: -48mm;
      width: 124mm;
      height: 124mm;
      border-radius: 36mm;
      background:
        linear-gradient(135deg, rgba(8, 47, 143, 0.11), rgba(8, 47, 143, 0)),
        url("{asset_src("cover/cover-background.png")}") center right / contain no-repeat;
      opacity: 0.18;
      pointer-events: none;
    }}
    .chapter-01-hero {{
      position: relative;
      z-index: 2;
      display: grid;
      grid-template-columns: 0.9fr 1.1fr;
      gap: 8mm;
      align-items: center;
      margin-bottom: 8mm;
    }}
    .chapter-01-copy h1 {{
      max-width: none;
      margin: 0 0 4mm;
      padding: 0;
      border: 0;
      color: var(--blue);
      font-size: 28pt;
      line-height: 1;
      letter-spacing: -0.05em;
    }}
    .chapter-number {{
      display: inline-flex;
      align-items: center;
      min-height: 8mm;
      margin-bottom: 5mm;
      padding: 0 4mm;
      border-radius: 999px;
      background: var(--blue);
      color: #ffffff;
      box-shadow: 0 10px 24px rgba(8, 47, 143, 0.22);
      font-size: 8pt;
      font-weight: 900;
      letter-spacing: 0.14em;
      text-transform: uppercase;
    }}
    .chapter-lead {{
      color: #233757;
      font-size: 12pt;
      line-height: 1.48;
      font-weight: 500;
      margin-bottom: 5mm;
    }}
    .chapter-01-metrics {{
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 2.8mm;
    }}
    .chapter-01-metrics div {{
      min-height: 21mm;
      padding: 3mm;
      border-radius: 4mm;
      background: #ffffff;
      border: 1px solid #dce7fb;
      box-shadow: 0 10px 26px rgba(23, 32, 51, 0.07);
    }}
    .chapter-01-metrics strong {{
      display: block;
      color: var(--blue);
      font-size: 21pt;
      line-height: 1;
      font-weight: 900;
    }}
    .chapter-01-metrics span {{
      display: block;
      margin-top: 1.5mm;
      color: #5d6b82;
      font-size: 7.4pt;
      font-weight: 800;
      line-height: 1.25;
      text-transform: uppercase;
    }}
    .chapter-visual,
    .roadmap-visual {{
      margin: 0;
      border-radius: 6mm;
      overflow: hidden;
      background: #ffffff;
      border: 1px solid #dbe7f8;
      box-shadow: 0 18px 44px rgba(23, 32, 51, 0.12);
      break-inside: avoid;
      page-break-inside: avoid;
    }}
    .chapter-visual img,
    .roadmap-visual img {{
      display: block;
      width: 100%;
      height: auto;
    }}
    .executive-cards {{
      position: relative;
      z-index: 2;
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 4mm;
      margin: 7mm 0;
      break-inside: avoid;
      page-break-inside: avoid;
    }}
    .executive-cards div {{
      min-height: 32mm;
      padding: 5mm;
      border-radius: 5mm;
      background: linear-gradient(180deg, #ffffff, #f8fbff);
      border: 1px solid #dbe7f8;
      box-shadow: 0 12px 30px rgba(23, 32, 51, 0.08);
    }}
    .executive-cards span {{
      display: inline-flex;
      align-items: center;
      justify-content: center;
      width: 8mm;
      height: 8mm;
      margin-bottom: 3mm;
      border-radius: 50%;
      color: #ffffff;
      background: var(--blue);
      font-size: 7.2pt;
      font-weight: 900;
    }}
    .executive-cards strong {{
      display: block;
      color: var(--blue-dark);
      font-size: 13pt;
      line-height: 1.1;
      margin-bottom: 2mm;
    }}
    .executive-cards p {{
      margin: 0;
      color: #536176;
      font-size: 8.8pt;
      line-height: 1.45;
    }}
    .roadmap-visual {{
      margin: 0 0 8mm;
    }}
    .chapter-01-body {{
      padding-top: 2mm;
    }}
    .chapter-01-body h1:first-child {{
      margin-top: 0;
    }}
    .chapter:last-child {{
      break-after: auto;
      page-break-after: auto;
    }}
    h1, h2, h3, h4 {{
      color: var(--blue-dark);
      line-height: 1.2;
      margin: 0 0 11pt;
      break-after: avoid;
      page-break-after: avoid;
    }}
    h1 {{
      max-width: 155mm;
      font-size: 27pt;
      font-weight: 850;
      letter-spacing: -0.04em;
      margin-top: 2mm;
      padding-bottom: 5mm;
      border-bottom: 1px solid var(--line);
    }}
    h1 + h1 {{
      margin-top: 4mm;
      color: var(--blue);
      border-bottom: 0;
      padding-bottom: 0;
    }}
    h2 {{
      position: relative;
      margin-top: 11mm;
      padding-left: 5mm;
      font-size: 15.5pt;
      font-weight: 800;
    }}
    h2::before {{
      content: "";
      position: absolute;
      left: 0;
      top: 2pt;
      width: 1.6mm;
      height: 82%;
      border-radius: 999px;
      background: var(--gold);
    }}
    h3 {{
      color: #24416f;
      font-size: 12.2pt;
      font-weight: 800;
      margin-top: 7mm;
    }}
    h4 {{
      color: #2e4f82;
      font-size: 10.8pt;
      text-transform: uppercase;
      letter-spacing: 0.08em;
      margin-top: 6mm;
    }}
    p {{
      margin: 0 0 8pt;
      color: #26344d;
    }}
    p strong {{
      color: var(--blue-dark);
    }}
    ul {{
      margin: 3mm 0 6mm;
      padding: 0;
      list-style: none;
    }}
    li {{
      position: relative;
      margin: 0 0 4.2pt;
      padding-left: 6mm;
      color: #26344d;
    }}
    li::before {{
      content: "";
      position: absolute;
      left: 0;
      top: 0.62em;
      width: 2.3mm;
      height: 2.3mm;
      border-radius: 50%;
      background: linear-gradient(135deg, var(--blue), #58a6ff);
      box-shadow: 0 0 0 1mm #edf4ff;
    }}
    blockquote {{
      border-left: 4px solid var(--gold);
      color: #233757;
      background: linear-gradient(90deg, #f8fbff, #ffffff);
      margin: 7mm 0;
      padding: 5mm 6mm;
      border-radius: 0 5mm 5mm 0;
      font-style: italic;
      box-shadow: inset 0 0 0 1px #e4ecf8;
    }}
    table {{
      width: 100%;
      border-collapse: separate;
      border-spacing: 0;
      margin: 7mm 0 8mm;
      overflow: hidden;
      border: 1px solid var(--line);
      border-radius: 4mm;
      font-size: 9.4pt;
      break-inside: avoid;
      page-break-inside: avoid;
    }}
    th, td {{
      border: 0;
      border-bottom: 1px solid var(--line);
      padding: 7pt 8pt;
      vertical-align: top;
    }}
    th {{
      background: linear-gradient(90deg, var(--blue-dark), var(--blue));
      color: #ffffff;
      text-align: left;
      font-weight: 800;
      letter-spacing: 0.02em;
    }}
    td {{
      background: #ffffff;
    }}
    tr:nth-child(even) td {{
      background: #f7faff;
    }}
    tr:last-child td {{
      border-bottom: 0;
    }}
    hr {{
      border: 0;
      height: 1px;
      background: linear-gradient(90deg, transparent, #c9d8ed, transparent);
      margin: 8mm 0;
    }}
    code, pre {{
      font-family: Consolas, "Courier New", monospace;
    }}
    code {{
      color: var(--blue-dark);
      background: #edf4ff;
      border-radius: 3px;
      padding: 0.5pt 3pt;
      font-size: 0.92em;
    }}
    pre {{
      background: #0d1b33;
      color: #e9f1ff;
      border: 1px solid #203a63;
      border-radius: 4mm;
      padding: 10pt 12pt;
      white-space: pre-wrap;
      break-inside: avoid;
      page-break-inside: avoid;
    }}
    pre code {{
      color: inherit;
      background: transparent;
      padding: 0;
    }}
    @media screen {{
      body {{
        padding: 18px 0;
      }}
      .chapter {{
        margin-bottom: 24px;
        box-shadow: 0 18px 50px rgba(23, 32, 51, 0.16);
      }}
      .cover-page {{
        margin-left: auto;
        margin-right: auto;
      }}
    }}
    @media print {{
      html, body {{
        background: #ffffff;
      }}
      body {{
        padding: 0;
      }}
      .chapter {{
        margin: 0;
        box-shadow: none;
      }}
    }}
  </style>
</head>
<body>
{chr(10).join(sections)}
</body>
</html>
"""


def write_html() -> None:
    PLAYBOOK_DIR.mkdir(exist_ok=True)
    HTML_OUTPUT.write_text(build_html(), encoding="utf-8")
    print(f"HTML generated: {HTML_OUTPUT}")


def generate_pdf() -> None:
    subprocess.run(["node", "generate_pdf.js"], cwd=ROOT, check=True)


def main() -> None:
    write_html()
    if os.environ.get("PLAYBOOK_HTML_ONLY", "").lower() in {"1", "true", "yes"}:
        return
    generate_pdf()


if __name__ == "__main__":
    main()