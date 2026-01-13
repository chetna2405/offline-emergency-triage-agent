import streamlit as st
from triage_rules import triage
import streamlit.components.v1 as components

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
        return "#2563eb"
    elif value > high:
        return "#dc2626"
    else:
        return "#16a34a"

# ---------------- THEME ----------------
st.markdown("""
<style>
            
header, footer { visibility: hidden; }

.stApp {
    background: radial-gradient(circle at top left,#e0f2fe,#ffffff);
    color: #0f172a;
}

.block-container { max-width: 920px; padding-top: 2rem; }

.hero {
    background: linear-gradient(135deg,#0f172a,#1e293b);
    color: white;
    padding: 2.6rem;
    border-radius: 24px;
    text-align: center;
    margin-bottom: 1.5rem;
}

.badges {
    display: flex;
    justify-content: space-between;
    margin-bottom: 2rem;
}

.badge {
    padding: 0.4rem 1rem;
    border-radius: 999px;
    font-size: 0.8rem;
    font-weight: 600;
}

.offline { background:#e0f2fe; color:#0369a1; }
.lang { background:#ecfeff; color:#0e7490; }

.card {
    background: white;
    padding: 2.2rem;
    border-radius: 22px;
    box-shadow: 0 20px 40px rgba(2,6,23,0.1);
    margin-bottom: 2.2rem;
}

.stButton > button {
    width: 100%;
    background: #2563eb;
    color: white;
    border-radius: 18px;
    padding: 1rem;
    font-size: 16px;
    font-weight: 700;
    border: none;
}

.result-critical { background:#fee2e2; border-left:8px solid #dc2626; }
.result-moderate { background:#fef3c7; border-left:8px solid #d97706; }
.result-mild { background:#dcfce7; border-left:8px solid #16a34a; }

.footer {
    text-align: center;
    color: #64748b;
    font-size: 0.85rem;
    margin-top: 3rem;
}
</style>
""", unsafe_allow_html=True)

# ---------------- HERO ----------------
st.markdown("""
<div class="hero">
<h1>🩺 Offline Emergency Triage Agent</h1>
<p>Decision support for disasters & low-connectivity healthcare</p>
</div>
""", unsafe_allow_html=True)

# ---------------- BADGES ----------------
st.markdown("""
<div class="badges">
<span class="badge offline">🔒 Offline Mode · No Cloud</span>
<span class="badge lang">🇮🇳 Hindi & English</span>
</div>
""", unsafe_allow_html=True)

# ---------------- INPUT ----------------
st.markdown('<div class="card">', unsafe_allow_html=True)

st.subheader("Quick Symptom Selection")
symptoms = [
    "Fever","Chest pain","Difficulty breathing",
    "Severe bleeding","Unconscious","Vomiting",
    "Abdominal pain","Dizziness","Injury / trauma"
]
selected = st.multiselect("Select observed symptoms", symptoms)

if selected:
    st.session_state.symptoms_text = ", ".join(selected)

st.subheader("Patient Symptom Notes")
st.text_area("Describe symptoms", key="symptoms_text", height=120)

st.subheader("Patient Vitals (Optional)")
c1, c2, c3 = st.columns(3)

with c1:
    temp = st.number_input("🌡️ Temp (°C)", 34.0, 43.0, 37.0, step=0.1)
    st.markdown(f"<span style='color:{vitals_color(temp,36.5,37.5)}'>Normal: 36.5–37.5</span>", unsafe_allow_html=True)

with c2:
    pulse = st.number_input("❤️ Pulse (bpm)", 30, 200, 80)
    st.markdown(f"<span style='color:{vitals_color(pulse,60,100)}'>Normal: 60–100</span>", unsafe_allow_html=True)

with c3:
    spo2 = st.number_input("🫁 SpO₂ (%)", 50, 100, 98)
    st.markdown(f"<span style='color:{vitals_color(spo2,95,100)}'>Normal: ≥95%</span>", unsafe_allow_html=True)

run = st.button("Run Triage")
st.markdown('</div>', unsafe_allow_html=True)

# ---------------- RESULT ----------------
if run and st.session_state.symptoms_text.strip():
    result = triage(st.session_state.symptoms_text)
    level = result["level"]

    box = "result-critical" if level=="CRITICAL" else "result-moderate" if level=="MODERATE" else "result-mild"

    st.markdown(f'<div class="card {box}">', unsafe_allow_html=True)
    st.markdown(f"### {result['color']} Urgency Level: **{level}**")

    st.markdown("### ✔️ Do")
    for a in result["do"]:
        st.markdown(f"- {a}")

    st.markdown("### ❌ Don’t")
    for d in result["dont"]:
        st.markdown(f"- {d}")

    st.markdown("### ⏱️ Monitor")
    for m in result["monitor"]:
        st.markdown(f"- {m}")

    speech = (
        f"Urgency level is {level}. "
        + " ".join(result["do"])
        + ". Do not: " + " ".join(result["dont"])
        + ". Monitor: " + " ".join(result["monitor"])
    )

    components.html(
        f"""
        <button onclick="
            const msg = new SpeechSynthesisUtterance({speech!r});
            window.speechSynthesis.cancel();
            window.speechSynthesis.speak(msg);
        "
        style="
            width:100%;
            margin-top:1rem;
            padding:14px;
            border:none;
            border-radius:18px;
            background:#2563eb;
            color:white;
            font-size:16px;
            font-weight:700;
            cursor:pointer;
        ">
        🔊 Read Instructions Aloud
        </button>
        """,
        height=80,
    )

    st.markdown("""
    <div style="margin-top:1.2rem;padding:1rem;
    border-left:8px solid #7c2d12;background:#fff;">
    🛑 If emergency services are unreachable, continue first-response steps
    and prepare transport to nearest PHC.
    </div>
    """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

# ---------------- FOOTER ----------------
st.markdown("""
<div class="footer">
⚠️ Decision support only. Not a medical diagnosis system.
</div>
""", unsafe_allow_html=True)
