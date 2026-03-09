import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
import pandas as pd
import os
import joblib
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder

class EarthDataset(Dataset):
    def __init__(self, features, labels):
        self.features = torch.tensor(features, dtype=torch.float32)
        self.labels = torch.tensor(labels, dtype=torch.long)
    def __len__(self):
        return len(self.labels)
    def __getitem__(self, idx):
        return self.features[idx], self.labels[idx]

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

def train_model(data_path, model_save_path):
    if not os.path.exists(data_path):
        print(f'Error: Data file not found at {data_path}')
        return
    df = pd.read_csv(data_path)
    # Updated features list to include planetary telemetry (total 9 features)
    features_list = ['temperature', 'humidity', 'air_quality', 'soil_moisture', 'light_intensity', 'water_level', 'vibration_intensity', 'precipitation', 'NDVI']
    features = df[features_list]
    labels = df['label']
    
    label_encoder = LabelEncoder()
    labels_encoded = label_encoder.fit_transform(labels)
    num_classes = len(label_encoder.classes_)

    counts = np.bincount(labels_encoded)
    total_samples = len(labels_encoded)
    weights = total_samples / (num_classes * counts)
    class_weights = torch.tensor(weights, dtype=torch.float32)

    scaler = StandardScaler()
    features_scaled = scaler.fit_transform(features)
    X_train, X_test, y_train, y_test = train_test_split(features_scaled, labels_encoded, test_size=0.2, random_state=42)
    train_dataset = EarthDataset(X_train, y_train)
    train_loader = DataLoader(train_dataset, batch_size=4, shuffle=True)

    # input_dim is now 9
    model = EarthSignalModel(X_train.shape[1], num_classes)
    criterion = nn.CrossEntropyLoss(weight=class_weights)
    optimizer = optim.Adam(model.parameters(), lr=0.001)

    print('Starting model training with 9 features and planetary telemetry...')
    for epoch in range(15):
        model.train()
        for inputs, targets in train_loader:
            optimizer.zero_grad()
            outputs = model(inputs)
            loss = criterion(outputs, targets)
            loss.backward()
            optimizer.step()
        print(f'Epoch {epoch+1}/15, Loss: {loss.item():.4f}')

    os.makedirs(os.path.dirname(model_save_path), exist_ok=True)
    torch.save(model.state_dict(), model_save_path)
    joblib.dump(label_encoder, os.path.join(os.path.dirname(model_save_path), 'label_encoder.pkl'))
    joblib.dump(scaler, os.path.join(os.path.dirname(model_save_path), 'scaler.pkl'))
    print(f'Model and artifacts saved to {os.path.dirname(model_save_path)}')

if __name__ == "__main__":
    DATA_PATH = '/content/vedic_quantum_intelligence_engine/data/raw/sample_earth_data.csv'
    MODEL_DIR = '/content/vedic_quantum_intelligence_engine/lightweight_ai/models/'
    MODEL_PATH = os.path.join(MODEL_DIR, 'earth_signal_model.pth')
    train_model(DATA_PATH, MODEL_PATH)
