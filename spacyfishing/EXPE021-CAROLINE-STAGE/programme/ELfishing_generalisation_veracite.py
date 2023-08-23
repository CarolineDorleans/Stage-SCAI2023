# -*- coding: utf-8 -*-
"""
Created on Thu May 11 21:59:45 2023

@author: dorle
"""

import json 
import glob

def lire_fichier (chemin):
    with open(chemin) as json_data: 
        dist =json.load(json_data)
        return dist

# Charger le fichier de référence
path_ref= "../DATA/ELTeC-Fra_2023/ADAM/ADAM_krakenbase/REF/ADAM_Mon-village_REF.txt_entitylinker-fishing-fr-lg.json"
reference = lire_fichier(path_ref)

# Parcourir les autres fichiers JSON dans le répertoire
for path in glob.glob("../DATA/ELTeC-Fra_2023/ADAM/ADAM_krakenbase/REF/*.json"):
    print(path)
    data=lire_fichier(path)
    
    for cle, valeur in reference.items() :
        for c, val in valeur.items():
            ref_id = valeur.get("ID")
            exactitude_ref = valeur.get("exactitude")
            for key, value in data.keys():
                for k, v in value.items():
                    a_id = value.get("ID")
                    if ref_id is not None and ref_id == a_id :
                        print (ref_id, a_id)
                        data.update({"exactitude": exactitude_ref})
                
            
            
        
    
    # # Parcourir les dictionnaires dans le fichier
    # for d in data:
    #     # Vérifier si l'URL de la commune existe dans la référence
    #     if d['span'] in reference:
    #         # Ajouter la clé "veracite" avec la même valeur que dans la référence
    #         d['exactitude'] = reference[d['span']]['exactitude']

    # # Écrire les modifications dans le fichier
    # #with open(path, 'w') as f:
    #     #json.dump(data, f)