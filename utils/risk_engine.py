def calculate_risk(latency, jitter, packet_loss, bandwidth):

    score = (
        latency * 0.4 +
        jitter * 0.2 +
        packet_loss * 2 -
        (bandwidth / 100)
    )

    if score < 30:
        return score, "LOW"
    elif score < 70:
        return score, "MEDIUM"
    else:
        return score, "HIGH"