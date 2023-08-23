import json
import spacy  # version 3.5
import glob
import matplotlib.pyplot as plt
import pandas as pd

def lire_fichier(chemin):
    with open(chemin, "r", encoding="utf-8") as fichier:
        texte = fichier.read()
        return texte

def stocker(chemin, contenu):
    with open(chemin, "w") as w:
        json.dump(contenu, w, indent=2)

modele = ["md"]
path_corpora = "../DATA/ELTeC-Fra_2023/ADAM/ADAM_krakenbase/*/*.txt"
common_urls_per_file = []
common_urls = []
non_common_urls = []

for mod in modele:
    print("Pour le modèle:", mod, "\n")
    nlp = spacy.load("fr_core_news_" + mod)
    nlp.add_pipe("entityLinker", last=True)
    for path in glob.glob(path_corpora):
        print("Entrée:", path)
        texte = lire_fichier(path)
        doc = nlp(texte)
        list_resultats = []
        list_entites = []
        compteur = 0
        intersect = 0
        nb_entite = 0

        i = 1
        dico={}
        for ent in doc.ents:
            
            contexte = str(texte[ent.start_char-50:ent.start_char])+str(ent.text)+ str(texte[ent.end_char:ent.end_char+50])
            entite = ent.text
            
            print(entite)
            liste_url_entourage = []
            liste_url_entite = []
            doc3 = nlp(entite)
            doc2 = nlp(contexte)
            for ent in doc2._.linkedEntities:
                url_entourage = ent.get_url()
                liste_url_entourage.append(url_entourage)
            for ent in doc3._.linkedEntities:
                url_entite = ent.get_url()
                liste_url_entite.append(url_entite)
                #print (liste_url_entite)
                for d in liste_url_entite :
                    if d in liste_url_entourage :
                        #print (d)
                        intersect = intersect + 1
                    compteur +=1
            nb_entite+= 1
        
        non = compteur-intersect
        print ("La REN de Spacy a identifié",nb_entite, "entités")
        print("L'entity linker a repéré", compteur,"entités")
        print("Il y a ",intersect, "élments communs")
        print ("Il y a", non, "éléments qui ne sont pas en communs" )
        
        
        
#             common_urls.extend(liste_url_entite)
#             common_urls_per_file.append((path, set(liste_url_entite) & set(liste_url_entourage)))

#         non_common_urls.extend(liste_url_entite)

# # Calculate proportions
# total_common_urls = len(common_urls)
# total_non_common_urls = len(non_common_urls)
# total_urls = total_common_urls + total_non_common_urls
# common_urls_proportion = total_common_urls / total_urls
# non_common_urls_proportion = total_non_common_urls / total_urls

# # Create a bar plot
# labels = ['Common URLs', 'Non-Common URLs']
# proportions = [common_urls_proportion, non_common_urls_proportion]

# plt.bar(labels, proportions, color=['blue', 'red'])
# plt.xlabel('URL Types')
# plt.ylabel('Proportion')
# plt.title('Proportion of Common URLs and Non-Common URLs')
# plt.show()
