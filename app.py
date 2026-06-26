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

/* ================= MAIN APP ================= */

.stApp {
    background-color: #0E1117;
}

/* ================= NAVBAR ================= */

.navbar {
    background: linear-gradient(90deg, #111827, #1F2937);
    padding: 15px;
    border-radius: 12px;
    margin-bottom: 20px;
    display: flex;
    justify-content: space-around;
    box-shadow: 0px 0px 15px rgba(0,255,204,0.15);
}

.nav-item {
    color: #00ffcc;
    font-size: 18px;
    font-weight: bold;
}

/* ================= TITLES ================= */

.big-title {
    font-size: 42px;
    font-weight: 800;
    color: #00ffcc;
    text-align: center;
}

.sub-title {
    font-size: 16px;
    color: #b0b0b0;
    text-align: center;
    margin-bottom: 20px;
}

/* ================= HEADINGS ================= */

h1, h2, h3 {
    color: #00ffcc !important;
}

/* ================= METRIC CARDS ================= */

[data-testid="stMetric"] {
    background-color: rgba(255,255,255,0.05);
    border-radius: 15px;
    padding: 15px;
    border: 1px solid rgba(0,255,204,0.15);
    box-shadow: 0px 0px 15px rgba(0,255,204,0.08);
}

/* ================= SIDEBAR ================= */

section[data-testid="stSidebar"] {
    background-color: #111827;
}

/* ================= BUTTONS ================= */

.stButton > button {
    width: 100%;
    background-color: #00ffcc;
    color: black;
    border-radius: 10px;
    font-weight: bold;
    border: none;
}

.stButton > button:hover {
    background-color: #00ccaa;
}

/* ================= RADIO BUTTONS ================= */

div[role="radiogroup"] label {
    font-size: 18px !important;
    font-weight: 700 !important;
}

/* ================= CHAT BOX ================= */

.stTextInput input {
    border-radius: 10px;
}

/* ================= GRAPHS ================= */

[data-testid="stVerticalBlock"] canvas {
    border-radius: 10px;
}

/* ================= SCROLLBAR ================= */

::-webkit-scrollbar {
    width: 8px;
}

::-webkit-scrollbar-thumb {
    background: #00ffcc;
    border-radius: 10px;
}

</style>
""", unsafe_allow_html=True)

tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "🏠 Dashboard",
    "📡 Live Monitor",
    "📊 Analytics",
    "🤖 AI Copilot",
    "🎫 Incident Center",
    "🌐 Topology"
])


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


st.markdown('<div class="big-title">🧠 AI NOC Copilot</div>', unsafe_allow_html=True)

st.markdown('<div class="sub-title">Real-Time Network Intelligence | ML Diagnostics | AI Root Cause Engine</div>', unsafe_allow_html=True)

st.markdown("---")

st.markdown("## 🎛️ Network Control Center")


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


# ================= HEADER =================

st.markdown("""
<h1 class="big-title">
📡 Live Network Intelligence Dashboard
</h1>

<p class="sub-title">
AI Powered Network Monitoring • Root Cause Analysis • Incident Prediction
</p>
""", unsafe_allow_html=True)

# ================= SIDEBAR =================

st.sidebar.image("https://img.icons8.com/color/96/network.png", width=80)

st.sidebar.title("AI NOC Copilot")

st.sidebar.success("🟢 System Online")

st.sidebar.markdown("---")

st.sidebar.write("### Project")

st.sidebar.write("✔ Live Monitoring")

st.sidebar.write("✔ ML Prediction")

st.sidebar.write("✔ AI Copilot")

st.sidebar.write("✔ Incident Center")

st.sidebar.write("✔ Root Cause Engine")

# ================= MODE SELECTION =================

col1, col2 = st.columns(2)

with col1:
    if st.button("📡 LIVE MONITORING MODE", use_container_width=True):
        st.session_state.mode = "LIVE"

with col2:
    if st.button("🔬 ML PREDICTION MODE", use_container_width=True):
        st.session_state.mode = "ML"

mode = st.session_state.get("mode", "LIVE")

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

    st.write("Latency =", latency)
    st.write("Jitter =", jitter)
    st.write("Packet Loss =", packet_loss)
    st.write("Bandwidth =", bandwidth)

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

    with tab2:

    # ================= ALERT PANEL =================

        st.markdown("## 🚨 Live Alerts")

        col1, col2, col3 = st.columns(3)

        with col1:
            if latency > 80:
                st.error("🔴 High Latency")
            else:
                st.success("🟢 Latency Stable")

        with col2:
            if packet_loss > 5:
                st.warning("🟠 Packet Loss Warning")
            else:
                st.success("🟢 Packet Loss Normal")

        with col3:
            if bandwidth < 300:
                st.info("ℹ️ Bandwidth Normal")
            else:
                st.success("🟢 High Bandwidth")

        if risk_level == "HIGH":
            st.error("🔴 NETWORK STATUS: CRITICAL")
        elif risk_level == "MEDIUM":
            st.warning("🟠 NETWORK STATUS: DEGRADED")
        else:
            st.success("🟢 NETWORK STATUS: HEALTHY")

    st.markdown("---")

    # ================= GRAPHS =================
    with tab3:

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
    with tab6:

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

# ================= AI COPILOT CHAT =================
    with tab4:

        st.markdown("## 🤖 AI Copilot Chat")

        user_msg = st.text_input(
            "Ask AI about network:",
            key="copilot_chat_input"
        )

        if "chat_history" not in st.session_state:
            st.session_state.chat_history = []

        if user_msg:

            reply = chatbot_response(
                user_msg,
                latency,
                jitter,
                packet_loss,
                bandwidth,
                risk_level
            )

            st.session_state.chat_history.append(("🧑 You", user_msg))
            st.session_state.chat_history.append(("🤖 Copilot", reply))

        for role, msg in st.session_state.chat_history:
            if role == "🧑 You":
                st.markdown(f"**🧑 You:** {msg}")
            else:
                st.markdown(f"**🤖 Copilot:** {msg}")
    # ================= INCIDENT TICKET =================

    with tab5:

        st.markdown("## 🎫 Incident Center")

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

        if st.button("🎬 Demo Failure Scenario"):

            st.error("🚨 Simulated Critical Network Failure")

            st.metric("Latency", 120)
            st.metric("Packet Loss", 15)
            st.metric("Bandwidth", 20)

            st.error("Risk Level : HIGH")

            st.write("🔴 High Latency")
            st.write("🔴 Packet Loss Spike")
            st.write("🔴 Network Instability")

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
    4. Increase available bandwidth
    5. Continue real-time monitoring
    """

            st.text_area("📄 AI Generated Report", report, height=300)