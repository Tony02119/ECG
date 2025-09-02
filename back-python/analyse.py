import os
import numpy as np
import joblib
import random
import glob
import tensorflow as tf
from sklearn.preprocessing import LabelEncoder
from reader import read_ecg_file_frag, read_ecg_file_csv, plot_ecg_medical_to_base64
from management import normalize_data
from werkzeug.utils import secure_filename

# --------- Global settings ---------
file_type = 'full'
base_dir = 'data/AR'

CLASS_NAMES = [
    "VFL", "VF", "VTHR", "VTLR", "B", "HGEA", "VER", "AFIB",
    "SVTA", "SBR", "BI", "NOD", "BBB", "N", "Ne"
]

TARGET_LENGTHS = {
    'frag': 361,
    'full': 361,
    '10_3': 361,
    '15_2': 361
}

# --------- Core Functions ---------
def load_model(model_choice):
    model_dir = f'models/{file_type}'
    if model_choice in ['lstm', 'rnn', 'cnn', 'deep']:
        model_path = os.path.join(model_dir, f'{model_choice}_model.h5')
        model = tf.keras.models.load_model(model_path)
    else:
        model_path = os.path.join(model_dir, f'{model_choice}_model.pkl')
        model = joblib.load(model_path)

    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Model {model_choice} for {file_type} not found.")
    return model

def load_label_encoder():
    label_classes = np.load('results/label_classes.npy')
    label_encoder = LabelEncoder()
    label_encoder.classes_ = label_classes
    return label_encoder

def resize_ecg_data(X):
    target_length = TARGET_LENGTHS.get(file_type, X.shape[0])
    if len(X) > target_length:
        return X[:target_length]
    elif len(X) < target_length:
        return np.pad(X, (0, target_length - len(X)), 'constant')
    return X

def predict_ecg(model, X, model_choice):
    X = resize_ecg_data(X)

    if X.ndim == 1:
        X = X.reshape(1, -1)

    if model_choice in ['lstm', 'rnn', 'cnn', 'deep']:
        X = np.expand_dims(X, axis=2)
        y_pred_prob = model.predict(X)
    else:
        y_pred_prob = model.predict_proba(X)

    return y_pred_prob

def evaluate_danger_level_with_percentage(class_probabilities, class_names=None):
    if class_names is None:
        class_names = CLASS_NAMES
    danger_mapping = {
        "VFL": 95, "VF": 100, "VTHR": 85, "VTLR": 75, "B": 50,
        "HGEA": 30, "VER": 40, "AFIB": 30, "SVTA": 25, "SBR": 20,
        "BI": 40, "NOD": 30, "BBB": 50, "N": 0, "Ne": 50
    }
    return sum(danger_mapping.get(class_name, 0) * class_probabilities[i]
               for i, class_name in enumerate(class_names))

def reclassify_into_main_categories(class_probabilities, class_names=None):
    if class_names is None:
        class_names = CLASS_NAMES
    main_categories = {
        "Sinus Rhythm": ["N", "Ne", "BBB"],
        "Supraventricular": ["BI", "SVTA", "NOD", "SBR", "AFIB"],
        "Potentially Dangerous": ["HGEA", "VTLR", "B", "VER"],
        "Threatening VT": ["VTHR"],
        "Special Form TdP": ["VTTdP"],
        "Dangerous VFL/VF": ["VFL", "VF"]
    }

    results = dict.fromkeys(main_categories, 0)
    for i, class_name in enumerate(class_names):
        for category, sub_classes in main_categories.items():
            if class_name in sub_classes:
                results[category] += class_probabilities[i]

    total = sum(results.values())
    if total > 0:
        for k in results:
            results[k] = (results[k] / total) * 100
    return results

def save_dataset(file, upload_folder):
    """
    Save uploaded file to the specified upload folder.
    
    Args:
        file: The uploaded file object
        upload_folder: Directory path where the file should be saved
    
    Returns:
        str: Path to the saved file
    
    Raises:
        ValueError: If file format is invalid
        IOError: If file cannot be saved
    """
    if file is None:
        raise ValueError("No file provided")
    
    # Secure the filename
    filename = file.filename
    if hasattr(file, 'filename'):
        # For file objects that have secure_filename available
        try:
            filename = secure_filename(file.filename)
        except ImportError:
            # Fallback if werkzeug is not available
            filename = os.path.basename(file.filename)
    
    # Validate file format
    if not filename.lower().endswith('.csv'):
        raise ValueError("Invalid file format. Only .csv supported.")
    
    # Create upload folder if it doesn't exist
    os.makedirs(upload_folder, exist_ok=True)
    
    # Save the file
    saved_path = os.path.join(upload_folder, filename)
    try:
        with open(saved_path, "wb") as f:
            if hasattr(file, 'read'):
                # For file-like objects
                f.write(file.file.read())
            else:
                # For file content passed directly
                f.write(file)
    except Exception as e:
        raise IOError(f"Failed to save file: {str(e)}")
    
    return saved_path

# Get a random color for dataset categorization
def get_random_color():
    return random.choice(["green", "yellow", "red"])

def get_random_dataset_by_color(color_choice='green'):
    base_path="categorize_dataset/categorize"

    # Verifies if the base path exists
    if not os.path.exists(base_path):
        return FileNotFoundError(f"Base path does not exist: {base_path}")

    # Define the folder ranges based on the color choice
    folder_ranges = []
    if color_choice == "green":
        folder_ranges = ["0.0-9.0", "10.0-19.0", "20.0-29.0"]
    elif color_choice == "yellow":
        folder_ranges = ["30.0-39.0", "40.0-49.0", "50.0-59.0"]
    elif color_choice == "red":
        folder_ranges = ["60.0-69.0", "70.0-79.0", "80.0-89.0", "90.0-99.0"]
    else:
        raise ValueError("Invalid color choice. Use 'green', 'yellow', or 'red'.")
    
    # Collects all CSV files from the specified folders
    all_csv_files = []
    for folder_range in folder_ranges:
        folder_path = os.path.join(base_path, folder_range)
        if os.path.exists(folder_path):
            # Find all CSV files in the folder
            csv_pattern = os.path.join(folder_path, "*.csv")
            csv_files = glob.glob(csv_pattern)
            all_csv_files.extend(csv_files)
        else:
            raise FileNotFoundError(f"Folder not found: {folder_path}")
    
    # Verify if any CSV files were found
    if not all_csv_files:
        raise FileNotFoundError(f"No CSV files found for color choice '{color_choice}'")
    
    # Select a random CSV file from the collected files
    saved_path = random.choice(all_csv_files)
    # Verify if the selected file exists
    if not os.path.exists(saved_path):
        raise FileNotFoundError(f"Selected file does not exist: {saved_path}")
    
    return saved_path

# Get base64 plot from a ECG file
def get_ecg_plot_base64(file_path):
    if file_path and os.path.exists(file_path):
        if file_type == 'frag':
            X = read_ecg_file_frag(file_path)
        else:
            X = read_ecg_file_csv(file_path)
    else:
        raise FileNotFoundError("Missing or invalid file path.")

    X = normalize_data(X)
    return plot_ecg_medical_to_base64(X)

# Get a ECG plot base64 from a color_choice
def get_ecg_plot_base64_from_color_choice(color_choice='green'):
    saved_dataset = get_random_dataset_by_color(color_choice)
    result = {
        "plot_url": get_ecg_plot_base64(saved_dataset),
        "color_choice": color_choice
    }
    return result


# --------- 🧠 Main analysis function ---------
def analyze_ecg(file_path, model_choice='cnn'):

    if file_path and os.path.exists(file_path):
        if file_type == 'frag':
            X = read_ecg_file_frag(file_path)
        else:
            X = read_ecg_file_csv(file_path)
    else:
        raise FileNotFoundError("Missing or invalid file path.")

    X = normalize_data(X)
    ecg_image_base64 = plot_ecg_medical_to_base64(X)
    model = load_model(model_choice)
    label_encoder = load_label_encoder()
    y_pred_prob = predict_ecg(model, X, model_choice)

    class_probabilities = y_pred_prob.flatten()
    class_names = label_encoder.classes_

    if len(class_probabilities) != len(class_names):
        raise ValueError("Mismatch in predicted and known class lengths.")

    top_3_indices = np.argsort(class_probabilities)[-3:][::-1]
    top_3_classes = [class_names[i] for i in top_3_indices]
    top_3_probabilities = [class_probabilities[i] for i in top_3_indices]
    predicted_class = class_names[np.argmax(class_probabilities)]

    result = {
        "predicted_class": predicted_class,
        "class_probabilities": class_probabilities.tolist(),
        "danger_level": evaluate_danger_level_with_percentage(class_probabilities, class_names),
        "top_3_classes": top_3_classes,
        "top_3_probabilities": [float(prob) for prob in top_3_probabilities],
        "main_category_probabilities": reclassify_into_main_categories(class_probabilities, class_names),
        "ecg_plot_base64": ecg_image_base64,
    }

    return result
