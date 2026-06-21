import subprocess
import re

TARGET_IP = "192.168.1.3"   # branch2 IP


def get_network_metrics():
    try:
        result = subprocess.check_output(
            ["ping", TARGET_IP, "-n", "4"],
            text=True
        )

        # Packet Loss
        loss = re.search(r"(\d+)% loss", result)
        packet_loss = int(loss.group(1)) if loss else 0

        # Average Latency
        avg = re.search(r"Average = (\d+)ms", result)
        latency = int(avg.group(1)) if avg else 0

        return {
            "latency": latency,
            "packet_loss": packet_loss
        }

    except Exception as e:
        return {
            "latency": 0,
            "packet_loss": 100
        }