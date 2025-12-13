import streamlit as st
import pandas as pd
import numpy as np

def show_projects():
    st.subheader("My Projects")
    
    # Sample project data
    projects = [
        {"name": "Project A", "description": "A machine learning project that predicts housing prices.", "technologies": "Python, Scikit-learn, Pandas"},
        {"name": "Project B", "description": "A web application for visualizing COVID-19 data.", "technologies": "Streamlit, Plotly, Dash"},
        {"name": "Project C", "description": "A deep learning model for image classification.", "technologies": "TensorFlow, Keras, OpenCV"},
    ]
    
    for project in projects:
        st.markdown(f"### {project['name']}")
        st.write(project['description'])
        st.markdown(f"**Technologies Used:** {project['technologies']}")
        st.markdown("---")