import streamlit as st
import requests
import json
from typing import Dict, Any

# Page configuration
st.set_page_config(
    page_title="Insurance Premium Predictor",
    page_icon="🏥",
    layout="centered"
)

# Title and description
st.title("🏥 Insurance Premium Predictor")
st.markdown("Predict your insurance premium category based on personal information")

# API endpoint
API_URL = "http://localhost:8000/predict"

# City options
tier_1_cities = ["Mumbai", "Delhi", "Bangalore", "Chennai", "Kolkata", "Hyderabad", "Pune"]
tier_2_cities = [
    "Jaipur", "Chandigarh", "Indore", "Lucknow", "Patna", "Ranchi", "Visakhapatnam", "Coimbatore",
    "Bhopal", "Nagpur", "Vadodara", "Surat", "Rajkot", "Jodhpur", "Raipur", "Amritsar", "Varanasi",
    "Agra", "Dehradun", "Mysore", "Jabalpur", "Guwahati", "Thiruvananthapuram", "Ludhiana", "Nashik",
    "Allahabad", "Udaipur", "Aurangabad", "Hubli", "Belgaum", "Salem", "Vijayawada", "Tiruchirappalli",
    "Bhavnagar", "Gwalior", "Dhanbad", "Bareilly", "Aligarh", "Gaya", "Kozhikode", "Warangal",
    "Kolhapur", "Bilaspur", "Jalandhar", "Noida", "Guntur", "Asansol", "Siliguri"
]
all_cities = tier_1_cities + tier_2_cities + ["Other"]

# Occupation options
occupations = ['retired', 'freelancer', 'student', 'government_job',
               'business_owner', 'unemployed', 'private_job']

def calculate_bmi(weight: float, height: float) -> float:
    """Calculate BMI from weight and height"""
    return weight / (height ** 2)

def get_lifestyle_risk(smoker: bool, bmi: float) -> str:
    """Calculate lifestyle risk based on smoking and BMI"""
    if smoker and bmi > 30:
        return "high"
    elif smoker or bmi > 27:
        return "medium"
    return "low"

def get_age_group(age: int) -> str:
    """Get age group based on age"""
    if age < 25:
        return "young"
    elif age < 45:
        return "adult"
    elif age < 60:
        return "middle_aged"
    return "senior"

def get_city_tier(city: str) -> int:
    """Get city tier based on city name"""
    if city in tier_1_cities:
        return 1
    elif city in tier_2_cities:
        return 2
    return 3

def predict_premium(user_data: Dict[str, Any]) -> Dict[str, Any]:
    """Make prediction request to API"""
    try:
        response = requests.post(API_URL, json=user_data, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error connecting to API: {str(e)}")
        return None

# Create form
with st.form("prediction_form"):
    st.subheader("Enter Your Information")

    col1, col2 = st.columns(2)

    with col1:
        age = st.number_input("Age", min_value=1, max_value=120, value=30)
        weight = st.number_input("Weight (kg)", min_value=1.0, max_value=300.0, value=70.0)
        height = st.number_input("Height (m)", min_value=0.5, max_value=2.5, value=1.7, step=0.01)
        income = st.number_input("Annual Income (LPA)", min_value=0.0, max_value=1000.0, value=5.0, step=0.1)

    with col2:
        smoker = st.selectbox("Do you smoke?", ["No", "Yes"]) == "Yes"
        city = st.selectbox("City", all_cities)
        occupation = st.selectbox("Occupation", occupations)

    # Calculate derived values
    bmi = calculate_bmi(weight, height)
    lifestyle_risk = get_lifestyle_risk(smoker, bmi)
    age_group = get_age_group(age)
    city_tier = get_city_tier(city)

    # Display calculated values
    st.subheader("Calculated Values")
    col3, col4, col5 = st.columns(3)
    with col3:
        st.metric("BMI", f"{bmi:.1f}")
    with col4:
        st.metric("Lifestyle Risk", lifestyle_risk.title())
    with col5:
        st.metric("Age Group", age_group.replace("_", " ").title())

    # Submit button
    submitted = st.form_submit_button("Predict Premium Category")

    if submitted:
        # Prepare data for API
        user_data = {
            "bmi": round(bmi, 2),
            "age_group": age_group,
            "lifestyle_risk": lifestyle_risk,
            "city_tier": city_tier,
            "income_lpa": income,
            "occupation": occupation
        }

        # Make prediction
        with st.spinner("Predicting..."):
            result = predict_premium(user_data)

        if result:
            st.success("Prediction Complete!")

            # Display results
            response = result.get("response", {})

            col6, col7 = st.columns(2)

            with col6:
                st.subheader("Prediction Results")
                st.metric("Predicted Category", response.get("predicted_category", "N/A"))
                st.metric("Confidence", f"{response.get('confidence', 0):.1%}")

            with col7:
                st.subheader("Class Probabilities")
                probs = response.get("class_probabilities", {})
                for category, prob in probs.items():
                    st.metric(category, f"{prob:.1%}")

# Footer
st.markdown("---")
st.markdown("Built with Streamlit & FastAPI")
st.markdown("Make sure the API is running on http://localhost:8000")