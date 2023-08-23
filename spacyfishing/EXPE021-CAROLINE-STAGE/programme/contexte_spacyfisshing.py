
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 30 10:21:29 2023

@author: antonomaz
"""

import spacy
import glob
import pandas as pd
import os
import time
import json

def lire_fichier(chemin):
    with open(chemin, "r", encoding="utf-8") as fichier:
        texte = fichier.read()
        return texte

def stocker(chemin, contenu):
    with open(chemin, "w") as fichier:
        json.dump(contenu, fichier, indent=2)

def stocker_tex(name, contenu):
    with open(name, "w") as file:
        file.write(contenu)

def tableau(data, path, table_name, mod):
    df = pd.DataFrame(data)
    table_latex = df.to_latex(index=False)
    stocker_tex("%s_test-contexte_%s-%s.tex" % (path, table_name, mod), df.to_latex(index=False))
    #dictionary = df.to_dict('index')
    #print(dictionary)
    stocker("%s_test-contexte_-%s-%s.json" % (path, table_name, mod ), df.to_dict('index'))

t0 = time.time()  
modele=["fr_core_news_sm","fr_core_news_md","fr_core_news_lg"]

#path_corpora = "../DATA/ELTeC-Fra_2023/ADAM/ADAM_krakenbase/REF/*.txt"
path_corpora = "../DATA/ELTeC-Fra_2023/*/*/*/*.txt"
#modele = ["fr_core_news_sm"]

bilan = []
tab_entite_hors_contexte = []
tab_noncommun = []
#tab_basename = []

for mod in modele:
    print("Pour le modèle:", mod, "\n")
    nlp = spacy.load(mod)
    nlp.add_pipe('entityfishing')
    
    for path in glob.glob(path_corpora):
        basename = os.path.basename(path)
        print("Entrée:", path)
        texte = lire_fichier(path)
        
        doc = nlp(texte)
        compteur = 0
        intersect = 0
        nb_entite = 0
        nb_ent_EL = 0
        liste_EL_seulement = []
        liste_ent =[]
        
        for ent in doc.ents:
            EL_seulement = ent.get_span()
            liste_EL_seulement.append(EL_seulement)
        nb_ent_EL = len(liste_EL_seulement)
            
        for ent in doc.ents:
            contexte = str(texte[ent.start_char-200:ent.start_char]) + str(ent.text) + str(texte[ent.end_char:ent.end_char+200])
            entite = ent.text
            liste_ent.append(entite)
        
            
            liste_url_entourage = []
            liste_url_entite = []
            liste_label_entourage = []
            liste_label_entite = []
            liste_description_entourage = []
            liste_description_entite = []
            liste_concat_entourage = []
            liste_concat_entite = []
            
            doc3 = nlp(entite)
            doc2 = nlp(contexte)
            
            for ent in doc2.ents:
                url_entourage = ent.get_url()
                label_entourage = ent.get_label()
                description_entourage = ent.get_description()
                liste_url_entourage.append(url_entourage)
                liste_label_entourage.append(label_entourage)
                liste_description_entourage.append(description_entourage)
                concat_entourage = f"{label_entourage}: {description_entourage}"
                liste_concat_entourage.append(concat_entourage)
            
            for ent in doc3.ents:
                url_entite = ent.get_url()
                #print(url_entite)
                nom_entite = ent.get_label()
                description_entite = ent.get_description()
                concat_entite = f"{nom_entite}: {description_entite}"
                liste_url_entite.append(url_entite)
                print(liste_url_entite)
                liste_concat_entite.append(concat_entite)
                
                tab_entite_hors_contexte.append({
                    "Modele": mod,
                    "Fichier": basename,
                    "Entite REN SpaCy": entite,
                    "nb d'entites EL": len(liste_url_entite),
                    "Entites EL": liste_concat_entite,
                    "urls des entités reconnues par l'Entity Linker": liste_url_entite
                })

            for d in liste_url_entite:
                compteur += 1
                if d in liste_url_entourage:
                    intersect += 1
                
                else:
                    tab_noncommun.append({
                        "Modele": mod,
                        "Fichier": basename,
                        "Entite REN SpaCy": entite,
                        "contexte d'apparition de l'entite" : contexte,
                        "EL sans contexte": liste_concat_entite,
                        "url EL sans contexte": liste_url_entite,
                        "entites EL en contexte": liste_concat_entourage,
                        "url EL en contexte": liste_url_entourage
                    })
                    
        tableau(tab_entite_hors_contexte, path,"hors_contexte", mod)
        #tableau(bilan, path, "bilan", mod)
        tableau(tab_noncommun, path,"difference", mod)


t1 = time.time()
total = t1 - t0

print("Le code a mis", total, "secondes pour s'exécuter")