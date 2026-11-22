"""Build a printable consulting report (PDF) from a JSON spec. Layout is fixed here; facts come from the spec.

    python build_report.py report.json out.pdf

Every page carries the engagement key, version and status, "Page x of y", and a QR code (also a clickable link) to
`record_url`. A Draft carries a DRAFT watermark. `synthetic: true` adds the synthetic-document footer.
Needs only reportlab. The spec's shape is in ../SKILL.md.
"""
import json
import sys
from xml.sax.saxutils import escape

from reportlab.graphics import renderPDF
from reportlab.graphics.barcode.qr import QrCodeWidget
from reportlab.graphics.shapes import Drawing
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas as pdfcanvas
from reportlab.platypus import (KeepTogether, PageBreak, Paragraph, SimpleDocTemplate, Spacer, Table,
                                TableStyle)

INK, MUTED, RULE, TINT = colors.HexColor("#1F2328"), colors.HexColor("#57606A"), colors.HexColor("#D0D7DE"), colors.HexColor("#F3F4F6")
SEVERITY_ORDER = {"High": 0, "Medium": 1, "Low": 2}


def e(x):
    return escape("" if x is None else str(x))


def load(path):
    s = json.load(open(path, encoding="utf-8"))
    for k in ("engagement", "as_at", "version", "status", "record_url"):
        if k not in s:
            raise SystemExit(f"spec is missing '{k}'")
    if s["status"] not in ("Draft", "Final"):
        raise SystemExit("status must be Draft or Final")
    return s


def make_canvas(spec):
    eng = spec["engagement"]
    left = f"{eng['id']}  ·  Version {spec['version']}  ·  {spec['status']}  ·  as at {spec['as_at']}"

    class NumberedCanvas(pdfcanvas.Canvas):
        """Two passes: count the pages, then draw 'Page x of y', the QR code and the watermark on each."""

        def __init__(self, *a, **k):
            super().__init__(*a, **k)
            self._pages = []

        def showPage(self):
            self._pages.append(dict(self.__dict__))
            self._startPage()

        def save(self):
            total, links = len(self._pages), 0
            for state in self._pages:
                self.__dict__.update(state)
                self._annotationCount = links  # restoring a page's state would otherwise reuse link names
                self._decorate(total)
                links = self._annotationCount
                super().showPage()
            super().save()

        def _decorate(self, total):
            W, H = LETTER
            if spec["status"] == "Draft":
                self.saveState()
                self.setFont("Helvetica-Bold", 86)
                self.setFillColor(colors.Color(0, 0, 0, alpha=0.06))
                self.translate(W / 2, H / 2)
                self.rotate(35)
                self.drawCentredString(0, 0, "DRAFT")
                self.restoreState()
            self.saveState()
            self.setStrokeColor(RULE)
            self.line(0.75 * inch, 0.95 * inch, W - 0.75 * inch, 0.95 * inch)
            self.setFillColor(MUTED)
            self.setFont("Helvetica", 8)
            self.drawString(0.75 * inch, 0.72 * inch, left)
            self.drawString(0.75 * inch, 0.56 * inch, f"Page {self._pageNumber} of {total}")
            if spec.get("synthetic"):
                self.drawString(0.75 * inch, 0.40 * inch, "Synthetic test document — InventDB Consulting")
            size = 0.62 * inch
            w = QrCodeWidget(spec["record_url"], barLevel="M")
            b = w.getBounds()
            d = Drawing(size, size, transform=[size / (b[2] - b[0]), 0, 0, size / (b[3] - b[1]), 0, 0])
            d.add(w)
            x, y = W - 0.75 * inch - size, 0.30 * inch
            renderPDF.draw(d, self, x, y)
            self.linkURL(spec["record_url"], (x, y, x + size, y + size), relative=0)
            self.setFont("Helvetica", 6.5)
            self.drawRightString(x - 6, 0.40 * inch, "Scan or click: open this engagement in the workspace (sign-in required)")
            self.restoreState()

    return NumberedCanvas


def build(spec, out):
    ss = getSampleStyleSheet()
    body = ParagraphStyle("body", parent=ss["BodyText"], fontName="Helvetica", fontSize=9.6, leading=13, textColor=INK,
                          alignment=TA_LEFT, spaceAfter=5)
    small = ParagraphStyle("small", parent=body, fontSize=8.4, leading=11, textColor=MUTED)
    cell = ParagraphStyle("cell", parent=body, fontSize=8.6, leading=11, spaceAfter=0)
    h1 = ParagraphStyle("h1", parent=body, fontName="Helvetica-Bold", fontSize=20, leading=25, spaceAfter=8)
    h2 = ParagraphStyle("h2", parent=body, fontName="Helvetica-Bold", fontSize=13, leading=17, spaceBefore=10, spaceAfter=6)
    h3 = ParagraphStyle("h3", parent=body, fontName="Helvetica-Bold", fontSize=10.5, leading=14, spaceBefore=6, spaceAfter=3)
    eng = spec["engagement"]

    def table(head, rows, widths):
        body_rows = [[Paragraph(e(c), cell) for c in r] for r in rows]
        data = ([[Paragraph(f"<b>{e(h)}</b>", cell) for h in head]] if head else []) + body_rows
        t = Table(data, colWidths=widths, repeatRows=1 if head else 0)
        style = [("LINEBELOW", (0, 0), (-1, -1), 0.4, RULE), ("VALIGN", (0, 0), (-1, -1), "TOP"),
                 ("LEFTPADDING", (0, 0), (-1, -1), 4), ("RIGHTPADDING", (0, 0), (-1, -1), 4)]
        t.setStyle(TableStyle(style + ([("BACKGROUND", (0, 0), (-1, 0), TINT)] if head else [])))
        return t

    story = []
    # Cover
    story += [Spacer(1, 0.6 * inch), Paragraph(e(spec.get("title") or f"Due diligence report: {eng.get('title', '')}"), h1),
              Paragraph(e(eng.get("property", "")), body), Spacer(1, 10)]
    facts = [("Engagement", eng["id"]), ("Client", eng.get("client")), ("Prepared by", eng.get("prepared_by")),
             ("Purchase price", eng.get("purchase_price")), ("Due diligence period ends", eng.get("dd_deadline")),
             ("Closing", eng.get("closing_date")), ("Report", f"Version {spec['version']}, {spec['status']}, as at {spec['as_at']}")]
    story.append(table(None, [(k, v) for k, v in facts if v], [2.1 * inch, 4.6 * inch]))
    if spec["status"] == "Draft":
        story += [Spacer(1, 8), Paragraph("Draft for the client's review. Not for reliance until issued as Final.", small)]
    story.append(PageBreak())
    # Summary and red flags
    story.append(Paragraph("Executive summary", h2))
    story += [Paragraph(e(p), body) for p in spec.get("summary", [])]
    flags = sorted(spec.get("red_flags", []), key=lambda f: (SEVERITY_ORDER.get(f.get("severity"), 9), f.get("key", "")))
    if flags:
        story.append(Paragraph("Red flags", h3))
        story.append(table(["Key", "Severity", "Issue", "Source"], [(f.get("key"), f.get("severity"), f.get("title"),
                                                                     f.get("source")) for f in flags],
                           [0.75 * inch, 0.7 * inch, 3.85 * inch, 1.4 * inch]))
    if spec.get("figures"):
        story.append(Paragraph("Key figures", h3))
        story.append(table(["Figure", "Value", "Source"], [(f.get("label"), f.get("value"), f.get("source"))
                                                         for f in spec["figures"]], [3.0 * inch, 1.6 * inch, 2.1 * inch]))
    # Findings by workstream
    for sec in spec.get("sections", []):
        story.append(Paragraph(e(sec["heading"]), h2))
        for n in sec.get("notes", []):
            story.append(Paragraph(e(n), body))
        for f in sorted(sec.get("findings", []), key=lambda f: SEVERITY_ORDER.get(f.get("severity"), 9)):
            block = [Paragraph(f"{e(f.get('key'))}  ·  {e(f.get('severity'))}  ·  {e(f.get('title'))}", h3)]
            if f.get("quote"):
                block.append(Paragraph(f"“{e(f['quote'])}” ({e(f.get('source'))})", small))
            for label in ("impact", "amount", "recommendation", "status"):
                if f.get(label) not in (None, ""):
                    block.append(Paragraph(f"<b>{label.capitalize()}:</b> {e(f[label])}", body))
            story.append(KeepTogether(block))
    if spec.get("open_requests"):
        story.append(Paragraph("Outstanding requests to the seller", h2))
        story.append(table(["Key", "Request", "Due", "Status"], [(r.get("key"), r.get("request"), r.get("due"), r.get("status"))
                                                                for r in spec["open_requests"]],
                           [0.75 * inch, 3.6 * inch, 1.0 * inch, 1.35 * inch]))
    if spec.get("documents"):
        story.append(Paragraph("Documents reviewed", h2))
        story.append(table(["Key", "Document", "Pages", "Status"], [(x.get("key"), x.get("title"), x.get("pages"), x.get("status"))
                                                                   for x in spec["documents"]],
                           [0.75 * inch, 4.35 * inch, 0.6 * inch, 1.0 * inch]))
    story.append(Paragraph("Scope and limitations", h2))
    for p in spec.get("limitations") or [
            "This report relies on documents supplied by the seller and third parties and on public records searched on the "
            "dates stated; it is not a legal opinion, survey, environmental assessment or engineering report.",
            "Figures are taken from the documents and records cited; each finding names its source document and page."]:
        story.append(Paragraph(e(p), body))
    doc = SimpleDocTemplate(out, pagesize=LETTER, leftMargin=0.75 * inch, rightMargin=0.75 * inch, topMargin=0.75 * inch,
                            bottomMargin=1.15 * inch, title=spec.get("title") or eng.get("title", "Report"),
                            author=eng.get("prepared_by", ""), subject=f"{eng['id']} version {spec['version']}")
    doc.build(story, canvasmaker=make_canvas(spec))


if __name__ == "__main__":
    if len(sys.argv) != 3:
        raise SystemExit(__doc__)
    build(load(sys.argv[1]), sys.argv[2])
    print("wrote", sys.argv[2])
