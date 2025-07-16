from pathlib import Path
from fpdf import FPDF  # fpdf2
import unicodedata


def save_markdown(summary: dict, path="summary.md") -> Path:
    path = Path(path)
    with open(path, "w", encoding="utf-8") as f:
        title = summary.get("meta", {}).get("title", "Untitled")
        author = summary.get("meta", {}).get("author", "Unknown Author")
        date = summary.get("meta", {}).get("date", "Unknown Date")
        url = summary.get("meta", {}).get("url", "")
        content = summary.get("content", "")
        summ = summary.get("summary", "")

        f.write(
            f"# {title}\n\n"
            f"**Author(s):** {author}  \n"
            f"**Date:** {date}  \n"
            f"**URL:** {url}\n\n"
            f"## Summary\n{summ}\n\n"
            f"## Full Content\n{content}"
        )
    return path


def clean(text):
    """Normalize text to ASCII-safe version"""
    if not isinstance(text, str):
        return "N/A"
    text = unicodedata.normalize("NFKD", text)
    text = text.encode("ascii", "ignore").decode("ascii")
    return text.strip() or "N/A"

def save_pdf(summary: dict, filename: str) -> str:
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)

    # Use Helvetica instead of Arial for safety
    pdf.set_font("Helvetica", size=12)

    def safe_cell(label, value):
        try:
            text = f"{label}: {clean(value)}"
            pdf.multi_cell(180, 10, text)
        except Exception:
            pdf.multi_cell(180, 10, f"{label}: [Error rendering]")

    # Get data safely
    meta = summary.get("meta", {})
    title = clean(meta.get("title", "Untitled"))
    author = clean(meta.get("author", "Unknown"))
    date = clean(meta.get("date", ""))
    url = clean(meta.get("url", ""))
    content = clean(summary.get("summary", "No summary available."))

    # Title
    pdf.set_font("Helvetica", "B", 14)
    pdf.multi_cell(180, 10, title)
    pdf.ln(5)

    # Metadata
    pdf.set_font("Helvetica", size=12)
    safe_cell("Author(s)", author)
    safe_cell("Date", date)
    safe_cell("URL", url)
    pdf.ln(5)

    # Summary
    pdf.multi_cell(180, 10, content)

    path = Path(filename)
    pdf.output(str(path))
    return str(path)