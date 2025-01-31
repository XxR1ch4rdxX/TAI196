
from fastapi import FastAPI
from typing import Optional
app = FastAPI(
    title='FastAPI richy con documentacion',
    description='Ricardo Giovanny Sandoval Bermudez',
    version='0.0.1'
)

#Base de datos temporal
usuarios = [
    {'id':1,'nombre':'Ricardo',"edad":25},
    {'id':2,'nombre':'Giovanny',"edad":21},
    {'id':3,'nombre':'Pancho',"edad":15},
    {'id':4,'nombre':'Juanito',"edad":45},
    {'id':5,'nombre':'Pedrito',"edad":22},
    {'id':6,'nombre':'Pablito',"edad":20},
]

@app.get("/",tags=['Raiz'])
def main():
    return {'Hola FastAPI!':' Hola Richy'}

@app.get("/promedio",tags=['EndPont-Promedio'])
def promedio():
    return 9.99

#endpoint parametro obligatorio
@app.get("/usuario/{id}",tags=['EndPont-Parametro Obligatorio'])
def consultaUsuario(id:int):
    #conectar con la DB
    #Consultas y resultados de la DB
    return{"Se encontro el usuario  ":id}


#endpoint parametro opcional
@app.get("/usuario/",tags=['EndPont-Parametro Opcional'])
def consultaUsuario2(id:Optional[int]=None): #este parametro es opcional
    
    #lo que hacemos aqui es iterar en la base de datos temporal
    #y si el id coincide con el id que se paso por parametro
    #retornamos el usuario
    if id is not None:
        for usuario in usuarios:
            if usuario['id']==id:
                return {'Mensaje:':'Usuario encontrado','Usuario':usuario}
        return{'Mensaje':f'No se ha encontrado el usuario con el id=:{id}'}
    else:
        return{'Mensaje':'No se ha pasado ningun parametro'}

#endpoint con mas  deu un parametro opcionales
#endpoint con varios parametro opcionales
@app.get("/usuarios/", tags=["3 parámetros opcionales"])
async def consulta_usuarios(
    usuario_id: Optional[int] = None,
    nombre: Optional[str] = None,
    edad: Optional[int] = None
):
    resultados = []

    for usuario in usuarios:
        if (
            (usuario_id is  None or usuario["id"] == usuario_id) and
            (nombre is None or usuario["nombre"].lower() == nombre.lower()) and
            (edad is  None or usuario["edad"] == edad)
        ):
            resultados.append(usuario)

    if resultados:
        return {"usuarios_encontrados": resultados}
    else:
        return {"mensaje": "No se encontraron usuarios que coincidan con los parámetros proporcionados."}