from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
import joblib


# =====================================================
# LOAD MODEL AND SCALER
# =====================================================

model = joblib.load("loan_approval_model.pkl")
scaler = joblib.load("loan_approval_scaler.pkl")


# =====================================================
# FASTAPI APP
# =====================================================

app = FastAPI(
    title="Loan Approval Prediction API",
    description="Predict whether a loan application will be approved.",
    version="1.0.0"
)


# =====================================================
# INPUT SCHEMA
# =====================================================

class LoanInput(BaseModel):

    Gender: str
    Education_Level: int

    Employment_Status: str
    Marital_Status: str

    Applicant_Income: float
    Coapplicant_Income: float
    Loan_Amount: float
    Loan_Term: float

    Credit_Score: float
    DTI_Ratio: float
    Savings: float

    Loan_Purpose: str
    Property_Area: str
    Employer_Category: str


# =====================================================
# HOME
# =====================================================

@app.get("/")
def home():

    return {
        "message": "Loan Approval Prediction API is running",
        "docs": "/docs"
    }


# =====================================================
# PREDICT
# =====================================================

@app.post("/predict")
def predict_loan(data: LoanInput):

    # Convert input to DataFrame
    input_data = pd.DataFrame([
        data.model_dump()
    ])


    # =================================================
    # FEATURE ENGINEERING
    # =================================================

    input_data["DTI_Ratio_sq"] = (
        input_data["DTI_Ratio"] ** 2
    )

    input_data["Credit_Score_sq"] = (
        input_data["Credit_Score"] ** 2
    )


    # Remove original features
    input_data = input_data.drop(
        columns=[
            "Credit_Score",
            "DTI_Ratio"
        ]
    )


    # =================================================
    # ONE-HOT ENCODING
    # =================================================

    categorical_cols = [
        "Employment_Status",
        "Marital_Status",
        "Loan_Purpose",
        "Property_Area",
        "Gender",
        "Employer_Category"
    ]


    input_data = pd.get_dummies(
        input_data,
        columns=categorical_cols,
        drop_first=True
    )


    # =================================================
    # MATCH TRAINING COLUMNS
    # =================================================

    if hasattr(model, "feature_names_in_"):

        input_data = input_data.reindex(
            columns=model.feature_names_in_,
            fill_value=0
        )


    # =================================================
    # SCALE DATA
    # =================================================

    input_scaled = scaler.transform(input_data)


    # =================================================
    # PREDICTION
    # =================================================

    prediction = model.predict(input_scaled)[0]


    # =================================================
    # PROBABILITY
    # =================================================

    probability = model.predict_proba(
        input_scaled
    )[0][1]


    # =================================================
    # RESULT
    # =================================================

    if prediction == 1:

        result = "Loan Approved"

    else:

        result = "Loan Not Approved"


    return {
        "prediction": int(prediction),
        "result": result,
        "approval_probability": round(
            float(probability) * 100,
            2
        )
    }