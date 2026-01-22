import joblib
import streamlit as st
import os

@st.cache_resource
def load_model():
    base_dir = os.path.dirname(os.path.dirname(__file__))
    model_path = os.path.join(base_dir, "models", "xgb_baseline_model.pkl")
    return joblib.load(model_path)
