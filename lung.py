# -*- coding: utf-8 -*-
"""
Created on Sun Jun 29 21:23:10 2025

@author: Vraj
"""

import pickle
import streamlit as st
from streamlit_option_menu import option_menu

# Load the trained logistic regression model
model = pickle.load(open('lung_model (1).sav', 'rb'))

# Set Streamlit page configuration
st.set_page_config(page_title="Lung Cancer Survival Predictor")
st.title("🫁 Lung Cancer Survival Predictor")

# Create navigation menu
selected = option_menu(
    menu_title="Main Menu",
    options=["Home", "Survival Prediction"],
    icons=["house", "activity"],
    default_index=1,
    orientation="horizontal"
)

# If 'Survival Prediction' is selected
if selected == "Survival Prediction":
    st.subheader("Enter Patient Information:")

    col1, col2, col3 = st.columns(3)

    # Input fields
    with col1:
        age = st.number_input("Age (years)", min_value=1, max_value=120, value=60)
        bmi = st.number_input("BMI", min_value=10.0, max_value=60.0, value=22.0)
        cholesterol = st.number_input("Cholesterol Level (mg/dL)", min_value=100, max_value=400, value=180)

    with col2:
        gender = st.selectbox("Gender", ["Male", "Female"])
        country = st.selectbox("Country", ["USA", "India", "Germany", "UK", "Other"])
        cancer_stage = st.selectbox("Cancer Stage", ["I", "II", "III", "IV"])

    with col3:
        treatment_type = st.selectbox("Treatment Type", ["Surgery", "Chemotherapy", "Combined"])
        family_history = st.radio("Family History of Cancer?", ["No", "Yes"])
        smoking_status = st.selectbox("Smoking Status", ["Never", "Passive Smoker", "Former Smoker", "Current Smoker"])
        hypertension = st.radio("Hypertension?", ["No", "Yes"])
        asthma = st.radio("Asthma?", ["No", "Yes"])
        cirrhosis = st.radio("Cirrhosis?", ["No", "Yes"])
        other_cancer = st.radio("Other Cancer?", ["No", "Yes"])

    # Prediction button
    if st.button("Predict Survival"):
        # Encode all inputs to match training
        input_data = [
            age,
            bmi,
            cholesterol,
            1 if gender == "Male" else 0,
            {"USA": 0, "India": 1, "Germany": 2, "UK": 3, "Other": 4}[country],
            {"I": 0, "II": 1, "III": 2, "IV": 3}[cancer_stage],
            1 if family_history == "Yes" else 0,
            {"Never": 0, "Passive Smoker": 1, "Former Smoker": 2, "Current Smoker": 3}[smoking_status],
            1 if hypertension == "Yes" else 0,
            1 if asthma == "Yes" else 0,
            1 if cirrhosis == "Yes" else 0,
            1 if other_cancer == "Yes" else 0,
            {"Surgery": 0, "Chemotherapy": 1, "Combined": 2}[treatment_type]
        ]

        # Make prediction
        prediction = model.predict([input_data])[0]

        # Display result
        if prediction == 1:
            st.success("✅ Predicted Outcome: Survived")
        else:
            st.error("❌ Predicted Outcome: Not Survived")
