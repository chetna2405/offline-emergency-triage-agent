import streamlit as st
from triage_rules import triage

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Offline Emergency Triage Agent",
    page_icon="🩺",
    layout="centered"
)

# ---------------- SESSION STATE ----------------
if "symptoms_text" not in st.session_state:
    st.session_state.symptoms_text = ""

# ---------------- HELPERS ----------------
def vitals_color(value, low, high):
    if value < low:
        return "#2563eb"   # blue (low)
    elif value > high:
        return "#dc2626"   # red (high)
    else:
        return "#16a34a"   # green (normal)

# ---------------- AURORA HEALTHCARE THEME ----------------
st.markdown("""
<style>
header, footer { visibility: hidden; }

.stApp {
    background: radial-gradient(
        circle at top left,
        #e0f2fe 0%,
        #f0f9ff 25%,
        #eef2ff 50%,
        #fdf4ff 75%,
        #ffffff 100%
    );
    color: #0f172a;
}

.block-container {
    max-width: 920px;
    padding-top: 2rem;
}

.hero {
    background: linear-gradient(135deg, #0f172a, #1e293b);
    color: white;
    padding: 2.8rem;
    border-radius: 26px;
    text-align: center;
    box-shadow: 0 35px 70px rgba(15,23,42,0.35);
    margin-bottom: 1.5rem;
}

.hero p { color: #cbd5f5; }

.badges {
    display: flex;
    justify-content: space-between;
    margin: 1.2rem 0 2.2rem 0;
}

.badge {
    padding: 0.5rem 1rem;
    border-radius: 999px;
    font-size: 0.82rem;
    font-weight: 600;
}

.offline { background: #e0f2fe; color: #0369a1; }
.lang { background: #ecfeff; color: #0e7490; }

.card {
    background: rgba(255,255,255,0.95);
    padding: 2.3rem;
    border-radius: 22px;
    box-shadow: 0 25px 50px rgba(2,6,23,0.1);
    margin-bottom: 2.3rem;
}

textarea {
    background-color: #f8fafc !important;
    color: #020617 !important;
    border-radius: 16px !important;
    border: 1px solid #c7d2fe !important;
}

.stButton > button {
    width: 100%;
    background: linear-gradient(135deg, #4f46e5, #2563eb);
    color: white;
    border-radius: 18px;
    padding: 1rem;
    font-size: 17px;
    font-weight: 700;
    border: none;
}

.result-box {
    padding: 2.2rem;
    border-radius: 20px;
    margin-top: 1.8rem;
}

.result-critical {
    background: linear-gradient(135deg, #fee2e2, #fecaca);
    border-left: 8px solid #dc2626;
}

.result-moderate {
    background: linear-gradient(135deg, #fef3c7, #fde68a);
    border-left: 8px solid #d97706;
}

.result-mild {
    background: linear-gradient(135deg, #dcfce7, #bbf7d0);
    border-left: 8px solid #16a34a;
}

.footer {
    text-align: center;
    color: #64748b;
    font-size: 0.85rem;
    margin-top: 3.5rem;
}
</style>
""", unsafe_allow_html=True)

# ---------------- HERO ----------------
st.markdown("""
<div class="hero">
    <h1>🩺 Offline Emergency Triage Agent</h1>
    <p>Edge AI decision support for low-connectivity healthcare settings</p>
</div>
""", unsafe_allow_html=True)

# ---------------- BADGES ----------------
st.markdown("""
<div class="badges">
    <span class="badge offline">🔒 Offline Mode · No Cloud Usage</span>
    <span class="badge lang">🇮🇳 Supports Hindi & English</span>
</div>
""", unsafe_allow_html=True)

# ---------------- INPUT CARD ----------------
st.markdown('<div class="card">', unsafe_allow_html=True)

# ---- Symptoms ----
st.subheader("Quick Symptom Selection")

symptom_options = [
    "Fever", "Chest pain", "Difficulty breathing",
    "Severe bleeding", "Unconscious", "Vomiting",
    "Abdominal pain", "Dizziness", "Injury / trauma"
]

selected_symptoms = st.multiselect("Tap to select observed symptoms", symptom_options)

if selected_symptoms:
    st.session_state.symptoms_text = ", ".join(selected_symptoms)

st.subheader("Patient Symptom Notes")

st.text_area(
    "Describe patient symptoms (English / हिंदी)",
    key="symptoms_text",
    height=140
)

# ---- VITALS (RESTORED) ----
st.subheader("Patient Vitals (Optional)")
st.caption("Color indicators show whether values are within normal range.")

c1, c2, c3 = st.columns(3)

with c1:
    temp = st.number_input("🌡️ Temperature (°C)", 34.0, 43.0, 37.0, step=0.1)
    st.markdown(
        f"<span style='color:{vitals_color(temp,36.5,37.5)};font-weight:600;'>Normal: 36.5–37.5 °C</span>",
        unsafe_allow_html=True
    )

with c2:
    pulse = st.number_input("❤️ Pulse (bpm)", 30, 200, 80)
    st.markdown(
        f"<span style='color:{vitals_color(pulse,60,100)};font-weight:600;'>Normal: 60–100 bpm</span>",
        unsafe_allow_html=True
    )

with c3:
    spo2 = st.number_input("🫁 SpO₂ (%)", 50, 100, 98)
    st.markdown(
        f"<span style='color:{vitals_color(spo2,95,100)};font-weight:600;'>Normal: ≥95%</span>",
        unsafe_allow_html=True
    )

run = st.button("Run Triage")
st.markdown('</div>', unsafe_allow_html=True)

# ---------------- RESULT ----------------
if run and st.session_state.symptoms_text.strip():
    result = triage(st.session_state.symptoms_text)
    level = result["level"]

    box_class = (
        "result-critical" if level == "CRITICAL"
        else "result-moderate" if level == "MODERATE"
        else "result-mild"
    )

    st.markdown(f'<div class="card result-box {box_class}">', unsafe_allow_html=True)

    st.markdown(f"### {result['color']} Urgency Level: **{level}**")

    # ---- CONDITION-SPECIFIC GUIDANCE ----
    st.markdown("### ✔️ Do")
    for a in result["do"]:
        st.markdown(f"- {a}")

    st.markdown("### ❌ Don’t")
    for d in result["dont"]:
        st.markdown(f"- {d}")

    st.markdown("### ⏱️ Monitor")
    for m in result["monitor"]:
        st.markdown(f"- {m}")

    # ---- NO-CONNECTIVITY BANNER ----
    st.markdown("""
    <div style="
        background:rgba(255,255,255,0.85);
        border-left:8px solid #7c2d12;
        padding:1.3rem;
        border-radius:16px;
        margin-top:1.5rem;
        color:#7c2d12;
        font-weight:600;">
    🛑 <strong>If emergency services are unreachable:</strong><br>
    Continue first-response steps and prepare for transport to nearest PHC
    when possible.
    </div>
    """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

# ---------------- FOOTER ----------------
st.markdown("""
<div class="footer">
⚠️ Decision support only. Not a medical diagnosis system.
</div>
""", unsafe_allow_html=True)
