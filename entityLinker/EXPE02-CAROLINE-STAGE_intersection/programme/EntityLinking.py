#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May  9 10:26:07 2023

@author: antonomaz
"""

import json
import spacy  # version 3.5
import glob


def lire_fichier(chemin):
    with open (chemin, "r", encoding="utf-8") as fichier:
        texte=fichier.read()
        return texte
def stocker(chemin, contenu):
    w =open(chemin, "w")
    w.write(json.dumps(contenu , indent = 2))
    w.close()
#modele=["sm","md","lg"]
modele=["md"]
# path_corpora = "../DATA/ELTeC-Fra_2023/*/*/*/*.txt"
path_corpora = "../DATA/ELTeC-Fra_2023/ADAM/ADAM_krakenbase/REF/*.txt"
for mod in modele:
    print("Pour le modèle : ",mod,"\n")
    # nlp = spacy.load("en_core_web_%s"%mod)
    nlp = spacy.load("fr_core_news_%s"%mod)
    nlp.add_pipe("entityLinker", last=True)
    
    
    for path in glob.glob(path_corpora):
        print("Entrée : ",path)
        txt=lire_fichier(path)
        doc = nlp(txt)  
        #doc = nlp(txt) 
        i=0
        dico_sent_tok ={}
        
        
        for ent in doc._.linkedEntities: 
                ide = "ID"+str(i)
                url_00 = ent.get_url()
                label_00=ent.get_label()
                description=ent.get_description()
                span_00=ent.get_span()
                span_oo=str(span_00)
                doc2=nlp(span_oo)
                for en in doc2.ents:#Pour le typage avec les labels de l'entity linking
                    
                    # print(en.label_)
                    dico_sent_tok[ide]={}
                    dico_sent_tok[ide]["url"]=url_00
                    dico_sent_tok[ide]["span"]=span_oo
                    dico_sent_tok[ide]["label"]=label_00
                    dico_sent_tok[ide]["description"]=description
                    dico_sent_tok[ide]["type"]=en.label_#Pour le typage avec les labels de l'entity linking
                    i+=1
                
        #*ùstocker("%s_entitylinker-spacy-fr-%s.json"%(path,mod),dico_sent_tok)