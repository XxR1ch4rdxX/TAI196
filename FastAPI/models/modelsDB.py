#nota: para un proyecto es recomendado tener un archivo por cada modelo
# es decir, un archivo de models por tabla para ubicarlas mas facilmente

from DB.conexion import Base
#aqui declaramos los datos que vamos a usar en nuestras tablas
from sqlalchemy import Column,Integer,String 

class User(Base):
    __tablename__='tb_users'
    id=Column(Integer,primary_key=True,autoincrement='auto')
    name=Column(String)
    age=Column(Integer)
    email=Column(String)
    