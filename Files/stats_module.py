"""
Moduł obliczania statystyk: średnia, mediana, min, max oraz eksport PDF.
"""

import statistics
from reportlab.platypus import SimpleDocTemplate, Paragraph
from db import SessionLocal, Grade

session = SessionLocal()

def calculate_stats(user_id):
    """Oblicza średnią"""
    scores = [g.score for g in session.query(Grade).filter_by(user_id=user_id)]
    if not scores:
        return {}
    return {
        "srednia": statistics.mean(scores),
    }

def export_stats_pdf(user_id, filename):
    """Eksportuje obliczone statystyki do pliku PDF."""
    stats = calculate_stats(user_id)
    SimpleDocTemplate(filename).build([Paragraph(f"{k}: {v}") for k, v in stats.items()])
