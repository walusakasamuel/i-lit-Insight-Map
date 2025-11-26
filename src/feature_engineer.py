import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.feature_selection import f_classif
import warnings
warnings.filterwarnings('ignore')

class MentalHealthFeatureEngineer:
    """
    Feature engineering pipeline for mental health risk prediction
    Incorporates biostatistical principles
    """
    
    def __init__(self):
        self.numeric_features = None
        self.categorical_features = None
        self.preprocessor = None
        
    def create_clinical_features(self, df):
        """
        Create clinically meaningful derived features
        """
        df_engineered = df.copy()
        
        # 1. Clinical risk categories (based on established cutoffs)
        df_engineered['phq9_category'] = pd.cut(
            df['phq9_score'], 
            bins=[-1, 4, 9, 14, 19, 27],
            labels=['None', 'Mild', 'Moderate', 'Moderately Severe', 'Severe']
        )
        
        df_engineered['gad7_category'] = pd.cut(
            df['gad7_score'],
            bins=[-1, 4, 9, 14, 21],
            labels=['None', 'Mild', 'Moderate', 'Severe']
        )
        
        # 2. BMI categories (clinical standards)
        df_engineered['bmi_category'] = pd.cut(
            df['bmi'],
            bins=[0, 18.5, 25, 30, 35, 100],
            labels=['Underweight', 'Normal', 'Overweight', 'Obese', 'Extreme Obesity']
        )
        
        # 3. Age groups (epidemiological standard)
        df_engineered['age_group'] = pd.cut(
            df['age'],
            bins=[0, 25, 45, 65, 100],
            labels=['Young', 'Middle', 'Older', 'Elderly']
        )
        
        # 4. Blood pressure categories (clinical guidelines)
        df_engineered['bp_category'] = pd.cut(
            df['bp_systolic'],
            bins=[0, 120, 130, 140, 180, 300],
            labels=['Normal', 'Elevated', 'Stage1', 'Stage2', 'Crisis']
        )
        
        # 5. Composite mental health score
        df_engineered['composite_mh_score'] = (
            df['phq9_score'] * 0.6 + df['gad7_score'] * 0.4
        )
        
        # 6. Risk interactions (biologically plausible)
        df_engineered['high_phq_high_bp'] = (
            (df['phq9_score'] > 10) & (df['bp_systolic'] > 140)
        ).astype(int)
        
        # 7. Social determinant scores
        employment_risk = {'Employed': 0, 'Unemployed': 2, 'Disabled': 3}
        education_risk = {'High School': 1, 'College': 0, 'Graduate': 0}
        
        df_engineered['social_risk_score'] = (
            df['employment'].map(employment_risk) + 
            df['education'].map(education_risk)
        )
        
        return df_engineered
    
    def calculate_statistical_features(self, df):
        """
        Create statistical features that might capture complex relationships
        """
        df_stats = df.copy()
        
        # Z-scores for outlier detection
        df_stats['phq9_zscore'] = (
            (df['phq9_score'] - df['phq9_score'].mean()) / df['phq9_score'].std()
        )
        
        # Polynomial features for non-linear relationships
        df_stats['age_squared'] = df['age'] ** 2
        df_stats['phq9_squared'] = df['phq9_score'] ** 2
        
        # Interaction terms (statistically motivated)
        df_stats['age_phq_interaction'] = df['age'] * df['phq9_score']
        df_stats['bmi_hr_interaction'] = df['bmi'] * df['heart_rate']
        
        return df_stats
    
    def create_preprocessor(self, X):
        """
        Create sklearn preprocessing pipeline
        """
        # Identify feature types
        self.numeric_features = X.select_dtypes(include=['int64', 'float64']).columns.tolist()
        self.categorical_features = X.select_dtypes(include=['object', 'category']).columns.tolist()
        
        print(f"Numeric features: {self.numeric_features}")
        print(f"Categorical features: {self.categorical_features}")
        
        # Create transformers
        numeric_transformer = Pipeline(steps=[
            ('imputer', SimpleImputer(strategy='median')),
            ('scaler', StandardScaler())
        ])
        
        categorical_transformer = Pipeline(steps=[
            ('imputer', SimpleImputer(strategy='constant', fill_value='missing')),
            ('onehot', OneHotEncoder(handle_unknown='ignore', sparse_output=False))
        ])
        
        # Create preprocessor
        self.preprocessor = ColumnTransformer(
            transformers=[
                ('num', numeric_transformer, self.numeric_features),
                ('cat', categorical_transformer, self.categorical_features)
            ]
        )
        
        return self.preprocessor
    
    def fit_transform(self, df, target_column='high_risk'):
        """
        Complete feature engineering pipeline
        """
        print("Starting feature engineering...")
        
        # Step 1: Create clinical features
        df_engineered = self.create_clinical_features(df)
        print("✓ Clinical features created")
        
        # Step 2: Create statistical features
        df_engineered = self.calculate_statistical_features(df_engineered)
        print("✓ Statistical features created")
        
        # Separate features and target
        X = df_engineered.drop(columns=[target_column, 'time_to_event', 'event_occurred'], errors='ignore')
        y = df_engineered[target_column] if target_column in df_engineered.columns else None
        
        # Step 3: Create and fit preprocessor
        self.preprocessor = self.create_preprocessor(X)
        X_processed = self.preprocessor.fit_transform(X)
        print("✓ Preprocessing completed")
        
        # Get feature names after preprocessing
        numeric_names = self.numeric_features
        
        # Get onehot encoded feature names
        categorical_names = []
        onehot = self.preprocessor.named_transformers_['cat'].named_steps['onehot']
        for i, feature in enumerate(self.categorical_features):
            categories = onehot.categories_[i]
            for category in categories:
                categorical_names.append(f"{feature}_{category}")
        
        feature_names = numeric_names + categorical_names
        
        print(f"✓ Final shape: {X_processed.shape}")
        print(f"✓ Total features: {len(feature_names)}")
        
        return X_processed, y, feature_names, df_engineered

def analyze_feature_importance(X, y, feature_names):
    """
    Statistical feature importance using ANOVA F-test
    """
    from sklearn.feature_selection import f_classif
    
    f_scores, p_values = f_classif(X, y)
    
    importance_df = pd.DataFrame({
        'feature': feature_names,
        'f_score': f_scores,
        'p_value': p_values
    }).sort_values('f_score', ascending=False)
    
    return importance_df