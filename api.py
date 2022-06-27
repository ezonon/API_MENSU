# -*- coding: utf-8 -*-
"""
Created on Fri May 27 18:47:10 2022

@author: Viho
"""

from fastapi import FastAPI
import uvicorn
import os
from typing import Optional
from pydantic import BaseModel
app=FastAPI()

class MensuIn(BaseModel): 
    type_mensu : list
    type_de_logement : int
    usage_cuisson :	list
    eau_chaude : Optional[list]
    Chauffage_individuel : list
    surface_du_logement : str
    part_energie_verte : str
    four :	Optional[list]
    climatiseur : Optional[str]
    television : Optional[str]
    ordinateur : Optional[str]
    machine_a_laver : Optional[str]
    refrigerateur :	Optional[str]
    lave_vaisselle : Optional[str]
    seche_linge : Optional[str]
    congelateur_indépendant : Optional[str]
    zone_tarifaire_gaz : Optional[int]
    tarif_propose : Optional[list]
    echeance_mensuelle : Optional[list]
      
class MensuOut(BaseModel): 
    type_mensu : list 
    tarif_propose : list
    echeance_mensuelle : list
   
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
    mensuin.type_mensu[0]=1
    mensuin.type_mensu[1]=0
    mensuin.tarif_propose [0]="ST9 75%"
    mensuin.tarif_propose [1]=""
    mensuin.echeance_mensuelle[0]=150
    mensuin.echeance_mensuelle[1]=0
    #mensuout=MensuOut("elec","ST9 75%",150)
    return mensuin
    

if __name__ == "__main__" and os.environ.get("ENVIRONMENT") != "PRODUCTION":
    uvicorn.run(app, host="0.0.0.0",port=8000)
	
