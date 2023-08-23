#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 16 14:43:10 2023

@author: antonomaz
"""
import spacy
import sklearn
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics import DistanceMetric
import glob
import json

def lire_fichier (chemin):
    with open(chemin) as json_data: 
        dist =json.load(json_data)
        file = json.dumps(dist)
        
    return file

def get_distances(texte1, texte2, N=1, liste_name =["jaccard", "braycurtis","dice", "cosinus"] ):
    dico = {}
    for metric_name in liste_name :
        dico[metric_name] = []
        liste_resultat_dist2 = []
        for n_max in range(1, N+1):###range([min, default = 0], max, [step, default = 1])

            #V = CountVectorizer(ngram_range=(1,n_max ), analyzer='char')
            V = CountVectorizer( analyzer='word')
            X = V.fit_transform([texte1, texte2]).toarray()
            
            if metric_name!= "cosinus" :  
                dist = DistanceMetric.get_metric(metric_name)    
                distance_tab1=dist.pairwise(X)
                liste_resultat_dist2.append(distance_tab1[0][1])
            else:
                distance_tab1=sklearn.metrics.pairwise.cosine_distances(X)
                liste_resultat_dist2.append(distance_tab1[0][1])
            dico[metric_name] = liste_resultat_dist2
    return dico
liste_span1 = []
liste_span2 = []

path_corpora = "../DATA/ELTeC-Fra_2023/ADAM/ADAM_krakenbase/*/*.json"
for subcorpus in glob.glob(path_corpora):
    dico = lire_fichier (subcorpus)
    for cle, valeur in dico.items():
        mot = dico.get("span")
        liste_span1.append(mot)
    for path in glob.glob(path_corpora):
        dicti = lire_fichier (path)
        for key, value in dicti.items():
            # print(cle)
            if key=="span":
                liste_span2.append(value)
    a = get_distances(liste_span1, liste_span2, liste_name =["jaccard", "braycurtis","dice", "cosinus"])
    print(a)

texte1 = "../DATA/ELTeC-Fra_2023/ADAM/ADAM_krakenbase/REF/ADAM_Mon-village_REF.txt_entitylinker-spacy-fr-lg.json"
texte2 = "../DATA/ELTeC-Fra_2023/ADAM/ADAM_krakenbase/REF/ADAM_Mon-village_REF.txt_entitylinker-spacy-fr-md.json"


