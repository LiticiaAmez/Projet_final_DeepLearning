import tensorflow as tf
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import pandas as pd
import numpy as np

# Fonction pour construire le modèle de réseau de neurones
def build_model(input_shape):
    # Création d'un modèle séquentiel
    model = tf.keras.Sequential([
        # Couche dense avec 128 neurones et activation ReLU
        tf.keras.layers.Dense(128, activation='relu', input_shape=input_shape),
        # Couche dense avec 64 neurones et activation ReLU
        tf.keras.layers.Dense(64, activation='relu'),
        # Couche dense avec 32 neurones et activation ReLU
        tf.keras.layers.Dense(32, activation='relu'),
        # Couche de sortie sans fonction d'activation (pour les régressions)
        tf.keras.layers.Dense(1)
    ])
    return model

#Fonction pour entrainer et évaluer le modèle
def train_and_evaluate_model(X_train_scaled, y_train, X_test_scaled, y_test):
    #construction du modèle
    model = build_model(X_train_scaled.shape[1:])
    # Compilation du modèle avec l'optimiseur Adam et la fonction de perte mean squared error
    model.compile(optimizer='adam', loss='mean_squared_error')
    # Entraînement du modèle sur les données d'entraînement avec validation split de 20%
    model.fit(X_train_scaled, y_train, epochs=50, batch_size=32, validation_split=0.2, verbose=0)

    return model
#Fonction pour effecuter des predictions
def make_predictions(model, X_test_scaled, y):
    #prediction des valeurs
    predictions = model.predict(X_test_scaled)
    results = []
    # Création d'un DataFrame pour stocker les résultats
    for i in range(len(predictions)):
        results.append({"Valeur prédite": predictions[i][0], "Valeur réelle": y.values[i]})
    df_results = pd.DataFrame(results)

    return df_results

# Fonction pour obtenir les résultats de prédiction
def get_prediction_results(df_preprocessed, column_to_predict, num_rows=1000 ):
    # Sélection d'un sous-ensemble des données
    df_subset = df_preprocessed.head(num_rows)
    # Séparation des caractéristiques et de la cible
    X = df_subset.drop(columns=[column_to_predict, 'ville'])
    # Encodage one-hot des caractéristiques catégorielles
    X = pd.get_dummies(X, columns=['description_usage', 'description_energie', 'nom_methode_dpe'])
    y = df_subset[column_to_predict]

    # Division des données en ensembles d'entraînement et de test
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Normalisation des données d'entraînement et de test
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    # Entraînement et évaluation du modèle
    model = train_and_evaluate_model(X_train_scaled, y_train, X_test_scaled, y_test)

    # Normalisation de l'ensemble de données initial pour les prédictions
    X_scaled = scaler.transform(X)

    # Prédictions sur l'ensemble de données
    prediction_results = make_predictions(model, X_scaled, y)
    # Calcul de la perte sur l'ensemble de test
    loss = model.evaluate(X_test_scaled, y_test)

    return prediction_results, loss


