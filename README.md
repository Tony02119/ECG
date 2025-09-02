# ECG Analysis with AI - Healthcare Prediction System

## 🎯 Project Overview

This project demonstrates the use of AI models for ECG (Electrocardiogram) analysis to detect dangerous cardiac arrhythmias that could indicate cardiovascular risks. The system uses multiple machine learning algorithms trained on medical datasets to classify heartbeats and provide risk assessments.

The solution combines a Python backend with AI models and a Vue.js frontend, providing an automated ECG analysis system capable of:
- Detecting various types of cardiac arrhythmias
- Classifying heartbeats into 15 different categories
- Providing danger level assessments (1-6 scale)
- Generating medical-grade ECG visualizations
- Supporting multiple AI model architectures

## 📁 Project Structure
```
healthview-ecg-prediction/ 
├── README.md 
├── docker-compose.yml 
├── .gitignore 
├── back-python/ # Backend API and AI models 
│   ├── ai-ecg.ipynb # Main analysis notebook (French) 
│   ├── ai-ecg-en.ipynb # English version of analysis 
│   ├── analyse.py # Core analysis functions 
│   ├── ia.py # AI model training script 
│   ├── lambda_function.py # FastAPI server 
│   ├── management.py # Data management utilities 
│   ├── reader.py # ECG data reading and visualization 
│   ├── graph.py # Data visualization utilities 
│   ├── ressources.py # Resource monitoring and logging 
│   ├── requirements.txt # Python dependencies 
│   ├── Dockerfile # Backend containerization 
│   ├── data/ # ECG datasets 
│   │   └── AR/ # Arrhythmia dataset 
│   ├── models/ # Trained AI models 
│   ├── results/ # Training results and metrics 
│   ├── uploaded_files/ # User-uploaded ECG files 
│   └── categorize_dataset/ # Dataset categorization tools 
└── front-vue/ # Frontend application 
    ├── src/ # Vue.js source code 
    ├── public/ # Static assets 
    ├── Dockerfile # Frontend containerization 
    └── package.json # Node.js dependencies
```

## 🚀 Getting Started

### Prerequisites

- Docker and Docker Compose V2

### Quick Start with Docker

1. Clone the repository:
```bash
git clone <repository-url>
cd healthview-ecg-prediction
```

2. Create a .env file and defined the api url

For example :
```
#.env
VITE_API_URL=http://localhost:8000
```

3. Start the entire application:
```bash
docker-compose up --build
```

3. Access the application:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/docs

## 🧠 Backend Architecture & AI Models

### AI Model Training

The AI model training is handled by [`back-python/ia.py`](back-python/ia.py), which implements comprehensive machine learning pipelines for ECG analysis.

The system supports multiple machine learning architectures:

**CNN (Convolutional Neural Networks)**: Best performance for ECG signal classification  
**RNN/LSTM**: Effective for sequential data and temporal dependencies  
**SVM (Support Vector Machines)**: Good for binary classification problems  
**Random Forest & Gradient Boosting**: Robust ensemble methods  
**KNN**: Simple baseline model

### ECG Analysis Engine [`analyse.py`](back-python/analyse.py)

**Core Functions:**
- `load_model(model_choice)`: Loads pre-trained models (Keras .h5 or joblib .pkl)
- `analyze_ecg(file_path, model_choice)`: Main analysis function
- `get_ecg_plot_base64(file_path)`: Generates medical-grade ECG visualizations
- `save_dataset(file, upload_folder)`: Handles file uploads

### Data Processing ([`reader.py`](back-python/reader.py), [`management.py`](back-python/management.py))

**Supported Data Formats:**
- CSV files: Standard comma-separated format
- WFDB files: Medical standard for ECG data
- Fragment types: 'frag', 'full', '10_3', '15_2'

### API Routes

**Main analysis Endpoint**
```
POST /analyze
Content-Type: multipart/form-data

Parameters:
- file: UploadFile (optional) - ECG data file
- color_choice: str (default: "green") - Predefined ECG selection
- model_choice: str (default: "cnn") - AI model to use

Response:
{
    "predicted_class": "N",
    "class_probabilities": [0.95, 0.02, ...],
    "danger_level": 15,
    "top_3_classes": ["N", "SBR", "BBB"],
    "top_3_probabilities": [0.95, 0.03, 0.02],
    "main_category_probabilities": {...},
    "ecg_plot_base64": "iVBORw0KGgoAAAANSUhEUgAA..."
}
```

**ECG Plot Generation Endpoint**
```
GET /get-random-plot

No Parameters, color_choice is picked randomly between "green", "yellow" and "red"

Response:
{
    "plot_url": "iVBORw0KGgoAAAANSUhEUgAA...",
    "color_choice": "green"
}
```

## 📊 Dataset Information

### Training Data Structure
The system uses the MIT-BIH Arrhythmia Database format and custom ECG datasets:

```
ECG_Point_1, ECG_Point_2, ..., ECG_Point_187, Label
```

**Example**:
```
0.1, 0.2, ..., 0.5, 0
```

*For more detailed documentation, please refer to the [`AI ECG Analysis Notebook`](back-python/ai-ecg-en.ipynb)*

### Risk Level Classification

Color-Coded Risk System [`categorize_dataset`](back-python/categorize_dataset/):
- Green: Normal/healthy ECG patterns (danger level 0-29)
- Yellow: Mild abnormalities (danger level 30-59)  
- Red: Critical arrhythmias requiring immediate attention (danger level 60-100)

---
**Built with:** Python, TensorFlow, FastAPI, Vue.js, Docker