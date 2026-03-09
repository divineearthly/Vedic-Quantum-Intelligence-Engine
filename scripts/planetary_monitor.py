import sys
import os
import pandas as pd
import time
import json

# Configure paths for VQIE modules
BASE_DIR = '/content/vedic_quantum_intelligence_engine'
sys.path.append(os.path.join(BASE_DIR, 'scripts'))
sys.path.append(os.path.join(BASE_DIR, 'lightweight_ai/utils'))

try:
    from api_gateways import EarthEnginePipeline, NASAPowerConnector
    from neuro_symbolic_pipeline import run_pipeline
    print("Successfully initialized Planetary Monitor dependencies.\n")
except ImportError as e:
    print(f"Initialization Error: {e}")
    sys.exit(1)

def start_planetary_monitor(project_id, lat, lon, iterations=3, interval=5):
    """Continuously fetches planetary telemetry and audits via VQIE pipeline."""
    print(f"--- VQIE Global Planetary Monitor Started ---")
    print(f"Location: ({lat}, {lon}) | Project: {project_id}\n")

    # Initialize API Connectors
    ee_pipe = EarthEnginePipeline(project_id)
    nasa_conn = NASAPowerConnector()

    if not ee_pipe.initialize_earth_engine():
        print("[ERROR] Failed to initialize Earth Engine. Exiting.")
        return

    for i in range(iterations):
        print(f"[Iteration {i+1}] Fetching real-time planetary telemetry...")
        
        # 1. Fetch NASA POWER Telemetry
        raw_nasa = nasa_conn.fetch_telemetry(lat, lon)
        nasa_data = nasa_conn.process_telemetry(raw_nasa)

        # 2. Fetch Earth Engine NDVI (Simulated for this iteration context)
        # In a full live environment, ee_pipe.verify_pipeline() or a similar get_ndvi method would be used
        current_ndvi = 0.25 # Simulated drought/stress seed for verification

        if nasa_data:
            # 3. Construct 9-feature DataFrame for Pipeline
            # Combining Live NASA/EE data with internal sensor defaults
            input_df = pd.DataFrame([{
                'temperature': nasa_data['temperature'],
                'humidity': 30.0,            # Default/Sensor placeholder
                'air_quality': 110,          # Default/Sensor placeholder
                'soil_moisture': 0.15,       # Default/Sensor placeholder
                'light_intensity': 800,      # Default/Sensor placeholder
                'water_level': 5.0,          # Default/Sensor placeholder
                'vibration_intensity': 0.1,  # Default/Sensor placeholder
                'precipitation': nasa_data['precipitation'],
                'NDVI': current_ndvi
            }])

            # 4. Pass to Neuro-Symbolic Pipeline
            try:
                state, verification = run_pipeline(input_df)
                print(f" >> AI Predicted State: {state}")
                print(f" >> Vedic Symbolic Audit: {verification['message']}")
            except Exception as e:
                print(f"[ERROR] Pipeline execution failed: {e}")
        
        print("-" * 50)
        if i < iterations - 1:
            time.sleep(interval)

if __name__ == '__main__':
    # Test execution for New Delhi
    TEST_PROJECT = "vqie-planetary-monitoring"
    start_planetary_monitor(project_id=TEST_PROJECT, lat=28.6139, lon=77.2090, iterations=2, interval=2)
