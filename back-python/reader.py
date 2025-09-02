import os
import wfdb
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as signal
import io
import base64
import scipy.interpolate as interp

# 1. Téléchargement et lecture des données
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

# Fonction pour lire un fichier ECG avec wfdb (pour frag)
def read_ecg_file_frag(filepath):
    try:
        record = wfdb.rdrecord(filepath)
        data = record.p_signal.flatten()
        return data
    except Exception as e:
        print(f"Erreur lors de la lecture du fichier {filepath}: {e}")
        return None

# Fonction pour lire un fichier CSV (pour full, 10_3, 15_2)
def read_ecg_file_csv(filepath):
    try:
        data = pd.read_csv(filepath, header=None)
        return data.values.flatten()
    except Exception as e:
        print(f"Erreur lors de la lecture du fichier {filepath}: {e}")
        return None


def detect_significant_changes(ecg_data, threshold=0.5):
    """
    Détecte les segments de l'ECG où les changements sont significatifs,
    en utilisant la dérivée du signal et un seuil défini.

    Arguments:
    ecg_data -- Array des données ECG
    threshold -- Seuil pour détecter les changements (par défaut 0.5)

    Retourne:
    start, end -- Indices définissant le début et la fin de la région intéressante
    """
    # Calcul de la dérivée pour détecter les variations rapides
    derivative = np.abs(np.diff(ecg_data))

    # Filtrage pour lisser le signal dérivé
    smoothed_derivative = signal.medfilt(derivative, kernel_size=5)

    # Trouver les indices où la variation dépasse le seuil
    significant_indices = np.where(smoothed_derivative > threshold)[0]

    if len(significant_indices) == 0:
        return 0, len(ecg_data)  # Si rien n'est trouvé, on retourne tout le signal

    # Retourner le premier et dernier indice où les changements sont significatifs
    start, end = significant_indices[0], significant_indices[-1]

    return start, end

def plot_ecg_medical_to_base64(ecg_data, fs=500, threshold=0.5):
    """
    Plot d'un signal ECG en utilisant un format médical avec grille, et renvoie l'image encodée en base64.
    Les points d'origine sont mis en évidence avec une couleur rouge foncé, et l'échelle s'ajuste dynamiquement.

    Arguments:
    ecg_data -- Array des données ECG
    fs -- Fréquence d'échantillonnage (par défaut 500 Hz)
    threshold -- Seuil pour détecter les changements flagrants (par défaut 0.5)

    Retourne:
    base64_string -- Image encodée en base64 du plot
    """
    # Détection des changements significatifs
    start, end = detect_significant_changes(ecg_data, threshold)
    ecg_segment = ecg_data[start:end]

    # Temps correspondant à ce segment
    t = np.arange(len(ecg_segment)) / fs

    # Interpolation cubique pour lisser le signal
    interp_func = interp.interp1d(t, ecg_segment, kind='cubic')

    # Générer plus de points entre les points d'origine pour une courbe lissée
    t_fine = np.linspace(t[0], t[-1], num=len(t) * 10)  # Plus de points pour le lissage
    ecg_smooth = interp_func(t_fine)

    # Détermination des limites pour l'axe Y
    amplitude_min, amplitude_max = np.min(ecg_smooth), np.max(ecg_smooth)
    margin = 0.1 * (amplitude_max - amplitude_min)  # Marge de 10 % pour éviter de couper la courbe

    # Création de la figure
    fig, ax = plt.subplots(figsize=(10, 6))

    # Couleur de fond de la grille comme le papier ECG
    ax.set_facecolor("#fce4e4")  # Couleur légèrement rosée, proche du papier ECG

    # Ajout de la grille avec divisions plus fréquentes
    ax.set_xticks(np.arange(0, t[-1], 0.01), minor=True)  # Petites divisions tous les 0.01s (plus petites divisions)
    ax.set_yticks(np.arange(np.floor(amplitude_min), np.ceil(amplitude_max), 0.1),
                  minor=True)  # Petites divisions tous les 0.1 mV (petit carré)
    ax.set_yticks(np.arange(np.floor(amplitude_min), np.ceil(amplitude_max),
                            0.5))  # Grandes divisions tous les 0.5 mV (grand carré)

    # Format de la grille médicale ECG avec des lignes plus visibles
    ax.grid(which='both', color='pink')  # Grille légèrement rose
    ax.grid(which='minor', linestyle=':', linewidth='0.5', color='pink')  # Grille fine pour les petites divisions
    ax.grid(which='major', linestyle='-', linewidth='1', color='red')  # Grille plus épaisse pour les grandes divisions

    # Plot de la courbe lissée de l'ECG
    ax.plot(t_fine, ecg_smooth, color="black", linewidth=1.5)  # Courbe en noir, plus proche des tracés ECG médicaux

    # Mettre en évidence les points originaux avec des marqueurs rouge foncé (bg-red-800)
    ax.scatter(t, ecg_segment, color="#7F1D1D", s=30, zorder=5)  # Marqueurs visibles sur la courbe

    # Titres et labels
    ax.set_title('Identified ECG Sector', fontsize=14)
    ax.set_xlabel('Time (s)')  # Garde l'unité en secondes pour l'axe des X
    ax.set_ylabel('Amplitude (mV)')

    # Ajustement dynamique des limites des axes pour s'assurer que la courbe n'est pas coupée
    ax.set_xlim([0, t[-1]])  # Ajuster automatiquement l'axe X à la durée réelle du signal
    ax.set_ylim([amplitude_min - margin, amplitude_max + margin])  # Limites ajustées en fonction du signal

    # Enregistrer l'image dans un buffer
    buffer = io.BytesIO()
    plt.tight_layout()
    plt.savefig(buffer, format='png')
    plt.close(fig)  # Fermer la figure pour libérer la mémoire

    # Encodage en base64
    buffer.seek(0)
    img_base64 = base64.b64encode(buffer.read()).decode('utf-8')
    buffer.close()

    return img_base64