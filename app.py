import streamlit as st
import pandas as pd
import joblib
import time
from collections import deque

from utils.simulator import get_live_network_data
from utils.risk_engine import calculate_risk
from utils.chatbot import chatbot_response

st.set_page_config(
    page_title="AI NOC Copilot",
    layout="wide"
)
st.markdown("""
<style>

/* MAIN BACKGROUND */
body {
    background-color: #0E1117;
}

/* SECTION HEADINGS */
h1, h2, h3 {
    color: #00ffcc;
}

/* METRIC CARDS STYLE */
[data-testid="stMetric"] {
    background-color: rgba(255, 255, 255, 0.05);
    border-radius: 12px;
    padding: 10px;
    box-shadow: 0px 0px 10px rgba(0,255,204,0.1);
}

/* SIDEBAR */
section[data-testid="stSidebar"] {
    background-color: #111827;
}

/* BUTTON STYLE */
.stButton>button {
    background-color: #00ffcc;
    color: black;
    border-radius: 8px;
    font-weight: bold;
}

.stButton>button:hover {
    background-color: #00ccaa;
}

</style>
""", unsafe_allow_html=True)
def root_cause_analysis(latency, jitter, packet_loss, bandwidth):
    causes = []
    actions = []

    if latency > 70:
        causes.append("🔴 High Latency Detected")
        actions.append("✅ Check routing / congestion")

    if packet_loss > 5:
        causes.append("🟠 Packet Loss Spike")
        actions.append("✅ Inspect cables / interface errors")

    if jitter > 15:
        causes.append("🔴 Network Instability")
        actions.append("✅ Stabilize routing path")

    if bandwidth > 85:
        causes.append("🟡 Congestion Possible")
        actions.append("✅ Shift traffic to backup link")

    if not causes:
        causes.append("🟢 Network Stable")
        actions.append("✅ No action needed")

    return causes, actions
def ai_copilot_response(user_input, latency, jitter, packet_loss, bandwidth):

    user_input = user_input.lower()

    if "slow" in user_input or "latency" in user_input:
        return "🔴 High latency detected" if latency > 70 else "🟢 Latency normal"

    if "packet" in user_input:
        return "🟠 Packet loss detected" if packet_loss > 5 else "🟢 No packet loss"

    if "bandwidth" in user_input:
        return "🟡 Low bandwidth" if bandwidth < 50 else "🟢 Bandwidth OK"

    if "fix" in user_input:
        return "💡 Restart interface + check routing"

    return "🤖 Ask about latency, packet loss, bandwidth"

st.markdown('<div class="big-title">🧠 AI NOC Copilot</div>', unsafe_allow_html=True)

st.markdown('<div class="sub-title">Real-Time Network Intelligence | ML Diagnostics | AI Root Cause Engine</div>', unsafe_allow_html=True)

st.markdown("---")

st.markdown("## 🎛️ Network Control Center")

col1, col2, col3, col4 = st.columns(4)

with col1:
    latency = st.slider("Latency (ms)", 0, 200, 50)

with col2:
    jitter = st.slider("Jitter (ms)", 0, 100, 10)

with col3:
    packet_loss = st.slider("Packet Loss (%)", 0, 50, 2)

with col4:
    bandwidth = st.slider("Bandwidth (Mbps)", 0, 1000, 60)



st.markdown("""
<style>
body {
    background-color: #0E1117;
}

.big-title {
    font-size: 40px;
    font-weight: 800;
    color: #00ffcc;
}

.sub-title {
    font-size: 16px;
    color: #a0a0a0;
}
</style>
""", unsafe_allow_html=True)

# ================= LOAD MODEL =================
model = joblib.load("network_model.pkl")

# ================= SESSION STATE (FOR GRAPHS) =================
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
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

    st.subheader("📥 Manual Network Input")

    latency = st.slider("Latency", 0, 100, 50)
    jitter = st.slider("Jitter", 0, 50, 10)
    packet_loss = st.slider("Packet Loss", 0, 20, 2)
    bandwidth = st.slider("Bandwidth", 0, 100, 60)

    if st.button("🚀 Predict Network Health"):

        data = [[latency, jitter, packet_loss, bandwidth]]

        result = model.predict(data)
        confidence = model.predict_proba(data)

        # ================= SCORE (FIXED SAFELY) =================
        score = round(max(confidence[0]) * 100, 2)

        # ================= METRICS DASHBOARD =================
        st.markdown("## 📊 Network Intelligence Dashboard")

        col1, col2, col3, col4 = st.columns(4)

        col1.metric("🔥 Risk Score", f"{score}%")
        col2.metric("📡 Latency", f"{latency} ms")
        col3.metric("📦 Packet Loss", f"{packet_loss}%")
        col4.metric("⚡ Bandwidth", f"{bandwidth} Mbps")

        st.progress(min(int(score), 100))

        # ================= STATUS BADGE =================
        if result[0] == 1 or score > 70:
            st.error("🔴 CRITICAL NETWORK RISK")
        elif score > 40:
            st.warning("🟠 MEDIUM NETWORK RISK")
        else:
            st.success("🟢 NETWORK HEALTHY")

        # ================= AI DIAGNOSTIC ENGINE =================
        causes, actions = root_cause_analysis(latency, jitter, packet_loss, bandwidth)

        st.markdown("## 🧠 AI Diagnostic Engine")

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("### 📍 Root Causes")
            for c in causes:
                st.info(c)

        with col2:
            st.markdown("### 💡 Recommended Actions")
            for a in actions:
                st.success(a)
# =========================================================
# 📡 MODE 2: LIVE SIMULATION + AI + GRAPHS
# =========================================================
else:

    st.subheader("📡 Live Network Intelligence Dashboard")

    # ================= LIVE DATA =================
    data = get_live_network_data()

    latency = data["latency"]
    jitter = data["jitter"]
    packet_loss = data["packet_loss"]
    bandwidth = data["bandwidth"]

    # ================= RISK ENGINE =================
    risk_score, risk_level = calculate_risk(
        latency,
        jitter,
        packet_loss,
        bandwidth
    )

    # ================= STORE HISTORY (ONLY ONCE - FIXED) =================
    st.session_state.latency_history.append(latency)
    st.session_state.packet_history.append(packet_loss)
    st.session_state.risk_history.append(risk_score)

    # ================= TOP METRICS =================
    st.markdown("## 🧠 Network Health Overview")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("📡 Latency", f"{latency} ms")
    col2.metric("📦 Packet Loss", f"{packet_loss} %")
    col3.metric("⚡ Bandwidth", f"{bandwidth} Mbps")
    col4.metric("🔥 Risk Score", f"{round(risk_score, 2)}")

    st.markdown("---")

    # ================= ALERT PANEL =================
    st.markdown("## 🚨 Live Alerts")

    alert1, alert2, alert3 = st.columns(3)

    with alert1:
        st.error("🔴 High Latency") if latency > 80 else st.success("🟢 Latency Stable")

    with alert2:
        st.warning("🟠 Packet Loss Warning") if packet_loss > 5 else st.success("🟢 Packet Loss Normal")

    with alert3:
        st.info("ℹ️ Bandwidth Normal") if bandwidth < 300 else st.success("🟢 High Bandwidth")

    st.markdown("---")

    # ================= STATUS =================
    if risk_level == "HIGH":
        st.error("🔴 NETWORK STATUS: CRITICAL")
    elif risk_level == "MEDIUM":
        st.warning("🟠 NETWORK STATUS: DEGRADED")
    else:
        st.success("🟢 NETWORK STATUS: HEALTHY")

    st.markdown("---")

    # ================= GRAPHS =================
    st.markdown("## 📊 Live Network Trends")

    colg1, colg2 = st.columns(2)

    with colg1:
        st.line_chart({
            "Latency": list(st.session_state.latency_history),
            "Packet Loss": list(st.session_state.packet_history)
        })

    with colg2:
        st.line_chart({
            "Risk Score": list(st.session_state.risk_history)
        })

    st.markdown("---")

    # ================= TOPOLOGY =================
    st.markdown("## 🌐 Network Topology")

    if risk_level == "HIGH":
        st.markdown("""
🔴 Router A ───── 🔴 Router B ───── 🔴 Server

        ╲
         ╲
          🔴 Backup Link (ACTIVE FAILOVER)
        """)
    elif risk_level == "MEDIUM":
        st.markdown("""
🟠 Router A ───── 🟠 Router B ───── 🟠 Server

        ╲
         ╲
          🟠 Backup Link (STANDBY)
        """)
    else:
        st.markdown("""
🟢 Router A ───── 🟢 Router B ───── 🟢 Server

        ╲
         ╲
          🟢 Backup Link (OPTIMAL)
        """)

    st.markdown("---")

    # ================= CHATBOT =================
    st.markdown("## 🤖 AI Copilot Chat")

    user_msg = st.text_input("Ask AI about network:")

    if user_msg:
        reply = ai_copilot_response(
            user_msg, latency, jitter, packet_loss, bandwidth
        )
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

    st.markdown("## 🤖 AI Copilot Chat")

    user_msg = st.text_input("Ask AI about network:")

    # ================= AI COPILOT CHAT =================
    st.markdown("## 🤖 AI Copilot Chat")

    user_msg = st.text_input("Ask AI about network:")

    if user_msg:
        reply = ai_copilot_response(
            user_msg,
            latency,
            jitter,
            packet_loss,
            bandwidth
        )

        st.session_state.chat_history.append(("🧑 You", user_msg))
        st.session_state.chat_history.append(("🤖 Copilot", reply))

# ================= CHAT HISTORY DISPLAY =================
    for role, msg in st.session_state.chat_history:
        if role == "🧑 You":
            st.markdown(f"**🧑 You:** {msg}")
        else:
            st.markdown(f"**🤖 Copilot:** {msg}")