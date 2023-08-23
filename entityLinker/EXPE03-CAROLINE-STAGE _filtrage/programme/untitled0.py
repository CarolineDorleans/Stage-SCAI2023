#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 24 08:31:52 2023

@author: antonomaz
"""

import os
import glob

import spacy
import sklearn
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics import pairwise_distances
import glob
import json

def lire_fichier(chemin):
    with open(chemin) as json_data: 
        dist = json.load(json_data)
    return dist

def get_distances(texte1, texte2, N=1, liste_name=["jaccard", "braycurtis", "dice", "cosine"]):
    dico = {}
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



path_corpora = "../DATA/ELTeC-Fra_2023/ADAM/ADAM_krakenbase/*/*.json"
ref_files_path = for subcorpus in glob.glob(path_corpora):

resultats = []  # Liste pour stocker les résultats des différentes analyses

# Lire le contenu des fichiers du dossier REF
ref_files = [] 

for ref_file_path in ref_files_path:
    with open(ref_file_path, 'r') as f:
        texte_ref = f.read()
    ref_files.append(texte_ref)

# Parcourir les fichiers du corpus
file_paths = glob.glob(path_corpora)

# Parcourir les fichiers restants
for file_path in file_paths:
    if ref_folder in file_path:
        continue  # Ignorer les fichiers du dossier REF
    
    # Lire le contenu du fichier
    with open(file_path, 'r') as f:
        texte = f.read()
    
    # Comparer avec les fichiers du dossier REF
    is_ref_file = False
    for ref_texte in ref_files:
        if texte == ref_texte:
            is_ref_file = True
            break
    
    if is_ref_file:
        continue  # Ignorer les fichiers identiques aux fichiers du dossier REF
    
    # Appliquer la fonction get_distances
    distances = get_distances(texte, texte_ref)
    
    # Ajouter les résultats à la liste
    resultats.append((file_path, distances))

# Afficher les résultats sous forme de tableau
for file_path, distances in resultats:
    print("Fichier analysé:", file_path)
    print("Métriques de distance:")
    for metric_name, liste_resultat_dist2 in distances.items():
        print(metric_name, ":", liste_resultat_dist2)
    print("-" * 20)
