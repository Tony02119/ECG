import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.fft import fft
import wfdb
import random
from reader import *

base_dir = "data/AR"

# 2. Prétraitement des données
# Fonction pour obtenir tous les chemins des fichiers selon le type de fichier
def get_file_paths(base_dir, file_type):
    file_paths = []
    extension = '.dat' if file_type == 'frag' else '.csv'
    for root, dirs, files in os.walk(base_dir):
        for file in files:
            if file.endswith(f"_{file_type}{extension}"):
                if file_type == 'frag':
                    file_paths.append(os.path.join(root, file[:-4]))  # retirer l'extension pour wfdb
                else:
                    file_paths.append(os.path.join(root, file))
    return file_paths

# Fonction pour lire et stocker tous les ECG fragments dans un DataFrame
def load_ecg_data(base_dir, file_type='frag'):
    file_paths = get_file_paths(base_dir, file_type)
    if not file_paths:
        print(f"Aucun fichier trouvé pour le type {file_type} dans le répertoire {base_dir}")
    else:
        print(f"Fichiers trouvés : {file_paths}")

    ecg_data = []
    labels = []
    for filepath in file_paths:
        if file_type == 'frag':
            ecg_fragment = read_ecg_file_frag(filepath)
        else:
            ecg_fragment = read_ecg_file_csv(filepath)

        if ecg_fragment is not None:
            ecg_data.append(ecg_fragment)
            label = os.path.basename(filepath).split('_')[2]  # extrait le label du nom de fichier
            labels.append(label)

    if not ecg_data:
        print(f"Aucun fragment ECG n'a pu être lu pour le type {file_type}")

    return pd.DataFrame({'ECG': ecg_data, 'Label': labels})

# Fonction pour visualiser un fragment ECG
def plot_ecg_fragment(ecg_fragment, title="ECG Fragment"):
    plt.figure(figsize=(10, 4))
    plt.plot(ecg_fragment)
    plt.title(title)
    plt.xlabel("Time (s)")
    plt.ylabel("Amplitude (mV)")
    plt.show()

# Fonction pour visualiser le spectre d'un fragment ECG
def plot_ecg_spectrum(ecg_fragment, title="ECG Spectrum"):
    N = len(ecg_fragment)
    T = 1.0 / 360.0  # Sample spacing (assuming 360 Hz sampling rate)
    yf = fft(ecg_fragment)
    xf = np.fft.fftfreq(N, T)[:N // 2]
    plt.figure(figsize=(10, 4))
    plt.plot(xf, 2.0 / N * np.abs(yf[:N // 2]))
    plt.title(title)
    plt.xlabel("Frequency (Hz)")
    plt.ylabel("Amplitude")
    plt.show()

# Fonction pour choisir ou randomiser un fragment ECG
def choose_ecg_fragment(ecg_data, index=None):
    if index is None:
        index = random.randint(0, len(ecg_data) - 1)
    elif index < 0 or index >= len(ecg_data):
        raise ValueError("Index out of bounds.")
    ecg_fragment = ecg_data['ECG'].iloc[index]
    label = ecg_data['Label'].iloc[index]
    return ecg_fragment, label

# 3. Visualisation et sauvegarde des données
# Fonction pour sauvegarder les visualisations des fragments et leurs spectres dans des répertoires séparés
def save_ecg_visualizations(ecg_data, file_type, output_base_dir="ecg_visualizations"):
    output_dir = os.path.join(output_base_dir, file_type)
    os.makedirs(output_dir, exist_ok=True)
    for idx, row in ecg_data.iterrows():
        ecg_fragment = row['ECG']
        label = row['Label']
        fragment_file = os.path.join(output_dir, f"{idx}_fragment_{label}.png")
        spectrum_file = os.path.join(output_dir, f"{idx}_spectrum_{label}.png")

        plt.figure(figsize=(10, 4))
        plt.plot(ecg_fragment)
        plt.title(f"ECG Fragment - {label}")
        plt.xlabel("Time (s)")
        plt.ylabel("Amplitude (mV)")
        plt.savefig(fragment_file)
        plt.close()

        N = len(ecg_fragment)
        T = 1.0 / 360.0
        yf = fft(ecg_fragment)
        xf = np.fft.fftfreq(N, T)[:N // 2]

        plt.figure(figsize=(10, 4))
        plt.plot(xf, 2.0 / N * np.abs(yf[:N // 2]))
        plt.title(f"ECG Spectrum - {label}")
        plt.xlabel("Frequency (Hz)")
        plt.ylabel("Amplitude")
        plt.savefig(spectrum_file)
        plt.close()

# Types de fichiers à traiter
file_types = ['frag', 'full', '10_3', '15_2']
# Charger, visualiser et sauvegarder les données pour chaque type de fichier
for file_type in file_types:
    ecg_data = load_ecg_data(base_dir, file_type)
    if not ecg_data.empty:
        save_ecg_visualizations(ecg_data, file_type)
