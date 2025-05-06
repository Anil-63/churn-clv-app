import streamlit as st
import pandas as pd
import numpy as np

# Set up Streamlit page
st.set_page_config(
    page_title="Customer Churn & CLV Dashboard",
    layout="centered"
)

st.title("📊 Customer Churn & CLV Dashboard")

# Load predictions from final_output.csv
@st.cache_data
def load_data():
    return pd.read_csv("final_output.csv")

data = load_data()

# Dropdown to select customer
cust_id = st.selectbox(
    "Select Customer ID", 
    options=data["Customer_Id"].sort_values().unique()
)

# Get selected customer row
row = data[data["Customer_Id"] == cust_id].iloc[0]

# Show churn/CLV/Expected Loss metrics
st.subheader("📈 Customer Metrics")
col1, col2, col3 = st.columns(3)
col1.metric("Churn Probability", f"{row['Churn_Prob']:.1%}")
col2.metric("Predicted CLV", f"${row['Predicted_CLV']:.2f}")
col3.metric("Expected Loss", f"${row['ExpectedLoss']:.2f}")

# Show action recommendation
st.subheader("🎯 Retention Recommendation")
if row["Action"] == "Retain":
    st.success("✅ Recommended Action: RETAIN this customer")
else:
    st.warning("ℹ️ Recommended Action: IGNORE (low expected loss)")

# Optional: Show full row if needed
with st.expander("🔍 See Full Data Row"):
    st.dataframe(row.to_frame().T)

# Footer
st.divider()
st.caption("Built for Customer Retention & CLV Prioritization using ML ✨")
