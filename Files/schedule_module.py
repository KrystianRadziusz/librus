"""
Moduł planu lekcji: dodawanie wpisów, czyszczenie, eksport CSV/PDF.
"""

import csv
from reportlab.platypus import SimpleDocTemplate, Table
from db import SessionLocal, ScheduleEntry

session = SessionLocal()

def add_entry(user_id, day, time, subject):
    """Dodaje wpis (dzień, godzina, przedmiot) do planu lekcji."""
    session.add(ScheduleEntry(user_id=user_id, day=day, time=time, subject=subject))
    session.commit()

def get_schedule(user_id):
    """Zwraca listę wpisów z planu lekcji dla danego użytkownika."""
    return session.query(ScheduleEntry).filter_by(user_id=user_id).all()

def clear_schedule(user_id):
    """Usuwa wszystkie wpisy planu lekcji danego użytkownika."""
    session.query(ScheduleEntry).filter_by(user_id=user_id).delete()
    session.commit()

def export_schedule_csv(user_id, filename):
    """Eksportuje plan lekcji do pliku CSV."""
    rows = [("Dzien","Godzina","Przedmiot")] + [
        (e.day, e.time, e.subject) for e in get_schedule(user_id)
    ]
    with open(filename, "w", newline="") as f:
        csv.writer(f).writerows(rows)

def export_schedule_pdf(user_id, filename):
    """Eksportuje plan lekcji do pliku PDF."""
    data = [("Dzien","Godzina","Przedmiot")] + [
        (e.day, e.time, e.subject) for e in get_schedule(user_id)
    ]
    SimpleDocTemplate(filename).build([Table(data)])
