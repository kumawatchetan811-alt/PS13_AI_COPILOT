def chatbot_response(user_input, latency, jitter, packet_loss, bandwidth, risk_level):

    user_input = user_input.lower()

    if "why" in user_input:

        reasons = []

        if latency > 80:
            reasons.append(f"High Latency ({latency} ms)")

        if packet_loss > 5:
            reasons.append(f"Packet Loss ({packet_loss}%)")

        if jitter > 30:
            reasons.append(f"High Jitter ({jitter})")

        if reasons:
            return "Risk is elevated because: " + ", ".join(reasons)

        return "Network is currently healthy."

    elif "fix" in user_input:

        fixes = []

        if latency > 80:
            fixes.append("• Check routing path")

        if packet_loss > 5:
            fixes.append("• Inspect interfaces and links")

        if bandwidth < 100:
            fixes.append("• Increase available bandwidth")

        if jitter > 30:
            fixes.append("• Reduce congestion")

        if fixes:
            return "\n".join(fixes)

        return "No corrective action required."

    elif "noc" in user_input:

        return """
1. Verify router health
2. Check congestion
3. Monitor packet drops
4. Escalate critical incidents
5. Review routing tables
"""

    return "Try: Why is risk high? | How to fix? | What should NOC engineer do?"