from fastapi import  HTTPException,Depends
from fastapi.responses import JSONResponse
from modelsPydantic import ModelUsuario
from tokenGen import createToken
from middleWares import BearerJWT
from fastapi import APIRouter

#importaciones para sqlalquemy
#importacion de la sesion, la base y el motor
from DB.conexion import Session
#importacion de nuestros modelos de las tablas
from models.modelsDB import User #Personas #Animales #etc

from fastapi.encoders import jsonable_encoder

#---------ROUTER---APIRouter()-----------------#
routerUsuario = APIRouter()


#----------endpoint Consultar-----------------#

#dependencies=[Depends(BearerJWT())] 
@routerUsuario.get('/usuarios',tags=['Operaciones CRUD'])
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
@routerUsuario.get('/usuarios/{id}',tags=['Operaciones CRUD'])
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
@routerUsuario.post('/registrar/', response_model=ModelUsuario,tags=['Operaciones CRUD'])
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

@routerUsuario.put('/actualizar/{id}', response_model=ModelUsuario, tags=['Operaciones CRUD'])
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
@routerUsuario.delete('/borrar/{id}', response_model=ModelUsuario, tags=['Operaciones CRUD'])
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