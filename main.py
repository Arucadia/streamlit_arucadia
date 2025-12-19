import streamlit as st

st.set_page_config(layout="wide")

st.sidebar.title("Navigation")

page = st.sidebar.radio(
    "Menu",
    ["Home", "About Me", "Projects"]
)

# session state untuk project aktif
if "active_project" not in st.session_state:
    st.session_state.active_project = None

# ======================
# HOME
# ======================
if page == "Home":
    st.session_state.active_project = None
    st.title("My Portfolio")
    st.header("Welcome to My Portfolio")
    st.subheader("Explore my projects and skills")

# ======================
# ABOUT ME
# ======================
elif page == "About Me":
    st.session_state.active_project = None
    import about
    about.about_me()

# ======================
# PROJECTS
# ======================
elif page == "Projects":

    if st.session_state.active_project is None:
        import project
        project.show_projects()
    else:
        # detail project
        if st.button("← Back to Projects"):
            st.session_state.active_project = None
            st.rerun()

        if st.session_state.active_project == "HR Promotion Dashboard":
            import HR_analysis
            HR_analysis.hr_dashboard()
