# OptiCrop – Smart Agricultural Production Optimization System

OptiCrop is an intelligent, machine-learning-based web application designed to optimize crop yields. By analyzing soil macronutrients and climatic parameters, OptiCrop provides farmers and agronomists with precise crop recommendations, appropriate growing seasons, and tailored fertilization and soil management guidelines.

---

## 📌 Features
- **Smart Crop Recommendation:** Uses a high-performance **Random Forest Classifier** trained on precision agriculture datasets to suggest the best crop.
- **Dynamic Confidence Meter:** Displays the percentage confidence score of the predicted crop recommendation.
- **Agronomic Advisor:** Provides personalized crop suggestions regarding watering requirements, soil texture, and season parameters.
- **Interactive Fertilizer Advisor:** Offers dynamic advice on soil Nitrogen (N), Phosphorus (P), and Potassium (K) levels.
- **Client-Side Form Validation:** Real-time boundary check with human-friendly range error alerts.
- **Modern Responsive UI:** Features a sleek forest-green color palette with card layouts, fade-in animations, and transitions.

---

## 🛠️ Technology Stack
- **Frontend:** HTML5, CSS3, Bootstrap 5, JavaScript (ES6)
- **Backend:** Python 3, Flask, Jinja2 Templates
- **Machine Learning:** Scikit-Learn, Pandas, NumPy, Pickle

---

## 📁 Folder Structure
```text
OptiCrop/
│
├── app.py                # Main Flask Application & Server Routes
├── train_model.py        # ML Dataset Downloader & Model Trainer
├── model.pkl             # Trained Random Forest Model File (Generated)
├── requirements.txt      # Project Dependencies
├── README.md             # Project Documentation
│
├── dataset/
│   └── Crop_recommendation.csv # Precision Agriculture CSV Dataset
│
├── static/
│   ├── style.css         # Custom CSS (Forest Theme, Animations)
│   ├── script.js         # Frontend Logic & Form Range Validation
│   └── images/           # Application Assets
│
├── templates/
│   ├── base.html         # Navbar, Footer & Layout Template
│   ├── index.html        # Product Welcome & Feature Showcase
│   ├── about.html        # Scientific Methodology & Scope Details
│   ├── predict.html      # Input Form for Nutrient & Climate Metrics
│   ├── result.html       # Crop Prediction & Soil Advisor Display
│   └── error.html        # Fallback Error / Validation Page
│
└── screenshots/          # Application Screenshots (Optional)
```

---

## ⚙️ Installation & Setup

Follow these steps to set up and run OptiCrop locally:

### 1. Clone or Extract the Project
Ensure all files are placed within your working directory:
```powershell
cd C:\Users\indra\.gemini\antigravity\scratch\OptiCrop
```

### 2. Install Project Dependencies
Run pip to install the required Python libraries:
```powershell
pip install -r requirements.txt
```

### 3. Download Dataset and Train the Machine Learning Model
Run the model training pipeline. This script will download the official crop recommendation dataset (or generate a fallback synthetic dataset if offline) and train the Random Forest Classifier:
```powershell
python train_model.py
```
*Note: This will output `model.pkl` in the root folder and display the accuracy metrics (should be >95%).*

### 4. Run the Flask Web Application
Launch the local web server:
```powershell
python app.py
```
*Output will indicate that the server is running on `http://127.0.0.1:5000/`.*

---

## 📊 Dataset Format
The training dataset contains the following attributes:
1. **N:** Ratio of Nitrogen content in soil (0 - 150 mg/kg)
2. **P:** Ratio of Phosphorus content in soil (5 - 150 mg/kg)
3. **K:** Ratio of Potassium content in soil (5 - 220 mg/kg)
4. **temperature:** Ambient temperature in °C (0 - 50)
5. **humidity:** Relative humidity in % (10 - 100)
6. **ph:** Soil pH level (3.5 - 10.0)
7. **rainfall:** Annual rainfall depth in mm (20 - 300)
8. **label:** Target variable (one of the 22 supported crop classes)

---

## 🧪 Testing Instructions

Test the model predictions using these sample soil profile entries in the predictor form:

| Test Case | Nitrogen (N) | Phosphorus (P) | Potassium (K) | Temp (°C) | Humidity (%) | pH | Rainfall (mm) | Expected Crop |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| **Case 1** | 90 | 42 | 43 | 20.8 | 82.0 | 6.5 | 202.9 | **Rice** |
| **Case 2** | 20 | 60 | 80 | 18.2 | 16.5 | 7.2 | 80.0 | **Chickpeas** |
| **Case 3** | 80 | 18 | 30 | 25.0 | 62.0 | 6.8 | 120.0 | **Coffee** |

### Client-Side Error Validation Testing:
- Try leaving fields empty and clicking **Predict Crop**. The form will block submission and highlight the missing fields.
- Try entering letters or text. The form will show a type mismatch warning.
- Try entering a pH of `2.0` or a Temperature of `65`. The script will display a red out-of-bounds validation message.

---

## 🔮 Future Enhancements
- **IoT Sensor Suite:** Connect soil moisture (FC-28) and NPK sensors directly to the cloud for real-time recommendations.
- **GPS Weather Integration:** Automatically fetch current temperature, humidity, and forecast rainfall based on regional location.
- **Bilingual Interface:** Translate the application into local vernacular languages to improve accessibility for smallholders.
- **Yield Mapping & Crop Rotation:** Recommend crop rotation schemes that maintain soil nutrients over multiple seasons.
