# -*- coding: utf-8 -*-
"""
Created on Fri May 27 18:47:10 2022

@author: Viho
"""

from fastapi import FastAPI
import uvicorn
import os
import pandas as pd
from typing import Optional
from pydantic import BaseModel
app=FastAPI()

class MensuIn(BaseModel): 
    type_mensu_elec : int
    type_mensu_gaz : int
    type_de_logement : int
    Chauffage_individuel_elec : int
    Chauffage_individuel_gaz : int
    surface_du_logement : int
    part_energie_verte_elec : str
    part_energie_verte_gaz : str
    usage_cuisson_elec :	Optional[int] 
    usage_cuisson_gaz :	Optional[int] 
    eau_chaude_elec : Optional[int]
    eau_chaude_gaz : Optional[int]
    four_elec : int
    four_gaz : int
    climatiseur : Optional[int]
    television : Optional[int]
    ordinateur : Optional[int]
    machine_a_laver : Optional[int]
    refrigerateur :	Optional[int]
    lave_vaisselle : Optional[int]
    seche_linge : Optional[int]
    congelateur_indépendant : Optional[int]
    zone_tarifaire_gaz : int
    tarif_propose_elec : str
    tarif_propose_gaz : str
    echeance_mensuelle_elec : int
    echeance_mensuelle_gaz : int
      
class MensuOut(BaseModel): 
    type_mensu_elec : int
    type_mensu_gaz : int
    tarif_propose_elec : str
    tarif_propose_gaz : str
    echeance_mensuelle_elec : int
    echeance_mensuelle_gaz : int
   
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
    mensuin.type_mensu_elec=1
    mensuin.type_mensu_gaz=1
    mensuin.type_de_logement=1
    #mensuin.surface_du_logement=70
    if mensuin.surface_du_logement<=39 :
        varsurface='[jusqu''à 39 m²]'
    elif mensuin.surface_du_logement<=50 :
        varsurface='[40--50]'
    elif mensuin.surface_du_logement<=69 :
        varsurface='[51--69]'
    elif mensuin.surface_du_logement<=100 :
        varsurface='[70--100]'
    else :
        varsurface='À partir de 101 m²'
    if mensuin.Chauffage_individuel_elec==1 :
        varcolonne=varsurface+' Ind'
    else:
        varcolonne = varsurface+' Col'
    grille_file = 'calculette_Mensu_Yéli_20220620.xlsx'
    elec_sheet = 'Grille_Elec' 
    gaz_sheet = 'Grille_Gaz'
    df_elec=pd.read_excel(io=grille_file, sheet_name=elec_sheet)
    df_gaz=pd.read_excel(io=grille_file, sheet_name=gaz_sheet)
    '''
    mensuin.part_energie_verte_elec='75%'
    mensuin.usage_cuisson=1
    mensuin.eau_chaude_elec=1
    mensuin.four=1
    mensuin.climatiseur=1
    mensuin.television=0
    mensuin.ordinateur=0
    mensuin.machine_a_laver=1
    mensuin.refrigerateur=0
    mensuin.lave_vaisselle=0
    mensuin.seche_linge = 0
    mensuin.congelateur_indépendant=0 
    '''
    var_stdt= mensuin.Chauffage_individuel_elec+mensuin.eau_chaude_elec
    varp_elec = mensuin.usage_cuisson_elec+mensuin.Chauffage_individuel_elec+mensuin.eau_chaude_elec
    if varp_elec<=2 :
        para_puissance=6
    else :
        para_puissance=9
    if mensuin.tarif_propose_elec=='' :
        if var_stdt==2 :
            mensuin.tarif_propose_elec='DT'+str(para_puissance) +' '+ mensuin.part_energie_verte_elec
        else :
            mensuin.tarif_propose_elec='ST'+str(para_puissance) +' '+ mensuin.part_energie_verte_elec
    vart_gaz=mensuin.eau_chaude_gaz+mensuin.four_gaz
    if mensuin.tarif_propose_gaz=='' :
        if mensuin.Chauffage_individuel_gaz==1:
            mensuin.tarif_propose_gaz='B1 : 6001-30000 ' + mensuin.part_energie_verte_gaz
        elif (mensuin.usage_cuisson_gaz==1) and (vart_gaz>0) :
            mensuin.tarif_propose_gaz='B1 : 6001-30000 ' + mensuin.part_energie_verte_gaz
        elif (mensuin.usage_cuisson_gaz==1) and (vart_gaz==0) :
            mensuin.tarif_propose_gaz='B0 : 0-1000 ' + mensuin.part_energie_verte_gaz
        elif (vart_gaz>0) :
            mensuin.tarif_propose_gaz='B1 : 6001-30000 ' + mensuin.part_energie_verte_gaz
        else :
            mensuin.tarif_propose_gaz='Base : 0-1000 ' + mensuin.part_energie_verte_gaz
    
    varligne_gaz=str(mensuin.zone_tarifaire_gaz) + ' : '+ mensuin.tarif_propose_gaz
    print(varligne_gaz)
    varligne=mensuin.tarif_propose_elec
    df_elec = df_elec[df_elec.TYPE==varligne]
    df_gaz = df_gaz[df_gaz.TYPE==varligne_gaz]
    print(df_gaz)
    mensuin.echeance_mensuelle_elec=df_elec[varcolonne]
    mensuin.echeance_mensuelle_gaz=df_gaz[varsurface]
    return mensuin
    
if __name__ == "__main__" and os.environ.get("ENVIRONMENT") != "PRODUCTION":
    uvicorn.run(app, host="0.0.0.0",port=8000)
	
