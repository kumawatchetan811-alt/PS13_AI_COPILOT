import pandas as pd 
from sklearn.ensemble import RandomForestClassifier
import joblib

data = pd.read_csv("network_data.csv")

# features
X = data[["latency","jitter","packet_loss","bandwidth"]]

# correct label column
y = data["label"]

model = RandomForestClassifier()
model.fit(X, y)

joblib.dump(model, "network_model.pkl")

print("Model Saved Successfully")