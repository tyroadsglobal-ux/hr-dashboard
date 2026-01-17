import streamlit as st
from datetime import datetime

# ================= PAGE CONFIG =================
st.set_page_config(
    page_title="Job Application | HR Portal",
    layout="centered"
)

# ================= GLOBAL STYLES =================
st.markdown("""
<style>
body {
    background-color: #0e1325;
}

.form-box {
    background: #131a36;
    padding: 28px;
    border-radius: 18px;
    box-shadow: 0 15px 35px rgba(0,0,0,0.4);
}

label {
    font-weight: 600;
}

.stButton>button {
    background: linear-gradient(135deg, #4b6cb7, #182848);
    color: white;
    border-radius: 10px;
    height: 45px;
    font-size: 16px;
}
</style>
""", unsafe_allow_html=True)

# ================= HEADER =================
st.markdown(
    "<h2 style='text-align:center;'>📝 Job Application Form</h2>"
    "<p style='text-align:center;color:#9aa4bf;'>Apply in under 2 minutes</p>",
    unsafe_allow_html=True
)

# ================= FORM =================
st.markdown("<div class='form-box'>", unsafe_allow_html=True)

with st.form("application_form", clear_on_submit=True):

    name = st.text_input("Full Name *")
    
    col1, col2 = st.columns(2)
    with col1:
        age = st.number_input("Age *", min_value=18, max_value=60)
    with col2:
        gender = st.selectbox("Gender *", ["Select", "Male", "Female", "Other"])

    location = st.text_input("Current Location *")
    industry = st.text_input("Industry / Field *")

    experience = st.selectbox(
        "Experience Level *",
        ["Select", "Fresher", "0–1 Years", "1–3 Years", "3–5 Years", "5+ Years"]
    )

    salary = st.number_input(
        "Expected Monthly Salary (₹)",
        min_value=0,
        step=1000
    )

    resume_link = st.text_input("Resume Link (Google Drive / Dropbox)")

    submitted = st.form_submit_button("🚀 Submit Application")

st.markdown("</div>", unsafe_allow_html=True)

# ================= VALIDATION =================
if submitted:
    errors = []

    if not name.strip():
        errors.append("Name is required")
    if gender == "Select":
        errors.append("Please select gender")
    if experience == "Select":
        errors.append("Please select experience level")
    if not location.strip():
        errors.append("Location is required")
    if not industry.strip():
        errors.append("Industry is required")

    if errors:
        for e in errors:
            st.error(e)
    else:
        st.success("✅ Application submitted successfully!")
        st.info("We will contact you if shortlisted.")

        # TEMPORARY PREVIEW (for testing)
        st.markdown("### 📄 Submitted Data Preview")
        st.json({
            "name": name,
            "age": age,
            "gender": gender,
            "location": location,
            "industry": industry,
            "experience": experience,
            "expected_salary": salary,
            "resume": resume_link,
            "submitted_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
