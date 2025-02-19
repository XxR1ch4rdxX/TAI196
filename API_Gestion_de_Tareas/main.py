from fastapi import FastAPI, HTTPException

#.\entornoTareas\Scripts\activate
#uvicorn main:app --reload --port 5000
app = FastAPI(
    title='Gestion de tareas',
    description='En esta API retomaremos los puntos vistos en clase',
    version='Sandoval Bermudez Ricardo Giovanny'
)

tareas = [
    {"id":1,"titulo":"Sacar a los perros","descripcion":"Sacar a los perros a pasear","vencimiento":"2025-12-02","estado":"completado"},
    {"id":2,"titulo":"Sacar la basura","descripcion":"sacar la basura a la calle","vencimiento":"2025-19-02","estado":"no completado"},
    {"id":3,"titulo":"Acabar la tarea","descripcion":"terminar la tarea del prof.isai","vencimiento":"2025-19-02","estado":"no completado"},
    {"id":4,"titulo":"Lavar la ropa","descripcion":"lavar la ropa, ya huele mal","\vencimiento":"2025-13-02","estado":"completado"},
    {"id":5,"titulo":"Dominar al mundo","descripcion":"unificar a los paises en una sola nacion","\vencimiento":"2100-01-01","estado":"no completado"},
]

@app.get("/",tags=['Raiz'])
def main():
    return {'Tamo en linea con Fastapi'}

@app.get('/Ver tareas',tags=['EP: Obtener todas las Tareas'])
def verall():
    return {'Tareas Registradas': tareas}
