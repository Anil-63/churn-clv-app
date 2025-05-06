import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="Churn & CLV Dashboard", layout="wide")
st.title("📊 Customer Churn & CLV Dashboard")

@st.cache_data
def load_data():
    df = pd.read_csv("final_output.csv")
    df['Segment'] = pd.qcut(df['Predicted_CLV'], q=3, labels=["Low", "Medium", "High"])
    return df

data = load_data()

# =========================
# Summary Metrics
# =========================
st.header("📌 Business Summary")

col1, col2, col3 = st.columns(3)
col1.metric("Total Customers", f"{len(data):,}")
col2.metric("Avg. Predicted CLV", f"${data['Predicted_CLV'].mean():.2f}")
col3.metric("Retention Priority", f"{data[data['Action'] == 'Retain'].shape[0]} customers")

# =========================
# Customer Selection
# =========================
st.sidebar.header("🎯 Customer Lookup")
cust = st.sidebar.selectbox("Select Customer ID", data["Customer_Id"].sort_values().unique())
row = data.loc[data["Customer_Id"] == cust].iloc[0]

st.subheader(f"Details for Customer ID: `{int(cust)}`")
col1, col2, col3 = st.columns(3)
col1.metric("Churn Probability", f"{row['Churn_Prob']:.1%}")
col2.metric("Predicted CLV", f"${row['Predicted_CLV']:.2f}")
col3.metric("Expected Loss", f"${row['ExpectedLoss']:.2f}")
st.markdown(f"**Action:** `{row['Action']}`")

# =========================
# Visual Insights
# =========================
st.header("📈 Visual Insights")

with st.expander("💡 CLV by Segment"):
    fig, ax = plt.subplots(figsize=(6, 3))
    data['Segment'].value_counts().plot(kind='bar', ax=ax, color='skyblue')
    ax.set_title("Customer Segments by CLV")
    ax.set_ylabel("Count")
    st.pyplot(fig)

with st.expander("📉 Churn Probability Distribution"):
    fig, ax = plt.subplots(figsize=(6, 3))
    data['Churn_Prob'].hist(bins=20, ax=ax, color='salmon')
    ax.set_title("Churn Probability Histogram")
    ax.set_xlabel("Probability")
    ax.set_ylabel("Customers")
    st.pyplot(fig)

# =========================
# Filter & Download
# =========================
st.header("🔍 Filter & Download")
action_filter = st.selectbox("Filter by Action", options=["All", "Retain", "Ignore"])

if action_filter != "All":
    filtered = data[data['Action'] == action_filter]
else:
    filtered = data.copy()

st.dataframe(filtered)

csv = filtered.to_csv(index=False).encode('utf-8')
st.download_button("⬇️ Download Filtered Data", data=csv, file_name="filtered_customers.csv", mime="text/csv")

# =========================
# Footer
# =========================
st.markdown("---")
st.markdown("*Built for churn and CLV-driven retention strategy.*")
