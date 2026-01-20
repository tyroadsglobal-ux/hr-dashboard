import streamlit as st
import pandas as pd
import os
from supabase import create_client

# ================= ENV =================

SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_KEY"]

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)


# ================= PAGE CONFIG =================
st.set_page_config(
    page_title="Recruitment Dashboard",
    layout="wide"
)

# ================= GLOBAL UI =================
st.markdown("""
<style>
#MainMenu, footer {visibility:hidden;}

html, body, [data-testid="stAppViewContainer"] {
    background: radial-gradient(circle at top, #11162b, #0b0f1e);
}

/* REMOVE STREAMLIT TOP GAP */
.block-container {
    padding-top: 1.5rem !important;
}

/* ================= CARDS ================= */
.section-card {
    background:#131a36;
    padding:28px;
    border-radius:22px;
    box-shadow:0 20px 40px rgba(0,0,0,.45);
    margin-bottom:30px;
}

/* ================= KPI ================= */
.kpi-card {
    background:linear-gradient(135deg,#1f2b45,#243b5e);
    padding:24px;
    border-radius:20px;
    color:white;
    box-shadow:0 18px 35px rgba(0,0,0,.45);
    transition:.25s ease;
}
.kpi-card:hover {
    transform: translateY(-4px);
}
.kpi-title {font-size:13px; opacity:.8;}
.kpi-value {font-size:30px; font-weight:700;}

/* ================= INPUTS ================= */
input, textarea, button {
    border-radius:14px !important;
}
</style>
""", unsafe_allow_html=True)

# ================= DASHBOARD =================
st.title("📊 Recruitment Dashboard")
st.caption("Clean, real-time hiring insights")

@st.cache_data(ttl=30)
def load_data():
    res = supabase.table("hr_candidates").select("*").execute()
    return pd.DataFrame(res.data or [])

df = load_data()

if df.empty:
    st.warning("No data found")
    st.stop()

# ================= FILTERS =================
st.markdown("<div class='section-card'>", unsafe_allow_html=True)
st.markdown("### 🔎 Filter Candidates")

with st.form("filters"):
    c1, c2, c3 = st.columns(3)

    with c1:
        f_location = st.multiselect(
            "Location",
            ["Bada Kampoo","Thatipur","Morar","DD Nagar","Lashkar","Hazira","Other"]
        )
    with c2:
        f_experience = st.multiselect(
            "Experience",
            ["Fresher","0–1 Years","1–2 Years","2–3 Years","3–5 Years","5+ Years"]
        )
    with c3:
        f_gender = st.multiselect("Gender", ["Male","Female","Other"])

    age_min, age_max = int(df.age.min()), int(df.age.max())
    f_age = st.slider("Age Range", age_min, age_max, (age_min, age_max))

    apply = st.form_submit_button("Apply Filters")

st.markdown("</div>", unsafe_allow_html=True)

# ================= FILTER LOGIC =================
filtered = df.copy()

if apply:
    if f_location:
        filtered = filtered[filtered.location.isin(f_location)]
    if f_experience:
        filtered = filtered[filtered.experience.isin(f_experience)]
    if f_gender:
        filtered = filtered[filtered.gender.isin(f_gender)]
    filtered = filtered[
        (filtered.age >= f_age[0]) &
        (filtered.age <= f_age[1])
    ]

# ================= KPI =================
total = len(filtered)
freshers = filtered.experience.str.contains("Fresher|0", case=False, na=False).sum()
experienced = total - freshers
avg_salary = int(filtered.expected_salary.mean()) if not filtered.empty else 0

st.markdown("### 📌 Recruitment Overview")

k1, k2, k3, k4 = st.columns(4)
k1.markdown(f"<div class='kpi-card'><div class='kpi-title'>Total Applications</div><div class='kpi-value'>{total}</div></div>", unsafe_allow_html=True)
k2.markdown(f"<div class='kpi-card'><div class='kpi-title'>Freshers</div><div class='kpi-value'>{freshers}</div></div>", unsafe_allow_html=True)
k3.markdown(f"<div class='kpi-card'><div class='kpi-title'>Experienced</div><div class='kpi-value'>{experienced}</div></div>", unsafe_allow_html=True)
k4.markdown(f"<div class='kpi-card'><div class='kpi-title'>Avg Salary</div><div class='kpi-value'>₹{avg_salary:,}</div></div>", unsafe_allow_html=True)

# ================= TABLE =================
st.markdown("### 📋 Candidate Details")

filtered["Resume"] = filtered.resume_link
display = filtered.drop(columns=["resume_link"])

st.dataframe(
    display.sort_values("created_at", ascending=False),
    hide_index=True,
    use_container_width=True,
    column_config={
        "Resume": st.column_config.LinkColumn("Resume", display_text="View")
    }
)

