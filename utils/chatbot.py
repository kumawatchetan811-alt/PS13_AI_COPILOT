def chatbot_response(user_input, latency, jitter, packet_loss, bandwidth, risk_level):

    user_input = user_input.lower()
    responses = []

    # ================= OVERALL HEALTH =================
    if risk_level == "HIGH":
        responses.append(
            "🚨 Critical Network Condition Detected. Immediate attention required."
        )
    elif risk_level == "MEDIUM":
        responses.append(
            "⚠️ Network performance is degraded. Monitoring recommended."
        )
    else:
        responses.append(
            "✅ Network is operating normally."
        )

    # ================= ROOT CAUSE =================
    if any(word in user_input for word in ["why", "cause", "risk"]):

        reasons = []

        if latency > 80:
            reasons.append(f"High Latency ({latency} ms)")

        if packet_loss > 5:
            reasons.append(f"Packet Loss ({packet_loss}%)")

        if jitter > 30:
            reasons.append(f"High Jitter ({jitter} ms)")

        if bandwidth < 100:
            reasons.append(f"Low Bandwidth ({bandwidth} Mbps)")

        if reasons:
            responses.append(
                "📍 Root Cause Analysis:\n• " +
                "\n• ".join(reasons)
            )

    # ================= RECOMMENDATIONS =================
    if any(word in user_input for word in ["fix", "solution", "recommend", "action"]):

        actions = []

        if latency > 80:
            actions.append("Optimize routing path")

        if packet_loss > 5:
            actions.append("Inspect interfaces and packet drops")

        if jitter > 30:
            actions.append("Reduce congestion and stabilize traffic")

        if bandwidth < 100:
            actions.append("Upgrade or reallocate bandwidth")

        if actions:
            responses.append(
                "💡 Recommended Actions:\n• " +
                "\n• ".join(actions)
            )

    # ================= NOC PLAYBOOK =================
    if any(word in user_input for word in ["noc", "engineer", "operator"]):

        responses.append("""
👨‍💻 NOC Response Plan

1. Validate device health
2. Check routing tables
3. Review interface statistics
4. Analyze packet drops
5. Verify backup links
6. Escalate if SLA threshold exceeded
""")

    # ================= STATUS =================
    if any(word in user_input for word in ["status", "summary", "health"]):

        responses.append(f"""
📊 Network Status Summary

Risk Level : {risk_level}
Latency    : {latency} ms
Jitter     : {jitter} ms
Packet Loss: {packet_loss} %
Bandwidth  : {bandwidth} Mbps
""")

    # ================= INCIDENT =================
    if "incident" in user_input:

        responses.append(f"""
🎫 Incident Assessment

Severity : {risk_level}

Primary Impact:
- User Experience
- Network Stability

Suggested Escalation:
{"Immediate" if risk_level == "HIGH" else "Monitor and Review"}
""")

    # ================= DEFAULT =================
    if len(responses) == 1:
        responses.append("""
🤖 Available Commands:

• Why is risk high?
• How to fix network issues?
• Show network status
• Generate incident summary
• What should NOC engineer do?
""")

    return "\n\n".join(responses)