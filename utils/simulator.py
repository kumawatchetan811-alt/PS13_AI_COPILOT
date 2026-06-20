import random

def get_live_network_data():
    return {
        "latency": random.randint(10, 120),
        "jitter": random.randint(1, 50),
        "packet_loss": random.randint(0, 20),
        "bandwidth": random.randint(50, 1000)
    }