# git:https://github.com/XxR1ch4rdxX/TAI196
from fastapi import FastAPI, HTTPException,Depends
from fastapi.responses import JSONResponse
from typing import Optional, List
from modelsPydantic import ModelUsuario, ModelAuth
from tokenGen import createToken
from middleWares import BearerJWT

#importaciones para sqlalquemy
#importacion de la sesion, la base y el motor
from DB.conexion import Session,Base, engine
#importacion de nuestros modelos de las tablas
from models.modelsDB import User #Personas #Animales #etc

from fastapi.encoders import jsonable_encoder

app = FastAPI(
    title='FastAPI richy con documentacion',
    description='Ricardo Giovanny Sandoval Bermudez',
    version='0.0.1'
)
#levantar las tabls definidas en los modelo
Base.metadata.create_all(bind=engine)

#Para correr el servidor en la terminal
#.\VEF\Scripts\activate
#uvicorn main:app --reload --port 5000
#Base de datos temporal


@app.get("/",tags=['Raiz'])
def main():
    return {'Hola FastAPI!':' Hola Richy'}



#----------endpoint Consultar-----------------#

#dependencies=[Depends(BearerJWT())] 
@app.get('/usuarios',tags=['Operaciones CRUD'])
def Consultar():
    db=Session()
    try:
        consulta=db.query(User).all()
        return JSONResponse(content=jsonable_encoder(consulta))
    except Exception as x:
         return  JSONResponse(status_code=201,
                             content={
                                 "Mensaje":"Ha ocurrido un error al consultar",
                                 "Exepcion": str(x) })
    finally:
        db.close()
        
#----------------endpoint----consulta por id-------------------------
@app.get('/usuarios/{id}',tags=['Operaciones CRUD'])
def ConsultarID(id:int):
    db=Session()
    try:
        consulta=db.query(User).filter(User.id==id).first()
        
        if not consulta:
            return JSONResponse(status_code=2001,content={"Mensaje":"No se encontro el usuario"})
        return JSONResponse(content=jsonable_encoder(consulta))
    
    except Exception as x:
         return  JSONResponse(status_code=201,
                             content={
                                 "Mensaje":"Ha ocurrido un error al consultar",
                                 "Exepcion": str(x) })
    finally:
        db.close()
#----------endpoint RegistroNuevo------CON LA BASE EN SQLALCHEMY-----------#
@app.post('/registrar/', response_model=ModelUsuario,tags=['Operaciones CRUD'])
def Registrar(UsuarioNuevo:ModelUsuario):
    db=Session()
    try:
        db.add(User(**UsuarioNuevo.model_dump()))
        db.commit()
        return  JSONResponse(status_code=201,
                             content={
                                 "Mensaje":"Usuario Guardado Correctamente",
                                 "Usuario": UsuarioNuevo.model_dump() })
    except Exception as e:
        db.rollback()
        return  JSONResponse(status_code=201,
                             content={
                                 "Mensaje":"Ha ocurrido un error al Guardar el usuario",
                                 "Exepcion": str(e) })
    finally:
        db.close()
        
#----------endpoint Actualizar-----------------#

@app.put('/actualizar/{id}', response_model=ModelUsuario, tags=['Operaciones CRUD'])
def Actualizar(id:int, UsuarioActualizado:ModelUsuario):
    db=Session()
    try:
        query=db.query(User).filter(User.id==id).first()
        db.commit()
        
        if not query:
            return JSONResponse(status_code=2001,content={"Mensaje":"No se encontro el usuario"})
        
        db.query(User).filter(User.id==id).update(UsuarioActualizado.model_dump())
        db.commit()
        return JSONResponse(content={"Se ha acutualizado el usuario":str(UsuarioActualizado)})
        
    except Exception as e:
        db.rollback()
        return  JSONResponse(status_code=201,
                             content={
                                 "Mensaje":"Ha ocurrido un error al actualizar el usuario",
                                 "Exepcion": str(e) })
    finally:
        db.close()

#----------endpoint Eliminar-----------------#
@app.delete('/borrar/{id}', response_model=ModelUsuario, tags=['Operaciones CRUD'])
def Borrar(id:int):
    db=Session()
    try:      
        query1=db.query(User).filter(User.id==id).first()
        db.commit()
        if not query1:
            return JSONResponse(status_code=2001,content={"Mensaje":"No se encontro el usuario"})
        
        db.delete(query1)
        db.commit()
        return JSONResponse(content=jsonable_encoder("Se borro al usuario con el id: "+str(id)))

    except Exception as e:
        db.rollback()
        return  JSONResponse(status_code=201,
                             content={
                                 "Mensaje":"Ha ocurrido un error al eliminar el usuario",
                                 "Exepcion": str(e) })
    finally:
        db.close()

# #----------endpoint Actualizar-----------------#
# @app.put('/actualizar/{id}', response_model=ModelUsuario, tags=['Operaciones CRUD'])
# def actualizar(id: int, usuarioactualizado: ModelUsuario):
#     for index, usr in enumerate(usuarios):
#         if usr["id"] == id:
#             usuarios[index] = usuarioactualizado.model_dump()  
#             return usuarios[index]  
#     raise HTTPException(status_code=404, detail="Usuario no encontrado")
# #----------endpoint Eliminar-----------------#
# @app.delete('/borrar/',tags=['Operaciones CRUD'])
# def Borrar(idu:int):
#     for usr in usuarios:
#         if usr["id"]==idu:
#             usuarios.remove(usr)
#             return {'Mensaje':'Usuario Eliminado'},usuarios   
#     raise HTTPException(status_code=404,detail="Usuario no encontrado")
    
#----------endpoint para verificar con token JWT---------
@app.post('/auth' ,tags=['Autenticacion'])
def login(autorizado:ModelAuth):
    if autorizado.correo == 'richy@upq.com' and autorizado.password=='123456789':
        token:str = createToken(autorizado.model_dump())
        print(token)
        return JSONResponse(content={"token":token})

    else:
        return {"Aviso: ":"Usuario no autorizado"}
    

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