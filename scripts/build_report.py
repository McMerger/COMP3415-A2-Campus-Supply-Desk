"""Render the editable report to PDF. Reporting dependency: reportlab."""

from html import escape
from pathlib import Path
import re

from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle,
    Preformatted,
)

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "output" / "pdf" / "Campus-Supply-Desk-A2-Report.pdf"


def inline(text):
    text = escape(text)
    return re.sub(r"`([^`]+)`", r'<font name="Courier" size="8">\1</font>', text)


def main(source_path=None, output_path=None,
         title="Campus Supply Desk - A2 local review report",
         footer="Local review copy  |  AI-assisted  |  November 8, 2026"):
    source_path = Path(source_path) if source_path else ROOT / "docs" / "final-report.md"
    output_path = Path(output_path) if output_path else OUTPUT
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle("BodyReport", fontName="Helvetica", fontSize=10,
                             leading=14, spaceAfter=9, textColor=colors.HexColor("#253145")))
    styles.add(ParagraphStyle("CellReport", parent=styles["BodyReport"], fontSize=8.4,
                             leading=11, spaceAfter=0, wordWrap="CJK"))
    styles.add(ParagraphStyle("BulletReport", parent=styles["BodyReport"],
                             leftIndent=12, firstLineIndent=-9, spaceAfter=5))
    styles["Title"].fontName = "Helvetica-Bold"
    styles["Title"].fontSize = 28
    styles["Title"].leading = 32
    styles["Title"].alignment = TA_LEFT
    styles["Title"].textColor = colors.HexColor("#153C58")
    for name, size in (("Heading2", 18), ("Heading3", 11)):
        styles[name].fontName = "Helvetica-Bold"
        styles[name].fontSize = size
        styles[name].leading = size + 4
        styles[name].textColor = colors.HexColor("#153C58")
        styles[name].spaceBefore = 10
        styles[name].spaceAfter = 8
    source = source_path.read_text(encoding="utf-8")
    # Use predictable glyphs in the PDF's built-in fonts.
    source = source.replace("\u2014", " - ").replace("\u2013", "-").replace("\u2019", "'")
    lines = source.splitlines()
    flow = []
    position = 0
    while position < len(lines):
        line = lines[position].strip()
        if not line:
            position += 1
            continue
        if line == "<!-- pagebreak -->":
            flow.append(PageBreak())
        elif line.startswith("```"):
            code = []
            position += 1
            while position < len(lines) and not lines[position].startswith("```"):
                code.append(lines[position])
                position += 1
            flow.append(Preformatted("\n".join(code), ParagraphStyle(
                "Code", fontName="Courier", fontSize=8.5, leading=12,
                leftIndent=8, spaceBefore=4, spaceAfter=12)))
        elif line.startswith("|"):
            rows = []
            while position < len(lines) and lines[position].startswith("|"):
                cells = [c.strip() for c in lines[position].strip().strip("|").split("|")]
                if not all(re.fullmatch(r"[-: ]+", c) for c in cells):
                    rows.append([Paragraph(inline(c), styles["CellReport"]) for c in cells])
                position += 1
            columns = len(rows[0])
            widths = ([155, 349] if columns == 2 else [127, 230, 147])
            table = Table(rows, colWidths=widths, repeatRows=1, hAlign="LEFT")
            table.setStyle(TableStyle([
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#E1EBF1")),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F5F8FA")]),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 7),
                ("RIGHTPADDING", (0, 0), (-1, -1), 7),
                ("TOPPADDING", (0, 0), (-1, -1), 7),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
                ("LINEBELOW", (0, 0), (-1, 0), 0.6, colors.HexColor("#8EABBD")),
            ]))
            flow.extend([table, Spacer(1, 10)])
            continue
        elif line.startswith("### "):
            flow.append(Paragraph(inline(line[4:]), styles["Heading3"]))
        elif line.startswith("## "):
            flow.append(Paragraph(inline(line[3:]), styles["Heading2"]))
        elif line.startswith("# "):
            flow.append(Paragraph(inline(line[2:]), styles["Title"]))
        else:
            paragraph = [line]
            position += 1
            while position < len(lines) and lines[position].strip() and not lines[position].startswith(("#", "|", "```", "<!--", "- ")):
                paragraph.append(lines[position].strip())
                position += 1
            text = " ".join(paragraph)
            bullet = text.startswith("- ")
            if bullet:
                text = "&#8226; " + inline(text[2:])
            else:
                text = inline(text)
            flow.append(Paragraph(text, styles["BulletReport" if bullet else "BodyReport"]))
            continue
        position += 1

    def decorate(canvas, doc):
        canvas.saveState()
        canvas.setStrokeColor(colors.HexColor("#BDD0DC"))
        canvas.line(54, 749, 558, 749)
        canvas.setFont("Helvetica", 8)
        canvas.setFillColor(colors.HexColor("#4B6475"))
        canvas.drawString(54, 760, "COMP3415  /  CAMPUS SUPPLY DESK")
        canvas.drawString(54, 29, footer)
        canvas.drawRightString(558, 29, str(doc.page))
        canvas.restoreState()

    output_path.parent.mkdir(parents=True, exist_ok=True)
    doc = SimpleDocTemplate(str(output_path), pagesize=(612, 792),
                            rightMargin=54, leftMargin=54, topMargin=56,
                            bottomMargin=48, title=title,
                            author="AI-assisted local project report")
    doc.build(flow, onFirstPage=decorate, onLaterPages=decorate)
    print(output_path)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--title", default="Campus Supply Desk - A2 local review report")
    parser.add_argument("--footer", default="Local review copy  |  AI-assisted  |  November 8, 2026")
    args = parser.parse_args()
    main(args.source, args.output, args.title, args.footer)
