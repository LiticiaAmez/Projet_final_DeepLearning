import pandas as pd

def order_columns(df):
    # Définir l'ordre des colonnes
    ordered_columns = ['code_postal', 'ville', 'annee_construction', 'type_batiment_Appartement', 'type_batiment_Maison',
                       'surface_habitale_en_m²', 'consommation_energie', 'nom_methode_dpe', 'tr001_modele_dpe_id',
                       'tr006_type_usage_id', 'description_usage', 'tr004_type_energie_id',
                       'description_energie', 'consommation_energie_finale', 'annee_DPE', 
                       'Latitude', 'Longitude']
    
    # Réorganiser les colonnes selon l'ordre spécifié
    df = df[ordered_columns]
    
    return df

def preprocess_data(df_ileDeFrance, df_HorsIleDeFrance):
   # Renommer les colonnes dans df_HorsIleDeFrance
    df_HorsIleDeFrance.rename(columns={'surface_habitable': 'surface_habitale_en_m²', 'description': 'description_usage', 'description.1': 'description_energie'}, inplace=True)

# Renommer les colonnes dans df_ileDeFrance
    df_ileDeFrance.rename(columns={'surface_habitable': 'surface_habitale_en_m²', 'description': 'description_usage', 'description.1': 'description_energie'}, inplace=True)
 

    # Convertir les valeurs des colonnes
    df_ileDeFrance['code_postal'] = df_ileDeFrance['code_postal'].astype(str)
    df_ileDeFrance['annee_construction'] = df_ileDeFrance['annee_construction'].apply(lambda x: str(int(x)) if not pd.isnull(x) else '')
    df_ileDeFrance['annee_DPE'] = df_ileDeFrance['annee_DPE'].apply(lambda x: str(int(x)) if not pd.isnull(x) else '')
   

    df_HorsIleDeFrance['code_postal'] = df_HorsIleDeFrance['code_postal'].astype(str)
    df_HorsIleDeFrance['annee_construction'] = df_HorsIleDeFrance['annee_construction'].apply(lambda x: str(int(x)) if not pd.isnull(x) else '')
    df_HorsIleDeFrance['annee_DPE'] = df_HorsIleDeFrance['annee_DPE'].apply(lambda x: str(int(x)) if not pd.isnull(x) else '')

    
    # Diviser la colonne 'coordonnees' en deux colonnes distinctes pour la latitude et la longitude pour le DataFrame hors_ile_de_france_df
    df_HorsIleDeFrance[['Latitude', 'Longitude']] = df_HorsIleDeFrance['coordonnees'].str.split(',', expand=True)
    # Convertir les valeurs de latitude et de longitude en nombres flottants
    df_HorsIleDeFrance['Latitude'] = df_HorsIleDeFrance['Latitude'].astype(float)
    df_HorsIleDeFrance['Longitude'] = df_HorsIleDeFrance['Longitude'].astype(float)
    # Supprimer la colonne 'coordonnees' d'origine
    df_HorsIleDeFrance.drop(columns=['coordonnees'], inplace=True)

    # Diviser la colonne 'coordonnees' en deux colonnes distinctes pour la latitude et la longitude pour le DataFrame ile_de_france_df
    df_ileDeFrance[['Latitude', 'Longitude']] = df_ileDeFrance['coordonnees'].str.split(',', expand=True)
    # Convertir les valeurs de latitude et de longitude en nombres flottants
    df_ileDeFrance['Latitude'] = df_ileDeFrance['Latitude'].astype(float)
    df_ileDeFrance['Longitude'] = df_ileDeFrance['Longitude'].astype(float)
    # Supprimer la colonne 'coordonnees' d'origine
    df_ileDeFrance.drop(columns=['coordonnees'], inplace=True)

    # Remplacer les valeurs manquantes dans le DataFrame de l'Île-de-France
    df_ileDeFrance['surface_habitale_en_m²'].fillna(-1, inplace=True)
    df_ileDeFrance.dropna(inplace=True)
    

    # Remplacer les valeurs manquantes dans le DataFrame pour le reste de la France
    df_HorsIleDeFrance['code_postal'].fillna('Inconnu', inplace=True)
    df_HorsIleDeFrance['surface_habitale_en_m²'].fillna(-1, inplace=True)
    df_HorsIleDeFrance['ville'].fillna('Inconnu', inplace=True)
    df_HorsIleDeFrance.dropna(inplace=True)

    # Appliquer l'encodage one-hot sur la colonne 'tr002_type_batiment_id' pour Île-de-France
    df_ileDeFrance = pd.get_dummies(df_ileDeFrance, columns=['tr002_type_batiment_id'], prefix='type_batiment', dtype=int)

    # Appliquer l'encodage one-hot sur la colonne 'tr002_type_batiment_id' pour le reste de la France
    df_HorsIleDeFrance = pd.get_dummies(df_HorsIleDeFrance, columns=['tr002_type_batiment_id'], prefix='type_batiment', dtype=int)
    
    # Réorganiser les colonnes dans un ordre spécifique
    df_ileDeFrance = order_columns(df_ileDeFrance)
    df_HorsIleDeFrance = order_columns(df_HorsIleDeFrance)

    return df_ileDeFrance, df_HorsIleDeFrance
