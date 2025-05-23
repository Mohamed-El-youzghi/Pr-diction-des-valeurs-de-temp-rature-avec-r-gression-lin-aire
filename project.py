# -*- coding: utf-8 -*-
"""project.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1QhShOpmRX6L0nUw0BzZFM1tL1YzpK8Z6
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import os

# Fonction pour sauvegarder les graphiques en PNG
def save_plot(figure, filename, directory='plots'):
    if not os.path.exists(directory):
        os.makedirs(directory)
    path = os.path.join(directory, filename)
    figure.savefig(path, format='png')
    print(f"Graphique sauvegardé sous {path}")

# Charger les données
df = pd.read_csv('GlobalWeatherRepository.csv')

# Convertir la colonne 'last_updated' en datetime
df['last_updated'] = pd.to_datetime(df['last_updated'])

# Gestion des données temporelles
df.set_index('last_updated', inplace=True)

# Interpolation des valeurs manquantes
df.interpolate(method='time', inplace=True)

# Identifier les valeurs manquantes
missing_values = df[df['temperature_celsius'].isna()]
print("Valeurs manquantes de température :")
print(missing_values[['temperature_celsius']])

# Identifier les valeurs aberrantes (en utilisant l'écart-type)
mean_temp = df['temperature_celsius'].mean()
std_temp = df['temperature_celsius'].std()
threshold = 3 * std_temp  # Seuil pour les valeurs aberrantes
outliers = df[(df['temperature_celsius'] < mean_temp - threshold) | (df['temperature_celsius'] > mean_temp + threshold)]
print("Valeurs aberrantes de température :")
print(outliers[['temperature_celsius']])

# Visualisation des tendances climatiques
plt.figure(figsize=(14, 8))
plt.plot(df.index, df['temperature_celsius'], label='Température (°C)', color='blue')
plt.scatter(outliers.index, outliers['temperature_celsius'], color='red', label='Valeurs aberrantes')
plt.title('Tendances Climatiques avec Valeurs Aberrantes')
plt.xlabel('Date')
plt.ylabel('Température (°C)')
plt.legend()
save_plot(plt.gcf(), 'tendances_climatiques.png')
plt.show()

# Prédiction des valeurs de température avec régression linéaire
# Préparer les données pour la régression
df['time_index'] = (df.index - df.index[0]).days  # Convertir les dates en jours depuis la première date
X = df[['time_index']]
y = df['temperature_celsius']

# Diviser les données en ensembles d'entraînement et de test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Entraîner le modèle de régression linéaire
model = LinearRegression()
model.fit(X_train, y_train)

# Prédire les valeurs
y_pred = model.predict(X)

# Afficher les performances du modèle
mse = mean_squared_error(y, y_pred)
print(f"Erreur quadratique moyenne (MSE) du modèle : {mse:.2f}")

# Visualiser les prédictions
plt.figure(figsize=(14, 8))
plt.plot(df.index, df['temperature_celsius'], label='Température réelle (°C)', color='blue')
plt.plot(df.index, y_pred, label='Prédiction de température (°C)', color='orange', linestyle='--')
plt.scatter(outliers.index, outliers['temperature_celsius'], color='red', label='Valeurs aberrantes')
plt.title('Prédiction des Valeurs de Température')
plt.xlabel('Date')
plt.ylabel('Température (°C)')
plt.legend()
save_plot(plt.gcf(), 'prediction_temperature.png')
plt.show()


# Analyse des corrélations
correlation_matrix = df[['temperature_celsius', 'humidity', 'wind_kph', 'pressure_mb']].corr()

plt.figure(figsize=(10, 8))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt='.2f')
plt.title('Matrice de Corrélation')
save_plot(plt.gcf(), 'matrice_correlation.png')
plt.show()

# Analyse de corrélation avec test de Pearson
pearson_coef, p_value = stats.pearsonr(df['temperature_celsius'], df['humidity'])
print(f"Corrélation de Pearson entre Température et Humidité: {pearson_coef:.2f}, p-value: {p_value:.2f}")

pearson_coef, p_value = stats.pearsonr(df['temperature_celsius'], df['wind_kph'])
print(f"Corrélation de Pearson entre Température et Vitesse du vent: {pearson_coef:.2f}, p-value: {p_value:.2f}")

pearson_coef, p_value = stats.pearsonr(df['temperature_celsius'], df['pressure_mb'])
print(f"Corrélation de Pearson entre Température et Pression atmosphérique: {pearson_coef:.2f}, p-value: {p_value:.2f}")

# Visualisation des tendances climatiques (partie supplémentaire)
plt.figure(figsize=(14, 8))
plt.plot(df.index, df['temperature_celsius'], label='Température (°C)')
plt.plot(df.index, df['humidity'], label='Humidité (%)')
plt.plot(df.index, df['wind_kph'], label='Vitesse du vent (km/h)')
plt.title('Tendances Climatiques')
plt.xlabel('Date')
plt.ylabel('Valeurs')
plt.legend()
save_plot(plt.gcf(), 'tendances_climatiques_supplementaires.png')
plt.show()