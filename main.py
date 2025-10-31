from fastapi import FastAPI, Form, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlmodel import Field, Session, SQLModel, create_engine, select

# --- Inisialisasi FastAPI ---
app = FastAPI()

# --- Setup template engine (Jinja2) ---
templates = Jinja2Templates(directory="templates")

# --- Model database ---
class Catatan(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    isi: str

# --- Setup database ---
sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"
engine = create_engine(sqlite_url, echo=False)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

# --- Routes ---
@app.get("/")
def read_root(request: Request):
    """Tampilkan semua catatan."""
    with Session(engine) as session:
        notes = session.exec(select(Catatan)).all()
    return templates.TemplateResponse("index.html", {"request": request, "notes": notes})

@app.post("/add")
def add_note(note: str = Form(...)):
    """Tambah catatan ke database."""
    with Session(engine) as session:
        catatan = Catatan(isi=note)
        session.add(catatan)
        session.commit()
    return RedirectResponse("/", status_code=303)

@app.get("/delete/{note_id}")
def delete_note(note_id: int):
    """Hapus catatan berdasarkan ID."""
    with Session(engine) as session:
        note = session.get(Catatan, note_id)
        if note:
            session.delete(note)
            session.commit()
    return RedirectResponse("/", status_code=303)
