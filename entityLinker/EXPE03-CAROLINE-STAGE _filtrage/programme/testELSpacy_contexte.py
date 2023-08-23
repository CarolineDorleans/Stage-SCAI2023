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
        dico = {}
        i = 1

        for ent in doc.ents:
            deb_contexte = str(doc[max(ent.start_char - 200, 0):ent.start_char])
            fin_contexte = str(doc[ent.end_char:min(ent.end_char + 200, len(doc))])
            context = deb_contexte + fin_contexte
            ide = "ID" + str(i)
            dico[ide] = {
                "texte": ent.text,
                "char_start": ent.start_char,
                "char_end": ent.end_char,
                "label": ent.label_,
                "contexte": context,
            }
            i += 1
            print(dico)
            for cle, valeur in dico.items():
                entourage = dico.get("contexte")
                entite = dico.get("texte")
                liste_entourage = []
                liste_entite = []
                liste_entite.append(entite)
                liste_entourage.append(entourage)
            for entourages in liste_entourage : 
                for ent in doc._.linkedEntities:
                    url_entourage = ent.get_url()
                    liste_url_entourage = []
                    liste_url_entourage.append[url_entourage]
            for entites in liste_entite : 
                for ent in doc._.linkedEntities:
                    url_entite = ent.get_url()
                    liste_url_entite= []
                    liste_url_entite.append[url_entite]
            
            if [c for c in liste_entourage if c in liste_url_entite] : 
                common_value = True
                
                
                    
                    
                
                