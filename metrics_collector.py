import csv, random, time, datetime, os

OUTPUT_FILE = 'metrics.csv'
TOWERS = [f'T{i}' for i in range(1, 6)]
FIELDNAMES = ['tower_id', 'timestamp', 'signal_strength', 'latency', 'packet_loss', 'throughput', 'status']

def generate_metrics(tower_id, is_fault=False):
    if is_fault:
        return {'tower_id': tower_id, 'timestamp': datetime.datetime.now().isoformat(), 'status': 1,
                'signal_strength': round(random.uniform(-110, -95), 2), 'latency': round(random.uniform(100, 500), 2),
                'packet_loss': round(random.uniform(5, 20), 2), 'throughput': round(random.uniform(1, 20), 2)}
    else:
        return {'tower_id': tower_id, 'timestamp': datetime.datetime.now().isoformat(), 'status': 0,
                'signal_strength': round(random.uniform(-90, -75), 2), 'latency': round(random.uniform(10, 30), 2),
                'packet_loss': round(random.uniform(0.01, 0.5), 2), 'throughput': round(random.uniform(100, 500), 2)}

if __name__ == "__main__":
    if not os.path.exists(OUTPUT_FILE):
        with open(OUTPUT_FILE, 'w', newline='') as f:
            csv.DictWriter(f, fieldnames=FIELDNAMES).writeheader()
    print("🚀 Generating bootstrap data for model training...")
    for _ in range(12): # Generate data for 1 minute
         with open(OUTPUT_FILE, 'a', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
            for tower in TOWERS:
                writer.writerow(generate_metrics(tower, is_fault=random.random() < 0.1))
         time.sleep(5)
    print("✅ Bootstrap data generated in metrics.csv.")
