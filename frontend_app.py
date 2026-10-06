import streamlit as st
import requests


# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="Loan Approval Prediction",
    page_icon="🏦",
    layout="centered"
)


# =====================================================
# TITLE
# =====================================================

st.title("🏦 Loan Approval Prediction")
st.write(
    "Enter applicant details to predict whether the loan "
    "will be approved or not."
)


# =====================================================
# FASTAPI URL
# =====================================================

API_URL = "http://127.0.0.1:8000/predict"


# =====================================================
# INPUT FORM
# =====================================================

with st.form("loan_form"):

    st.subheader("Applicant Information")

    gender = st.selectbox(
        "Gender",
        ["Male", "Female"]
    )

    education = st.selectbox(
        "Education Level",
        ["Graduate", "Not Graduate"]
    )

    employment = st.selectbox(
        "Employment Status",
        ["Employed", "Self-Employed", "Unemployed"]
    )

    marital = st.selectbox(
        "Marital Status",
        ["Married", "Single"]
    )

    applicant_income = st.number_input(
        "Applicant Income",
        min_value=0.0,
        value=50000.0,
        step=1000.0
    )

    coapplicant_income = st.number_input(
        "Coapplicant Income",
        min_value=0.0,
        value=0.0,
        step=1000.0
    )

    loan_amount = st.number_input(
        "Loan Amount",
        min_value=0.0,
        value=100000.0,
        step=5000.0
    )

    loan_term = st.number_input(
        "Loan Term",
        min_value=1.0,
        value=360.0,
        step=1.0
    )

    credit_score = st.number_input(
        "Credit Score",
        min_value=300.0,
        max_value=900.0,
        value=700.0,
        step=1.0
    )

    dti_ratio = st.number_input(
        "DTI Ratio",
        min_value=0.0,
        value=0.30,
        step=0.01
    )

    savings = st.number_input(
        "Savings",
        min_value=0.0,
        value=50000.0,
        step=1000.0
    )

    loan_purpose = st.selectbox(
        "Loan Purpose",
        [
            "Home",
            "Education",
            "Personal",
            "Business",
            "Car"
        ]
    )

    property_area = st.selectbox(
        "Property Area",
        [
            "Urban",
            "Semiurban",
            "Rural"
        ]
    )

    employer_category = st.selectbox(
        "Employer Category",
        [
            "Private",
            "Government",
            "Self-Employed",
            "Other"
        ]
    )


    submitted = st.form_submit_button(
        "🔍 Predict Loan Approval"
    )


# =====================================================
# SEND DATA TO FASTAPI
# =====================================================

if submitted:

    # Education encoding
    if education == "Graduate":
        education_value = 0
    else:
        education_value = 1


    payload = {

        "Gender": gender,

        "Education_Level": education_value,

        "Employment_Status": employment,

        "Marital_Status": marital,

        "Applicant_Income": applicant_income,

        "Coapplicant_Income": coapplicant_income,

        "Loan_Amount": loan_amount,

        "Loan_Term": loan_term,

        "Credit_Score": credit_score,

        "DTI_Ratio": dti_ratio,

        "Savings": savings,

        "Loan_Purpose": loan_purpose,

        "Property_Area": property_area,

        "Employer_Category": employer_category
    }


    # =================================================
    # CALL FASTAPI
    # =================================================

    try:

        response = requests.post(
            API_URL,
            json=payload,
            timeout=10
        )


        if response.status_code == 200:

            result = response.json()

            st.divider()

            st.subheader("Prediction Result")


            if result["prediction"] == 1:

                st.success(
                    "🎉 Loan Approved!"
                )

            else:

                st.error(
                    "❌ Loan Not Approved"
                )


            # Probability
            probability = result.get(
                "approval_probability"
            )


            if probability is not None:

                st.metric(
                    "Approval Probability",
                    f"{probability}%"
                )


        else:

            st.error(
                f"API Error: {response.status_code}"
            )

            st.write(response.text)


    except requests.exceptions.ConnectionError:

        st.error(
            "❌ Cannot connect to FastAPI."
        )

        st.info(
            "Please start FastAPI first using:\n\n"
            "`python -m uvicorn app:app --reload`"
        )


    except Exception as e:

        st.error(
            f"Something went wrong: {str(e)}"
        )