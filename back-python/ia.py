import os
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
import joblib
import plotly.express as px
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import classification_report, accuracy_score
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, SimpleRNN, Conv1D, MaxPooling1D, Dense, Dropout, Flatten, Input
from tensorflow.keras.utils import to_categorical
from management import *
from ressources import evaluate_and_log_results

# -----------------------------------------------------------------
# Paramètres globaux de traitement des données
# -----------------------------------------------------------------

# Chemin du répertoire contenant les données
base_dir = "data/AR"
# Type de fichier à charger ('frag', 'full', '10_3', '15_2')
file_type = 'full'
# Méthode d'équilibrage des classes ('smote', 'under', 'none')
method = 'none'
# Facteur d'augmentation des données
factor = 4
# Paramètres globaux de traitement des données (True/False)
use_scaler = True
# Équilibrer les classes en dupliquant les échantillons pour égaliser le nombre d'échantillons par classe
equal_class = True
# Sauvegarder le modèle après l'entraînement (True/False)
save_model = True

# -----------------------------------------------------------------
# Paramètres des modèles d'IA
# -----------------------------------------------------------------
# Choisir le modèle à utiliser ('svm', 'knn', 'rf', 'gbm', 'lstm', 'rnn', 'cnn', 'deep')
model_choice = 'rnn'
# Pour SVM
svm_kernel = 'rbf'  # Choix du noyau pour SVM ('linear', 'poly', 'rbf', 'sigmoid')
# Pour KNN
knn_neighbors = 5  # Nombre de voisins pour KNN
# Pour Random Forest
rf_n_estimators = 100  # Nombre d'arbres dans la forêt
# Pour Gradient Boosting Machine (GBM)
gbm_n_estimators = 100  # Nombre d'itérations de boosting

# Pour LSTM, RNN, CNN, Deep Learning
epochs = 10 # Nombre d'époques d'entraînement
batch_size = 32  # Taille des lots pour l'entraînement

# Paramètres spécifiques aux réseaux de neurones
lstm_units = 64  # Nombre de neurones dans les couches LSTM
rnn_units = 64  # Nombre de neurones dans les couches RNN
cnn_filters = 64  # Nombre de filtres dans les couches CNN
dense_units = 128  # Nombre de neurones dans les couches Dense

# Paramètres spécifiques au Q-learning
qlearning_params = {
    'n_states': 10,  # Nombre d'états pour le Q-learning
    'n_actions': None,  # Sera défini plus tard en fonction du nombre de classes
    'alpha': 0.1,  # Taux d'apprentissage
    'gamma': 0.99,  # Facteur de discount
    'epsilon': 0.1  # Facteur d'exploration
}

# -----------------------------------------------------------------
# Début du pipeline d'entraînement
# -----------------------------------------------------------------

# Charger les données et étiquettes
X, y = load_and_label_data(base_dir, file_type)


# Vérifier que toutes les séquences ont la même longueur
def verify_length():
    if len(set(map(len, X))) != 1:
        raise ValueError(
            "Les séquences ECG n'ont pas la même longueur. Assurez-vous de choisir un seul type de fichier à la fois.")


verify_length()

# Encoder les étiquettes
label_encoder = LabelEncoder()
y = label_encoder.fit_transform(y)

# Sauvegarder les classes d'étiquettes pour une utilisation future
np.save('results/label_classes.npy', label_encoder.classes_)

# Normaliser les données
X = normalize_data(X)

# Équilibrer les classes en dupliquant les échantillons pour égaliser le nombre d'échantillons par classe
if equal_class:
    X, y = balance_classes_by_duplication(X, y)

# Équilibrer les classes (si nécessaire)
X, y = balance_classes(X, y, method=method)

# Augmenter les données (si nécessaire)
if factor > 1:
    X, y = augment_data(X, y, factor=factor)

# Afficher la quantité de données et la distribution des classes
print(f"Quantité totale de données: {len(X)}")
print(f"Classes disponibles: {label_encoder.classes_}")
unique, counts = np.unique(y, return_counts=True)
class_distribution = dict(zip(label_encoder.inverse_transform(unique), counts))
print("Distribution des classes :", class_distribution)

# Diviser les données en ensembles d'entraînement et de test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Normalisation des données (utilisation d'un scaler après la division)
if use_scaler:
    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)

# Reshaper les données pour le LSTM, RNN, CNN et deep learning si nécessaire
if model_choice in ['lstm', 'rnn', 'cnn', 'deep']:
    # Ajouter une dimension de temps pour RNN/LSTM/CNN
    X_train = np.expand_dims(X_train, axis=2)
    X_test = np.expand_dims(X_test, axis=2)
    # Conversion des labels pour les rendre compatibles avec les modèles de Keras
    y_train = to_categorical(y_train)
    y_test = to_categorical(y_test)

# Utilisation de match-case pour choisir le modèle
match model_choice:
    case 'svm':
        # Entraîner une SVM avec un noyau radial
        model = SVC(kernel=svm_kernel, probability=True)
        model_params = {'kernel': svm_kernel}
    case 'knn':
        # Entraîner un KNN
        model = KNeighborsClassifier(n_neighbors=knn_neighbors)
        model_params = {'n_neighbors': knn_neighbors}
    case 'rf':
        # Entraîner un Random Forest
        model = RandomForestClassifier(n_estimators=rf_n_estimators, random_state=42)
        model_params = {'n_estimators': rf_n_estimators}
    case 'gbm':
        # Entraîner un Gradient Boosting Machine
        model = GradientBoostingClassifier(n_estimators=gbm_n_estimators, random_state=42)
        model_params = {'n_estimators': gbm_n_estimators}
    case 'lstm':
        # Construire et entraîner un modèle LSTM
        model = Sequential()
        model.add(Input(shape=(X_train.shape[1], X_train.shape[2])))  # Utiliser Input pour définir la forme d'entrée
        model.add(LSTM(lstm_units, return_sequences=True))
        model.add(Dropout(0.2))
        model.add(LSTM(lstm_units))
        model.add(Dropout(0.2))
        model.add(Dense(y_train.shape[1], activation='softmax'))

        model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
        model.fit(X_train, y_train, epochs=epochs, batch_size=batch_size, validation_data=(X_test, y_test))
        model_params = {'lstm_units': lstm_units, 'epochs': epochs, 'batch_size': batch_size}
    case 'rnn':
        # Construire et entraîner un modèle RNN
        model = Sequential()
        model.add(Input(shape=(X_train.shape[1], X_train.shape[2])))  # Utiliser Input pour définir la forme d'entrée
        model.add(SimpleRNN(rnn_units, return_sequences=True))
        model.add(Dropout(0.2))
        model.add(SimpleRNN(rnn_units))
        model.add(Dropout(0.2))
        model.add(Dense(y_train.shape[1], activation='softmax'))

        model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
        model.fit(X_train, y_train, epochs=epochs, batch_size=batch_size, validation_data=(X_test, y_test))
        model_params = {'rnn_units': rnn_units, 'epochs': epochs, 'batch_size': batch_size}
    case 'cnn':
        # Construire et entraîner un modèle CNN
        model = Sequential()
        model.add(Input(shape=(X_train.shape[1], X_train.shape[2])))  # Utiliser Input pour définir la forme d'entrée
        model.add(Conv1D(cnn_filters, kernel_size=3, activation='relu'))
        model.add(MaxPooling1D(pool_size=2))
        model.add(Dropout(0.2))
        model.add(Flatten())
        model.add(Dense(dense_units, activation='relu'))
        model.add(Dropout(0.2))
        model.add(Dense(y_train.shape[1], activation='softmax'))

        model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
        model.fit(X_train, y_train, epochs=epochs, batch_size=batch_size, validation_data=(X_test, y_test))
        model_params = {'cnn_filters': cnn_filters, 'dense_units': dense_units, 'epochs': epochs,
                        'batch_size': batch_size}
    case 'deep':
        # Construire et entraîner un modèle Deep Learning (Dense)
        model = Sequential()
        model.add(Input(shape=(X_train.shape[1], X_train.shape[2])))  # Aplatir les données pour l'entrée Dense
        model.add(Flatten())
        model.add(Dense(dense_units, activation='relu'))
        model.add(Dropout(0.2))
        model.add(Dense(dense_units, activation='relu'))
        model.add(Dropout(0.2))
        model.add(Dense(y_train.shape[1], activation='softmax'))

        model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
        model.fit(X_train, y_train, epochs=epochs, batch_size=batch_size, validation_data=(X_test, y_test))
        model_params = {'dense_units': dense_units, 'epochs': epochs, 'batch_size': batch_size}
    case _:
        raise ValueError("Modèle non supporté. Choisissez l'un de ceux disponible.")

# Entraînement du modèle
model.fit(X_train, y_train)

# Prédiction et évaluation du modèle
if model_choice in ['lstm', 'rnn', 'cnn', 'deep']:
    # Évaluation du modèle LSTM/RNN/CNN/Deep
    loss, accuracy = model.evaluate(X_test, y_test)
    y_pred = model.predict(X_test)
    y_pred = y_pred.argmax(axis=1)  # Convertir les prédictions en classes pour les métriques

    if len(y_test.shape) > 1 and y_test.shape[1] > 1:
        y_test = y_test.argmax(axis=1)  # Convertir y_test en classes pour les métriques
    print("Accuracy:", accuracy)
else:
    # Évaluation pour les autres modèles
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print("Accuracy:", accuracy)
    print(classification_report(y_test, y_pred))

# Enregistrer les résultats
evaluate_and_log_results(model, X_test, y_test, y_pred, model_choice, model_params, file_type, method, factor,
                         csv_file='results/results.csv')

# Sauvegarder le modèle si l'option est activée
if save_model:
    # Créer le répertoire spécifique au type de fichier s'il n'existe pas
    model_dir = f'models/{file_type}'
    os.makedirs(model_dir, exist_ok=True)

    if model_choice in ['lstm', 'rnn', 'cnn', 'deep']:
        model_save_path = os.path.join(model_dir, f'{model_choice}_model.h5')
        model.save(model_save_path)
        print(f"Modèle Keras sauvegardé sous: {model_save_path}")
    else:
        model_save_path = os.path.join(model_dir, f'{model_choice}_model.pkl')
        joblib.dump(model, model_save_path)
        print(f"Modèle Scikit-learn sauvegardé sous: {model_save_path}")
