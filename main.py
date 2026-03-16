from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

tareas = []

@app.get("/tareas")
def obtener_tareas():
    return tareas

@app.post("/tareas")
def crear_tarea(tarea: dict):
    tareas.append(tarea)
    return tarea

@app.delete("/tareas/{indice}")
def eliminar_tarea(indice: int):
    if indice < len(tareas):
        tareas.pop(indice)
    return tareas
@app.put("/tareas/{indice}")
def completar_tarea(indice: int):
    if indice < len(tareas):
        tareas[indice]["completada"] = not tareas[indice]["completada"]
    return tareas