# VQIE Deployment Guide

## 1. Edge Preparation
To prepare the VQIE for edge devices (ARM-based), run the edge compilation script. This will export the neural model to a platform-independent TorchScript artifact.

**Command:**
```bash
bash scripts/edge_compile.sh
```

## 2. Native Compilation on ARM Hardware (Raspberry Pi/Jetson)
After transferring the `vedic_algorithms/src/` directory to the target device, perform native compilation to ensure compatibility with the target's Python headers:

**Command:**
```bash
g++ -O3 -Wall -std=c++17 -Iinclude $(python3 -m pybind11 --includes) -fPIC -shared kernel.cpp urdhva_tiryagbhyam.cpp vedic_logic.cpp -o vedic_engine.so
```
