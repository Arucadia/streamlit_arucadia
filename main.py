import streamlit as st

st.set_page_config(layout='wide')
st.title("My Portfolio")
st.header("Welcome to My Portfolio")
st.subheader("Explore my projects and skills")

st.sidebar.title('Navigation')

page = st.sidebar.radio("Go to", ["Home", "About Me", "Projects"])

if page == "About Me":
    import about
    about.about_me()
elif page == "Projects":
    import project
    project.show_projects()
