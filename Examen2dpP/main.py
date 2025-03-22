from fastapi import FastAPI, HTTPException,Depends
from fastapi.responses import JSONResponse
from typing import Optional, List
from ModelsPydantic import ModelEnvio


app=FastAPI(
    title='APIEvios2p',
    description='Api para el examen'
)

DBenvios = [
    {"cp":77777,"destino":"Mayami","peso":300},
    {"cp":88344,"destino":"Haway","peso":100},
    {"cp":1274,"destino":"Tumbuktu","peso":200},
    {"cp":85734,"destino":"Oklajoma","peso":30},
    {"cp":3484,"destino":"Ojayo","peso":10}
]
    
    
@app.get("/",tags=['Main'])
def main():
    return {'Hola FastAPI!':' Hola Richy'}

@app.get("/VerEnvios",response_model=ModelEnvio,tags=['EDP ver envios'])
def VerEnvios():
    return DBenvios

@app.post("/RegEnvio",response_model=ModelEnvio,tags=['EDP registrar envio'])
def RegEnvio(NewEnvio:ModelEnvio):
    for Env in DBenvios:
        if Env["cp"]==NewEnvio.cp:
            raise HTTPException(status_code=400,detail="Ese CP ya se uso")
    DBenvios.append(NewEnvio)
    return NewEnvio

@app.delete("/EliEnvio",tags=['EDP Elminar envio por CP'])
def EliuEnvio(cpELI:int):
    for envios in DBenvios:
        if envios["cp"]==cpELI:
            DBenvios.remove(envios)
            return {f'Se elimino el pedido {envios}'}
        else:
            raise HTTPException(status_code=404,detail="Esa cp no existe")