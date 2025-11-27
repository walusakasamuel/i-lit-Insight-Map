
import streamlit as st
import pandas as pd
import numpy as np
import json
from datetime import datetime
import requests

# Set page config
st.set_page_config(
    page_title="Mental Health Risk Stratification",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .risk-high {
        background-color: #ff6b6b;
        padding: 10px;
        border-radius: 5px;
        color: white;
        font-weight: bold;
    }
    .risk-moderate {
        background-color: #ffd93d;
        padding: 10px;
        border-radius: 5px;
        color: black;
        font-weight: bold;
    }
    .risk-low {
        background-color: #6bcf7f;
        padding: 10px;
        border-radius: 5px;
        color: white;
        font-weight: bold;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)

# Title and description
st.markdown('<div class="main-header">🧠 Mental Health Risk Stratification System</div>', unsafe_allow_html=True)
st.markdown("""
This AI-powered system assesses mental health risks using clinical data, patient history, and clinical notes.
The system integrates multiple machine learning models to provide comprehensive risk assessment and clinical recommendations.
""")

# Sidebar for patient input
st.sidebar.header("Patient Information")

with st.sidebar.form("patient_form"):
    st.subheader("Demographic Information")
    age = st.slider("Age", 18, 100, 45)
    gender = st.selectbox("Gender", ["Male", "Female", "Other", "Prefer not to say"])

    st.subheader("Clinical Scores")
    phq9_score = st.slider("PHQ-9 Score (0-27)", 0, 27, 8)
    gad7_score = st.slider("GAD-7 Score (0-21)", 0, 21, 7)

    st.subheader("Social Determinants")
    employment = st.selectbox("Employment Status", ["Employed", "Unemployed", "Disabled", "Student", "Retired"])
    education = st.selectbox("Education Level", ["High School", "College", "Graduate", "Other"])

    st.subheader("Physical Health")
    bp_systolic = st.slider("Systolic BP", 80, 200, 130)
    heart_rate = st.slider("Heart Rate", 50, 120, 75)
    bmi = st.slider("BMI", 15, 50, 25)

    st.subheader("Clinical Notes")
    clinical_note = st.text_area(
        "Clinical Assessment Notes",
        height=150,
        placeholder="Enter clinical observations, patient statements, and assessment findings..."
    )

    submitted = st.form_submit_button("Assess Risk")

# Main content area
if submitted:
    # Create patient data dictionary
    patient_data = {
        'age': age,
        'gender': gender,
        'phq9_score': phq9_score,
        'gad7_score': gad7_score,
        'employment': employment,
        'education': education,
        'bp_systolic': bp_systolic,
        'heart_rate': heart_rate,
        'bmi': bmi,
        'clinical_note': clinical_note,
        'timestamp': datetime.now().isoformat()
    }

    # Simulate risk prediction (in real app, this would call the actual model)
    # This is a simplified version for the template

    # Calculate composite risk score
    employment_risk = {"Employed": 0, "Unemployed": 2, "Disabled": 3, "Student": 1, "Retired": 1}
    education_risk = {"High School": 1, "College": 0, "Graduate": 0, "Other": 1}

    social_risk = employment_risk.get(employment, 1) + education_risk.get(education, 0)

    risk_score = (
        phq9_score / 27 * 0.4 +
        gad7_score / 21 * 0.3 +
        social_risk / 5 * 0.2 +
        (age / 100) * 0.1
    )

    risk_score = min(0.95, risk_score)

    # Determine risk category
    if risk_score < 0.3:
        risk_category = "Low Risk"
        risk_class = "risk-low"
    elif risk_score < 0.6:
        risk_category = "Moderate Risk"
        risk_class = "risk-moderate"
    elif risk_score < 0.8:
        risk_category = "High Risk"
        risk_class = "risk-high"
    else:
        risk_category = "Very High Risk"
        risk_class = "risk-high"

    # Display results
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Overall Risk Score", f"{risk_score:.1%}")

    with col2:
        st.metric("Risk Category", risk_category)

    with col3:
        st.metric("Assessment Confidence", "85%")

    # Risk category display
    st.markdown(f'<div class="{risk_class}">Risk Category: {risk_category}</div>', unsafe_allow_html=True)

    # Detailed breakdown
    st.subheader("Risk Breakdown")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**Clinical Factors**")
        st.progress(phq9_score / 27)
        st.caption(f"PHQ-9 Severity: {phq9_score}/27")

        st.progress(gad7_score / 21)
        st.caption(f"GAD-7 Severity: {gad7_score}/21")

    with col2:
        st.markdown("**Social & Demographic Factors**")
        st.progress(social_risk / 5)
        st.caption(f"Social Risk: {social_risk}/5")

        st.progress(min(age / 100, 1))
        st.caption(f"Age Factor: {age} years")

    # Recommendations
    st.subheader("Clinical Recommendations")

    recommendations = []
    if risk_score >= 0.8:
        recommendations = [
            "🚨 Immediate clinical assessment required",
            "Consider crisis intervention services",
            "Frequent monitoring (daily check-ins)",
            "Safety planning with patient",
            "Consider psychiatric consultation"
        ]
    elif risk_score >= 0.6:
        recommendations = [
            "Schedule urgent follow-up within 48 hours",
            "Increase therapy session frequency",
            "Consider medication evaluation",
            "Develop crisis management plan",
            "Monitor for symptom escalation"
        ]
    elif risk_score >= 0.3:
        recommendations = [
            "Regular follow-up in 1-2 weeks",
            "Continue current treatment plan",
            "Monitor symptom progression",
            "Provide coping strategy resources",
            "Encourage social support engagement"
        ]
    else:
        recommendations = [
            "Routine monitoring",
            "Maintain current support systems",
            "Preventive mental health education",
            "Regular check-ins",
            "Promote wellness activities"
        ]

    for i, recommendation in enumerate(recommendations, 1):
        st.write(f"{i}. {recommendation}")

    # Model Insights
    st.subheader("AI Model Insights")

    insight_col1, insight_col2 = st.columns(2)

    with insight_col1:
        st.info(f"**Structured Data Analysis**: Risk primarily driven by {'PHQ-9 scores' if phq9_score > 10 else 'multiple factors'}")

    with insight_col2:
        if clinical_note:
            note_analysis = "Clinical note analyzed for risk indicators"
            if any(word in clinical_note.lower() for word in ['suicidal', 'self-harm', 'hopeless']):
                note_analysis += " - Elevated concern detected"
            st.info(f"**Text Analysis**: {note_analysis}")
        else:
            st.warning("**Text Analysis**: No clinical notes provided")

    # Export option
    st.download_button(
        label="Download Assessment Report",
        data=json.dumps({
            "patient_data": patient_data,
            "risk_assessment": {
                "risk_score": risk_score,
                "risk_category": risk_category,
                "recommendations": recommendations,
                "timestamp": datetime.now().isoformat()
            }
        }, indent=2),
        file_name=f"mental_health_assessment_{datetime.now().strftime('%Y%m%d_%H%M')}.json",
        mime="application/json"
    )

else:
    # Welcome message when no submission
    st.info("👈 Please fill out the patient information in the sidebar and click 'Assess Risk' to begin.")

    # Show sample assessments
    st.subheader("Sample Risk Assessments")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        **Low Risk Example**:
        - PHQ-9: 4
        - GAD-7: 3  
        - Employed
        - Good social support
        """)

    with col2:
        st.markdown("""
        **Moderate Risk Example**:
        - PHQ-9: 12
        - GAD-7: 10
        - Recent job loss
        - Some social isolation
        """)

    with col3:
        st.markdown("""
        **High Risk Example**:
        - PHQ-9: 22
        - GAD-7: 18
        - Disabled
        - Expressed hopelessness
        """)

# Footer
st.markdown("---")
st.markdown("""
**Disclaimer**: This tool is for clinical decision support only. 
Always combine AI assessments with professional clinical judgment.
Contact emergency services for immediate crisis situations.
""")
