import sys
import os
import pandas as pd
import json
import time

# Configure paths for VQIE modules
BASE_DIR = '/content/vedic_quantum_intelligence_engine'
sys.path.append(os.path.join(BASE_DIR, 'scripts'))
sys.path.append(os.path.join(BASE_DIR, 'lightweight_ai/utils'))

try:
    from mqtt_adapter import VQIE_MQTT_Client
    from neuro_symbolic_pipeline import run_pipeline
    from actuation_layer import process_actuation_command
    print("Successfully initialized Real-Time Monitor with MQTT and Actuation Support.\n")
except ImportError as e:
    print(f"Initialization Error: {e}")
    sys.exit(1)

def start_monitor(adapter, iterations=10, poll_delay=1.0):
    """
    VQIE Closed-Loop Monitor:
    1. Ingests live packets from MQTT broker.
    2. Audits packets via Neuro-Symbolic Pipeline.
    3. Triggers hardware actions via Actuation Layer.
    """
    print(f"--- VQIE Live MQTT Monitoring Started ---")
    
    count = 0
    while count < iterations:
        packet = adapter.get_packet()
        
        if packet:
            count += 1
            print(f"[MQTT Event {count}] Processing packet...")
            
            try:
                # Convert packet to DataFrame (Model expects 9 features, Pipeline handles mapping)
                input_df = pd.DataFrame([packet])
                
                # Ensure label is dropped if present in the telemetry
                if 'label' in input_df.columns: 
                    input_df = input_df.drop(columns=['label'])

                # 1. Neuro-Symbolic Audit
                state, verification = run_pipeline(input_df)
                print(f" >> AI State: {state}")

                # 2. Closed-Loop Actuation
                # The Vedic engine returns 'message' and 'command' if a rule matches
                if 'command' in str(verification):
                    process_actuation_command(verification)
                else:
                    print(f" >> Vedic Audit: {verification.get('message', 'No intervention required')}")
                
                print("-" * 40)
            except Exception as e:
                print(f"[Error] Pipeline failure on packet {count}: {e}")
        
        time.sleep(poll_delay)

if __name__ == '__main__':
    # Initialize and start the MQTT Client
    adapter = VQIE_MQTT_Client()
    adapter.start()
    
    try:
        # Run for a limited number of iterations for demonstration
        start_monitor(adapter, iterations=5, poll_delay=1.0)
    except KeyboardInterrupt:
        print("\nMonitoring stopped by user.")
    finally:
        adapter.stop()
        print("VQIE Monitor Shutdown.")
