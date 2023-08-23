import glob
import os
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import pairwise_distances
import json
from sklearn.neighbors import DistanceMetric
import sklearn

tab_distance = {}

def lire_fichier(chemin):
    with open(chemin) as json_data: 
        dist = json.load(json_data)
        return dist
def nom_mod(chemin):
    file_name=chemin.split("/")[-1]
    file_name=file_name.split("_")
    file_name=("_").join([file_name[2],file_name[-1]])
    
    return file_name
    
def tableau(data):
    # Création du tableau récapitulatif
    df = pd.DataFrame(data)
    print(df)
    table_latex = df.to_latex(index=False)
    print(table_latex)

def get_distances_word(texte1, texte2, N=1, liste_name =["jaccard", "braycurtis","dice", "cosinus"] ):
    dico = {}
    for metric_name in liste_name :
        dico[metric_name] = []
        liste_resultat_dist2 = []
#        for n_max in range(1, N+1):###range([min, default = 0], max, [step, default = 1]) 
        V = CountVectorizer(analyzer='word')
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

chemin = "../DATA/ELTeC-Fra_2023/ADAM/*/*/*.json"
fichiers = glob.glob(chemin)
resultats_distances = {}

for i in range(len(fichiers)):
      # Réinitialisation de la liste à chaque itération
    for j in range(i + 1, len(fichiers)):
        
        liste_span1 = []
        liste_span2 = []  # Réinitialisation de la liste à chaque itération
        fichier1 = lire_fichier(fichiers[i])
        file_name1=nom_mod(fichiers[i])
        fichier2 = lire_fichier(fichiers[j])
        file_name2=nom_mod(fichiers[j])
        # print(file_name1,"--",file_name2)
        resultats_distances[file_name1+"--"+file_name2]={}

    
        for cle, valeur in fichier1.items():
            for c, val in valeur.items():
                # print(k)
                if c == "label":
                    
                    # span1 = fichier1["span"]
                    liste_span1.append(val)
                    
        for key, value in fichier2.items():
            for k, v in value.items():
                if k == "label":
                    # span2 = fichier2["span"]
                    liste_span2.append(v)

        distances = get_distances_word(str(liste_span1), str(liste_span2))
        resultats_distances[file_name1+"--"+file_name2]=distances
        print (resultats_distances)
        
        

# # Affichage des résultats
# for resultat in resultats_distances:
#     fichier1, fichier2, distances = resultat
 
#     tab_distance = {}
#     tab_distance["fichier1"] = fichier1
#     tab_distance["fichier2"] = fichier2
#     tab_distance.update(distances)
    
   # print("-------------------")
    #tableau(tab_distance)
