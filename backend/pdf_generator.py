import io
from datetime import datetime, timezone
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    HRFlowable,
    KeepTogether,
)
from reportlab.graphics.shapes import Drawing, Rect, String, Circle
from reportlab.graphics import renderPDF

# ── Brand colours ─────────────────────────────────────────────────────────────
MG_DARK = colors.HexColor("#1C1C1C")
MG_MID = colors.HexColor("#333333")
MG_BG = colors.HexColor("#F5F4EF")
MG_BORDER = colors.HexColor("#E0DFD9")
MG_SURFACE = colors.HexColor("#EEEEE9")
MG_MUTED = colors.HexColor("#6B6B6B")
MG_TEXT = colors.HexColor("#1C1C1C")
MG_PASS = colors.HexColor("#1C1C1C")
MG_PASS_BG = colors.HexColor("#EEEEE9")
MG_WARN = colors.HexColor("#B45309")
MG_WARN_BG = colors.HexColor("#FEF3C7")
MG_FAIL = colors.HexColor("#DC2626")
MG_FAIL_BG = colors.HexColor("#FEF2F2")
MG_WHITE = colors.white

GRADE_COLOURS = {
    "A": colors.HexColor("#1C1C1C"),
    "B": colors.HexColor("#333333"),
    "C": colors.HexColor("#B45309"),
    "D": colors.HexColor("#F97316"),
    "F": colors.HexColor("#DC2626"),
}

STATUS_COLOURS = {
    "pass": (MG_PASS, MG_PASS_BG),
    "warning": (MG_WARN, MG_WARN_BG),
    "fail": (MG_FAIL, MG_FAIL_BG),
}

STATUS_LABELS = {"pass": "PASS", "warning": "WARNING", "fail": "FAIL"}

W, H = A4
MARGIN = 18 * mm


# ── Styles ────────────────────────────────────────────────────────────────────
def _styles():
    return {
        "h1": ParagraphStyle(
            "h1",
            fontName="Helvetica-Bold",
            fontSize=22,
            textColor=MG_DARK,
            leading=28,
            spaceAfter=4,
        ),
        "h2": ParagraphStyle(
            "h2",
            fontName="Helvetica-Bold",
            fontSize=14,
            textColor=MG_DARK,
            leading=20,
            spaceAfter=4,
        ),
        "h3": ParagraphStyle(
            "h3",
            fontName="Helvetica-Bold",
            fontSize=11,
            textColor=MG_DARK,
            leading=16,
            spaceAfter=2,
        ),
        "body": ParagraphStyle(
            "body",
            fontName="Helvetica",
            fontSize=10,
            textColor=MG_TEXT,
            leading=15,
            spaceAfter=4,
        ),
        "muted": ParagraphStyle(
            "muted", fontName="Helvetica", fontSize=9, textColor=MG_MUTED, leading=13
        ),
        "small_bold": ParagraphStyle(
            "small_bold",
            fontName="Helvetica-Bold",
            fontSize=9,
            textColor=MG_DARK,
            leading=13,
        ),
        "rec": ParagraphStyle(
            "rec",
            fontName="Helvetica-Oblique",
            fontSize=9,
            textColor=colors.HexColor("#78350F"),
            leading=14,
        ),
        "badge": ParagraphStyle(
            "badge",
            fontName="Helvetica-Bold",
            fontSize=8,
            leading=10,
            alignment=TA_CENTER,
        ),
        "footer": ParagraphStyle(
            "footer",
            fontName="Helvetica",
            fontSize=8,
            textColor=MG_MUTED,
            leading=11,
            alignment=TA_CENTER,
        ),
        "url": ParagraphStyle(
            "url", fontName="Helvetica", fontSize=10, textColor=MG_DARK, leading=14
        ),
    }


# ── Grade circle drawing ──────────────────────────────────────────────────────
def _grade_drawing(grade: str, percentage: float) -> Drawing:
    d = Drawing(130, 130)
    colour = GRADE_COLOURS.get(grade, MG_MUTED)
    cx, cy, r = 65, 65, 52

    ring = Circle(cx, cy, r)
    ring.strokeColor = colour
    ring.strokeWidth = 5
    ring.fillColor = colors.white
    d.add(ring)

    letter = String(
        cx,
        cy + 8,
        grade,
        fontName="Helvetica-Bold",
        fontSize=36,
        fillColor=colour,
        textAnchor="middle",
    )
    d.add(letter)

    pct = String(
        cx,
        cy - 16,
        f"{percentage}%",
        fontName="Helvetica",
        fontSize=11,
        fillColor=MG_MUTED,
        textAnchor="middle",
    )
    d.add(pct)

    return d


# ── Score bar drawing ─────────────────────────────────────────────────────────
def _score_bar(percentage: float, grade: str, width: float = 120) -> Drawing:
    h = 10
    d = Drawing(width, h)
    colour = GRADE_COLOURS.get(grade, MG_MUTED)
    filled = (percentage / 100) * width

    bg = Rect(0, 0, width, h, rx=5, ry=5)
    bg.fillColor = MG_BORDER
    bg.strokeColor = None
    d.add(bg)

    if filled > 0:
        fill = Rect(0, 0, filled, h, rx=5, ry=5)
        fill.fillColor = colour
        fill.strokeColor = None
        d.add(fill)

    return d


# ── Header banner ─────────────────────────────────────────────────────────────
def _header_banner(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(MG_DARK)
    canvas.rect(0, H - 14 * mm, W, 14 * mm, fill=True, stroke=False)

    # misgav (white)
    canvas.setFillColor(MG_WHITE)
    canvas.setFont("Helvetica-Bold", 11)
    canvas.drawString(MARGIN, H - 9 * mm, "misgav")

    # Divider
    canvas.setFillColor(colors.HexColor("#555555"))
    canvas.setFont("Helvetica", 11)
    canvas.drawString(MARGIN + 40, H - 9 * mm, "|")

    # ShieldScan (grey)
    canvas.setFillColor(colors.HexColor("#A0A0A0"))
    canvas.setFont("Helvetica-Bold", 11)
    canvas.drawString(MARGIN + 50, H - 9 * mm, "ShieldScan")

    # Tagline (right)
    canvas.setFillColor(colors.HexColor("#A0A0A0"))
    canvas.setFont("Helvetica", 9)
    canvas.setFillAlpha(0.6)
    canvas.drawRightString(W - MARGIN, H - 9 * mm, "Website Security Audit")
    canvas.setFillAlpha(1)

    canvas.restoreState()


# ── Page footer ───────────────────────────────────────────────────────────────
def _footer(canvas, doc):
    canvas.saveState()
    canvas.setStrokeColor(MG_BORDER)
    canvas.setLineWidth(0.5)
    canvas.line(MARGIN, 14 * mm, W - MARGIN, 14 * mm)
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(MG_MUTED)
    canvas.drawString(
        MARGIN,
        9 * mm,
        "misgav ShieldScan  ·  hello@misgav.co.za  ·  www.misgav.co.za",
    )
    canvas.drawRightString(W - MARGIN, 9 * mm, f"Page {doc.page}")
    canvas.restoreState()


def _on_page(canvas, doc):
    _header_banner(canvas, doc)
    _footer(canvas, doc)


# ── Main generator ────────────────────────────────────────────────────────────
def generate_pdf(result: dict) -> bytes:
    buf = io.BytesIO()
    styles = _styles()

    doc = SimpleDocTemplate(
        buf,
        pagesize=A4,
        leftMargin=MARGIN,
        rightMargin=MARGIN,
        topMargin=20 * mm,
        bottomMargin=20 * mm,
        title=f"misgav ShieldScan Report — {result['url']}",
        author="misgav ShieldScan",
    )

    story = []
    usable_w = W - 2 * MARGIN

    story.append(Spacer(1, 4 * mm))
    story.append(Paragraph("Security Audit Report", styles["h1"]))
    story.append(
        Paragraph(
            f"Prepared by misgav ShieldScan  ·  Report ID: {result.get('scan_id', 'N/A')}",
            styles["muted"],
        )
    )
    story.append(Spacer(1, 6 * mm))
    story.append(HRFlowable(width=usable_w, color=MG_BORDER, thickness=0.5))
    story.append(Spacer(1, 6 * mm))

    grade_d = _grade_drawing(result["grade"], result["percentage"])
    bar_d = _score_bar(result["percentage"], result["grade"], width=180)

    scanned_str = result.get("scanned_at", "")
    try:
        dt = datetime.fromisoformat(scanned_str).strftime("%d %b %Y, %H:%M UTC")
    except Exception:
        dt = scanned_str

    pass_n = sum(1 for c in result["checks"] if c["status"] == "pass")
    warn_n = sum(1 for c in result["checks"] if c["status"] == "warning")
    fail_n = sum(1 for c in result["checks"] if c["status"] == "fail")

    meta_data = [
        [
            Paragraph("<b>URL</b>", styles["small_bold"]),
            Paragraph(result["url"], styles["url"]),
        ],
        [
            Paragraph("<b>Scanned</b>", styles["small_bold"]),
            Paragraph(dt, styles["body"]),
        ],
        [
            Paragraph("<b>Score</b>", styles["small_bold"]),
            Paragraph(
                f"{result['score']} / {result['max_score']} points", styles["body"]
            ),
        ],
        [
            Paragraph("<b>Grade</b>", styles["small_bold"]),
            Paragraph(f"{result['grade']} — {result['label']}", styles["body"]),
        ],
        [
            Paragraph("<b>Passed</b>", styles["small_bold"]),
            Paragraph(f"{pass_n} checks", styles["body"]),
        ],
        [
            Paragraph("<b>Warnings</b>", styles["small_bold"]),
            Paragraph(f"{warn_n} checks", styles["body"]),
        ],
        [
            Paragraph("<b>Failed</b>", styles["small_bold"]),
            Paragraph(f"{fail_n} checks", styles["body"]),
        ],
    ]

    meta_table = Table(meta_data, colWidths=[30 * mm, 90 * mm])
    meta_table.setStyle(
        TableStyle(
            [
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("ROWBACKGROUNDS", (0, 0), (-1, -1), [MG_WHITE, MG_BG]),
                ("LEFTPADDING", (0, 0), (-1, -1), 6),
                ("RIGHTPADDING", (0, 0), (-1, -1), 6),
                ("TOPPADDING", (0, 0), (-1, -1), 5),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
                ("ROUNDEDCORNERS", [4]),
            ]
        )
    )

    bar_block = [
        [Paragraph("<b>Score breakdown</b>", styles["small_bold"])],
        [bar_d],
        [
            Paragraph(
                f"<font color='#1C1C1C'>✓ {pass_n} passed</font>   "
                f"<font color='#B45309'>⚠ {warn_n} warnings</font>   "
                f"<font color='#DC2626'>✕ {fail_n} failed</font>",
                styles["muted"],
            )
        ],
    ]
    bar_table = Table(bar_block, colWidths=[usable_w * 0.45])
    bar_table.setStyle(
        TableStyle(
            [
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("LEFTPADDING", (0, 0), (-1, -1), 0),
                ("TOPPADDING", (0, 0), (-1, -1), 3),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
            ]
        )
    )

    summary_table = Table(
        [[grade_d, meta_table]], colWidths=[45 * mm, usable_w - 45 * mm]
    )
    summary_table.setStyle(
        TableStyle(
            [
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("LEFTPADDING", (0, 0), (-1, -1), 0),
                ("RIGHTPADDING", (0, 0), (-1, -1), 8),
                ("TOPPADDING", (0, 0), (-1, -1), 0),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
            ]
        )
    )

    story.append(summary_table)
    story.append(Spacer(1, 5 * mm))
    story.append(bar_table)
    story.append(Spacer(1, 8 * mm))
    story.append(HRFlowable(width=usable_w, color=MG_BORDER, thickness=0.5))

    story.append(Spacer(1, 6 * mm))
    story.append(Paragraph("Detailed Findings", styles["h2"]))
    story.append(
        Paragraph(
            "Checks are ordered by priority — failed items appear first.",
            styles["muted"],
        )
    )
    story.append(Spacer(1, 4 * mm))

    STATUS_ORDER = {"fail": 0, "warning": 1, "pass": 2}
    sorted_checks = sorted(
        result["checks"], key=lambda c: STATUS_ORDER.get(c["status"], 9)
    )

    for check in sorted_checks:
        status = check["status"]
        fg, bg = STATUS_COLOURS.get(status, (MG_MUTED, MG_WHITE))
        label = STATUS_LABELS.get(status, status.upper())

        badge_para = Paragraph(
            f'<font color="white"><b>{label}</b></font>', styles["badge"]
        )
        badge_table = Table([[badge_para]], colWidths=[18 * mm])
        badge_table.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, -1), fg),
                    ("ROUNDEDCORNERS", (0, 0), (-1, -1), [3]),
                    ("LEFTPADDING", (0, 0), (-1, -1), 4),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 4),
                    ("TOPPADDING", (0, 0), (-1, -1), 3),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
                ]
            )
        )

        pts_para = Paragraph(
            f'<b>{check["points_earned"]}</b>/{check["points_possible"]} pts',
            styles["muted"],
        )
        header_row = Table(
            [[badge_table, Paragraph(check["title"], styles["h3"]), pts_para]],
            colWidths=[22 * mm, usable_w - 40 * mm, 18 * mm],
        )
        header_row.setStyle(
            TableStyle(
                [
                    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                    ("LEFTPADDING", (0, 0), (-1, -1), 0),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 0),
                    ("ALIGN", (2, 0), (2, 0), "RIGHT"),
                ]
            )
        )

        inner_rows = [[header_row]]
        inner_rows.append([Paragraph(check.get("detail", ""), styles["body"])])

        if check.get("recommendation"):
            rec_table = Table(
                [[Paragraph("💡  " + check["recommendation"], styles["rec"])]],
                colWidths=[usable_w - 16 * mm],
            )
            rec_table.setStyle(
                TableStyle(
                    [
                        ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#FFFBEB")),
                        ("ROUNDEDCORNERS", (0, 0), (-1, -1), [4]),
                        ("LEFTPADDING", (0, 0), (-1, -1), 8),
                        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
                        ("TOPPADDING", (0, 0), (-1, -1), 6),
                        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
                        ("BOX", (0, 0), (-1, -1), 0.5, colors.HexColor("#FDE68A")),
                    ]
                )
            )
            inner_rows.append([rec_table])

        inner = Table(inner_rows, colWidths=[usable_w - 8 * mm])
        inner.setStyle(
            TableStyle(
                [
                    ("VALIGN", (0, 0), (-1, -1), "TOP"),
                    ("LEFTPADDING", (0, 0), (-1, -1), 0),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 0),
                    ("TOPPADDING", (0, 0), (-1, -1), 4),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
                ]
            )
        )

        card = Table([[inner]], colWidths=[usable_w])
        card.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, -1), bg),
                    ("ROUNDEDCORNERS", (0, 0), (-1, -1), [6]),
                    ("LEFTPADDING", (0, 0), (-1, -1), 8),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 8),
                    ("TOPPADDING", (0, 0), (-1, -1), 8),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
                    ("LINEAFTER", (0, 0), (0, -1), 2, fg),
                ]
            )
        )

        story.append(KeepTogether(card))
        story.append(Spacer(1, 4 * mm))

    story.append(Spacer(1, 4 * mm))
    story.append(HRFlowable(width=usable_w, color=MG_BORDER, thickness=0.5))
    story.append(Spacer(1, 4 * mm))
    story.append(
        Paragraph(
            "This report was generated automatically by misgav ShieldScan. It reflects the "
            "security posture of the scanned URL at the time of the scan. It does not "
            "constitute a full penetration test. For a comprehensive security audit, "
            "contact misgav at hello@misgav.co.za.",
            styles["muted"],
        )
    )

    doc.build(story, onFirstPage=_on_page, onLaterPages=_on_page)
    return buf.getvalue()
