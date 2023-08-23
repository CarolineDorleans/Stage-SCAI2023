#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 22 16:58:03 2023

@author: antonomaz
"""
import glob
import spacy
import json

def lire_fichier (chemin):
    with open(chemin) as json_data: 
        dist =json.load(json_data)
    return dist

def stocker(chemin, contenu):
    with open(chemin, "w") as w:
        json.dump(contenu, w, indent=2)

path_corpora = "../DATA/ELTeC-Fra_2023/ADAM/ADAM_krakenbase/REF/*.txt"

    # bouclez à travers tous les fichiers dans le dossier
for path in glob.glob(path_corpora): 
    if "REN" in str(path):
        nlp = spacy.load("fr_core_news_lg")
        liste_resultat = []
        common_values = 0
        print(path)
        dictionnaires=lire_fichier(path)
        #doc = nlp(txt[:5000])  
        for cle, valeur in dictionnaires.items():
            liste_entourage = []
            liste_entite = []
            liste_url_entite = []
            liste_url_entourage = []
            entourage = valeur["contexte"]
            entite = valeur["texte"]
            liste_entite.append(entite)
            liste_entourage.append(entourage)
            nlp.add_pipe("entityLinker", last=True)
            doc = nlp(entourage[50000])
            doc2 = nlp(entite[50000])
            for ent in doc._.linkedEntities:
                url_entourage = ent.get_url()
                liste_url_entourage.append(url_entourage)

            for ent in doc2._.linkedEntities:
                url_entite = ent.get_url()
                liste_url_entite.append(url_entite)
            if (liste_url_entite & liste_url_entourage):
                common_values =+1
                
        liste_resultat.append(common_values)
            
