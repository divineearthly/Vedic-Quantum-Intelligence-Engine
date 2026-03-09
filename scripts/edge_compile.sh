#!/bin/bash

echo "--- VQIE Edge Deployment Packaging System ---"

BASE_DIR="/content/vedic_quantum_intelligence_engine"
MODEL_PATH="$BASE_DIR/lightweight_ai/models/earth_signal_model.pth"
EXPORT_PATH="$BASE_DIR/lightweight_ai/models/earth_signal_model_ts.pt"

# 1. Neural Layer: Export PyTorch Model to TorchScript
echo "[1/2] Exporting Neural Model to TorchScript..."

python3 - <<EOF
import torch
import os
import sys
# Use absolute path for sys.path to avoid ModuleNotFoundError
sys.path.append(os.path.join('$BASE_DIR', 'lightweight_ai/models'))
from train_model import EarthSignalModel

model = EarthSignalModel(9, 5)

if os.path.exists('$MODEL_PATH'):
    try:
        model.load_state_dict(torch.load('$MODEL_PATH'))
        model.eval()
        example_input = torch.rand(1, 9)
        traced_model = torch.jit.trace(model, example_input)
        traced_model.save('$EXPORT_PATH')
        print(f"[SUCCESS] TorchScript artifact saved: $EXPORT_PATH")
    except Exception as e:
        print(f"[ERROR] Model export failed: {e}")
else:
    print(f"[ERROR] Trained weights not found at $MODEL_PATH")
EOF

# 2. Symbolic Layer: Provide Native Compilation Instructions
echo ""
echo "[2/2] Packaging C++ Kernels for Symbolic Audit..."
echo "---------------------------------------------------------"
echo "NATIVE COMPILATION INSTRUCTIONS FOR ARM TARGET:"
echo "1. Transfer 'vedic_algorithms/src/' to the target device."
echo "2. Execute the following command on the target hardware:"
echo ""
echo "   g++ -O3 -Wall -std=c++17 -Iinclude \$(python3 -m pybind11 --includes) \\"
echo "       -fPIC -shared kernel.cpp urdhva_tiryagbhyam.cpp vedic_logic.cpp \\"
echo "       -o vedic_engine.so"
echo "---------------------------------------------------------"

echo "Deployment script finalized."
