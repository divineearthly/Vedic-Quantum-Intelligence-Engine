import torch
import torch.nn as nn
import pandas as pd
import joblib
import os

class EarthSignalModel(nn.Module):
    def __init__(self, input_dim, num_classes):
        super(EarthSignalModel, self).__init__()
        self.fc1 = nn.Linear(input_dim, 128)
        self.relu = nn.ReLU()
        self.fc2 = nn.Linear(128, 64)
        self.fc3 = nn.Linear(64, 32)
        self.fc4 = nn.Linear(32, num_classes)

    def forward(self, x):
        x = self.relu(self.fc1(x))
        x = self.relu(self.fc2(x))
        x = self.relu(self.fc3(x))
        x = self.fc4(x)
        return x

def predict(model_path, scaler_path, encoder_path, new_data_df):
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Model not found: {model_path}")

    label_encoder = joblib.load(encoder_path)
    num_classes = len(label_encoder.classes_)
    # Updated to 9 features
    input_dim = 9

    model = EarthSignalModel(input_dim, num_classes)
    model.load_state_dict(torch.load(model_path))
    model.eval()

    scaler = joblib.load(scaler_path)
    # Updated features list to include planetary telemetry
    features_to_scale = ['temperature', 'humidity', 'air_quality', 'soil_moisture', 'light_intensity', 'water_level', 'vibration_intensity', 'precipitation', 'NDVI']
    new_data_scaled = scaler.transform(new_data_df[features_to_scale])
    new_data_tensor = torch.tensor(new_data_scaled, dtype=torch.float32)

    with torch.no_grad():
        outputs = model(new_data_tensor)
        _, predicted = torch.max(outputs.data, 1)

    return label_encoder.inverse_transform(predicted.numpy())

if __name__ == '__main__':
    BASE_DIR = '/content/vedic_quantum_intelligence_engine/lightweight_ai/models/'
    MODEL_PATH = os.path.join(BASE_DIR, 'earth_signal_model.pth')
    SCALER_PATH = os.path.join(BASE_DIR, 'scaler.pkl')
    ENCODER_PATH = os.path.join(BASE_DIR, 'label_encoder.pkl')

    test_data = pd.DataFrame({
        'temperature': [28.5],
        'humidity': [62.0],
        'air_quality': [90],
        'soil_moisture': [0.55],
        'light_intensity': [400],
        'water_level': [12.0],
        'vibration_intensity': [0.3],
        'precipitation': [5.0],
        'NDVI': [0.45]
    })

    print("Running inference with updated 9-feature architecture...")
    try:
        preds = predict(MODEL_PATH, SCALER_PATH, ENCODER_PATH, test_data)
        print(f"Inference Result: {preds[0]}")
    except Exception as e:
        print(f"Inference failed: {e}")
