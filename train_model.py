import os
import pickle
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report

# Configuration
DATASET_DIR = "dataset"
DATASET_PATH = os.path.join(DATASET_DIR, "Crop_recommendation.csv")
MODEL_PATH = "model.pkl"

# Define ranges for synthetic data fallback
CROP_PROFILES = {
    'rice': {'N': (80, 100), 'P': (35, 50), 'K': (35, 45), 'temp': (20, 27), 'humidity': (80, 90), 'ph': (5.5, 6.5), 'rainfall': (200, 250)},
    'maize': {'N': (60, 80), 'P': (35, 50), 'K': (15, 25), 'temp': (18, 27), 'humidity': (55, 70), 'ph': (5.7, 7.0), 'rainfall': (60, 110)},
    'chickpeas': {'N': (20, 40), 'P': (55, 70), 'K': (75, 85), 'temp': (17, 21), 'humidity': (15, 20), 'ph': (5.5, 8.5), 'rainfall': (65, 95)},
    'kidneybeans': {'N': (20, 40), 'P': (55, 70), 'K': (15, 25), 'temp': (15, 25), 'humidity': (18, 25), 'ph': (5.5, 6.0), 'rainfall': (60, 150)},
    'pigeonpeas': {'N': (20, 40), 'P': (55, 75), 'K': (15, 25), 'temp': (18, 35), 'humidity': (30, 70), 'ph': (4.5, 8.5), 'rainfall': (90, 200)},
    'mothbeans': {'N': (0, 20), 'P': (35, 60), 'K': (15, 25), 'temp': (25, 30), 'humidity': (40, 65), 'ph': (3.5, 10.0), 'rainfall': (30, 75)},
    'mungbean': {'N': (0, 20), 'P': (35, 60), 'K': (15, 25), 'temp': (27, 30), 'humidity': (80, 90), 'ph': (6.2, 7.2), 'rainfall': (35, 60)},
    'blackgram': {'N': (20, 40), 'P': (55, 70), 'K': (15, 25), 'temp': (25, 35), 'humidity': (60, 70), 'ph': (6.5, 7.5), 'rainfall': (60, 75)},
    'lentil': {'N': (0, 20), 'P': (55, 70), 'K': (15, 25), 'temp': (18, 30), 'humidity': (60, 70), 'ph': (5.9, 6.9), 'rainfall': (35, 50)},
    'pomegranate': {'N': (0, 20), 'P': (5, 30), 'K': (35, 45), 'temp': (18, 25), 'humidity': (85, 92), 'ph': (5.5, 7.3), 'rainfall': (100, 115)},
    'banana': {'N': (80, 100), 'P': (70, 95), 'K': (45, 55), 'temp': (25, 30), 'humidity': (75, 85), 'ph': (5.5, 6.5), 'rainfall': (90, 115)},
    'mango': {'N': (0, 20), 'P': (20, 40), 'K': (25, 35), 'temp': (27, 36), 'humidity': (45, 55), 'ph': (4.5, 7.0), 'rainfall': (90, 105)},
    'grapes': {'N': (20, 40), 'P': (120, 145), 'K': (195, 205), 'temp': (10, 40), 'humidity': (80, 85), 'ph': (5.5, 6.0), 'rainfall': (65, 75)},
    'watermelon': {'N': (80, 100), 'P': (5, 30), 'K': (45, 55), 'temp': (24, 27), 'humidity': (80, 90), 'ph': (6.0, 7.0), 'rainfall': (40, 60)},
    'muskmelon': {'N': (80, 100), 'P': (5, 30), 'K': (45, 55), 'temp': (27, 30), 'humidity': (90, 95), 'ph': (6.0, 6.8), 'rainfall': (20, 30)},
    'apple': {'N': (0, 20), 'P': (120, 145), 'K': (195, 205), 'temp': (21, 24), 'humidity': (90, 95), 'ph': (5.5, 6.5), 'rainfall': (100, 125)},
    'orange': {'N': (0, 20), 'P': (5, 30), 'K': (5, 15), 'temp': (10, 35), 'humidity': (90, 95), 'ph': (6.0, 8.0), 'rainfall': (100, 120)},
    'papaya': {'N': (30, 60), 'P': (45, 70), 'K': (45, 55), 'temp': (23, 44), 'humidity': (90, 95), 'ph': (6.5, 7.0), 'rainfall': (240, 250)},
    'coconut': {'N': (0, 20), 'P': (5, 30), 'K': (25, 35), 'temp': (25, 30), 'humidity': (90, 99), 'ph': (5.5, 6.5), 'rainfall': (130, 230)},
    'cotton': {'N': (100, 120), 'P': (35, 50), 'K': (15, 25), 'temp': (22, 26), 'humidity': (75, 85), 'ph': (5.8, 8.0), 'rainfall': (60, 100)},
    'jute': {'N': (60, 80), 'P': (35, 50), 'K': (35, 45), 'temp': (23, 27), 'humidity': (70, 90), 'ph': (6.0, 7.0), 'rainfall': (150, 200)},
    'coffee': {'N': (80, 100), 'P': (15, 30), 'K': (25, 35), 'temp': (20, 28), 'humidity': (50, 65), 'ph': (6.0, 7.5), 'rainfall': (115, 190)}
}

def generate_synthetic_data(num_samples_per_crop=100):
    print("Generating high-quality synthetic agricultural dataset...")
    data = []
    np.random.seed(42)
    for crop, profile in CROP_PROFILES.items():
        for _ in range(num_samples_per_crop):
            row = {
                'N': max(0.0, np.random.normal(loc=(profile['N'][0] + profile['N'][1]) / 2, scale=(profile['N'][1] - profile['N'][0]) / 4)),
                'P': max(0.0, np.random.normal(loc=(profile['P'][0] + profile['P'][1]) / 2, scale=(profile['P'][1] - profile['P'][0]) / 4)),
                'K': max(0.0, np.random.normal(loc=(profile['K'][0] + profile['K'][1]) / 2, scale=(profile['K'][1] - profile['K'][0]) / 4)),
                'temperature': np.random.normal(loc=(profile['temp'][0] + profile['temp'][1]) / 2, scale=(profile['temp'][1] - profile['temp'][0]) / 4),
                'humidity': np.clip(np.random.normal(loc=(profile['humidity'][0] + profile['humidity'][1]) / 2, scale=(profile['humidity'][1] - profile['humidity'][0]) / 4), 10.0, 100.0),
                'ph': np.clip(np.random.normal(loc=(profile['ph'][0] + profile['ph'][1]) / 2, scale=(profile['ph'][1] - profile['ph'][0]) / 4), 3.5, 10.0),
                'rainfall': max(0.0, np.random.normal(loc=(profile['rainfall'][0] + profile['rainfall'][1]) / 2, scale=(profile['rainfall'][1] - profile['rainfall'][0]) / 4)),
                'label': crop
            }
            data.append(row)
    df = pd.DataFrame(data)
    
    # Save dataset file
    os.makedirs(DATASET_DIR, exist_ok=True)
    df.to_csv(DATASET_PATH, index=False)
    print(f"Dataset successfully created and saved at: {DATASET_PATH}")
    return df

def load_dataset():
    if not os.path.exists(DATASET_PATH):
        try:
            print("Attempting to download Crop_recommendation.csv from raw GitHub content...")
            import requests
            url = "https://raw.githubusercontent.com/gabbygab1233/Crop-Recommender/main/Crop_recommendation.csv"
            response = requests.get(url, timeout=15)
            if response.status_code == 200:
                os.makedirs(DATASET_DIR, exist_ok=True)
                with open(DATASET_PATH, 'wb') as f:
                    f.write(response.content)
                print("Download completed successfully.")
                df = pd.read_csv(DATASET_PATH)
            else:
                print(f"Download failed with status code {response.status_code}.")
                df = generate_synthetic_data()
        except Exception as e:
            print(f"Error downloading dataset: {e}")
            df = generate_synthetic_data()
    else:
        print("Dataset found locally.")
        df = pd.read_csv(DATASET_PATH)
    return df

def train():
    df = load_dataset()
    
    # Define features and label
    X = df[['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall']]
    y = df['label']
    
    # Split dataset
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Initialize Random Forest Classifier
    print("Training Random Forest Classifier...")
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    
    # Predict and evaluate
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print("\n--- MODEL PERFORMANCE ---")
    print(f"Accuracy Score: {accuracy * 100:.2f}%")
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred))
    
    # Save model.pkl
    with open(MODEL_PATH, 'wb') as f:
        pickle.dump(model, f)
    print(f"Trained model saved successfully as: {MODEL_PATH}")

if __name__ == "__main__":
    train()
