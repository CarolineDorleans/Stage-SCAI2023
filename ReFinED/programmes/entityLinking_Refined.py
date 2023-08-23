#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 27 07:14:41 2023

@author: antonomaz
"""

import json
import glob
from refined.inference.processor import Refined


refined = Refined.from_pretrained(model_name='wikipedia_model_with_numbers',
                                  entity_set="wikipedia")


def lire_fichier(chemin):
    with open (chemin, "r", encoding="utf-8") as fichier:
        texte=fichier.read()
        return texte
def stocker(chemin, contenu):
    w =open(chemin, "w")
    w.write(json.dumps(contenu , indent = 2))
    w.close()

path_corpora = "../DATA/ELTeC-Fra_2023/*/*/*/*.txt"
#path_corpora = "../DATA/ELTeC-Fra_2023/ADAM/ADAM_krakenbase/REF/*.txt"


for path in glob.glob(path_corpora):
    print("Entrée : ",path)
    txt=lire_fichier(path)
    spans = refined.process_text(txt)
    ide= 1
    dico = {}
    for span in spans:
        str_span = str(span)
        dictionnaire = span.__dict__
        help(dictionnaire)
        #print(type(dictionnaire))
        dico[ide]= str_span
        ide+=1
    stocker("%s_entitylinker-refined.json"%(path),dico)