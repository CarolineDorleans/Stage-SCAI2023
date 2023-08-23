#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 24 20:36:55 2023

@author: antonomaz
"""

import spacy
import sklearn
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics import pairwise_distances
import glob
import json

def lire_fichier(chemin):
    with open(chemin) as json_data: 
        dist = json.load(json_data)
        donnee = json.dumps(dist)
    return donnee

def get_distances(texte1, texte2, N=1):
    dico = {}
    liste_name=["jaccard", "braycurtis", "dice", "cosine"]
    for metric_name in liste_name:
        dico[metric_name] = []
        liste_resultat_dist2 = []
        for n_max in range(1, N+1):
            V = CountVectorizer(ngram_range=(1, n_max), analyzer='word')
            X = V.fit_transform([texte1, texte2]).toarray()

            if metric_name != "cosine":
                distance_tab1 = pairwise_distances(X, metric=metric_name)
                liste_resultat_dist2.append(distance_tab1[0][1])
            else:
                distance_tab1 = pairwise_distances(X, metric="cosine")
                liste_resultat_dist2.append(distance_tab1[0][1])
        dico[metric_name] = liste_resultat_dist2
    return dico

liste_span1 = []
liste_span2 = []

path_corpora = "../DATA/ELTeC-Fra_2023/ADAM/ADAM_krakenbase/*/*.json"
for path in glob.glob(path_corpora):
    dico = lire_fichier(path)
    for file in glob.glob(path_corpora):
        dict = lire_fichier(file)
        get_distances(dict, dico, N=1)
        