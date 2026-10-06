# 🏦 Loan Approval Prediction

A Machine Learning web application that predicts whether a loan application will be **approved or not** based on applicant and financial information.

## 🛠️ Tech Stack

* Python
* Pandas, NumPy
* Scikit-learn
* Logistic Regression
* FastAPI
* Streamlit
* Joblib

## ✨ Features

* Loan approval prediction
* Approval probability
* Applicant income & credit score analysis
* DTI ratio and loan details
* REST API using FastAPI
* Interactive UI using Streamlit

## 🚀 Run Locally

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Start FastAPI

```bash
python -m uvicorn app:app --reload
```

API Docs:

```text
http://127.0.0.1:8000/docs
```

### Start Streamlit

```bash
python -m streamlit run frontend_app.py
```

Open:

```text
http://localhost:8501
```

## 📂 Project Structure

```text
loan-Prediction/
├── app.py
├── frontend_app.py
├── loan_approval_model.pkl
├── loan_approval_scaler.pkl
├── loan_approval_data.csv
├── requirements.txt
└── README.md
```

## 👨‍💻 Author

**Sachin Kumar Yadav**

B.Tech CSE | Data Science Intern
