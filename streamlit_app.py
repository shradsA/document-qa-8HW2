# streamlit_app.py
import streamlit as st
from hws import hw1, hw2  # Ensure both files have the correct run functions

# -------------------------------
# App Configuration
# -------------------------------
st.set_page_config(page_title="📚 HW Manager", layout="wide")
st.title("📚 HW Manager")
st.write("Select a homework page from the sidebar to continue.")

# -------------------------------
# Sidebar Page Selection
# -------------------------------
pages = {
    "HW1 - Document Q&A": hw1.run,        # HW1 should have run()
    "HW2 - URL Summarizer": hw2.run_hw2, # HW2 should have run_hw2()
}

choice = st.sidebar.selectbox("Choose a page", list(pages.keys()))

# -------------------------------
# Run the Selected Page
# -------------------------------
try:
    pages[choice]()
except Exception as e:
    st.error(f"Error running the selected page: {e}")
    st.stop()

# -------------------------------
# Optional Footer
# -------------------------------
st.markdown("---")
st.markdown("HW Manager - Multi-page Streamlit App | Created by Shraddha Aher")
