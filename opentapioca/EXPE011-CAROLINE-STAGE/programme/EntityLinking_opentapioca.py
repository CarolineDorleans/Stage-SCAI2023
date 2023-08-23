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
import nltk
nltk.download('punkt') 

# def lire_fichier(chemin):
#     with open (chemin, "r", encoding="utf-8") as fichier:
#         texte=fichier.read()
#         return texte
def stocker(chemin, contenu):
    w =open(chemin, "w")
    w.write(json.dumps(contenu , indent = 2))
    w.close()

def decouper_en_phrases(chemin_fichier):
    with open(chemin_fichier, 'r', encoding='utf-8') as fichier:
        texte = fichier.read()
    phrases = nltk.sent_tokenize(texte)
    return phrases


modele=["md"]
# path_corpora = "../DATA/ELTeC-Fra_2023/*/*/*/*.txt"
path_corpora = "../DATA/ELTeC-Fra_2023/ADAM/ADAM_krakenbase/REF/*.txt"
delay = 20


for mod in modele:
    print("Pour le modèle : ",mod,"\n")
    # nlp = spacy.load("en_core_web_%s"%mod)
    nlp = spacy.load("fr_core_news_%s"%mod)
    nlp.add_pipe('opentapioca')
    
    for path in glob.glob(path_corpora):
        print("Entrée : ",path)
        txt=decouper_en_phrases(path)
        for phrase in txt : 
            doc = nlp(phrase) 
            i=0
            dico_sent_tok ={}
            for span in doc.ents:#Pour le typage avec les labels de l'entity linking
                ide = "ID"+str(i)
                dico_sent_tok[ide]={}
                dico_sent_tok[ide]["label"]= span.label_
                dico_sent_tok[ide]["description"]=span._.description
                # print(en.label_)
                dico_sent_tok[ide]["span"]=span.text
                dico_sent_tok[ide]["score"]= span._.score
                dico_sent_tok[ide]["ID wikidata"]=span.kb_id_
                i+=1
                time.sleep(delay)
                    
        stocker("%s_entitylinker-opentapioca-fr-%s.json"%(path,mod),dico_sent_tok)