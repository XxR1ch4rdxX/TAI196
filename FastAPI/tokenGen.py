import jwt

def createToken(datos:dict):
    token:str = jwt.encode(payload=datos,key='passwrd',algorithm='HS256')
    return token
    