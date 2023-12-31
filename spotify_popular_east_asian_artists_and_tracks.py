# -*- coding: utf-8 -*-
"""Spotify Popular East Asian Artists and Tracks.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1ojkCLPTq2TrEQ0dCtkPsFGzdveUpe54w
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from textblob import TextBlob
from tabulate import tabulate

#carga de data
# top artists
top_artists = pd.read_csv('/content/drive/MyDrive/practica/east_asia_top_artists.csv')

#top tracks
top_tracks = pd.read_csv('/content/drive/MyDrive/practica/east_asia_top_tracks.csv')

# Mostrar las primeras 5 filas del DataFrame top_artists
print(top_artists.head())

# Mostrar las primeras 5 filas del DataFrame top_tracks
print(top_tracks.head())

# Mostrar estadísticas descriptivas para las columnas numéricas
#top artista
print(top_artists.describe())

# Cambiar los nombres de las columnas para el dataset de pistas
df_tracks = top_tracks.rename(columns={
    'song_name': 'name',
    'album_name': 'album',
    'album_link': 'album_spotify_link',
    'artist_name': 'artist',
    'popularity': 'popularity_track',
    'release_date': 'release_date_track',
    'song_link': 'spotify_link',
    'duration_ms': 'duration_ms_track',
    'explicit': 'explicit_track',
    'query_genre': 'genre_track'
})

# Cambiar los nombres de las columnas para el dataset de artistas
df_artists = top_artists.rename(columns={
    'artist_name': 'artist',
    'popularity': 'popularity_artist',
    'followers': 'followers_artist',
    'artist_link': 'spotify_link_artist',
    'genres': 'genres_artist',
    'top_track': 'top_track_artist',
    'top_track_album': 'top_track_album_artist',
    'top_track_popularity': 'top_track_popularity_artist',
    'top_track_release_date': 'top_track_release_date_artist',
    'top_track_duration_ms': 'top_track_duration_ms_artist',
    'top_track_explicit': 'top_track_explicit_artist',
    'top_track_link': 'top_track_spotify_link_artist',
    'top_track_album_link': 'top_track_album_spotify_link_artist',
    'query_genre': 'query_genre_artist'
})

"""**Popularidad de artistas y pistas: se  identificara qué artistas y canciones son más populares en la región.**"""

#Realizar el análisis (Punto 1)
# Ordenar las pistas por popularidad en orden descendente
df_tracks_sorted = df_tracks.sort_values(by='popularity_track', ascending=False)

# Obtener las 10 canciones más populares
top_10_popular_tracks = df_tracks_sorted.head(10)

# Imprimir las 10 canciones más populares
print("Las 10 canciones más populares:")
print(top_10_popular_tracks[['name', 'artist', 'popularity_track']])

"""**Análisis de géneros: distribución de géneros musicales presentes en el dataset y analizar cuáles son los géneros más populares en Asia Oriental.**"""

# Para el punto 2:

plt.figure(figsize=(10, 6))
df_tracks['genre_track'].value_counts().plot(kind='bar', color='salmon')
plt.title('Distribución de Géneros Musicales en Pistas')
plt.xlabel('Género')
plt.ylabel('Cantidad de Pistas')
plt.xticks(rotation=45)
plt.show()

"""**Duración de las pistas**"""

# Realizar el análisis (Punto 3)
# Calcular la duración promedio de las pistas musicales
average_duration = df_tracks['duration_ms_track'].mean()

# Calcular la variación en la duración entre diferentes artistas o géneros
duration_variation_by_artist = df_tracks.groupby('artist')['duration_ms_track'].std()
duration_variation_by_genre = df_tracks.groupby('genre_track')['duration_ms_track'].std()

# Imprimir los resultados
print("Duración promedio de las pistas musicales: {:.2f} segundos".format(average_duration / 1000))
print("\nVariación en la duración por artista:")
print(duration_variation_by_artist)
print("\nVariación en la duración por género:")
print(duration_variation_by_genre)

"""**análisis de tendencias a lo largo del tiempo para observar cómo ha cambiado la popularidad de ciertos artistas o géneros a lo largo de los años.**"""

# Convertir la columna 'release_date_track' a tipo datetime
df_tracks['release_date_track'] = pd.to_datetime(df_tracks['release_date_track'], errors='coerce')

# Eliminar filas con fechas fuera del rango válido (opcional)
df_tracks = df_tracks.dropna(subset=['release_date_track'])

# Realizar el análisis (Punto 4)
# Agrupar por año y sumar las reproducciones para obtener la popularidad a lo largo del tiempo
popularity_by_year = df_tracks.groupby(df_tracks['release_date_track'].dt.year)['popularity_track'].sum()

# Crear la visualización
plt.figure(figsize=(12, 8))  # Ajustar el tamaño de la figura
popularity_by_year.plot(kind='line', marker='o', color='skyblue')
plt.title('Tendencias de Popularidad a lo largo de los años')
plt.xlabel('Año')
plt.ylabel('Reproducciones Totales')
plt.xticks(popularity_by_year.index, rotation=45)
plt.grid(True)

# Ajustar el tamaño de fuente para los números del eje y
plt.ticklabel_format(style='plain')  # Evitar notación científica en el eje y
plt.tick_params(axis='both', which='major', labelsize=12)

plt.show()

# Realizar el análisis (Punto 4)
# Convertir la columna 'release_date_track' a tipo datetime
df_tracks['release_date_track'] = pd.to_datetime(df_tracks['release_date_track'], errors='coerce')

# Extraer el año de la fecha de lanzamiento de las pistas
df_tracks['release_year'] = df_tracks['release_date_track'].dt.year

# Calcular la popularidad promedio de las pistas por año
average_popularity_by_year = df_tracks.groupby('release_year')['popularity_track'].mean()

# Imprimir los resultados
print("Popularidad promedio de las pistas por año:")
print(average_popularity_by_year)

# Realizar el análisis (Punto 4)
# Convertir la columna 'release_date_track' a tipo datetime
df_tracks['release_date_track'] = pd.to_datetime(df_tracks['release_date_track'], errors='coerce')

# Extraer el año de la fecha de lanzamiento de las pistas
df_tracks['release_year'] = df_tracks['release_date_track'].dt.year

# Calcular la popularidad promedio de las pistas por año
average_popularity_by_year = df_tracks.groupby('release_year')['popularity_track'].mean()

# Crear un gráfico de línea para mostrar los resultados
plt.plot(average_popularity_by_year)
plt.xlabel('Año')
plt.ylabel('Popularidad promedio')
plt.title('Popularidad promedio de las pistas por año')
plt.show()

"""**Colaboraciones: Examina qué artistas han colaborado más entre sí en pistas y cómo estas colaboraciones pueden haber influido en su popularidad.**"""

# Realizar el análisis (Punto 5)
# Contar las colaboraciones entre artistas en las pistas
collaborations_count = df_tracks.groupby('artist')['artist'].count()

# Ordenar los resultados en orden descendente
top_collaborations = collaborations_count.nlargest(10)

# Crear un dataframe con los resultados
result_dataframe = pd.DataFrame({'Artista': top_collaborations.index, 'Cantidad de Colaboraciones': top_collaborations.values})

# Imprimir el dataframe en formato de tabla
print("Top 10 artistas con más colaboraciones:")
display(result_dataframe.style.hide_index())

"""**analizar el sentimiento de las letras de las canciones y observar si hay tendencias en las emociones expresadas por los artistas.**"""

# Verificar si el dataset contiene la columna 'lyrics'
if 'lyrics' in df_tracks.columns:
    # Realizar el análisis de sentimiento (Punto 6)
    df_tracks['lyrics_sentiment'] = df_tracks['lyrics'].apply(lambda x: TextBlob(x).sentiment.polarity)

    # Imprimir los resultados
    print("Puntaje de sentimiento de las letras de las canciones:")
    print(df_tracks[['name', 'artist', 'lyrics_sentiment']])
else:
    print("El dataset no contiene la columna 'lyrics'. No es posible realizar el análisis de sentimiento.")

"""**Análisis geográfico:  investigar si hay diferencias en la popularidad de artistas y géneros en diferentes países de Asia Oriental**"""

# Realizar el análisis (Punto 7)
plt.figure(figsize=(10, 6))
sns.histplot(df_artists['popularity_artist'], kde=True, color='skyblue')
plt.title('Distribución de la Popularidad de los Artistas')
plt.xlabel('Popularidad')
plt.ylabel('Cantidad de Artistas')
plt.grid(True)
plt.show()

"""**Popularidad en diferentes países: Analiza en qué países fuera de Asia Oriental los artistas y pistas tienen más reproducciones y seguidores, para identificar su alcance global.**"""

# Realizar el análisis (Punto 8)
# Obtener la cuenta de géneros y su popularidad promedio por género
genres_count = df_artists['genres_artist'].str.split(';').explode().value_counts()
genres_popularity_mean = df_artists.groupby(df_artists['genres_artist'].str.split(';').explode())['popularity_artist'].mean()

# Crear la visualización de los géneros más populares
plt.figure(figsize=(12, 8))
genres_count.nlargest(10).plot(kind='bar', color='skyblue', alpha=0.8)
plt.title('Top 10 Géneros Musicales Más Populares de los Artistas')
plt.xlabel('Género Musical')
plt.ylabel('Cantidad de Artistas')
plt.grid(True)
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()

# Crear la visualización de la popularidad promedio por género
plt.figure(figsize=(12, 8))
genres_popularity_mean.nlargest(10).plot(kind='bar', color='orange', alpha=0.8)
plt.title('Top 10 Géneros Musicales con Mayor Popularidad Promedio de los Artistas')
plt.xlabel('Género Musical')
plt.ylabel('Popularidad Promedio')
plt.grid(True)
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()