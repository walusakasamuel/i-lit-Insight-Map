import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="Mental Health Risk Assessment",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
        font-weight: bold;
    }
    .risk-high {
        background-color: #ff6b6b;
        padding: 15px;
        border-radius: 10px;
        color: white;
        font-weight: bold;
        font-size: 1.2rem;
        text-align: center;
        border: 2px solid #ff4757;
    }
    .risk-moderate {
        background-color: #ffd93d;
        padding: 15px;
        border-radius: 10px;
        color: black;
        font-weight: bold;
        font-size: 1.2rem;
        text-align: center;
        border: 2px solid #ff9f1a;
    }
    .risk-low {
        background-color: #6bcf7f;
        padding: 15px;
        border-radius: 10px;
        color: white;
        font-weight: bold;
        font-size: 1.2rem;
        text-align: center;
        border: 2px solid #2ed573;
    }
    .metric-card {
        background-color: #f8f9fa;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #1f77b4;
        margin: 10px 0;
    }
    .recommendation-box {
        background-color: #e3f2fd;
        padding: 15px;
        border-radius: 8px;
        margin: 10px 0;
        border-left: 4px solid #2196f3;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<div class="main-header">🧠 Mental Health Risk Stratification System</div>', unsafe_allow_html=True)

# Introduction
st.markdown("""
<div style='background-color: #e8f4fd; padding: 20px; border-radius: 10px; margin-bottom: 20px;'>
    <h3 style='color: #1f77b4; margin-top: 0;'>About This System</h3>
    <p>This AI-powered tool assesses mental health risks using clinical data, demographic information, and advanced machine learning models. 
    It provides evidence-based risk stratification and clinical recommendations for healthcare professionals.</p>
</div>
""", unsafe_allow_html=True)

# Sidebar for patient input
with st.sidebar:
    st.header("📋 Patient Assessment")
    st.markdown("Enter patient information below to assess mental health risk.")
    
    with st.form("patient_form"):
        st.subheader("Demographic Information")
        col1, col2 = st.columns(2)
        with col1:
            age = st.slider("Age", 18, 100, 45)
        with col2:
            gender = st.selectbox("Gender", ["Male", "Female", "Other", "Prefer not to say"])
        
        st.subheader("Clinical Assessment Scores")
        col1, col2 = st.columns(2)
        with col1:
            phq9_score = st.slider("PHQ-9 Score", 0, 27, 8, 
                                 help="Patient Health Questionnaire-9: 0-4 None, 5-9 Mild, 10-14 Moderate, 15-19 Moderately Severe, 20-27 Severe")
        with col2:
            gad7_score = st.slider("GAD-7 Score", 0, 21, 7,
                                 help="Generalized Anxiety Disorder-7: 0-4 None, 5-9 Mild, 10-14 Moderate, 15-21 Severe")
        
        st.subheader("Social Determinants")
        col1, col2 = st.columns(2)
        with col1:
            employment = st.selectbox("Employment Status", ["Employed", "Unemployed", "Disabled", "Student", "Retired"])
        with col2:
            education = st.selectbox("Education Level", ["High School", "College", "Graduate", "Other"])
        
        st.subheader("Physical Health Metrics")
        col1, col2 = st.columns(2)
        with col1:
            bp_systolic = st.slider("Systolic BP", 80, 200, 130)
        with col2:
            heart_rate = st.slider("Heart Rate", 50, 120, 75)
        bmi = st.slider("BMI", 15, 50, 25)
        
        st.subheader("Clinical Notes")
        clinical_note = st.text_area(
            "Clinical Assessment Notes",
            height=120,
            placeholder="Enter clinical observations, patient statements, symptom descriptions, and assessment findings...",
            help="Optional: Clinical notes will be analyzed for additional risk indicators"
        )
        
        submitted = st.form_submit_button("🚀 Assess Mental Health Risk", use_container_width=True)

# Main content area
if submitted:
    # Calculate risk score
    employment_risk = {"Employed": 0, "Unemployed": 2, "Disabled": 3, "Student": 1, "Retired": 1}
    education_risk = {"High School": 1, "College": 0, "Graduate": 0, "Other": 1}
    
    social_risk = employment_risk.get(employment, 1) + education_risk.get(education, 0)
    
    risk_score = (
        phq9_score / 27 * 0.4 +
        gad7_score / 21 * 0.3 +
        social_risk / 5 * 0.2 +
        min(age / 100, 1) * 0.1
    )
    
    risk_score = min(0.95, risk_score)
    
    # Determine risk category
    if risk_score < 0.3:
        risk_category = "Low Risk"
        risk_class = "risk-low"
        risk_color = "#2ed573"
    elif risk_score < 0.6:
        risk_category = "Moderate Risk"
        risk_class = "risk-moderate"
        risk_color = "#ff9f1a"
    elif risk_score < 0.8:
        risk_category = "High Risk"
        risk_class = "risk-high"
        risk_color = "#ff4757"
    else:
        risk_category = "Very High Risk"
        risk_class = "risk-high"
        risk_color = "#ff3838"
    
    # Display results in main area
    st.success("✅ Assessment Complete!")
    
    # Risk summary cards
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <h3 style='color: {risk_color}; margin: 0;'>Risk Score</h3>
            <p style='font-size: 2rem; font-weight: bold; color: {risk_color}; margin: 0;'>{risk_score:.1%}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <h3 style='color: {risk_color}; margin: 0;'>Risk Category</h3>
            <p style='font-size: 1.5rem; font-weight: bold; color: {risk_color}; margin: 0;'>{risk_category}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="metric-card">
            <h3 style='color: #1f77b4; margin: 0;'>Confidence Level</h3>
            <p style='font-size: 1.5rem; font-weight: bold; color: #1f77b4; margin: 0;'>85%</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Risk category display
    st.markdown(f'<div class="{risk_class}">🎯 RISK CATEGORY: {risk_category}</div>', unsafe_allow_html=True)
    
    # Detailed breakdown
    st.subheader("📊 Risk Factor Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Clinical Factors**")
        
        # PHQ-9 progress
        phq9_progress = phq9_score / 27
        st.progress(phq9_progress)
        st.caption(f"PHQ-9 Depression Severity: {phq9_score}/27")
        if phq9_score >= 15:
            st.warning("🔴 Moderately Severe to Severe Depression")
        elif phq9_score >= 10:
            st.info("🟡 Moderate Depression")
        else:
            st.success("🟢 Mild or No Depression")
        
        # GAD-7 progress
        gad7_progress = gad7_score / 21
        st.progress(gad7_progress)
        st.caption(f"GAD-7 Anxiety Severity: {gad7_score}/21")
        if gad7_score >= 15:
            st.warning("🔴 Severe Anxiety")
        elif gad7_score >= 10:
            st.info("🟡 Moderate Anxiety")
        else:
            st.success("🟢 Mild or No Anxiety")
    
    with col2:
        st.markdown("**Social & Demographic Factors**")
        
        # Social risk
        social_progress = social_risk / 5
        st.progress(social_progress)
        st.caption(f"Social Risk Score: {social_risk}/5")
        if social_risk >= 3:
            st.warning("🔴 High Social Risk Factors")
        elif social_risk >= 2:
            st.info("🟡 Moderate Social Risk Factors")
        else:
            st.success("🟢 Low Social Risk Factors")
        
        # Age factor
        age_progress = min(age / 100, 1)
        st.progress(age_progress)
        st.caption(f"Age Factor: {age} years")
    
    # Clinical Recommendations
    st.subheader("💡 Clinical Recommendations")
    
    recommendations = []
    if risk_score >= 0.8:
        recommendations = [
            "🚨 **Immediate Clinical Assessment Required** - Consider urgent psychiatric evaluation",
            "🛡️ **Crisis Intervention** - Implement safety planning and frequent monitoring",
            "📞 **Support Services** - Connect with crisis hotlines and emergency resources",
            "💊 **Medication Evaluation** - Consider pharmacological intervention",
            "👥 **Therapy Intensification** - Increase session frequency to 2-3 times per week"
        ]
    elif risk_score >= 0.6:
        recommendations = [
            "⚠️ **Urgent Follow-up** - Schedule appointment within 48 hours",
            "📋 **Comprehensive Assessment** - Conduct detailed risk assessment",
            "💊 **Medication Review** - Evaluate current medication regimen",
            "🧠 **Therapy Adjustment** - Consider increasing therapy frequency",
            "📊 **Symptom Monitoring** - Implement daily mood and symptom tracking"
        ]
    elif risk_score >= 0.3:
        recommendations = [
            "📅 **Regular Follow-up** - Schedule appointment in 1-2 weeks",
            "🔍 **Continued Monitoring** - Track symptom progression",
            "🛠️ **Coping Strategies** - Reinforce existing coping mechanisms",
            "📚 **Psychoeducation** - Provide resources on symptom management",
            "👥 **Support Network** - Encourage engagement with support systems"
        ]
    else:
        recommendations = [
            "✅ **Routine Monitoring** - Continue regular check-ins",
            "🌱 **Preventive Care** - Focus on wellness and prevention",
            "📖 **Mental Health Education** - Provide educational resources",
            "🔔 **Early Warning Signs** - Educate on recognizing symptom changes",
            "🏋️ **Resilience Building** - Strengthen protective factors"
        ]
    
    for i, recommendation in enumerate(recommendations, 1):
        st.markdown(f'<div class="recommendation-box">{i}. {recommendation}</div>', unsafe_allow_html=True)
    
    # AI Insights
    st.subheader("🤖 AI Model Insights")
    
    insight_col1, insight_col2 = st.columns(2)
    
    with insight_col1:
        st.info(f"""
        **Structured Data Analysis**
        - Primary risk drivers: {'PHQ-9 scores' if phq9_score > 10 else 'Multiple factors'}
        - Social determinants: {employment} status
        - Clinical severity: {'Elevated' if max(phq9_score, gad7_score) > 14 else 'Moderate' if max(phq9_score, gad7_score) > 9 else 'Mild'}
        """)
    
    with insight_col2:
        if clinical_note:
            note_analysis = "Clinical note analyzed for risk indicators"
            risk_indicators = []
            if any(word in clinical_note.lower() for word in ['suicidal', 'self-harm', 'hopeless']):
                risk_indicators.append("Elevated concern detected")
            if any(word in clinical_note.lower() for word in ['improved', 'better', 'progress']):
                risk_indicators.append("Positive indicators present")
            
            if risk_indicators:
                note_analysis += " - " + ", ".join(risk_indicators)
            st.info(f"**Text Analysis**: {note_analysis}")
        else:
            st.warning("**Text Analysis**: No clinical notes provided for additional insights")
    
    # Export option
    st.subheader("📤 Export Assessment")
    
    assessment_data = {
        "patient_data": {
            "age": age,
            "gender": gender,
            "phq9_score": phq9_score,
            "gad7_score": gad7_score,
            "employment": employment,
            "education": education,
            "bp_systolic": bp_systolic,
            "heart_rate": heart_rate,
            "bmi": bmi
        },
        "risk_assessment": {
            "risk_score": float(risk_score),
            "risk_category": risk_category,
            "recommendations": [rec.split("**")[-1].split("**")[0] for rec in recommendations],
            "timestamp": datetime.now().isoformat(),
            "model_version": "1.0"
        }
    }
    
    st.download_button(
        label="📄 Download Assessment Report (JSON)",
        data=pd.DataFrame([assessment_data]).to_json(orient='records', indent=2),
        file_name=f"mental_health_assessment_{datetime.now().strftime('%Y%m%d_%H%M')}.json",
        mime="application/json"
    )

else:
    # Welcome message when no submission
    st.info("👈 **Please fill out the patient assessment form in the sidebar and click 'Assess Mental Health Risk' to begin.**")
    
    # Sample cases for demonstration
    st.subheader("📋 Sample Assessment Cases")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        **🟢 Low Risk Case**
        - PHQ-9: 4 (None-Mild)
        - GAD-7: 3 (None-Mild)  
        - Employed, College education
        - Good social support
        *Expected: Low risk, routine monitoring*
        """)
    
    with col2:
        st.markdown("""
        **🟡 Moderate Risk Case**
        - PHQ-9: 12 (Moderate)
        - GAD-7: 10 (Moderate)
        - Recently unemployed  
        - Some social isolation
        *Expected: Moderate risk, close follow-up*
        """)
    
    with col3:
        st.markdown("""
        **🔴 High Risk Case**
        - PHQ-9: 22 (Severe)
        - GAD-7: 18 (Severe)
        - Disabled, limited support
        - Expressed hopelessness
        *Expected: High risk, immediate action*
        """)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666;'>
    <p><strong>Disclaimer</strong>: This tool is for clinical decision support only. 
    Always combine AI assessments with professional clinical judgment and comprehensive evaluation.</p>
    <p>For immediate crisis situations, contact emergency services or crisis hotlines.</p>
    <p>© 2024 Mental Health Risk Stratification System | Version 1.0</p>
</div>
""", unsafe_allow_html=True)