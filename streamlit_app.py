import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="Customer Churn & CLV Dashboard", layout="centered")
st.title("📊 Customer Churn & CLV Dashboard")

@st.cache_data
def load_data():
    return pd.read_csv("final_output.csv")

data = load_data()

# Customer selection
cust = st.selectbox("Select Customer ID", data["Customer_Id"].sort_values().unique())
row = data.loc[data["Customer_Id"] == cust].iloc[0]

# Display core metrics
st.subheader("🔑 Customer Insights")
col1, col2, col3 = st.columns(3)
col1.metric("Churn Probability", f"{row['Churn_Prob']:.1%}")
col2.metric("Predicted CLV", f"${row['Predicted_CLV']:.2f}")
col3.metric("Expected Loss", f"${row['ExpectedLoss']:.2f}")
st.markdown(f"**🧠 Recommended Action:** `{row['Action']}`")

# CLV percentile
clv_percentile = np.round(np.sum(data['Predicted_CLV'] < row['Predicted_CLV']) / len(data) * 100, 1)
st.metric("CLV Percentile Rank", f"{clv_percentile}th")

# Progress bar
st.subheader("📉 Churn Probability Progress")
st.progress(float(row["Churn_Prob"]))

# Histogram: CLV Distribution
st.subheader("📈 Where This Customer Falls (CLV Distribution)")
fig, ax = plt.subplots(figsize=(8, 2))
ax.hist(data["Predicted_CLV"], bins=50, color="skyblue", edgecolor="black")
ax.axvline(row["Predicted_CLV"], color="red", linestyle="--", linewidth=2, label="Selected Customer")
ax.set_xlabel("Predicted CLV")
ax.set_yticks([])
ax.legend()
st.pyplot(fig)
