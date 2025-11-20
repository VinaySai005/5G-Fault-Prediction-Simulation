import random
import time
from prometheus_client import start_http_server, Gauge

# Create Prometheus metrics with a 'tower_id' label
SIGNAL_STRENGTH = Gauge('g5_signal_strength_dbm', 'Signal Strength (dBm)', ['tower_id'])
LATENCY = Gauge('g5_latency_ms', 'Network Latency (ms)', ['tower_id'])
PACKET_LOSS = Gauge('g5_packet_loss_percent', 'Packet Loss (%)', ['tower_id'])
THROUGHPUT = Gauge('g5_throughput_mbps', 'Throughput (Mbps)', ['tower_id'])

TOWERS = [f'T{i}' for i in range(1, 6)]

if __name__ == '__main__':
    # Start an HTTP server to expose the metrics on port 8000
    start_http_server(8000)
    print("🚀 5G Metrics Exporter running on http://localhost:8000")

    # Generate and update metrics indefinitely
    while True:
        for tower in TOWERS:
            is_fault = random.random() < 0.05
            
            # Set metric values based on normal or fault state
            SIGNAL_STRENGTH.labels(tower_id=tower).set(random.uniform(-110, -95) if is_fault else random.uniform(-90, -75))
            LATENCY.labels(tower_id=tower).set(random.uniform(100, 500) if is_fault else random.uniform(10, 30))
            PACKET_LOSS.labels(tower_id=tower).set(random.uniform(5, 20) if is_fault else random.uniform(0.01, 0.5))
            THROUGHPUT.labels(tower_id=tower).set(random.uniform(1, 20) if is_fault else random.uniform(100, 500))
        
        time.sleep(5)
