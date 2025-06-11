from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship, declarative_base

engine = create_engine("sqlite:///student_app.db")
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

class User(Base):
    """Tabela użytkowników: login i zaszyfrowane hasło."""
    __tablename__ = "users"
    id       = Column(Integer, primary_key=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)
    schedules = relationship("ScheduleEntry", back_populates="user")
    grades    = relationship("Grade", back_populates="user")

class ScheduleEntry(Base):
    """Pojedynczy wpis w planie lekcji (dzień, godzina, przedmiot)."""
    __tablename__ = "schedule"
    id      = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    day     = Column(String)
    time    = Column(String)
    subject = Column(String)
    user    = relationship("User", back_populates="schedules")

class Grade(Base):
    """Pojedyncza ocena (przedmiot, wartość)."""
    __tablename__ = "grades"
    id      = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    subject = Column(String)
    score   = Column(Float)
    user    = relationship("User", back_populates="grades")

Base.metadata.create_all(bind=engine)

""" Sprawdzenie wszystkich zarejestrowanych uzytkownikow. """

#def list_users():
   # session = SessionLocal()
   # return [u.username for u in session.query(User).all()]

#print(list_users())
