#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May  9 10:26:07 2023

@author: antonomaz
"""

import json
import spacy  # version 3.5
import glob
import time

def lire_fichier(chemin):
    with open (chemin, "r", encoding="utf-8") as fichier:
        texte=fichier.read()
        return texte
def stocker(chemin, contenu):
    w =open(chemin, "w")
    w.write(json.dumps(contenu , indent = 2))
    w.close()
modele=["sm","md","lg"]
#modele=["md"]
path_corpora = "../DATA/ELTeC-Fra_2023/*/*/*/*.txt"
#path_corpora = "../DATA/ELTeC-Fra_2023/ADAM/ADAM_krakenbase/REF/*.txt"

for mod in modele:
    print("Pour le modèle : ",mod,"\n")
    # nlp = spacy.load("en_core_web_%s"%mod)
    nlp = spacy.load("fr_core_news_%s"%mod)
    nlp.add_pipe('entityfishing')
    
    for path in glob.glob(path_corpora):
        print("Entrée : ",path)
        txt=lire_fichier(path)
        doc = nlp(txt)  
        #doc = nlp(txt) 
        i=0
        dico_sent_tok ={}
        
        
        for ent in doc.ents:
                ide = "ID"+str(i)
                dico_sent_tok[ide]={}
                dico_sent_tok[ide]["label"]=ent.label_
                #dico_sent_tok[ide]["description"]=description
                dico_sent_tok[ide]["span"]=ent.text
                dico_sent_tok[ide]["score"]=ent._.nerd_score
                dico_sent_tok[ide]["URL"]=ent._.url_wikidata
                dico_sent_tok[ide]["ID"]=ent._.kb_qid
                i+=1
        stocker("%s_entitylinker-fishing-fr-%s.json"%(path,mod),dico_sent_tok)