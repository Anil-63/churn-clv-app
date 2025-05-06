import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(
    page_title="Churn & CLV Dashboard",
    layout="centered",
)

st.title("📊 Customer Churn & CLV Dashboard")

@st.cache_data
def load_data():
    # final_output.csv should live next to this script in your repo
    return pd.read_csv("final_output.csv")

data = load_data()

# let user pick a customer
cust = st.selectbox(
    "Select Customer ID", 
    data["Customer_Id"].sort_values().unique()
)

row = data.loc[data["Customer_Id"] == cust].iloc[0]

# display key metrics
col1, col2, col3 = st.columns(3)
col1.metric("Churn Probability", f"{row['Churn_Prob']:.1%}")
col2.metric("Predicted CLV",     f"${row['Predicted_CLV']:.2f}")
col3.metric("Expected Loss",     f"${row['ExpectedLoss']:.2f}")

st.markdown(
    f"**Recommended Action:** **{row['Action']}**"
)
