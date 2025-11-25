import pandas as pd
import numpy as np
from sklearn.datasets import make_classification
import warnings
warnings.filterwarnings('ignore')

def generate_synthetic_mh_data(n_samples=1000):
    """
    Generate synthetic mental health dataset for i-Lit Insight Map
    mimicking real clinical data with realistic risk patterns
    """
    np.random.seed(42)
    
    # Basic demographics
    age = np.random.normal(45, 15, n_samples).astype(int)
    gender = np.random.choice(['Male', 'Female', 'Other'], n_samples, p=[0.45, 0.50, 0.05])
    
    # Clinical scores (PHQ-9, GAD-7 common in mental health)
    phq9 = np.random.poisson(8, n_samples)  # PHQ-9 scores (0-27)
    gad7 = np.random.poisson(7, n_samples)   # GAD-7 scores (0-21)
    
    # Vital signs with some correlation to mental health
    bp_systolic = np.random.normal(130, 20, n_samples)
    heart_rate = np.random.normal(75, 15, n_samples)
    
    # Lab values (simplified)
    bmi = np.random.normal(28, 6, n_samples)
    
    # Social determinants
    education = np.random.choice(['High School', 'College', 'Graduate'], n_samples)
    employment = np.random.choice(['Employed', 'Unemployed', 'Disabled'], n_samples)
    
    # Create features matrix
    features = pd.DataFrame({
        'age': age,
        'gender': gender,
        'phq9_score': phq9,
        'gad7_score': gad7,
        'bp_systolic': bp_systolic,
        'heart_rate': heart_rate,
        'bmi': bmi,
        'education': education,
        'employment': employment
    })
    
    # Generate synthetic outcomes with realistic relationships
    # Higher PHQ-9, older age, unemployment increase risk
    risk_score = (
        0.1 * (phq9 - 8) + 
        0.05 * (gad7 - 7) + 
        0.02 * (age - 45) +
        0.3 * (employment == 'Unemployed') +
        0.2 * (employment == 'Disabled') +
        np.random.normal(0, 0.5, n_samples)
    )
    
    # Create binary outcome (high risk vs low risk)
    high_risk = (risk_score > 0.5).astype(int)
    
    # Add survival data (time to event)
    time_to_event = np.random.exponential(365, n_samples)  # days
    # Censor some observations
    censored = np.random.binomial(1, 0.3, n_samples)
    event_occurred = high_risk & (1 - censored)
    
    features['high_risk'] = high_risk
    features['time_to_event'] = time_to_event
    features['event_occurred'] = event_occurred
    features['data_source'] = 'i-Lit_Synthetic_v1.0'
    features['generation_date'] = pd.Timestamp.now().strftime('%Y-%m-%d')
    
    return features

# Generate and save data
if __name__ == "__main__":
    data = generate_synthetic_mh_data(1500)
    data.to_csv('data/raw/synthetic_mh_data.csv', index=False)
    print("Synthetic data generated with shape:", data.shape)
    print("\nRisk distribution:")
    print(data['high_risk'].value_counts())
    print("\nFirst 5 rows:")
    print(data.head())