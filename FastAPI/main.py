# git:https://github.com/XxR1ch4rdxX/TAI196
from fastapi import FastAPI, HTTPException
from typing import Optional, List
from modelsPydantic import ModelUsuario

app = FastAPI(
    title='FastAPI richy con documentacion',
    description='Ricardo Giovanny Sandoval Bermudez',
    version='0.0.1'
)
#Para correr el servidor en la terminal
#.\VEF\Scripts\activate
#uvicorn main:app --reload --port 5000
#Base de datos temporal
usuarios = [
    {"id":1,"nombre":"Ricardo","edad":25,"correo":"Richy@gmail.com"},
    {"id":2,"nombre":"Giovanny","edad":23,"correo":"Giovanny@gmail.com"},
    {"id":3,"nombre":"Sandoval","edad":24,"correo":"Sandoval@exemplo.com"},
    {"id":4,"nombre":"Bermudez","edad":26,"correo":"Bermudez@hola.com"},
    {"id":5,"nombre":"Pepito","edad":27,"correo":"Pepeloco@hotnail.com"},
]

@app.get("/",tags=['Raiz'])
def main():
    return {'Hola FastAPI!':' Hola Richy'}

#----------endpoint Consultar-----------------#
@app.get('/usuarios', response_model=List[ModelUsuario] , tags=['Operaciones CRUD'])
def Consultar():
    return usuarios

#----------endpoint RegistroNuevo-----------------#
@app.post('/registrar/', response_model=ModelUsuario,tags=['Operaciones CRUD'])
def Registrar(UsuarioNuevo:ModelUsuario):
    for usr in usuarios:
        if usr["id"]==UsuarioNuevo.id:
            raise HTTPException(status_code=400,detail="Error ID ya utilizada")
        
    usuarios.append(UsuarioNuevo)
    return UsuarioNuevo    

#----------endpoint Actualizar-----------------#
@app.put('/actualizar/{id}', response_model=ModelUsuario, tags=['Operaciones CRUD'])
def actualizar(id: int, usuarioactualizado: ModelUsuario):
    for index, usr in enumerate(usuarios):
        if usr["id"] == id:
            usuarios[index] = usuarioactualizado.model_dump()  
            return usuarios[index]  
    raise HTTPException(status_code=404, detail="Usuario no encontrado")
#----------endpoint Eliminar-----------------#
@app.delete('/borrar/',tags=['Operaciones CRUD'])
def Borrar(idu:int):
    for usr in usuarios:
        if usr["id"]==idu:
            usuarios.remove(usr)
            return {'Mensaje':'Usuario Eliminado'},usuarios   
    raise HTTPException(status_code=404,detail="Usuario no encontrado")
    
       
    

# @app.get("/promedio",tags=['EndPont-Promedio'])
# def promedio():
#     return 9.99

# #endpoint parametro obligatorio
# @app.get("/usuario/{id}",tags=['EndPont-Parametro Obligatorio'])
# def consultaUsuario(id:int):
#     #conectar con la DB
#     #Consultas y resultados de la DB
#     return{"Se encontro el usuario  ":id}


# #endpoint parametro opcional
# @app.get("/usuario/",tags=['EndPont-Parametro Opcional'])
# def consultaUsuario2(id:Optional[int]=None): #este parametro es opcional
    
#     #lo que hacemos aqui es iterar en la base de datos temporal
#     #y si el id coincide con el id que se paso por parametro
#     #retornamos el usuario
#     if id is not None:
#         for usuario in usuarios:
#             if usuario['id']==id:
#                 return {'Mensaje:':'Usuario encontrado','Usuario':usuario}
#         return{'Mensaje':f'No se ha encontrado el usuario con el id=:{id}'}
#     else:
#         return{'Mensaje':'No se ha pasado ningun parametro'}

# #endpoint con mas  deu un parametro opcionales
# #endpoint con varios parametro opcionales
# @app.get("/usuarios/", tags=["3 parámetros opcionales"])
# async def consulta_usuarios(
#     usuario_id: Optional[int] = None,
#     nombre: Optional[str] = None,
#     edad: Optional[int] = None
# ):
#     resultados = []

#     for usuario in usuarios:
#         if (
#             (usuario_id is  None or usuario["id"] == usuario_id) and
#             (nombre is None or usuario["nombre"].lower() == nombre.lower()) and
#             (edad is  None or usuario["edad"] == edad)
#         ):
#             resultados.append(usuario)

#     if resultados:
#         return {"usuarios_encontrados": resultados}
#     else:
#         return {"mensaje": "No se encontraron usuarios que coincidan con los parámetros proporcionados."}