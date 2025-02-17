# Streamlit Code for Visualization
import streamlit as st  # Web application framework
import requests  # HTTP requests handling
import pandas as pd  # Data handling
from background import set_background

API_URL = "http://localhost:8000"  # Base API URL


def analytics_by_month_tab():
    set_background("#EAEAEA")
    """Fetch and display monthly expense summary using Streamlit."""
    response = requests.get(f"{API_URL}/monthly_summary/")  # Fetch data from API
    monthly_summary = response.json()

    # Convert API response to a Pandas DataFrame
    df = pd.DataFrame(monthly_summary)

    # Rename columns for better readability
    if "month" in df.columns:
        df.rename(columns={"month": "Month Name", "total": "Total"}, inplace=True)
    else:
        df.rename(columns={"month_name": "Month Name", "total": "Total"}, inplace=True)

    # Define proper month order
    month_order = [
        "January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December"
    ]

    # Convert 'Month Name' to categorical type and sort
    df["Month Name"] = pd.Categorical(df["Month Name"], categories=month_order, ordered=True)
    df_sorted = df.sort_values("Month Name")

    st.markdown(
        '<h1 style="font-size: 30px; color: blue; font-weight: normal;">Expense Breakdown By Month</h1>',
        unsafe_allow_html=True
    )  # Page title

    # Display bar chart of monthly expenses
    st.bar_chart(data=df_sorted.set_index("Month Name")["Total"], width=0, height=0, use_container_width=True)

    # Format 'Total' values to two decimal places
    df_sorted["Total"] = df_sorted["Total"].map("{:.2f}".format)

    # Display data as a table
    st.table(df_sorted)


