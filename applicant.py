import streamlit as st
from supabase import create_client
from datetime import datetime
import os

# ================= CONFIG =================
st.set_page_config(page_title="Job Application", layout="centered")

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# ================= UI =================
st.markdown("""
<style>
body { background-color: #0e1325; }
.box {
    background:#131a36;
    padding:28px;
    border-radius:18px;
}
</style>
""", unsafe_allow_html=True)

st.markdown("<h2 style='text-align:center;'>📝 Job Application</h2>", unsafe_allow_html=True)

st.markdown("<div class='box'>", unsafe_allow_html=True)

with st.form("apply", clear_on_submit=True):
    name = st.text_input("Full Name *")
    age = st.number_input("Age *", 18, 60)
    gender = st.selectbox("Gender *", ["Select","Male","Female","Other"])
    location = st.text_input("Location *")
    industry = st.text_input("Industry *")
    experience = st.selectbox(
        "Experience *",
        ["Select","Fresher","0–1","1–3","3–5","5+"]
    )
    salary = st.number_input("Expected Salary (₹)", step=1000)
    resume = st.text_input("Resume Link")

    submit = st.form_submit_button("Submit Application")

st.markdown("</div>", unsafe_allow_html=True)

# ================= SAVE TO DB =================
if submit:
    if not name or gender == "Select" or experience == "Select":
        st.error("Please fill all required fields")
    else:
        supabase.table("hr_candidates").insert({
            "name": name,
            "age": age,
            "gender": gender,
            "location": location,
            "industry": industry,
            "experience": experience,
            "expected_salary": salary,
            "resume_link": resume
        }).execute()

        st.success("✅ Application submitted successfully!")
