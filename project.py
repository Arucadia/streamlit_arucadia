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
            "name": "Project A",
            "description": "Machine learning model to predict housing prices.",
            "tools": "Python, Scikit-learn"
        }
    ]

    for p in projects:
        if st.button(p["name"], key=p["name"]):
            st.session_state.active_project = p["name"]
            st.rerun()

        st.write(p["description"])
        st.markdown(f"**Tools:** {p['tools']}")
        st.markdown("---")
