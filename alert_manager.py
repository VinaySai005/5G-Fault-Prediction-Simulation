from flask import Flask, jsonify
import pandas as pd
import time
import os
import threading

app = Flask(__name__)
ALERTS_FILE = 'alerts.csv'
processed_alerts = set()

def monitor_and_alert():
    if not os.path.exists(ALERTS_FILE):
        with open(ALERTS_FILE, 'w') as f:
            f.write("tower_id,timestamp,fault_prob\n")
            
    print("⚡️ Starting Alert Manager...")
    while True:
        try:
            if os.path.exists('predictions.csv') and os.path.getsize('predictions.csv') > 0:
                df_preds = pd.read_csv('predictions.csv')
                potential_alerts = df_preds[df_preds['predicted_fault_probability'] > 0.8]
                with open(ALERTS_FILE, 'a', newline='') as f:
                    for _, row in potential_alerts.iterrows():
                        alert_key = (row['tower_id'], row['timestamp'])
                        if alert_key not in processed_alerts:
                            print(f"⚠️  ALERT: High fault probability ({row['predicted_fault_probability']:.2f}) for {row['tower_id']}")
                            f.write(f"{row['tower_id']},{row['timestamp']},{row['predicted_fault_probability']:.2f}\n")
                            processed_alerts.add(alert_key)
        except (pd.errors.EmptyDataError, FileNotFoundError):
            pass 
        except Exception as e:
            print(f"Alerter error: {e}")
        time.sleep(5)

@app.route('/alerts')
def get_alerts():
    df = pd.read_csv(ALERTS_FILE)
    return jsonify({"active_alerts": df.to_dict('records')})

if __name__ == "__main__":
    monitor_thread = threading.Thread(target=monitor_and_alert, daemon=True)
    monitor_thread.start()
    print("🌍 Flask API server running at http://127.0.0.1:5000/alerts")
    app.run(host='0.0.0.0', port=5000)
