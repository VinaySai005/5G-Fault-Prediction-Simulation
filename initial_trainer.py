import pandas as pd, joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

print("⏳ Training initial model from metrics.csv...")
df = pd.read_csv('metrics.csv')
features = ['signal_strength', 'latency', 'packet_loss', 'throughput']

X_train, X_test, y_train, y_test = train_test_split(df[features], df['status'], test_size=0.2, random_state=42, stratify=df['status'])
model = RandomForestClassifier(n_estimators=100, random_state=42, class_weight='balanced').fit(X_train, y_train)

print(f"--- Model Accuracy: {accuracy_score(y_test, model.predict(X_test)):.4f} ---")
joblib.dump(model, 'fault_model.pkl')
print("💾 Initial model saved as fault_model.pkl!")
