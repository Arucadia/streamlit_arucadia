import streamlit as st
import pandas as pd
from utils.inference import load_model


def show_machine_failure():
    st.title("Machine Failure Prediction")

    st.write(
        """
        This application predicts machine failure using the **best-performing XGBoost baseline model**.
        The model was selected based on **confusion matrix trade-off analysis** to balance
        false negatives and false positives for operational reliability.
        """
    )

    # Load trained model (cached)
    model = load_model()

    st.subheader("Input Machine Sensor Data")

    col1, col2 = st.columns(2)

    with col1:
        air_temp = st.number_input(
            "Air Temperature [K]", min_value=250.0, max_value=400.0, value=300.0
        )
        process_temp = st.number_input(
            "Process Temperature [K]", min_value=250.0, max_value=450.0, value=310.0
        )
        torque = st.number_input(
            "Torque [Nm]", min_value=0.0, max_value=100.0, value=40.0
        )

    with col2:
        rpm = st.number_input(
            "Rotational Speed [rpm]", min_value=0, max_value=5000, value=1500
        )
        tool_wear = st.number_input(
            "Tool Wear [min]", min_value=0, max_value=300, value=0
        )

        machine_type = st.selectbox(
            "Machine Type",
            options=["L", "M", "H"],
            index=0
        )


    # Mapping Machine Type (UI → Model)
    # drop-first encoding:
    # L -> (1, 0)
    # M -> (0, 1)
    # H -> (0, 0)
    type_l = 1 if machine_type == "L" else 0
    type_m = 1 if machine_type == "M" else 0

    input_df = pd.DataFrame({
        "air_temperature": [air_temp],
        "process_temperature": [process_temp],
        "rotational_speed": [rpm],
        "torque": [torque],
        "tool_wear": [tool_wear],
        "type_l": [type_l],
        "type_m": [type_m],
    })

    if st.button("Predict Failure"):
        prediction = model.predict(input_df)[0]
        probability = model.predict_proba(input_df)[0][1]

        if prediction == 1:
            st.error(
                f"⚠️ **Failure Detected**\n\n"
                f"Probability of failure: **{probability:.2%}**"
            )
        else:
            st.success(
                f"✅ **No Failure Detected**\n\n"
                f"Probability of failure: **{probability:.2%}**"
            )

    st.markdown("---")

    st.markdown(
        """
        ### Model Information
        - **Algorithm:** XGBoost
        - **Imbalance Handling:** `scale_pos_weight`
        - **Categorical Encoding:** One-hot encoding (drop-first)
        - **Model Selection:** Confusion Matrix Analysis
        - **Deployment:** Inference-only (no retraining)
        """
    )
