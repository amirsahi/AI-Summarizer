from pathlib import Path
from fpdf import FPDF  # fpdf2


def save_markdown(summary: dict, path: str | Path):
    md = (
        f"# {summary['title'] or 'Untitled'}\n\n"
        f"*URL*: {summary['url']}\n"
        f"*Author*: {summary.get('author','N/A')}  \n"
        f"*Published*: {summary.get('date','N/A')}\n\n"
        f"## Summary\n\n{summary['summary']}\n"
    )
    Path(path).write_text(md, encoding="utf‑8")
    return path


def save_pdf(summary: dict, path: str | Path):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Helvetica", size=12)

    def write(txt, ln=True):
        pdf.multi_cell(0, 10, txt)
        if ln:
            pdf.ln(2)

    write(summary["title"] or "Untitled")
    write(f"URL: {summary['url']}")
    write(f"Author: {summary.get('author','N/A')}")
    write(f"Published: {summary.get('date','N/A')}\n")
    write("Summary:\n")
    write(summary["summary"])
    pdf.output(str(path))
    return path
