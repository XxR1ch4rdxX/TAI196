from fastapi import HTTPException, Request
from fastapi.security import HTTPBearer
from tokenGen import validateToken

#Sincronia: método de priogramacion que no espera a que el servidor 
# responda, lanza la petición y en cuanto responda, arroja algo.
#Asincronia: método de programación que espera a que el servidor responda para lanzar la sig, petición.
#En este caso, el método __call__ es asíncrono, porque espera a que el servidor responda para lanzar la siguiente petición.

class BearerJWT(HTTPBearer):
    async def __call__(self, request:Request):
        auth= await super().__call__(request)
        data= validateToken(auth.credentials)
        
        if not isinstance(data,dict):
            raise HTTPException(status_code=403,detail="Formato Incorrecto del token")
        
        if data.get('correo')!='richy@upq.com':
            raise HTTPException(status_code=403,detail="Credenciales no validas")
        