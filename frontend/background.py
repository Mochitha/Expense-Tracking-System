import streamlit as st
# Function to set custom background color
def set_background(color="#F5F5F5"):
    """Set background color for the entire Streamlit app."""
    st.markdown(
        f"""
        <style>
            .stApp {{
                background-color: {color} !important;
            }}
        </style>
        """,
        unsafe_allow_html=True
    )