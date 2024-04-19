#PARTIE MAP
import folium
from streamlit_folium import folium_static
import plotly.express as px
import streamlit as st

def display_map(df):
    # Limiter le DataFrame aux 1000 premières lignes
    df = df.head(2000)

    # Création de la carte Folium
    map = folium.Map(location=[48.8566, 2.3522], zoom_start=7)

    # Ajout des marqueurs pour Île-de-France
    for index, row in df.iterrows():
        folium.Marker(location=[row['Latitude'], row['Longitude']], popup=row['ville']).add_to(map)
    
    # Afficher la carte
    folium_static(map, width=900, height=600)

#-------------------------
#Partie Graphe à barre

import numpy as np

def create_interactive_bar_chart(df, x_column, y_column, y_function):
    # Group by the x_column and aggregate the y_column values based on the selected function
    if y_function == "Somme":
        grouped_data = df.groupby(x_column)[y_column].sum()
    elif y_function == "Moyenne":
        grouped_data = df.groupby(x_column)[y_column].mean()
    elif y_function == "Maximum":
        grouped_data = df.groupby(x_column)[y_column].max()
    elif y_function == "Minimum":
        grouped_data = df.groupby(x_column)[y_column].min()
    elif y_function == "Écart-type":
        grouped_data = df.groupby(x_column)[y_column].std()

    # Reset index to make the grouped data a DataFrame
    grouped_data = grouped_data.reset_index()

    # Create the bar chart using Plotly Express
    fig = px.bar(grouped_data, x=x_column, y=y_column)

    return fig

#--------------------
# Partie Histogramme
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

import plotly.graph_objects as go

import plotly.graph_objects as go

def create_histogram(df, x_column, y_column, y_function):
    # Group by the x_column and aggregate the y_column values based on the selected function
    if y_function == "Somme":
        grouped_data = df.groupby(x_column)[y_column].sum()
    elif y_function == "Moyenne":
        grouped_data = df.groupby(x_column)[y_column].mean()
    elif y_function == "Maximum":
        grouped_data = df.groupby(x_column)[y_column].max()
    elif y_function == "Minimum":
        grouped_data = df.groupby(x_column)[y_column].min()
    elif y_function == "Écart-type":
        grouped_data = df.groupby(x_column)[y_column].std()

    # Reset index to make the grouped data a DataFrame
    grouped_data = grouped_data.reset_index()

    # Create the histogram using Plotly Express
    fig = go.Figure(data=[go.Histogram(x=grouped_data[x_column], y=grouped_data[y_column], marker=dict(color='green'))])

    # Set axis labels
    fig.update_layout(xaxis_title=x_column, yaxis_title=y_column)

    return fig



#-----------------
# Partie Nuages de points
import plotly.express as px

def create_scatter_plot(df, x_column, y_column, y_function, color='blue'):
    # Group by the x_column and aggregate the y_column values based on the selected function
    df = df.head(1000)
    if y_function == "Somme":
        grouped_data = df.groupby(x_column)[y_column].sum()
    elif y_function == "Moyenne":
        grouped_data = df.groupby(x_column)[y_column].mean()
    elif y_function == "Maximum":
        grouped_data = df.groupby(x_column)[y_column].max()
    elif y_function == "Minimum":
        grouped_data = df.groupby(x_column)[y_column].min()
    elif y_function == "Écart-type":
        grouped_data = df.groupby(x_column)[y_column].std()

    # Reset index to make the grouped data a DataFrame
    grouped_data = grouped_data.reset_index()

    # Create the scatter plot using Plotly Express with custom color
    fig = px.scatter(grouped_data, x=x_column, y=y_column, color_discrete_sequence=['orange'])

    return fig

#----------------------------
##Partie Graphe à barre avec 3 colonnes
def stacked_bar_chart(df, x_column, y_column, category_column, title):
    fig = px.bar(df, x=x_column, y=y_column, color=category_column, title=title, 
                 labels={x_column: 'Année', y_column: 'Consommation d\'énergie', category_column: 'Catégorie'})
    st.plotly_chart(fig)
