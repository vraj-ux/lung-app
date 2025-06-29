import pickle
import streamlit as st
from streamlit_option_menu import option_menu

# Load model (must place lung_model.sav in same folder)
model = pickle.load(open('lung_model.sav', 'rb'))

st.set_page_config(page_title="Lung Cancer Survival Predictor")
st.title("🫁 Lung Cancer Survival Predictor")

selected = option_menu(
    menu_title="Main Menu",
    options=["Home", "Survival Prediction"],
    icons=["house", "activity"],
    default_index=1,
    orientation="horizontal"
)

if selected == "Survival Prediction":
    st.subheader("Enter Patient Information:")

    col1, col2, col3 = st.columns(3)

    with col1:
        age = st.number_input("Age", 1, 120, 60)
        bmi = st.number_input("BMI", 10.0, 60.0, 22.0)
        cholesterol = st.number_input("Cholesterol", 100, 400, 180)

    with col2:
        gender = st.selectbox("Gender", ["Male", "Female"])
        country = st.selectbox("Country", ["USA", "India", "Germany", "UK", "Other"])
        cancer_stage = st.selectbox("Cancer Stage", ["I", "II", "III", "IV"])

    with col3:
        treatment_type = st.selectbox("Treatment", ["Surgery", "Chemotherapy", "Combined"])
        family_history = st.radio("Family History?", ["No", "Yes"])
        smoking_status = st.selectbox("Smoking Status", ["Never", "Passive Smoker", "Former Smoker", "Current Smoker"])
        hypertension = st.radio("Hypertension?", ["No", "Yes"])
        asthma = st.radio("Asthma?", ["No", "Yes"])
        cirrhosis = st.radio("Cirrhosis?", ["No", "Yes"])
        other_cancer = st.radio("Other Cancer?", ["No", "Yes"])

    if st.button("Predict Survival"):
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

        prediction = model.predict([input_data])[0]
        if prediction == 1:
            st.success("✅ Predicted Outcome: Survived")
        else:
            st.error("❌ Predicted Outcome: Not Survived")
