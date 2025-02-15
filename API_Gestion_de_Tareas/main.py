from fastapi import FastAPI, HTTPException

#.\entornoTareas\Scripts\activate
#uvicorn main:app --reload --port 5000
app = FastAPI(
    title='Gestion de tareas',
    description='En esta API retomaremos los puntos vistos en clase',
    version='Sandoval Bermudez Ricardo Giovanny'
)

@app.get("/")
def main():
    return {'Tamo en linea"':'Hola buenas'}