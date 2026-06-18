"""
Export notes to a PDF file using fpdf2.
Returns the path of the generated file.
"""
import os
from datetime import datetime
from fpdf import FPDF


class NotesPDF(FPDF):
    def header(self):
        self.set_font("Helvetica", "B", 10)
        self.set_text_color(100, 100, 120)
        self.cell(0, 8, "LectureMind AI — Study Notes", align="C", new_x="LMARGIN", new_y="NEXT")
        self.ln(2)

    def footer(self):
        self.set_y(-14)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(150, 150, 160)
        self.cell(0, 8, f"Page {self.page_no()}  |  Generated {datetime.now().strftime('%B %d, %Y')}", align="C")


def export_notes_to_pdf(title: str, summary: str, keywords: list, output_dir: str) -> str:
    """
    Generate a professional PDF of the lecture notes.

    Args:
        title:      Lecture title
        summary:    Full summary text
        keywords:   List of keyword strings
        output_dir: Directory to save the PDF

    Returns:
        Absolute path to the generated PDF file.
    """
    os.makedirs(output_dir, exist_ok=True)
    safe_title = "".join(c if c.isalnum() or c in " _-" else "_" for c in title)[:60]
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    out_path = os.path.join(output_dir, f"{safe_title}_{timestamp}.pdf")

    pdf = NotesPDF()
    pdf.set_auto_page_break(auto=True, margin=18)
    pdf.add_page()
    pdf.set_margins(20, 20, 20)

    # --- Title ---
    pdf.set_font("Helvetica", "B", 18)
    pdf.set_text_color(80, 40, 180)
    pdf.multi_cell(0, 10, title, align="L", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "", 9)
    pdf.set_text_color(140, 140, 160)
    pdf.cell(0, 6, f"Generated on {datetime.now().strftime('%A, %B %d, %Y at %H:%M')}", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(4)

    # Divider
    pdf.set_draw_color(120, 60, 200)
    pdf.set_line_width(0.8)
    pdf.line(20, pdf.get_y(), 190, pdf.get_y())
    pdf.ln(6)

    # --- Executive Summary ---
    pdf.set_font("Helvetica", "B", 13)
    pdf.set_text_color(60, 60, 80)
    pdf.cell(0, 8, "Executive Summary", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(2)

    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(40, 40, 60)
    for line in summary.split("\n"):
        line = line.strip()
        if not line:
            pdf.ln(3)
            continue
        if line.startswith("•") or line.startswith("-"):
            pdf.set_x(26)
            pdf.multi_cell(0, 6, line, new_x="LMARGIN", new_y="NEXT")
        else:
            pdf.multi_cell(0, 6, line, new_x="LMARGIN", new_y="NEXT")
    pdf.ln(4)

    # --- Key Concepts ---
    if keywords:
        pdf.set_font("Helvetica", "B", 13)
        pdf.set_text_color(60, 60, 80)
        pdf.cell(0, 8, "Key Concepts", new_x="LMARGIN", new_y="NEXT")
        pdf.ln(2)

        pdf.set_font("Helvetica", "", 10)
        pdf.set_text_color(80, 40, 180)
        kw_line = "  ·  ".join(kw.strip() for kw in keywords if kw.strip())
        pdf.multi_cell(0, 7, kw_line, new_x="LMARGIN", new_y="NEXT")

    pdf.output(out_path)
    return out_path