# VQIE System Architecture

## 1. Three-Layer Modular Design
The Vedic Quantum Intelligence Engine (VQIE) is structured into three distinct domain-specific layers to ensure high performance, scalability, and logical integrity.

### A. Neural Layer (Neural Learning)
- **Location**: `lightweight_ai/models/`
- **Function**: Implements high-speed Multi-Layer Perceptrons (MLP) using **PyTorch**. It processes raw environmental signals to predict discrete states (e.g., Normal, Warning, Critical).

### B. Symbolic Layer (Mathematical Core)
- **Location**: `vedic_algorithms/src/`
- **Function**: Contains optimized **C++ Vedic Kernels** for deterministic mathematical operations. These kernels (e.g., Urdhva Tiryagbhyam) provide a high-performance substrate for symbolic reasoning.

### C. Logic Engine (Sanskrit Logic)
- **Location**: `sanskrit_logic_engine/rules/`
- **Function**: Manages the `rules.json` repository of Sanskrit-inspired sutras. It audits neural predictions against deterministic environmental safety thresholds and triggers mitigation actions.

## 2. Secure API Gateway System
The system implements a centralized credential management protocol via `lightweight_ai/utils/api_gateways.py`.
- **Security**: Utilizes `google.colab.userdata` to securely retrieve sensitive service account JSONs and API keys (e.g., `NASA_API_KEY`, `EE_SERVICE_ACCOUNT_JSON`).
- **Providers**: Interfaces with **NASA POWER**, **Google Earth Engine (GEE)**, and **ISRO Bhuvan** to ingest planetary-scale telemetry.

## 3. Data Flow & Serialization
1. **Ingestion**: Raw telemetry from IoT sensors and satellite APIs is normalized into a 9-feature vector.
2. **Prediction**: The Neural Layer outputs a probabilistic state label.
3. **Serialization**: Data (Predicted State + Telemetry Values) is serialized into a **JSON payload**.
4. **Audit**: The JSON is passed via **pybind11** to the C++ Vedic Logic Engine for final verification and command generation.
