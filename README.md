# Projet_DeepLearning

#AMEZIANE Liticia

##Pour lancer l'application, exécutez la commande "streamlit run main.py"

##Le fichier CSV "Base des diagnostics de performance énergétique (DPE) par commune (jusqu'en 2016)" récupéré est divisé en deux DataFrames : l'un pour la région Île-de-France et le deuxième pour toutes les autres régions qui sont hors Île-de-France.

##Le fichier mis à disposition en open data comprend les variables suivantes:

Code_postal = "code postal" : 5 caractères
tr002_type_batiment_id = "type de bâtiment" : maison (code 1) ; appartement (code 2)
annee_construction = "année de construction" : 4 caractères
surface_habitable = "surface habitable" : en m²
consommation_energie = "consommation énergie" : Consommation tous usages en kWh/m²
date_reception_dpe = "année du DPE" : 4 caractères
nom_methode_dpe = "méthode utilisée" : il y a plusieurs méthodes aggrées pour calculer et rendre compte du DPE.
tr001_modele_dpe_id = "type de DPE" : caractérise s'il s'agit d'une vente, d'une location, du neuf, ... et comment le DPE a été calculé. 
tr006_type_usage_id = code usage (cf champ suivant)
description = usage : chauffage dans pratiquement tous les cas de cette extraction
tr004_type_energie_id = code énergie
description = "énergie" : énergie correspondant à usage (chauffage) : liste de valeur (Bois, Biomasse, électricité, gaz, autre...)
consommation_energie_finale= "consommation énergie finale" : Consommation pour le usage uniquement (chauffage) (KWh)

