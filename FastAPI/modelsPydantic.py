from pydantic import BaseModel,Field,EmailStr

#gt=0 es para que el id sea mayor a 0
class ModelUsuario(BaseModel):
    name:str =Field(...,min_length=3,max_length=15,description="Solo cadenas de texto, debe contener letras y espacios")
    age:int = Field(...,gt=0,le=130,description="Edad debe ser un entero, mayor a 0 y menor a 130")
    email: EmailStr = Field(...,example="Usuario@correo.com",description="Correo electronico valido, ejemplo:Usuario@correo.com")

class ModelAuth(BaseModel):
    correo:EmailStr
    password:str = Field(...,min_length=8,strip_whitespace=True,description="Contrasenna mayor a 8 caracteres")
