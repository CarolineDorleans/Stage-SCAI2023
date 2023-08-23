#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 22 15:24:32 2023

@author: antonomaz
"""

import json
import spacy  # version 3.5
import glob


def lire_fichier(chemin):
    with open(chemin, "r", encoding="utf-8") as fichier:
        texte = fichier.read()
        return texte


def stocker(chemin, contenu):
    with open(chemin, "w") as w:
        json.dump(contenu, w, indent=2)


modele = ["md"]
path_corpora = "../DATA/ELTeC-Fra_2023/ADAM/ADAM_krakenbase/REF/*.txt"

for mod in modele:
    print("Pour le modèle:", mod, "\n")
    nlp = spacy.load("fr_core_news_" + mod)
    nlp.add_pipe("entityLinker", last=True)
    # Set up entity linker with knowledge base
    # Refer to Spacy documentation for entity linking setup

    for path in glob.glob(path_corpora):
        print("Entrée:", path)
        texte = lire_fichier(path)
        doc = nlp(texte)
        list_resultats = []
        list_entites = []
        i = 1
        dico={}
        for ent in doc.ents:
            #deb_contexte = str(doc[max(ent.start_char - 10, 0):ent.start_char])
            #fin_contexte = str(doc[ent.end_char:min(ent.end_char + 10, len(doc))])
            #context = deb_contexte + fin_contexte
            contexte = str(texte[ent.start_char-100:ent.start_char])+str(ent.text)+ str(texte[ent.end_char:ent.end_char+100])
            ide = "ID" + str(i)
            print(ide)
            #list_entites.append(ent.text)
            #resultat = str(doc[ent.start_char-50:ent.start_char])+ str(ent.text) + str(doc[ent.end_char:ent.end_char+50])
            #list_resultats.append(resultat)
            dico[ide]={}
            dico[ide]["texte"]= ent.text
            dico[ide]["char_start"]= ent.start_char
            dico[ide]["char_end"]= ent.end_char
            dico[ide]["label"]= ent.label_
            dico[ide]["contexte"]= contexte
            i += 1
            
            print(dico)
            #print(list_resultats)
            #stocker("%s_NER_contexte.json"%path,dico)
