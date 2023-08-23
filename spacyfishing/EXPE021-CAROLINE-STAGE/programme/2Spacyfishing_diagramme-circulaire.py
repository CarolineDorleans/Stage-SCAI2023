#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 27 07:54:47 2023

@author: antonomaz
"""

import json 
import glob
from collections import Counter
import matplotlib.pyplot as plt
#import seaborn as sns

tab_exactitude = []
tab_nb = []
tab_label = []

def lire_fichier (chemin):
    with open(chemin) as json_data: 
        dist =json.load(json_data)
        return dist

# Charger le fichier de référence
path= "../DATA/ELTeC-Fra_2023/ADAM/ADAM_krakenbase/REF/commente_ADAM_Mon-village_REF.txt_entitylinker-fishing-fr-lg.json"


# Parcourir les autres fichiers JSON dans le répertoire

data=lire_fichier(path)
for cle, valeur in data.items() :
    for c, val in valeur.items():
        exactitude = valeur.get("exactitude")
        if exactitude== None :
            print (cle)
        tab_exactitude.append(exactitude)
c = Counter(tab_exactitude)
for key, value in c.items() :
    tab_nb.append(value)
    tab_label.append(key)

labels = "faux positif", "entités n'ayants pas de référents Wikidata", "entités bien liées", "entités mal liées mais de manière cohérente","entités liées d'une manière incohérente", "entités ayant un référent Wikidata mais non liées", "entitées relevées avec leur entourage" 
#sizes = [15, 80, 45, 40]
colors = ['yellowgreen', 'gold', 'lightskyblue', 'lightcoral','IndianRed','c','orchid']
plt.rc('legend', fontsize=6.2)

plt.pie(tab_nb, colors=colors, autopct='%1.0f%%', shadow=True, labeldistance = None, startangle=180)
#plt.pie(tab_nb, colors=sns.color_palette('Set2'), autopct='%1.0f%%', shadow=True, labeldistance = None, startangle=180)

plt.xticks(rotation=180)
plt.axis('equal')
#plt.figure(figsize=(8,8))
#plt.legend(labels, loc='best')
plt.legend(labels, loc='center', bbox_to_anchor=(0.5, 0.5, 0.8, 0.5))

#plt.savefig('PieChart02.png')
#plt.show()

        
        