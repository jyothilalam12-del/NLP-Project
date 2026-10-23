
import json
import os
from datetime import datetime
from io import BytesIO

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    HRFlowable
)

HISTORY_FILE = "study_history.json"


def load_history():
    """Load saved study history."""
    if not os.path.exists(HISTORY_FILE):
        return []

    try:
        with open(HISTORY_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)
            return data if isinstance(data, list) else []
    except (json.JSONDecodeError, OSError):
        return []


def save_history(history):
    """Save study history to a local JSON file."""
    with open(HISTORY_FILE, "w", encoding="utf-8") as file:
        json.dump(history, file, ensure_ascii=False, indent=2)


def add_history(history, activity, question, result):
    """Add an activity to the saved history."""
    entry = {
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "activity": activity,
        "question": str(question),
        "result": str(result)
    }

    history.append(entry)

    # Keep the most recent 500 entries.
    history = history[-500:]
    save_history(history)

    return history


def create_pdf(title, content):
    """Create a downloadable PDF from plain text."""
    buffer = BytesIO()

    document = SimpleDocTemplate(
        buffer,
        rightMargin=0.65 * inch,
        leftMargin=0.65 * inch,
        topMargin=0.7 * inch,
        bottomMargin=0.7 * inch
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "StudyTitle",
        parent=styles["Title"],
        alignment=TA_CENTER,
        textColor=colors.HexColor("#3730A3"),
        spaceAfter=16
    )

    body_style = ParagraphStyle(
        "StudyBody",
        parent=styles["BodyText"],
        leading=16,
        spaceAfter=9
    )

    story = [
        Paragraph(title, title_style),
        HRFlowable(
            width="100%",
            thickness=1,
            color=colors.HexColor("#C7D2FE")
        ),
        Spacer(1, 16)
    ]

    # Escape special characters before placing text in PDF paragraphs.
    from xml.sax.saxutils import escape

    for line in str(content).splitlines():
        if line.strip():
            story.append(Paragraph(escape(line), body_style))
        else:
            story.append(Spacer(1, 7))

    document.build(story)
    buffer.seek(0)

    return buffer.getvalue()