import streamlit as st

def show_projects():
    st.title("Projects")

    projects = [
        {
            "name": "HR Promotion Dashboard",
            "description": "HR analytics dashboard for evaluating promotion readiness using RFM segmentation.",
            "tools": "Python, Pandas, Plotly, Streamlit"
        },
        {
            "name": "Machine Failure Prediction",
            "description": "End-to-end machine learning project to predict machine failure using XGBoost, selected based on confusion matrix trade-off.",
            "tools": "Python, Scikit-learn, XGBoost, Streamlit"
        }
    ]

    for p in projects:
        if st.button(p["name"], key=p["name"]):
            st.session_state.active_project = p["name"]
            st.rerun()

        st.write(p["description"])
        st.markdown(f"**Tools:** {p['tools']}")
        st.markdown("---")