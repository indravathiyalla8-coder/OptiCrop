import os
import pickle
import numpy as np
import pandas as pd
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)
MODEL_PATH = "model.pkl"

# Crop dynamic advisory dictionary
CROP_ADVISORY = {
    'rice': {
        'season': 'Kharif (June - October)',
        'suggestions': 'Requires clayey/loamy soil that holds water. Keep water level at 5-10 cm during the vegetative stage. Maintain good drainage toward maturity.',
        'fertilizer': 'Requires high Nitrogen (N) input. If your N input is low, consider adding Urea or Ammonium Sulfate. Ensure balanced P and K.'
    },
    'maize': {
        'season': 'Kharif / Spring',
        'suggestions': 'Thrives in well-drained loamy soil. Requires moderate irrigation; avoid waterlogging at all stages, especially flowering.',
        'fertilizer': 'Requires moderate Nitrogen and Phosphorus. Consider adding NPK 15-15-15 or DAP (Diammonium Phosphate) during early growth stages.'
    },
    'chickpeas': {
        'season': 'Rabi (November - April)',
        'suggestions': 'Thrives in cool, dry winter weather. Extremely sensitive to waterlogging; requires light, well-distributed watering.',
        'fertilizer': 'Being a legume, it fixes its own Nitrogen. Focus on Phosphorus (P) and Potassium (K) application (e.g., Single Super Phosphate).'
    },
    'kidneybeans': {
        'season': 'Rabi / Spring',
        'suggestions': 'Requires loose, well-aerated sandy loam soil. Keep soil uniformly moist but not soggy to prevent root rot.',
        'fertilizer': 'Low Nitrogen requirement. Apply a starter dose of Nitrogen along with rich Phosphorus and Potassium fertilizers.'
    },
    'pigeonpeas': {
        'season': 'Kharif (June - March)',
        'suggestions': 'Deep-rooted and highly drought-tolerant. Best suited for well-drained sandy loam or black soils. Avoid waterlogged fields.',
        'fertilizer': 'Requires primary application of Phosphorus. Rhizobium seed treatment is highly recommended to enhance self nitrogen-fixation.'
    },
    'mothbeans': {
        'season': 'Kharif (Rainfed)',
        'suggestions': 'Extremely drought-resistant crop suitable for arid and semi-arid regions. Grows well in poor sandy soils with minimum care.',
        'fertilizer': 'Minimal fertilizer required. Light application of Phosphorus before sowing can significantly improve root development.'
    },
    'mungbean': {
        'season': 'Summer / Kharif',
        'suggestions': 'Short-duration crop (60-70 days). Requires light loam soil. Water at critical stages: flowering and pod-filling.',
        'fertilizer': 'Apply small dose of starter Nitrogen and a primary dose of Phosphorus (DAP) during field preparation.'
    },
    'blackgram': {
        'season': 'Kharif / Summer',
        'suggestions': 'Prefers heavy clay loam soils. Needs moderate irrigation. Good soil structure helps in better root aeration and nodulation.',
        'fertilizer': 'Requires Phosphorus (DAP) and Potassium. Nitrogen-fixing, so no heavy nitrogenous top-dressing is necessary.'
    },
    'lentil': {
        'season': 'Rabi (November - March)',
        'suggestions': 'Requires cold climate and well-drained light loam soils. Highly sensitive to waterlogging; provide light irrigation.',
        'fertilizer': 'Phosphorus and Potassium are crucial for yield. Apply single superphosphate (SSP) and muriate of potash (MOP).'
    },
    'pomegranate': {
        'season': 'All Year (Pruning dependent)',
        'suggestions': 'Requires deep, well-drained loamy soil. Tolerates salinity well. Regular drip irrigation is key to avoiding fruit cracking.',
        'fertilizer': 'Heavy feeder of Nitrogen and Potassium (K). Apply farmyard manure along with MOP and Urea in split doses.'
    },
    'banana': {
        'season': 'Tropical (Plant throughout year)',
        'suggestions': 'Heavy water consumer. Requires rich, well-drained soil, high humidity, and protection from strong winds.',
        'fertilizer': 'Extremely high requirement of Potassium (K) and Nitrogen (N). Feed regularly with Muriate of Potash and Urea.'
    },
    'mango': {
        'season': 'Summer (Perennial)',
        'suggestions': 'Needs deep, well-drained alluvial or loamy soil. Requires dry period during flowering, followed by watering during fruit growth.',
        'fertilizer': 'Apply balanced NPK fertilizer and organic compost annually after harvest. Increase Potassium during fruit development.'
    },
    'grapes': {
        'season': 'Spring / Summer',
        'suggestions': 'Requires well-drained soil with a trellis system for vine support. Control watering during ripening to increase sugar content.',
        'fertilizer': 'Requires high Potassium (K) for fruit size and quality. Ensure sufficient levels of Boron and Magnesium in the soil.'
    },
    'watermelon': {
        'season': 'Summer (March - June)',
        'suggestions': 'Requires sandy loam soils that drain quickly, high temperatures, and full sunlight. Limit watering as fruits ripen.',
        'fertilizer': 'High Nitrogen early for vine growth, switching to high Potassium and Phosphorus during flowering and fruiting.'
    },
    'muskmelon': {
        'season': 'Summer (March - June)',
        'suggestions': 'Prefers hot, dry weather and well-drained sandy loam soil. Drip irrigation is highly recommended to prevent leaf diseases.',
        'fertilizer': 'Ensure balanced NPK levels. Apply calcium-rich fertilizers to prevent blossom end rot in melons.'
    },
    'apple': {
        'season': 'Rabi (Temperate zones)',
        'suggestions': 'Grows in deep, fertile loamy soil. Requires sufficient winter chilling hours. Pruning is essential for air circulation.',
        'fertilizer': 'Apply balanced NPK in spring. Ensure adequate Calcium and Boron supply to maintain fruit crispness and storage life.'
    },
    'orange': {
        'season': 'Rabi / Spring (Sub-tropical)',
        'suggestions': 'Requires well-drained sandy loam or clay loam soil. Maintain regular watering. Protect from frost during winters.',
        'fertilizer': 'Requires nitrogenous fertilizers in split doses. Supplement with Zinc, Iron, and Manganese foliar sprays.'
    },
    'papaya': {
        'season': 'Tropical (All Year)',
        'suggestions': 'Fast-growing crop. Requires rich sandy loam soil with excellent drainage. Highly vulnerable to waterlogging and wind damage.',
        'fertilizer': 'Heavy feeder. Feed with Urea, Superphosphate, and Potash every two months for continuous fruit production.'
    },
    'coconut': {
        'season': 'Tropical (All Year)',
        'suggestions': 'Thrives in sandy soils along coastal areas. Requires high humidity and regular moisture. Provide basin-type watering.',
        'fertilizer': 'Requires substantial Potassium (K) and Sodium (NaCl). Apply Muriate of Potash and common salt for optimum yields.'
    },
    'cotton': {
        'season': 'Kharif (May - October)',
        'suggestions': 'Thrives in deep black clayey soil (Regur) which retains moisture. Requires moderate rainfall and a long frost-free period.',
        'fertilizer': 'Apply Nitrogen in split doses. Ensure adequate Phosphorus during early root growth and Potassium during boll-forming.'
    },
    'jute': {
        'season': 'Kharif (March - September)',
        'suggestions': 'Requires clean, warm, humid conditions. Prefers fertile alluvial soils. Harvest at the early flowering stage for fiber quality.',
        'fertilizer': 'Primarily requires Nitrogen (N) for rapid stem and fiber growth. Apply Urea in split doses after weeding.'
    },
    'coffee': {
        'season': 'Tropical / High Altitude',
        'suggestions': 'Grows under shade tree canopies in cool upland climates. Prefers deep, rich, organic, acidic loamy soils with good drainage.',
        'fertilizer': 'High Potassium (MOP) and Nitrogen requirement. Supplement with Magnesium and Zinc to prevent nutritional leaf yellowing.'
    }
}

def load_model():
    if os.path.exists(MODEL_PATH):
        try:
            with open(MODEL_PATH, 'rb') as f:
                model = pickle.load(f)
            return model
        except Exception as e:
            print(f"Error loading model: {e}")
            return None
    return None

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/predict')
def predict():
    return render_template('predict.html')

@app.route('/result', methods=['POST'])
def predict_result():
    try:
        # Extract inputs from POST request
        n_val = request.form.get('N')
        p_val = request.form.get('P')
        k_val = request.form.get('K')
        temp_val = request.form.get('temperature')
        hum_val = request.form.get('humidity')
        ph_val = request.form.get('ph')
        rain_val = request.form.get('rainfall')

        # 1. Empty Field Validation
        if not all([n_val, p_val, k_val, temp_val, hum_val, ph_val, rain_val]):
            return render_template('predict.html', error="All input fields are mandatory. Please fill in all parameters.")

        # 2. Numeric Validation
        try:
            N = float(n_val)
            P = float(p_val)
            K = float(k_val)
            temperature = float(temp_val)
            humidity = float(hum_val)
            ph = float(ph_val)
            rainfall = float(rain_val)
        except ValueError:
            return render_template('predict.html', error="All fields must contain valid numeric entries.")

        # 3. Range Validation
        validation_rules = [
            (N, 0, 150, "Nitrogen (N) must be between 0 and 150 mg/kg."),
            (P, 5, 150, "Phosphorus (P) must be between 5 and 150 mg/kg."),
            (K, 5, 220, "Potassium (K) must be between 5 and 220 mg/kg."),
            (temperature, 0, 50, "Temperature must be between 0°C and 50°C."),
            (humidity, 10, 100, "Relative Humidity must be between 10% and 100%."),
            (ph, 3.5, 10.0, "Soil pH must be between 3.5 and 10.0."),
            (rainfall, 20, 300, "Annual Rainfall must be between 20 mm and 300 mm.")
        ]

        for val, min_val, max_val, msg in validation_rules:
            if val < min_val or val > max_val:
                return render_template('predict.html', error=msg)

        # Load Trained model.pkl
        model = load_model()
        if model is None:
            return render_template('error.html', error_message="Machine Learning model file 'model.pkl' could not be loaded. Please ensure the training script was run successfully.")

        # Perform ML inference prediction
        input_data = pd.DataFrame([[N, P, K, temperature, humidity, ph, rainfall]], 
                                  columns=['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall'])
        
        predicted_crop = model.predict(input_data)[0]
        
        # Calculate Confidence Score
        probabilities = model.predict_proba(input_data)[0]
        max_prob_idx = np.argmax(probabilities)
        confidence_score = int(round(probabilities[max_prob_idx] * 100))

        # Retrieve dynamic agricultural suggestions based on crop
        advisory = CROP_ADVISORY.get(predicted_crop, {
            'season': 'General growing season',
            'suggestions': 'Follow standard regional agricultural extension rules for soil hydration and spacing.',
            'fertilizer': 'Apply balanced NPK chemical or organic manures depending on pre-sowing soil reports.'
        })

        return render_template('result.html', 
                               crop=predicted_crop,
                               confidence=confidence_score,
                               season=advisory['season'],
                               suggestions=advisory['suggestions'],
                               fertilizer_suggestion=advisory['fertilizer'],
                               N=N, P=P, K=K, 
                               temperature=temperature, 
                               humidity=humidity, 
                               ph=ph, 
                               rainfall=rainfall)

    except Exception as e:
        return render_template('error.html', error_message=str(e))

@app.errorhandler(404)
def page_not_found(e):
    return render_template('error.html', error_message="Page Not Found (404). The requested URL does not exist on this server."), 404

@app.errorhandler(500)
def server_error(e):
    return render_template('error.html', error_message="Internal Server Error (500). An unexpected error occurred on our end."), 500

if __name__ == '__main__':
    app.run(debug=True)
