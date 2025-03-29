from fastapi.responses import JSONResponse
from modelsPydantic import ModelAuth
from tokenGen import createToken
from fastapi import APIRouter

#---------ROUTER---APIRouter()-----------------#
routerAuth = APIRouter()

    

@routerAuth.post('/auth' ,tags=['Autenticacion'])
def login(autorizado:ModelAuth):
    if autorizado.correo == 'richy@upq.com' and autorizado.password=='123456789':
        token:str = createToken(autorizado.model_dump())
        print(token)
        return JSONResponse(content={"token":token})

    else:
        return {"Aviso: ":"Usuario no autorizado"}
    