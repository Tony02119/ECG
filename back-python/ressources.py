import os
import psutil
import time
import pandas as pd
from sklearn.metrics import classification_report, accuracy_score, precision_score, recall_score, f1_score


# Fonction pour surveiller les ressources (CPU et RAM) pendant l'exécution
def monitor_resources():
    cpu_usage = psutil.cpu_percent(interval=1)  # Utilisation CPU en pourcentage
    ram_usage = psutil.virtual_memory().percent  # Utilisation RAM en pourcentage
    return cpu_usage, ram_usage


# Fonction pour évaluer et enregistrer les résultats
def evaluate_and_log_results(model, X_test, y_test, y_pred, model_name, model_params, file_type, method, factor,
                             csv_file='results.csv'):
    # Calcul des métriques
    accuracy = accuracy_score(y_test, y_pred)
    class_report = classification_report(y_test, y_pred, output_dict=True)
    precision = precision_score(y_test, y_pred, average='weighted')
    recall = recall_score(y_test, y_pred, average='weighted')
    f1 = f1_score(y_test, y_pred, average='weighted')

    # Surveillance des ressources
    cpu_usage, ram_usage = monitor_resources()

    # Création du DataFrame pour stocker les résultats
    data = {
        'Model': [model_name],
        'Parameters': [str(model_params)],
        'File Type': [file_type],
        'Balancing Method': [method],
        'Augmentation Factor': [factor],
        'Accuracy': [accuracy],
        'Precision': [precision],
        'Recall': [recall],
        'F1 Score': [f1],
        'CPU Usage (%)': [cpu_usage],
        'RAM Usage (%)': [ram_usage]
    }

    # Ajout des accuracy par classe
    for label, metrics in class_report.items():
        if isinstance(metrics, dict):
            data[f'Precision_Class_{label}'] = [metrics['precision']]
            data[f'Recall_Class_{label}'] = [metrics['recall']]
            data[f'F1_Class_{label}'] = [metrics['f1-score']]

    df = pd.DataFrame(data)

    # Enregistrer ou ajouter les résultats au fichier CSV
    if csv_file and os.path.exists(csv_file):
        existing_df = pd.read_csv(csv_file)
        df = pd.concat([existing_df, df], ignore_index=True)

    df.to_csv(csv_file, index=False)
    print(f"Results logged in {csv_file}")
