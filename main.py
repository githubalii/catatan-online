from fastapi import FastAPI, Request, Form
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from sqlalchemy import Column, Integer, String, DateTime, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker, Session
from datetime import datetime
from typing import List

# =====================================================
# 🚀 KONFIGURASI DASAR
# =====================================================
app = FastAPI()

# Mount folder static (CSS, JS, gambar)
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

# =====================================================
# 🧩 DATABASE SETUP
# =====================================================
Base = declarative_base()

class Note(Base):
    __tablename__ = "note"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.now)  # ✅ otomatis isi waktu

# Buat engine SQLite
sqlite_file_name = "notes.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"
engine = create_engine(sqlite_url, echo=True)

# Session untuk interaksi database
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

# Buat tabel jika belum ada
Base.metadata.create_all(bind=engine)

# =====================================================
# 🌐 ROUTES
# =====================================================

@app.get("/")
def home(request: Request):
    with SessionLocal() as session:
        notes: List[Note] = session.query(Note).all()
    return templates.TemplateResponse("index.html", {"request": request, "notes": notes})


@app.post("/add")
def add_note(content: str = Form(...)):
    with SessionLocal() as session:
        note = Note(content=content)
        session.add(note)
        session.commit()
    return RedirectResponse(url="/", status_code=303)


@app.post("/edit/{note_id}")
def edit_note(note_id: int, content: str = Form(...)):
    with SessionLocal() as session:
        note = session.get(Note, note_id)
        if note:
            note.content = content
            session.commit()
    return RedirectResponse(url="/", status_code=303)


@app.post("/delete/{note_id}")
def delete_note(note_id: int):
    with SessionLocal() as session:
        note = session.get(Note, note_id)
        if note:
            session.delete(note)
            session.commit()
    return RedirectResponse(url="/", status_code=303)
