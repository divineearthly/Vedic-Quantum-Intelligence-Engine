import sys
import os
import pandas as pd

# Configure paths to import the pipeline
BASE_DIR = '/content/vedic_quantum_intelligence_engine'
scripts_path = os.path.join(BASE_DIR, 'scripts')
if scripts_path not in sys.path:
    sys.path.append(scripts_path)

try:
    from neuro_symbolic_pipeline import run_pipeline
    print("Successfully imported run_pipeline from neuro_symbolic_pipeline.\n")
except ImportError as e:
    print(f"Import Error: {e}")
    sys.exit(1)

def get_scenarios():
    """Defines a set of sensor scenarios for testing including regional Bhuvan telemetry."""
    return [
        {
            "name": "Normal Operations",
            "data": pd.DataFrame({
                'temperature': [24.5], 'humidity': [55.0], 'air_quality': [40],
                'soil_moisture': [0.4], 'light_intensity': [500], 'water_level': [10.0],
                'vibration_intensity': [0.1], 'precipitation': [5.0], 'NDVI': [0.45],
                'bhuvan_soil_moisture': [0.42], 'regional_land_use': ['Urban']
            })
        },
        {
            "name": "Global Drought Scenario",
            "data": pd.DataFrame({
                'temperature': [35.0], 'humidity': [20.0], 'air_quality': [100],
                'soil_moisture': [0.15], 'light_intensity': [900], 'water_level': [2.0],
                'vibration_intensity': [0.05], 'precipitation': [0.05], 'NDVI': [0.25],
                'bhuvan_soil_moisture': [0.12], 'regional_land_use': ['Rural']
            })
        },
        {
            "name": "Critical Flood Risk (Regional Stress)",
            "data": pd.DataFrame({
                'temperature': [18.0], 'humidity': [95.0], 'air_quality': [30],
                'soil_moisture': [0.95], 'light_intensity': [50], 'water_level': [25.0],
                'vibration_intensity': [0.8], 'precipitation': [120.0], 'NDVI': [0.85],
                'bhuvan_soil_moisture': [0.85], 'regional_land_use': ['Wetland']
            })
        }
    ]

if __name__ == '__main__':
    scenarios = get_scenarios()
    print(f"Starting VQIE Regional Stress Testing ({len(scenarios)} cases)...\n")
    print("-" * 50)

    for scenario in scenarios:
        name = scenario['name']
        df = scenario['data']

        try:
            state, verification = run_pipeline(df)
            print(f"Scenario: {name}")
            print(f"AI Predicted State: {state}")
            print(f"Vedic Verification: {verification['message']}")
        except Exception as e:
            print(f"Error processing scenario '{name}': {e}")

        print("-" * 50)
