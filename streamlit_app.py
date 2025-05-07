import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

st.set_page_config(page_title="Customer Churn & CLV Dashboard", layout="wide")

@st.cache_data
def load_data():
    return pd.read_csv("final_output.csv")

data = load_data()

# ========================
# Sidebar Filters
# ========================
st.sidebar.title("🔍 Filter Customers")

clv_segments = ['All'] + list(data['Action'].unique())
selected_action = st.sidebar.selectbox("Filter by Recommended Action", clv_segments)

churn_slider = st.sidebar.slider("Minimum Churn Probability", 0.0, 1.0, 0.5)

filtered = data.copy()
if selected_action != 'All':
    filtered = filtered[filtered['Action'] == selected_action]
filtered = filtered[filtered['Churn_Prob'] >= churn_slider]

# ========================
# Dashboard Header
# ========================
st.title("📊 Customer Churn & CLV Dashboard")

# ========================
# Top-Level Metrics
# ========================
st.markdown("### 🔢 Overview Metrics")
col1, col2, col3 = st.columns(3)
col1.metric("Total Customers", len(filtered))
col2.metric("Avg. Predicted CLV", f"${filtered['Predicted_CLV'].mean():.2f}")
col3.metric("Avg. Churn Probability", f"{filtered['Churn_Prob'].mean():.1%}")

# ========================
# Tabs for Layout
# ========================
tab1, tab2, tab3, tab4 = st.tabs(["📋 Customer Table", "📈 Visual Insights", "🔍 Customer Drilldown", "📥 Export"])

# ========================
# Tab 1: Table
# ========================
with tab1:
    st.dataframe(filtered.sort_values(by="Churn_Prob", ascending=False), use_container_width=True)

# ========================
# Tab 2: Visual Insights
# ========================
with tab2:
    st.subheader("💡 Churn Probability Distribution")
    fig1 = px.histogram(data, x="Churn_Prob", nbins=40, title="Churn Probability of All Customers", color_discrete_sequence=['salmon'])
    st.plotly_chart(fig1, use_container_width=True)

    st.subheader("💡 CLV Segmentation")
    bins = pd.qcut(data["Predicted_CLV"], q=3, labels=["Low", "Medium", "High"])
    fig2 = px.histogram(data, x=bins, title="CLV Segments (Tertiles)", color_discrete_sequence=["skyblue"])
    st.plotly_chart(fig2, use_container_width=True)

# ========================
# Tab 3: Drilldown
# ========================
with tab3:
    st.subheader("🔎 Customer Details")
    cust_id = st.selectbox("Select Customer ID", data["Customer_Id"].sort_values().unique())
    row = data.loc[data["Customer_Id"] == cust_id].iloc[0]

    st.markdown(f"#### 🎯 Action: **{row['Action']}**")

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Churn Probability", f"{row['Churn_Prob']:.1%}")
    col2.metric("Predicted CLV", f"${row['Predicted_CLV']:.2f}")
    col3.metric("Expected Loss", f"${row['ExpectedLoss']:.2f}")
    percentile = np.round((data["Predicted_CLV"] < row["Predicted_CLV"]).mean() * 100, 1)
    col4.metric("CLV Percentile Rank", f"{percentile}th")

    # CLV & Churn Histograms
    st.markdown("### 📉 Customer in Context")
    fig3, ax = plt.subplots(1, 2, figsize=(14, 3))

    sns.histplot(data["Predicted_CLV"], bins=40, ax=ax[0], color="lightblue")
    ax[0].axvline(row["Predicted_CLV"], color="red", linestyle="--")
    ax[0].set_title("CLV Distribution")
    ax[0].set_xlabel("CLV")

    sns.histplot(data["Churn_Prob"], bins=40, ax=ax[1], color="salmon")
    ax[1].axvline(row["Churn_Prob"], color="blue", linestyle="--")
    ax[1].set_title("Churn Probability Distribution")
    ax[1].set_xlabel("Churn Prob")

    st.pyplot(fig3)

# ========================
# Tab 4: Export
# ========================
with tab4:
    st.subheader("📥 Download Reports")
    st.download_button("📤 Download Filtered Customers (CSV)", data=filtered.to_csv(index=False), file_name="filtered_customers.csv")

    st.markdown("Generate filtered report based on the left-side filters.")
    st.info("Use this data for follow-up campaigns or retention strategies.")

# ========================
# Footer
# ========================
st.markdown("---")
st.caption("Created by Team AI | Powered by Churn & CLV Model ✅")
