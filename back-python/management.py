import numpy as np
from imblearn.over_sampling import SMOTE
from imblearn.under_sampling import RandomUnderSampler
from sklearn.utils import shuffle
from reader import *


# Fonction pour charger et étiqueter les données
def load_and_label_data(base_dir, file_type):
    all_data = []
    all_labels = []

    file_paths = get_file_paths(base_dir, file_type)
    for filepath in file_paths:
        if file_type == 'frag':
            data = read_ecg_file_frag(filepath)
        else:
            data = read_ecg_file_csv(filepath)

        if data is not None:
            all_data.append(data)
            label = os.path.basename(filepath).split('_')[2]
            all_labels.append(label)
    return np.array(all_data), np.array(all_labels)


# Fonction pour équilibrer les classes
def balance_classes(X, y, method):
    """
    Équilibre les classes dans les données.
    method : 'smote' pour sur-échantillonnage, 'under' pour sous-échantillonnage
    """
    unique, counts = np.unique(y, return_counts=True)
    class_distribution = dict(zip(unique, counts))

    # Vérification si SMOTE est applicable
    if method == 'smote':
        if any(count < 2 for count in counts):
            print("SMOTE ne peut pas être appliqué car certaines classes ont moins de 2 échantillons.")
            return X, y  # Retourner les données sans modification

        smote = SMOTE()
        X_res, y_res = smote.fit_resample(X, y)
    elif method == 'under':
        under = RandomUnderSampler()
        X_res, y_res = under.fit_resample(X, y)
    elif method == 'none':
        X_res, y_res = (X, y)
    else:
        raise ValueError("Méthode non supportée. Utilisez 'smote' ou 'under'.")

    X_res, y_res = shuffle(X_res, y_res)  # Mélanger les données pour éviter l'ordre biaisé
    return X_res, y_res


# Fonction pour augmenter les données
def augment_data(X, y, factor):
    """
    Multiplie les données en répétant les échantillons existants.
    factor : nombre de fois que les données doivent être répétées
    """
    if len(X) != len(y):
        raise ValueError("Les dimensions de X et y doivent être compatibles avant l'augmentation.")

    X_augmented = np.repeat(X, factor, axis=0)
    y_augmented = np.repeat(y, factor, axis=0)

    X_augmented, y_augmented = shuffle(X_augmented, y_augmented)  # Mélanger les données pour éviter l'ordre biaisé
    return X_augmented, y_augmented


# Fonction pour normaliser les données si nécessaire
def normalize_data(X):
    return (X - np.mean(X, axis=0)) / np.std(X, axis=0)

def balance_classes_by_duplication(X, y):
    """
    Équilibre le nombre d'échantillons par classe en dupliquant au hasard des échantillons pour les classes avec moins d'échantillons.
    """
    unique_classes, counts = np.unique(y, return_counts=True)
    max_count = max(counts)

    X_balanced = []
    y_balanced = []

    for cls in unique_classes:
        cls_indices = np.where(y == cls)[0]
        cls_samples = X[cls_indices]
        cls_labels = y[cls_indices]

        # Dupliquer les échantillons au hasard jusqu'à ce que la classe atteigne la taille maximale
        while len(cls_samples) < max_count:
            additional_samples = cls_samples[np.random.choice(len(cls_samples), max_count - len(cls_samples), replace=True)]
            cls_samples = np.vstack([cls_samples, additional_samples])
            cls_labels = np.hstack([cls_labels, np.full(len(additional_samples), cls)])

        X_balanced.append(cls_samples)
        y_balanced.append(cls_labels)

    X_balanced = np.vstack(X_balanced)
    y_balanced = np.hstack(y_balanced)

    return X_balanced, y_balanced