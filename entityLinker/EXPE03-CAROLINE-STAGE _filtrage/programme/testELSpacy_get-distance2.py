#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 23 11:08:45 2023

@author: antonomaz
"""

import spacy
import sklearn
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics import DistanceMetric
import glob
import json
import re

def lire_fichier(chemin):
    with open(chemin) as json_data: 
        dist = json.load(json_data)
        #file = json.dump(dist)
    return dist

def stocker(chemin, contenu):
    w =open(chemin, "w")
    w.write(json.dumps(contenu , indent = 2))
    w.close()

def nom_repertoire(chemin):
    for mot in glob.glob(chemin): 
        noms_rep = re.split("/", chemin)
        noms_repo = re.split("_",noms_rep[5])
        noms_repo = re.split("_",noms_repo[-1])
        noms_repo ="".join(noms_repo)
#        print("NOM FICHIER",noms_fichiers)
        return noms_repo
    
def recup_url(dico):
    liste_url=[]
    for key, value in data.items():
        # print(value)
        for cle, valeur in value.items():
            # print(cle)
            if cle=="url":
                liste_url.append(valeur)
            set_url=set(liste_url)
    return set_url

def nom_mod(path):
    for mot in glob.glob(path): 
        noms_mod = re.split("/", path)
        noms_mods = re.split("_",noms_mod[6])[-1]
        # nm = re.split("_",noms_mods[-2])
        # nmod ="".join(nm)
        return noms_mods

def get_distances(texte1, texte2):
    dico = {}
    N=1
    liste_name=["jaccard", "braycurtis", "dice", "cosinus"]
    for metric_name in liste_name:
        dico[metric_name] = []
        liste_resultat_dist2 = []
        for n_max in range(1, N+1):
            V = CountVectorizer(analyzer='word')
            X = V.fit_transform([texte1, texte2]).toarray()
            
            if metric_name != "cosinus":
                dist = DistanceMetric.get_metric(metric_name)    
                distance_tab1 = dist.pairwise(X)
                liste_resultat_dist2.append(distance_tab1[0][1])
            else:
                distance_tab1 = sklearn.metrics.pairwise.cosine_distances(X)
                liste_resultat_dist2.append(distance_tab1[0][1])
        
        dico[metric_name] = liste_resultat_dist2
    
    return dico

#path_corpora = "../DATA/ELTeC-Fra_2023/*/*/*"
path_corpora = "../DATA/ELTeC-Fra_2023/ADAM/*/*/*.json"
liste_EN_ocr = []
liste_EN_pp = []

for subcorpus in sorted(glob.glob(path_corpora)):
    for path in sorted(glob.glob("%s/*.json" % subcorpus)):
        print("subsubcorpus", path)
        auteur = subcorpus.split("/")[-2]
        auteur = auteur.split("_")[0]
        version_ocr = subcorpus.split("/")[-2]
        version_ocr = version_ocr.split("_")[-1]
        
        data = lire_fichier(path)
        nomrep = nom_repertoire(path)

        if nomrep == "REF" or nomrep == "PP":
            print(nomrep)
            liste_EN_pp.append(path)
            liste_EN_pp.append(version_ocr)
            liste_EN_pp.append(recup_url(data))
        elif nomrep == "OCR" or nomrep =="MOD":
            print(nomrep)
            liste_EN_ocr.append(path)
            liste_EN_ocr.append(version_ocr)
            liste_EN_ocr.append(recup_url(data))
    
liste_ocr_verif = [] 
liste_pp_verif = [] 
i = 0      

while i < len(liste_EN_ocr):
    nom_mod_ocr = nom_mod(liste_EN_ocr[i])
    nom_mod_pp = nom_mod(liste_EN_pp[i])
    liste_ocr_verif.append(nom_mod_ocr)
    liste_pp_verif.append(nom_mod_pp)
    i = i + 3

print(liste_ocr_verif)
print(liste_pp_verif)

result = True

for j in range(0, len(liste_ocr_verif)):
    if liste_ocr_verif[j] != liste_pp_verif[j]:
        result = False

k = 0

if result != False:
    while k < len(liste_EN_pp):
        path_base = liste_EN_ocr[k].split("/")
        path_out = "/".join([path_base[0], path_base[1], path_base[2], path_base[3]])
        file_name = path_base[-1]
        
        distances = get_distances(liste_EN_pp[k+2], liste_EN_ocr[k+2])
        # Utilisez les distances calculées selon les métriques souhaitées
        print (distances)
        #stocker("%s/%s_distance.png" % (path_out, file_name))
        k = k + 3
else:
    print("NOT OK")
