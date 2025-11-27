# i-lit-Insight-Map: # 🧠 Mental Health Risk Stratification System

An **AI-powered clinical decision support tool** for mental health risk assessment. It predicts **Low**, **Moderate**, or **High risk** using machine learning, NLP, and survival analysis, helping clinicians provide timely, evidence-based interventions.

---

## 🚀 Live Demo
- **Streamlit App:** [Open in Streamlit](https://i-lit-insight-map-5chrh336kg4m6uz9cod7ef.streamlit.app/)  
---

## 📌 Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Demo](#demo)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Results](#results)
- [Deployment](#deployment)
- [Contributing](#contributing)
- [License](#license)
- [Disclaimer](#disclaimer)

---

## 📖 Overview
The system integrates:

- **Clinical scores**: PHQ-9, GAD-7  
- **Demographics & social factors**  
- **Clinical notes** via NLP  
- **Survival analysis** for longitudinal risk  

Built during the **PLP Academy AI for Software Engineering course**, it demonstrates end-to-end AI application for clinical decision support.

---

## ✨ Features

### 🔹 Risk Assessment
- Real-time mental health risk scoring  
- Confidence intervals for predictions  
- Clinically validated inputs  

### 🤖 Machine Learning & NLP
- Random Forest, Gradient Boosting, Logistic Regression  
- NLP for clinical note sentiment & topic modeling  
- Kaplan-Meier and Cox survival models  

### 💻 User Interface
- Streamlit web dashboard  
- REST API for EHR integration  
- Downloadable assessment reports  

---

## 🎥 Demo

### Web App
[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](YOUR_STREAMLIT_URL_HERE)

### Sample Risk Cases
| Low Risk | Moderate Risk | High Risk |
|----------|---------------|-----------|
| PHQ-9: 4 | PHQ-9: 12 | PHQ-9: 22 |
| GAD-7: 3 | GAD-7: 10 | GAD-7: 18 |
| Employed | Unemployed | Disabled |
| **Low Risk** | **Moderate Risk** | **High Risk** |

---

## 🛠️ Installation

### 1️⃣ Clone the repo
```bash
git clone https://github.com/yourusername/mental-health-risk.git
cd mental-health-risk
2️⃣ Create virtual environment
python -m venv mental_env
source mental_env/bin/activate       # Windows: mental_env\Scripts\activate
3️⃣ Install dependencies
pip install -r requirements.txt

4️⃣ Run the Streamlit app
cd app
streamlit run mental_health_app.py
🧪 Usage
Web App

Open browser: http://localhost:8501

Enter demographics and PHQ-9/GAD-7 scores

Optionally input clinical notes

Click “Assess Mental Health Risk”

📁 Project Structure
mental-health-risk/
├── app/                   # Streamlit web app
│   └── mental_health_app.py
├── api/                   # Flask API
│   └── app.py
├── src/                   # ML & NLP utilities
│   ├── feature_engineer.py
│   └── data_loader.py
├── models/                # Saved models
├── data/
│   ├── raw/               # Synthetic raw data
│   └── processed/         # Processed data
├── notebooks/             # Jupyter analysis
├── requirements.txt       # Python dependencies
├── README.md
└── ETHICS.md              # Ethical framework & guidelines

📊 Results
Model	AUC	Accuracy	Precision	Recall
Random Forest	0.89	0.85	0.83	0.82
Gradient Boosting	0.87	0.83	0.81	0.80
Logistic Regression	0.85	0.81	0.79	0.78

Key Insights:

PHQ-9 & GAD-7 are strongest predictors

Clinical note sentiment correlates with risk (r = -0.72)

Survival analysis shows clear stratification of risk groups

🌐 Deployment
Streamlit Community Cloud

Push repo to GitHub

Visit share.streamlit.io

Select repo and main file: app/mental_health_app.py

Click Deploy

Render (Optional)

Build Command: pip install -r requirements.txt

Start Command: streamlit run app/mental_health_app.py --server.port $PORT --server.address 0.0.0.0

🤝 Contributing

Pull requests welcome

For major changes, open an issue first

Ensure tests pass before merging

📄 License

MIT License — see LICENSE file.

⚠️ Disclaimer

This tool is for clinical decision support only.
It does NOT replace professional medical judgment.
For mental health crises, contact emergency services immediately.