
from flask import Flask, request, jsonify
from datetime import datetime
import numpy as np
import joblib
import pandas as pd
from typing import Dict, Any
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

class MentalHealthAPI:
    """Mental Health Risk Assessment API"""
    
    def __init__(self):
        self.models = self.load_models()
        logger.info("Mental Health API initialized")
    
    def load_models(self):
        """Load trained models"""
        try:
            models = {}
            # Load your actual models here
            # models['risk_model'] = joblib.load('models/best_risk_model.pkl')
            # models['nlp_model'] = joblib.load('models/text_risk_model.pkl')
            logger.info("Models loaded successfully")
            return models
        except Exception as e:
            logger.warning(f"Models not loaded, using demo mode: {e}")
            return {'demo_mode': True}
    
    def predict_risk(self, patient_data: Dict[str, Any]) -> Dict[str, Any]:
        """Predict mental health risk"""
        try:
            # Extract features
            features = self.extract_features(patient_data)
            
            # Calculate risk score (simplified for demo)
            risk_score = self.calculate_risk_score(features)
            
            # Generate response
            return {
                'risk_score': risk_score,
                'risk_category': self.categorize_risk(risk_score),
                'confidence': 0.85,
                'recommendations': self.generate_recommendations(risk_score),
                'timestamp': datetime.now().isoformat(),
                'model_version': '1.0'
            }
            
        except Exception as e:
            logger.error(f"Prediction error: {e}")
            return {'error': str(e), 'risk_score': 0.5, 'risk_category': 'Unknown'}
    
    def extract_features(self, patient_data: Dict[str, Any]) -> Dict[str, float]:
        """Extract and calculate features"""
        employment_risk = {"Employed": 0, "Unemployed": 2, "Disabled": 3, "Student": 1, "Retired": 1}
        education_risk = {"High School": 1, "College": 0, "Graduate": 0, "Other": 1}
        
        employment = patient_data.get('employment', 'Employed')
        education = patient_data.get('education', 'College')
        
        social_risk = employment_risk.get(employment, 1) + education_risk.get(education, 0)
        
        return {
            'phq9_score': patient_data.get('phq9_score', 0),
            'gad7_score': patient_data.get('gad7_score', 0),
            'social_risk': social_risk,
            'age': patient_data.get('age', 45),
            'composite_score': patient_data.get('phq9_score', 0) * 0.6 + patient_data.get('gad7_score', 0) * 0.4
        }
    
    def calculate_risk_score(self, features: Dict[str, float]) -> float:
        """Calculate risk score from features"""
        risk_score = (
            features['phq9_score'] / 27 * 0.4 +
            features['gad7_score'] / 21 * 0.3 +
            features['social_risk'] / 5 * 0.2 +
            min(features['age'] / 100, 1) * 0.1
        )
        return min(0.95, max(0.05, risk_score))
    
    def categorize_risk(self, risk_score: float) -> str:
        """Categorize risk score"""
        if risk_score < 0.3:
            return 'Low Risk'
        elif risk_score < 0.6:
            return 'Moderate Risk'
        elif risk_score < 0.8:
            return 'High Risk'
        else:
            return 'Very High Risk'
    
    def generate_recommendations(self, risk_score: float) -> list:
        """Generate clinical recommendations based on risk"""
        if risk_score >= 0.8:
            return [
                "Immediate clinical assessment required",
                "Consider crisis intervention services",
                "Frequent monitoring recommended",
                "Safety planning with patient"
            ]
        elif risk_score >= 0.6:
            return [
                "Schedule urgent follow-up within 48 hours",
                "Increase therapy session frequency",
                "Consider medication evaluation",
                "Develop crisis management plan"
            ]
        elif risk_score >= 0.3:
            return [
                "Regular follow-up in 1-2 weeks",
                "Continue current treatment plan",
                "Monitor symptom progression",
                "Provide coping strategy resources"
            ]
        else:
            return [
                "Routine monitoring",
                "Maintain current support systems",
                "Preventive mental health education",
                "Regular check-ins"
            ]

# Initialize API
api_handler = MentalHealthAPI()

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'version': '1.0'
    })

@app.route('/predict', methods=['POST'])
def predict():
    """Risk prediction endpoint"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No JSON data provided'}), 400
        
        # Validate required fields
        required_fields = ['phq9_score', 'gad7_score']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        # Make prediction
        prediction = api_handler.predict_risk(data)
        
        logger.info(f"Prediction made: {prediction['risk_category']}")
        
        return jsonify(prediction)
        
    except Exception as e:
        logger.error(f"Prediction endpoint error: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/batch_predict', methods=['POST'])
def batch_predict():
    """Batch prediction endpoint"""
    try:
        data = request.get_json()
        
        if not data or 'patients' not in data:
            return jsonify({'error': 'No patients data provided'}), 400
        
        predictions = []
        for patient in data['patients']:
            prediction = api_handler.predict_risk(patient)
            predictions.append({
                'patient_id': patient.get('patient_id', 'unknown'),
                **prediction
            })
        
        return jsonify({
            'predictions': predictions,
            'total_patients': len(predictions),
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Batch prediction error: {e}")
        return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
