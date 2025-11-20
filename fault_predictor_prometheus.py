import pandas as pd
import joblib
import time
import os
import requests

PROMETHEUS_URL = 'http://localhost:9090'
MODEL_FILE = 'fault_model.pkl'
PREDICTIONS_FILE = 'predictions.csv'

def query_prometheus():
    """Queries Prometheus for all relevant 5G metrics."""
    metric_queries = {
        'signal_strength': 'g5_signal_strength_dbm',
        'latency': 'g5_latency_ms',
        'packet_loss': 'g5_packet_loss_percent',
        'throughput': 'g5_throughput_mbps'
    }
    
    tower_data = {}
    for metric_name, query in metric_queries.items():
        response = requests.get(f'{PROMETHEUS_URL}/api/v1/query', params={'query': query})
        results = response.json()['data']['result']
        for result in results:
            tower_id = result['metric']['tower_id']
            if tower_id not in tower_data:
                tower_data[tower_id] = {}
            tower_data[tower_id][metric_name] = float(result['value'][1])
            
    # Convert the dictionary to a structured DataFrame
    return pd.DataFrame.from_dict(tower_data, orient='index').reset_index().rename(columns={'index': 'tower_id'})

if __name__ == "__main__":
    # Load the pre-trained model
    model = joblib.load(MODEL_FILE)
    
    # Ensure predictions file has a header
    if not os.path.exists(PREDICTIONS_FILE):
        with open(PREDICTIONS_FILE, 'w') as f:
            f.write("tower_id,timestamp,predicted_fault_probability,predicted_label\n")
            
    print("🤖 AI Predictor waiting for Prometheus data...")
    
    while True:
        try:
            live_data = query_prometheus()
            if not live_data.empty:
                features = ['signal_strength', 'latency', 'packet_loss', 'throughput']
                X_live = live_data[features]
                
                fault_probs = model.predict_proba(X_live)[:, 1]
                labels = model.predict(X_live)
                
                timestamp = pd.Timestamp.now().isoformat()
                with open(PREDICTIONS_FILE, 'a', newline='') as f:
                    for i, tower in enumerate(live_data['tower_id']):
                        f.write(f"{tower},{timestamp},{fault_probs[i]},{labels[i]}\n")
                        
                print(f"[{pd.Timestamp.now().strftime('%H:%M:%S')}] Predicted on live data for {len(live_data)} towers.")
        
        except requests.exceptions.ConnectionError:
            print("Predictor error: Cannot connect to Prometheus. Is it running?")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            
        time.sleep(15)
