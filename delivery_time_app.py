import streamlit as st
import joblib
import pandas as pd

def show_delivery_time():

    st.title("Delivery Time Prediction")

    st.markdown(
        """
        This application predicts food delivery time using the best-performing 
        Linear Regression pipeline model. The model was selected based on 
        lowest Test RMSE (8.83) and highest Test R² (0.826).
        """
    )

    st.markdown("## Input Order Data")

    model = joblib.load("models/linear_final_model.pkl")

    col1, col2 = st.columns(2)

    with col1:
        distance = st.number_input(
            "Distance [km]",
            min_value=0.59,
            max_value=19.99,
            value=10.0
        )

        preparation_time = st.number_input(
            "Preparation Time [min]",
            min_value=5,
            max_value=29,
            value=17
        )

        courier_experience = st.number_input(
            "Courier Experience [years]",
            min_value=0.0,
            max_value=9.0,
            value=4.0
        )

    with col2:
        weather = st.selectbox(
            "Weather",
            ['Windy', 'Clear', 'Foggy', 'Rainy', 'Snowy']
        )

        traffic = st.selectbox(
            "Traffic Level",
            ['Low', 'Medium', 'High']
        )

        time_of_day = st.selectbox(
            "Time of Day",
            ['Afternoon', 'Evening', 'Night', 'Morning']
        )

        vehicle = st.selectbox(
            "Vehicle Type",
            ['Scooter', 'Bike', 'Car']
        )

    if st.button("Predict Delivery Time"):

        input_df = pd.DataFrame([{
            "Distance_km": distance,
            "Preparation_Time_min": preparation_time,
            "Courier_Experience_yrs": courier_experience,
            "Weather": weather,
            "Traffic_Level": traffic,
            "Time_of_Day": time_of_day,
            "Vehicle_Type": vehicle
        }])

        prediction = model.predict(input_df)[0]

        st.success(f"Estimated Delivery Time: {prediction:.2f} minutes")

        if prediction <= 45:
            st.info("Status: On Time (SLA Met)")
        else:
            st.error("Status: Risk of Delay (SLA Breach)")
