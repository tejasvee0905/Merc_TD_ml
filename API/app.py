from flask import Flask, request, jsonify, render_template
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import FunctionTransformer
from sklearn.linear_model import LogisticRegression
from sklearn.base import BaseEstimator, TransformerMixin

app = Flask(__name__)

# # Custom validator class
# class DataSetValidator(BaseEstimator, TransformerMixin):
#     def fit(self, X, y=None):
#         return self

#     def transform(self, X):
#         if ((X["Credit_History"] > 0) & (X["Credit_History"] < 3)).any():
#             raise ValueError("Credit_History should be 0 or 1")
#         if (X["ApplicantIncome"] < 0).any():
#             raise ValueError("ApplicantIncome cannot be negative")
#         return X

# Train model on startup
def train_model():
    print("Loading and training model...")
    
    # Load data
    df = pd.read_csv("Loan_dataset.csv")
    df = df.dropna(subset=["Loan_Status"])
    
    X = df.drop(columns=["Loan_Status", "Loan_ID", "Gender", "Dependents"])
    y = df["Loan_Status"].map({"Y": 1, "N": 0})
    
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    
    # Define columns
    log_cols = ["ApplicantIncome", "CoapplicantIncome"]
    num_cols = ["LoanAmount", "Credit_History", "Loan_Amount_Term"]
    cat_cols = ["Married", "Self_Employed", "Education", "Property_Area"]
    
    # Create pipelines
    numeric_pipeline = Pipeline([
        ("imputer", SimpleImputer(strategy="median")),
        ("scaler", StandardScaler())
    ])
    
    log_numeric_pipeline = Pipeline([
        ("imputer", SimpleImputer(strategy="median")),
        ("log", FunctionTransformer(np.log1p, validate=False)),
        ("scaler", StandardScaler())
    ])
    
    categorical_pipeline = Pipeline([
        ("imputer", SimpleImputer(strategy="most_frequent")),
        ("encoder", OneHotEncoder(handle_unknown="ignore"))
    ])
    
    preprocessor = ColumnTransformer([
        ("log_num", log_numeric_pipeline, log_cols),
        ("num", numeric_pipeline, num_cols),
        ("cat", categorical_pipeline, cat_cols)
    ])
    
    model_pipeline = Pipeline([
        # ("dataset_validation", DataSetValidator()),
        ("preprocess", preprocessor),
        ("model", LogisticRegression(class_weight="balanced"))
    ])
    
    # Train the model
    model_pipeline.fit(X_train, y_train)
    
    print("Model trained successfully!")
    return model_pipeline

# Train model
model = train_model()

@app.route('/')
def home():
    """Serve the HTML page"""
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    """Handle prediction requests"""
    try:
        # Get JSON data from request
        data = request.get_json()
        
        # Convert to DataFrame
        input_df = pd.DataFrame([{
            "Married": data['married'],
            "Education": data['education'],
            "Self_Employed": data['selfEmployed'],
            "ApplicantIncome": float(data['applicantIncome']),
            "CoapplicantIncome": float(data['coapplicantIncome']),
            "LoanAmount": float(data['loanAmount']),
            "Loan_Amount_Term": float(data['loanTerm']),
            "Credit_History": float(data['creditHistory']),
            "Property_Area": data['propertyArea']
        }])
        
        # Make prediction
        prediction = model.predict(input_df)[0]
        probability = model.predict_proba(input_df)[0]
        
        # Prepare response
        result = {
            "success": True,
            "prediction": "Approved ✓" if prediction == 1 else "Rejected ✗",
            "status": "approved" if prediction == 1 else "rejected",
            "probability": {
                "rejection": round(float(probability[0]) * 100, 2),
                "approval": round(float(probability[1]) * 100, 2)
            },
            "confidence": round(float(max(probability)) * 100, 2)
        }
        
        return jsonify(result), 200
        
    except ValueError as ve:
        return jsonify({"success": False, "error": str(ve)}), 400
    except Exception as e:
        return jsonify({"success": False, "error": f"Prediction failed: {str(e)}"}), 500

if __name__ == '__main__':
    print("\n" + "="*60)
    print("🚀 Loan Prediction Web App is running!")
    print("="*60)
    print("📍 URL: http://127.0.0.1:5000")
    print("="*60 + "\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
