import pandas as pd
import requests
import os
import json
import logging
from collections import defaultdict

def setup_logging():
    """Configure le système de logging"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('categorize_datasets.log'),
            logging.StreamHandler()  # Pour afficher aussi dans la console
        ]
    )
    return logging.getLogger(__name__)

def categorize_datasets():
    logger = setup_logging()
    
    # Lire le fichier CSV
    df = pd.read_csv('../back-python/data/mitbih_test.csv')
    logger.info(f"Début du traitement de {len(df)} lignes")
    
    # Créer le dossier categorize s'il n'existe pas
    os.makedirs('categorize', exist_ok=True)
    
    # Compteurs pour le résumé
    category_counts = defaultdict(int)
    success_count = 0
    error_count = 0
    
    # Traiter chaque ligne
    for index, row in df.iterrows():
        # Convertir la ligne en CSV string
        csv_line = ','.join(map(str, row.values))

        # Créer un fichier temporaire pour la ligne
        temp_line_df = pd.DataFrame([row.values], columns=df.columns)
        csv_path_temp = f"temp_line.csv"
        temp_line_df.to_csv(csv_path_temp, index=False, header=False)

        # Afficher le contenu de la ligne
        logger.info(f"Traitement de la ligne {index}: {csv_line}")
            
        try:
            # Appeler l'API
            with open(csv_path_temp, 'rb') as f:
                files = {'file': (csv_path_temp, f, 'text/csv')}
                data = {
                    'model_choice': 'cnn'
                }
                response = requests.post(
                    'http://localhost:8000/analyze',
                    files=files,
                    data=data
                )
            
            if response.status_code == 200:
                result = response.json()
                danger_level = result.get('danger_level', 0)
                
                # Déterminer le rang (0-9, 10-19, 20-29, etc.)
                rank = (danger_level // 10) * 10
                rank_folder = f"{rank}-{rank + 9}"
                
                # Créer le dossier pour cette catégorie
                folder_path = f"categorize/{rank_folder}"
                os.makedirs(folder_path, exist_ok=True)
                
                # Créer un fichier CSV pour cette ligne spécifique
                line_df = pd.DataFrame([row.values], columns=df.columns)
                csv_path = f"{folder_path}/line_{index:04d}.csv"
                line_df.to_csv(csv_path, index=False, header=False)
                
                # Compter pour le résumé
                category_counts[rank_folder] += 1
                success_count += 1
                
                logger.info(f"Ligne {index}: danger_level={danger_level}, catégorie={rank_folder}")
                logger.info(f"  -> Créé {csv_path}")
            else:
                error_count += 1
                logger.error(f"Erreur API pour ligne {index}: {response.status_code}")
                logger.error(f"  -> {response.text}")

            # Supprimer le fichier temporaire
            if os.path.exists(csv_path_temp):
                os.remove(csv_path_temp)
            
        except Exception as e:
            error_count += 1
            logger.error(f"Erreur pour la ligne {index}: {e}")
            # Nettoyer le fichier temporaire en cas d'erreur
            if os.path.exists(csv_path_temp):
                os.remove(csv_path_temp)
    
    # Résumé final
    logger.info("=" * 50)
    logger.info("RÉSUMÉ DE LA CATÉGORISATION")
    logger.info("=" * 50)
    logger.info(f"Total lignes traitées: {len(df)}")
    logger.info(f"Succès: {success_count}")
    logger.info(f"Erreurs: {error_count}")
    logger.info("")
    logger.info("Répartition par catégorie:")
    
    total_files = 0
    for category in sorted(category_counts.keys()):
        count = category_counts[category]
        total_files += count
        logger.info(f"  {category}: {count} fichiers")
    
    logger.info(f"\nTotal fichiers créés: {total_files}")
    
    # Vérifier la cohérence
    if total_files != success_count:
        logger.warning(f"Incohérence détectée: {success_count} succès mais {total_files} fichiers comptés")

if __name__ == "__main__":
    categorize_datasets()