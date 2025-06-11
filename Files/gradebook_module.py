"""
Moduł dziennika ocen: dodawanie, czyszczenie, eksport CSV/PDF.
"""

import csv
from reportlab.platypus import SimpleDocTemplate, Table
from db import SessionLocal, Grade

session = SessionLocal()

def add_grade(user_id, subject, score):
    """Dodaje ocenę (przedmiot, wartość) do bazy."""
    session.add(Grade(user_id=user_id, subject=subject, score=score))
    session.commit()

def get_grades(user_id):
    """Zwraca listę ocen dla wybranego użytkownika."""
    return session.query(Grade).filter_by(user_id=user_id).all()

def clear_grades(user_id):
    """Usuwa wszystkie oceny danego użytkownika."""
    session.query(Grade).filter_by(user_id=user_id).delete()
    session.commit()

def export_grades_csv(user_id, filename):
    """Eksportuje oceny do pliku CSV."""
    rows = [("Przedmiot","Ocena")] + [
        (g.subject, g.score) for g in get_grades(user_id)
    ]
    with open(filename, "w", newline="") as f:
        csv.writer(f).writerows(rows)

def export_grades_pdf(user_id, filename):
    """Eksportuje oceny do pliku PDF."""
    data = [("Przedmiot","Ocena")] + [
        (g.subject, g.score) for g in get_grades(user_id)
    ]
    SimpleDocTemplate(filename).build([Table(data)])
