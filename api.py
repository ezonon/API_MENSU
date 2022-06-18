# -*- coding: utf-8 -*-
"""
Created on Fri May 27 18:47:10 2022

@author: Viho
"""

from fastapi import FastAPI
import uvicorn
from typing import Optional
from pydantic import BaseModel
app=FastAPI()

class MensuIn(BaseModel): 
    type_mensu : str 
    type_de_logement : str
    usage_cuisson :	str
    eau_chaude : Optional[str]
    Chauffage_individuel : str
    surface_du_logement : str
    part_energie_verte : str
    four :	Optional[str]
    climatiseur : Optional[str]
    television : Optional[str]
    ordinateur : Optional[str]
    machine_a_laver : Optional[str]
    refrigerateur :	Optional[str]
    lave_vaisselle : Optional[str]
    seche_linge : Optional[str]
    congelateur_indépendant : Optional[str]
    type_mensu : Optional[str] 
    tarif_propose : Optional[str]
    echeance_mensuelle : Optional[int]
class MensuOut(BaseModel): 
    type_mensu : str 
    tarif_propose : str
    echeance_mensuelle : int
    # machine_a_laver : Optional[str]
    # refrigerateur :	Optional[str]
    # lave_vaisselle : Optional[str]
    # seche_linge : Optional[str]

#get. put. delete.
#get
@app.get("/")
async def hello_world():
    return {"hello":" world"}
@app.post("/mensualisation/", response_model=MensuOut)
async def make_mensu(mensuin:MensuIn):
    mensuin.type_mensu="elec"
    mensuin.tarif_propose="ST9 75%"
    mensuin.echeance_mensuelle=150
    #mensuout=MensuOut("elec","ST9 75%",150)
    return mensuin
    

if __name__ == "__main__":
    uvicorn.run(app.host=="127.0.0.1",port=8000)
