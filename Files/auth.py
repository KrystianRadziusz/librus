"""
Proste logowanie i rejestracja użytkowników (z hasłem szyfrowanym przez `utils`).
"""

from db import SessionLocal, User
from utils import encrypt, decrypt

session = SessionLocal()

def register(username, password):
    """Rejestruje nowego użytkownika lub zgłasza, że istnieje."""
    if session.query(User).filter_by(username=username).first():
        return False, "Uzytkownik istnieje"
    session.add(User(username=username, password=encrypt(password)))
    session.commit()
    return True, "Rejestracja przebiegla pomyslnie"

def login(username, password):
    """Weryfikuje login i hasło; zwraca (True, user_id) lub (False, komunikat)."""
    user = session.query(User).filter_by(username=username).first()
    if not user:
        return False, "Uzytkownik nie istnieje"
    if decrypt(user.password) != password:
        return False, "Bledne haslo"
    return True, user.id
