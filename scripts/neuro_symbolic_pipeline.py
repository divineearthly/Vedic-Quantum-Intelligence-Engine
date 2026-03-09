import sys
import os
import json
import pandas as pd
import torch

# Define absolute base directory
BASE_DIR = '/content/vedic_quantum_intelligence_engine'

# Add paths to sys.path for local module imports
sys.path.append(os.path.join(BASE_DIR, 'lightweight_ai/models'))
sys.path.append(os.path.join(BASE_DIR, 'vedic_algorithms/src'))

try:
    # Import AI inference function
    from inference import predict
    # Import compiled C++ engine
    import vedic_engine
    print("Successfully imported AI inference and Vedic Engine modules.")
except ImportError as e:
    print(f"Import Error: {e}")

# Define artifact paths
MODEL_PATH = os.path.join(BASE_DIR, 'lightweight_ai/models/earth_signal_model.pth')
SCALER_PATH = os.path.join(BASE_DIR, 'lightweight_ai/models/scaler.pkl')
ENCODER_PATH = os.path.join(BASE_DIR, 'lightweight_ai/models/label_encoder.pkl')
RULES_PATH = os.path.join(BASE_DIR, 'sanskrit_logic_engine/rules/rules.json')

def run_pipeline(input_data_df):
    """
    VQIE Neuro-Symbolic Pipeline:
    1. Neural Layer: AI Prediction (9 features used for model)
    2. Symbolic Layer: Vedic Verification (Includes Bhuvan regional telemetry)
    """
    # 1. AI Prediction
    prediction = predict(MODEL_PATH, SCALER_PATH, ENCODER_PATH, input_data_df)
    predicted_state = prediction[0]

    # 2. Extract Planetary and Regional Telemetry for Symbolic Layer
    precip = float(input_data_df['precipitation'].iloc[0])
    ndvi = float(input_data_df['NDVI'].iloc[0])
    bhuvan_sm = float(input_data_df['bhuvan_soil_moisture'].iloc[0])

    # 3. Prepare JSON for C++ Engine (Including Planetary and Regional Features)
    input_json = json.dumps({
        "state": predicted_state,
        "precipitation": precip,
        "NDVI": ndvi,
        "bhuvan_soil_moisture": bhuvan_sm
    })

    # 4. Vedic Logic Verification
    vedic_engine.load_rules(RULES_PATH)
    result = vedic_engine.process_sutra("VerificationSutra", input_json)

    return predicted_state, json.loads(result)

if __name__ == '__main__':
    # Updated Example Test Data with 11 core features + 2 regional features (Total 13 columns matching dataset)
    test_df = pd.DataFrame({
        'temperature': [28.5],
        'humidity': [62.0],
        'air_quality': [90],
        'soil_moisture': [0.55],
        'light_intensity': [400],
        'water_level': [12.0],
        'vibration_intensity': [0.3],
        'precipitation': [0.05],
        'NDVI': [0.25],
        'bhuvan_soil_moisture': [0.42],
        'regional_land_use': ['Urban']
    })

    state, verification = run_pipeline(test_df)
    print(f"AI Predicted State: {state}")
    print(f"Vedic Verification: {verification['message']}")
