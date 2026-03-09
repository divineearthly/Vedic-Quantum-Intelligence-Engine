# VQIE Usage Guide

## 1. Local IoT Monitoring
To monitor local sensor data via the MQTT simulation or live broker, use the `realtime_monitor.py` script. This script ingests sensor packets and performs real-time neuro-symbolic audits.

**Command:**
```bash
python scripts/realtime_monitor.py
```

## 2. Planetary-Scale Telemetry Auditing
For global environmental monitoring using NASA POWER and Google Earth Engine data, use the `planetary_monitor.py` script. This script fetches live satellite telemetry and audits it against the Global Protection Sutras.

**Command:**
```bash
python scripts/planetary_monitor.py
```
