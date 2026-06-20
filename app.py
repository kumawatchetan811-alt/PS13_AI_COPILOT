import streamlit as st
import joblib
import time
from collections import deque

from utils.simulator import get_live_network_data
from utils.risk_engine import calculate_risk
from utils.chatbot import chatbot_response

# ================= LOAD MODEL =================
model = joblib.load("network_model.pkl")

# ================= SESSION STATE (FOR GRAPHS) =================
if "latency_history" not in st.session_state:
    st.session_state.latency_history = deque(maxlen=20)

if "packet_history" not in st.session_state:
    st.session_state.packet_history = deque(maxlen=20)

if "risk_history" not in st.session_state:
    st.session_state.risk_history = deque(maxlen=20)

# ================= TITLE =================
st.title("🧠 AI NOC Copilot v3 (ML + Live AI + Graph Intelligence)")
st.sidebar.title("🚨 Live Alerts")
mode = st.radio("Select Mode:", ["🔬 ML Prediction Mode", "📡 Live Simulation Mode"])

# =========================================================
# 🔬 MODE 1: ML PREDICTION
# =========================================================
if mode == "🔬 ML Prediction Mode":

    st.subheader("Manual Network Input")

    latency = st.slider("Latency", 0, 100, 50)
    jitter = st.slider("Jitter", 0, 50, 10)
    packet_loss = st.slider("Packet Loss", 0, 20, 2)
    bandwidth = st.slider("Bandwidth", 0, 100, 60)

    if st.button("Predict Network Health"):

        data = [[latency, jitter, packet_loss, bandwidth]]

        result = model.predict(data)
        confidence = model.predict_proba(data)

        score = round(max(confidence[0]) * 100, 2)

        st.metric("Risk Score", score)

        if result[0] == 1:
            st.error("⚠️ High Failure Risk")

            if latency > 70:
                st.write("🔴 High Latency")
            if packet_loss > 5:
                st.write("🔴 Packet Loss Spike")
            if jitter > 15:
                st.write("🔴 Network Instability")
            if bandwidth > 85:
                st.write("🔴 Congestion")

            st.progress(int(score))

        else:
            st.success("✅ Network Healthy")
            st.progress(int(score))

# =========================================================
# 📡 MODE 2: LIVE SIMULATION + AI + GRAPHS
# =========================================================
else:
    
    st.subheader("Live Network Intelligence Dashboard")

    data = get_live_network_data()

    risk_score, risk_level = calculate_risk(
        data["latency"],
        data["jitter"],
        data["packet_loss"],
        data["bandwidth"]
    )

    latency = data["latency"]
    jitter = data["jitter"]
    packet_loss = data["packet_loss"]
    bandwidth = data["bandwidth"]

    # Alerts
    if latency > 80:
        st.sidebar.error("🔴 High Latency")

    if packet_loss > 5:
        st.sidebar.warning("🟠 Packet Loss Warning")

    if bandwidth > 300:
        st.sidebar.success("🟢 Bandwidth Healthy")

    # ================= STORE HISTORY =================
    st.session_state.latency_history.append(data["latency"])
    st.session_state.packet_history.append(data["packet_loss"])
    st.session_state.risk_history.append(risk_score)

    # ================= METRICS =================
    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Latency", data["latency"])
    col2.metric("Packet Loss", data["packet_loss"])
    col3.metric("Bandwidth", data["bandwidth"])
    col4.metric("Risk Score", round(risk_score, 2))

    # ================= STATUS =================
    if risk_level == "HIGH":
        st.error(f"🚨 Network Status: {risk_level}")
    elif risk_level == "MEDIUM":
        st.warning(f"⚠️ Network Status: {risk_level}")
    else:
        st.success(f"✅ Network Status: {risk_level}")

    # ================= NETWORK TOPOLOGY =================

    st.subheader("🌐 Network Topology")

    if risk_level == "HIGH":
        st.markdown("""
    🔴 Router A ───── 🔴 Router B ───── 🔴 Server

              ╲
               ╲
                🔴 Backup Link
    """)
    else:
        st.markdown("""
    🟢 Router A ───── 🟢 Router B ───── 🟢 Server
    
              ╲
               ╲
                🟢 Backup Link
    """)
    # ================= CHATBOT =================
    st.subheader("🤖 AI Copilot Chat")

    user_input = st.text_input("Ask AI about network:")

    if user_input:
        reply = chatbot_response(user_input,latency,jitter,packet_loss,bandwidth,risk_level)
        st.info(reply)
    # ================= INCIDENT TICKET =================

    if st.button("🎫 Generate Incident Ticket"):

        st.code(f"""
    Incident ID : INC-001

                
    Issue : Network Instability

    Severity : {risk_level}

    Latency : {latency}

    Packet Loss : {packet_loss}

    Bandwidth : {bandwidth}

    Recommended Action :
    - Check Routing
    - Monitor Traffic
    - Inspect Interfaces
    """)
        # ================= DEMO FAILURE SCENARIO =================

    if st.button("🎬 Demo Failure Scenario"):

        st.error("🚨 Simulated Critical Network Failure")

        st.metric("Latency", 120)
        st.metric("Packet Loss", 15)
        st.metric("Bandwidth", 20)

        st.error("Risk Level : HIGH")

        st.write("🔴 High Latency")
        st.write("🔴 Packet Loss Spike")
        st.write("🔴 Network Instability")
    # ================= AI EXECUTIVE SUMMARY =================

    if st.button("🤖 Generate AI Report"):

        report = f"""
    # Network Health Summary

    Current Status : {risk_level}

    Current Latency : {latency}

    Current Packet Loss : {packet_loss}

    Current Bandwidth : {bandwidth}

    Risk Score : {round(risk_score, 2)}

    Primary Issues:
    """

        if latency > 80:
            report += "\n• High Latency"

        if packet_loss > 5:
            report += "\n• Packet Loss Spike"

        if bandwidth < 100:
            report += "\n• Low Available Bandwidth"

        report += """

    Recommended Actions:

    1. Check routing path
    2. Monitor packet drops
    3. Verify network interfaces
    4. Increase available bandwidth if needed
    5. Continue real-time monitoring
    """

        st.text_area("📄 AI Generated Report", report, height=300)
    # ================= LIVE GRAPHS =================
    st.subheader("📊 Live Network Trends")

    st.line_chart({
        "Latency": list(st.session_state.latency_history),
        "Packet Loss": list(st.session_state.packet_history),
        "Risk Score": list(st.session_state.risk_history)
    })

    # ================= AUTO REFRESH =================
    time.sleep(2)
    st.rerun()