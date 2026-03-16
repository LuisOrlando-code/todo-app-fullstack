from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from database import SessionLocal, Tarea, Base, engine

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/tareas")
def obtener_tareas(db: Session = Depends(get_db)):
    return db.query(Tarea).all()

@app.post("/tareas")
def crear_tarea(tarea: dict, db: Session = Depends(get_db)):
    nueva = Tarea(titulo=tarea["titulo"], completada=False)
    db.add(nueva)
    db.commit()
    db.refresh(nueva)
    return nueva

@app.delete("/tareas/{id}")
def eliminar_tarea(id: int, db: Session = Depends(get_db)):
    tarea = db.query(Tarea).filter(Tarea.id == id).first()
    if tarea:
        db.delete(tarea)
        db.commit()
    return {"ok": True}

@app.put("/tareas/{id}")
def completar_tarea(id: int, db: Session = Depends(get_db)):
    tarea = db.query(Tarea).filter(Tarea.id == id).first()
    if tarea:
        tarea.completada = not tarea.completada
        db.commit()
    return tarea