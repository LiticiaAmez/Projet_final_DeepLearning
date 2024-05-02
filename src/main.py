import streamlit as st
import pandas as pd
from get_data import load_data
from pretraitements import preprocess_data
import visualisations
from visualisations import create_scatter_plot, create_histogram, create_interactive_bar_chart, stacked_bar_chart
from predictions import get_prediction_results
import folium

def main():
    st.title("Application basée sur la base des diagnostics de performance énergétique (DPE) par commune en France")

    data = load_data()

    if data:
        # Titre de la section de navigation avec une taille de police plus grande
        st.sidebar.markdown("<h1 style='text-align: left;'>Navigation</h1>", unsafe_allow_html=True)

    # Initialisation des variables
    df_ileDeFrance_preprocessed = None
    df_HorsIleDeFrance_preprocessed = None

    # Chargement des données depuis les fichiers CSV
    df_ileDeFrance = pd.read_csv("df_ileDeFrance.csv")
    df_HorsIleDeFrance = pd.read_csv("df_HorsIleDeFrance.csv")

    # Section de sélection des options générales
    section = st.sidebar.selectbox("Sélectionnez une section :", ["Données Brutes", "Données Prétraitées", "Visualisations", "Prédictions"])

    # Afficher la section sélectionnée
    if section == "Données Brutes":
        st.subheader("Données Brutes de L'API")
        st.write(data)  # Afficher les données brutes

    elif section == "Données Prétraitées":
        # Sélection du type de données prétraitées
        preprocess_type = st.sidebar.radio("Sélectionnez une catégorie de données prétraitées :", ["Île-de-France", "Hors Île-de-France"])

        if preprocess_type == "Île-de-France":
            st.subheader("Données prétraitées - Île-de-France")
            df_ileDeFrance_preprocessed, _ = preprocess_data(df_ileDeFrance, df_HorsIleDeFrance)
            st.write(df_ileDeFrance_preprocessed)  # Afficher les données prétraitées de l'Île-de-France

        elif preprocess_type == "Hors Île-de-France":
            st.subheader("Données prétraitées - Hors Île-de-France")
            _, df_HorsIleDeFrance_preprocessed = preprocess_data(df_ileDeFrance, df_HorsIleDeFrance)
            st.write(df_HorsIleDeFrance_preprocessed)  # Afficher les données prétraitées hors Île-de-France

    elif section == "Visualisations":
        # Sélection de la région à visualiser
        region_selection = st.sidebar.radio("Sélectionnez la région à visualiser :", ["Île-de-France", "Hors Île-de-France"])

        if region_selection == "Île-de-France":
            st.subheader("Visualisations pour la région d'Île-de-France")
            type_graphe = st.sidebar.radio("Sélectionnez le type de graphe  :", ["MAP", "Graphe à Barre", "Autres Graphes"])
            if type_graphe == "MAP":
                df_ileDeFrance_preprocessed, _ = preprocess_data(df_ileDeFrance, df_HorsIleDeFrance)
                visualisations.display_map(df_ileDeFrance_preprocessed)

            elif type_graphe == "Graphe à Barre":
                 df_ileDeFrance_preprocessed, _ = preprocess_data(df_ileDeFrance, df_HorsIleDeFrance)

                 stacked_bar_chart(df_ileDeFrance_preprocessed, 'annee_DPE', 'consommation_energie', 'surface_habitale_en_m²', 'Consommation d\'énergie par année et surface habitable en m²')
                 stacked_bar_chart(df_ileDeFrance_preprocessed, 'annee_DPE', 'consommation_energie', 'tr001_modele_dpe_id', 'Consommation d\'énergie par année et type du modele DPE')
                
            elif type_graphe == "Autres Graphes":
                df_ileDeFrance_preprocessed, _ = preprocess_data(df_ileDeFrance, df_HorsIleDeFrance)

                # Sélection de la fonction statistique pour l'axe Y
                y_function = st.selectbox("Sélectionnez la fonction statistique pour l'axe Y :", ["Somme", "Moyenne", "Maximum", "Minimum", "Écart-type"])

                # Sélection des colonnes pour les axes x et y
                x_column = st.selectbox("Sélectionnez la variable pour l'axe x :", df_ileDeFrance_preprocessed.columns)
                y_column = st.selectbox("Sélectionnez la variable pour l'axe Y :", ['consommation_energie', 'surface_habitale_en_m²', 'tr001_modele_dpe_id', 'tr006_type_usage_id', 'tr004_type_energie_id', 'consommation_energie_finale'])

                # Sélection du type de graphique
                type_graphique = st.selectbox("Sélectionnez le type de graphique :", ["Graphe à Barre", "Histogramme", "Nuages de points"])

                if type_graphique == "Graphe à Barre":
                    st.plotly_chart(create_interactive_bar_chart(df_ileDeFrance_preprocessed, x_column, y_column, y_function))
                elif type_graphique == "Histogramme":
                    fig = create_histogram(df_ileDeFrance_preprocessed, x_column, y_column, y_function)
                    st.plotly_chart(fig)
                elif type_graphique == "Nuages de points":
                    fig = create_scatter_plot(df_ileDeFrance_preprocessed, x_column, y_column, y_function)
                    st.plotly_chart(fig)
                
        #selection de la region Hors Île-de-France   
        elif region_selection == "Hors Île-de-France":
            st.subheader("Visualisations pour la région Hors Île-de-France")
            type_graphe = st.sidebar.radio("Sélectionnez le type de graphe :", ["MAP", "Graphe à barre","Autres Graphes"])
            if type_graphe == "MAP":
                _, df_HorsIleDeFrance_preprocessed = preprocess_data(df_ileDeFrance, df_HorsIleDeFrance)
                visualisations.display_map(df_HorsIleDeFrance_preprocessed)

            elif type_graphe == "Autres Graphes":
                _, df_HorsIleDeFrance_preprocessed = preprocess_data(df_ileDeFrance, df_HorsIleDeFrance)

                # Sélection de la fonction statistique pour l'axe Y
                y_function = st.selectbox("Sélectionnez la fonction statistique pour l'axe Y :", ["Somme", "Moyenne", "Maximum", "Minimum", "Écart-type"])

                # Sélection des colonnes pour les axes x et y
                x_column = st.selectbox("Sélectionnez la variable pour l'axe x :", df_HorsIleDeFrance_preprocessed.columns)
                y_column = st.selectbox("Sélectionnez la variable pour l'axe Y :", ['consommation_energie', 'surface_habitale_en_m²', 'tr001_modele_dpe_id', 'tr006_type_usage_id', 'tr004_type_energie_id', 'consommation_energie_finale'])

                # Sélection du type de graphique
                type_graphique = st.selectbox("Sélectionnez le type de graphique :", ["Graphe à Barre", "Histogramme", "Nuages de points"])

                if type_graphique == "Graphe à Barre":
                    st.plotly_chart(create_interactive_bar_chart(df_HorsIleDeFrance_preprocessed, x_column, y_column, y_function))
                elif type_graphique == "Histogramme":
                    fig = create_histogram(df_HorsIleDeFrance_preprocessed, x_column, y_column, y_function)
                    st.plotly_chart(fig)
                elif type_graphique == "Nuages de points":
                    fig = create_scatter_plot(df_HorsIleDeFrance_preprocessed, x_column, y_column, y_function)
                    st.plotly_chart(fig)
    
    elif section == "Prédictions":
    # Afficher les résultats de prédiction
        st.subheader("Prédictions de la consommation d'énergie :")

    #fonction pour afficher les predictions sur MAP
        def pred_viz(df, column_to_predict):
        # Obtenir les résultats de prédiction
            prediction_results, loss = get_prediction_results(df,column_to_predict)
            print(type(prediction_results))
            y_pred_column = prediction_results['Valeur prédite']

        # Afficher les résultats de prédiction
            st.write(prediction_results)

        # Afficher la perte (loss)
            st.subheader("Perte (Loss)")
            st.write("Perte (Loss) :", loss)

            df = df.drop(columns=['consommation_energie_finale'])
            df['Consommation_totale_predit'] = y_pred_column

            df= df.head(1000)

            st.subheader('Visualisation des prédictions des consomations totals par commune')
            m = folium.Map(location=[48.8566, 2.3522], zoom_start=5)
        # Ajouter des marqueurs pour chaque station
            for index, row in df.iterrows():
                popup_text = f"Code postal: {row['code_postal']}, Consommation_totale_predit: {row['Consommation_totale_predit']}"
                folium.Marker(location=[row['Latitude'], row['Longitude']], popup= popup_text).add_to(m)
        # Convertir la carte en HTML
            m_html = m.get_root().render()
        # Afficher la carte dans Streamlit
            st.components.v1.html(m_html, width=800, height=600)

        #Ajout d'un selectbox pour selectionner la valeur à prédire
        column_name_mapping = {
         "Consommation pour tous usages": "consommation_energie",
         "Consommation pour l'usage (chauffage) ": "consommation_energie_finale" 
         
        }
        column_to_predict_display = st.selectbox("Sélectionner la colonne à prédire", list(column_name_mapping.keys()))
        column_to_predict = column_name_mapping[column_to_predict_display]
        

        #Faire appel a la fonction pred_viz avc les deux dataframes
        st.subheader("Île-de-France")
        df_ileDeFrance_preprocessed, _ = preprocess_data(df_ileDeFrance, df_HorsIleDeFrance)
        pred_viz(df_ileDeFrance_preprocessed, column_to_predict)

        st.subheader("Hors Île-de-France")
        df_HorsIleDeFrance_preprocess = pd.read_csv("df_horsiledefrance_pret.zip",
                         
                         compression='zip',
                        index_col=None)
        #df_HorsIleDeFrance_preprocess= pd.read_csv("df_horsiledefrance_pret.csv")
        df_HorsIleDeFrance_preprocess['code_postal'] = df_HorsIleDeFrance_preprocess['code_postal'].replace('17 000', '17000')
        pred_viz(df_HorsIleDeFrance_preprocess, column_to_predict)



if __name__ == "__main__":
    main()
