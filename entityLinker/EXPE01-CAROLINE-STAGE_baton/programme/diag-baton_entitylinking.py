#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May  4 11:07:50 2023

@author: obtic2023
"""
import json
import glob
import matplotlib.pyplot as plt

def lire_fichier (chemin):
    with open(chemin) as json_data: 
        dist =json.load(json_data)
    return dist


def stocker_graph(nomfich): 
    
    name_fig = "%s.png"
    print(" nom de la figure ", name_fig)
    plt.ylabel("nombre d'entités liées")
    plt.xlabel("OCR Version")
    plt.xticks(fontsize=10,rotation=25)
    # plt.axis([-1,7,0,1])  
    # plt.legend(loc="lower left",ncol=2, bbox_to_anchor=(0,0.98))
    # plt.legend 
    plt.gcf().set_size_inches(8, 9)
    plt.savefig(nomfich)
    plt.clf()
    
    return nomfich 

path_corpora = "../DATA/ELTeC-Fra_2023/*"

for subcorpus in glob.glob(path_corpora):
    x=["Réf"]
    
    # print(subcorpus)
    
  
    for path_version in glob.glob("%s/*"%subcorpus):  
        version_OCR = path_version.split("/")[-1]
        version_OCR = version_OCR.split("_")[-1]
        x.append(version_OCR)
        liste_loc_sm = []
        liste_loc_lg = []
        liste_autre_sm = []
        liste_autre_lg = []
        liste_loc_ref_lg=[]
        liste_autre_ref_lg=[] 
        liste_loc_ref_sm=[]
        liste_autre_ref_sm=[] 
        
        output=path_version.split("/")[-1]
        output=output.split("_")[0]        
        #print(x)
       

        for path in glob.glob("%s/*/*/*.json"%subcorpus):
            # liste_res=[]
            # print(path)
   
            data=lire_fichier(path)
            Loc = 0
            autre = 0
            cK=0
            
         
            for key, value in data.items():
                # print(value)
                cK+=1
                for cle, valeur in value.items():
                    # print(cle)
                    if cle == "type" and valeur =="LOC":
                        # print(valeur)
                        Loc+=1
                    # else:
                    #     autre+=1#le else ne compte pas les autre valeur de la clé "type"
                autre=cK-Loc
                
            if "REF" in path:
                if "sm" in path:
                    liste_loc_ref_sm.append(Loc)
                    liste_autre_ref_sm.append(autre)
                else:
                    liste_loc_ref_lg.append(Loc)
                    liste_autre_ref_lg.append(autre)

            else:
                if "sm" in path:
                    liste_loc_sm.append(Loc)
                    liste_autre_sm.append(autre)
                else:
                    liste_loc_lg.append(Loc)
                    liste_autre_lg.append(autre)
    print(path)
    print( liste_loc_ref_lg,liste_autre_ref_lg)
   
    liste_loc_sm.insert(0,liste_loc_ref_sm[0])
    liste_autre_sm.insert(0,liste_autre_ref_sm[0])
    liste_loc_lg.insert(0,liste_loc_ref_lg[0])
    liste_autre_lg.insert(0,liste_autre_ref_lg[0])
    dico_mod={}
    dico_mod["sm"]={}
    dico_mod["sm"]["Loc"]=liste_loc_sm
    dico_mod["sm"]["autre"]=liste_autre_sm
    dico_mod["sm"]["bottom"]=liste_loc_sm
    dico_mod["lg"]={}
    dico_mod["lg"]["Loc"]=liste_loc_lg
    dico_mod["lg"]["autre"]=liste_autre_lg
    dico_mod["lg"]["bottom"]=liste_loc_lg
       
    for k, va in dico_mod.items():
        print(k,va)
        for kk, vv in va.items():
            largeur_barre = 0.8
            ax=range(len(vv))
            if kk=="Loc":
                plt.bar(x,vv, width = largeur_barre, color = "red")
                plt.xticks(ax, x, rotation=90)
            if kk=="autre":
                plt.bar(x, vv, width = largeur_barre, bottom =dico_mod[k]["bottom"] , color = "blue")
            plt.xticks(ax, x, rotation=90)
        stocker_graph("../DATA/%s_spaCy-%s-linking.png"%(output,k))
    
        
    
       
        
        
        
        # # # Tracé
        
        
         
       
         
       
           
        # plt.show()
        # print(path)
        # 
        

  
  