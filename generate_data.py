import pandas as pd
import random

data = []

for i in range(1500):  # 1500 rows dataset
    latency = random.randint(10, 100)
    jitter = random.randint(1, 50)
    packet_loss = random.randint(0, 20)
    bandwidth = random.randint(10, 100)

    # Failure logic (realistic pattern)
    if latency > 75 or packet_loss > 7 or jitter > 20:
        label = 1  # failure
    else:
        label = 0  # healthy

    data.append([latency, jitter, packet_loss, bandwidth, label])

df = pd.DataFrame(data, columns=[
    "latency", "jitter", "packet_loss", "bandwidth", "label"
])

df.to_csv("network_data.csv", index=False)

print("Dataset generated successfully!")