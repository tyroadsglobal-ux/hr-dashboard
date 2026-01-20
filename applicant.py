import streamlit as st
from datetime import datetime
from uuid import uuid4
import os
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()
supabase = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))

st.set_page_config(page_title="Job Application", layout="centered")

st.markdown("""
<style>
#MainMenu, footer, header {visibility: hidden;}
body {background:#0e1325;}
.form-box {
    background:#131a36;
    padding:28px;
    border-radius:22px;
    box-shadow:0 20px 45px rgba(0,0,0,.5);
}
.stButton>button {
    width:100%;
    height:48px;
    border-radius:14px;
    font-size:16px;
    font-weight:600;
}
</style>
""", unsafe_allow_html=True)

st.markdown("<div class='form-box'>", unsafe_allow_html=True)
st.markdown("## 📝 Job Application")
st.caption("Takes less than 2 minutes")

with st.form("apply", clear_on_submit=True):
    name = st.text_input("Full Name *")
    age = st.number_input("Age *", 18, 60)
    gender = st.selectbox("Gender *", ["Male","Female","Other"])

    location = st.selectbox(
        "Location *",
        ["Bada Kampoo","Thatipur","Morar","DD Nagar","Lashkar","Hazira","Other"]
    )

    custom_location = ""
    if location == "Other":
        custom_location = st.text_input("Enter your location")

    industry = st.text_input("Industry / Field *")

    experience = st.selectbox(
        "Experience *",
        ["Fresher","0–1 Years","1–2 Years","2–3 Years","3–5 Years","5+ Years"]
    )

    salary = st.number_input("Expected Salary (₹)", 0, step=1000)
    resume = st.file_uploader("Upload Resume (PDF ≤5MB)", type=["pdf"])

    submit = st.form_submit_button("Submit Application")

if submit:
    final_location = custom_location if location == "Other" else location

    if not all([name, industry, final_location]):
        st.error("Please fill all required fields")
        st.stop()

    resume_url = None
    if resume:
        path = f"resumes/{datetime.now().strftime('%Y-%m')}/{uuid4()}.pdf"
        supabase.storage.from_("resumes").upload(
            path, resume.getvalue(),
            {"content-type":"application/pdf"}
        )
        resume_url = supabase.storage.from_("resumes").get_public_url(path)

    supabase.table("hr_candidates").insert({
        "name": name,
        "age": age,
        "gender": gender,
        "location": final_location,
        "industry": industry,
        "experience": experience,
        "expected_salary": salary,
        "resume_link": resume_url
    }).execute()

    st.success("✅ Application submitted successfully")

st.markdown("</div>", unsafe_allow_html=True)
