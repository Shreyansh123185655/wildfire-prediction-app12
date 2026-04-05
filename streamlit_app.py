import streamlit as st
import pandas as pd
import joblib
import numpy as np
import os

# -------------------------------
# ✅ Load model from correct path
# -------------------------------
MODEL_PATH = "notebooks/wildfire_risk_model.pkl"

if not os.path.exists(MODEL_PATH):
    st.error(f"❌ Model file not found at: {MODEL_PATH}")
    st.stop()

model = joblib.load(MODEL_PATH)
st.success("✅ Model loaded successfully!")

# -------------------------------
# 🧾 Streamlit UI
# -------------------------------
st.title("🔥 Wildfire Risk Prediction App")

st.write("Enter environmental details to predict wildfire risk:")

# User Inputs
col1, col2 = st.columns(2)

with col1:
    temperature = st.number_input("🌡️ Temperature (°F)", min_value=-50.0, max_value=150.0, value=85.0)
    min_temp = st.number_input("❄️ Minimum Temperature (°F)", min_value=-50.0, max_value=150.0, value=65.0)
    rainfall = st.number_input("🌧️ Rainfall (mm)", min_value=0.0, max_value=500.0, value=0.0)
    wind_speed = st.number_input("💨 Wind Speed (km/h)", min_value=0.0, max_value=200.0, value=18.0)

with col2:
    month = st.slider("📅 Month", 1, 12, 6)
    day_of_year = st.slider("📆 Day of Year", 1, 365, 180)
    lagged_rainfall = st.number_input("🌧️ Previous Day Rainfall (mm)", min_value=0.0, max_value=500.0, value=0.0)
    lagged_wind = st.number_input("💨 Previous Day Wind Speed (km/h)", min_value=0.0, max_value=200.0, value=15.0)

season = st.selectbox("🗓️ Season", ["Winter", "Spring", "Summer", "Autumn"])

# Predict Button
if st.button("🚀 Predict Wildfire Risk"):
    try:
        # Calculate derived features
        temp_range = temperature - min_temp
        wind_temp_ratio = wind_speed / (temperature + 1)  # Add 1 to avoid division by zero
        
        # Prepare input as DataFrame
        input_data = pd.DataFrame([{
            "temperature": temperature,
            "rainfall": rainfall,
            "wind_speed": wind_speed,
            "season": season,
            "MIN_TEMP": min_temp,
            "TEMP_RANGE": temp_range,
            "WIND_TEMP_RATIO": wind_temp_ratio,
            "MONTH": month,
            "LAGGED_PRECIPITATION": lagged_rainfall,
            "LAGGED_AVG_WIND_SPEED": lagged_wind,
            "DAY_OF_YEAR": day_of_year
        }])

        # Prediction
        prediction = model.predict(input_data)[0]
        probability = model.predict_proba(input_data)[0][1]

        # Output
        st.subheader("🔥 Prediction Result:")
        if prediction == 1:
            st.error(f"⚠️ High Wildfire Risk ({probability*100:.2f}% probability)")
        else:
            st.success(f"✅ Low Wildfire Risk ({probability*100:.2f}% probability)")

    except Exception as e:
        st.error(f"❌ Error during prediction: {e}")
