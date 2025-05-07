import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px

st.set_page_config(page_title="Churn & CLV Dashboard", layout="centered")
st.title("📊 Customer Churn & CLV Dashboard")

@st.cache_data
def load_data():
    return pd.read_csv("final_output.csv")

data = load_data()

# Select a customer
cust = st.selectbox("🔍 Select Customer ID", data["Customer_Id"].sort_values().unique())
row = data.loc[data["Customer_Id"] == cust].iloc[0]

st.subheader("🔑 Key Customer Metrics")
col1, col2, col3 = st.columns(3)
col1.metric("Churn Probability", f"{row['Churn_Prob']:.1%}")
col2.metric("Predicted CLV", f"${row['Predicted_CLV']:.2f}")
col3.metric("Expected Loss", f"${row['ExpectedLoss']:.2f}")
st.markdown(f"**🧠 Recommended Action:** `{row['Action']}`")

# CLV Percentile
clv_percentile = np.round(np.sum(data['Predicted_CLV'] < row['Predicted_CLV']) / len(data) * 100, 1)
st.metric("🎯 CLV Percentile Rank", f"{clv_percentile}th")

# 1️⃣ Gauge Plot (Churn Meter)
st.subheader("🧭 Churn Risk Meter")
gauge_fig = go.Figure(go.Indicator(
    mode="gauge+number",
    value=row["Churn_Prob"] * 100,
    domain={'x': [0, 1], 'y': [0, 1]},
    title={'text': "Churn Risk %"},
    gauge={
        'axis': {'range': [0, 100]},
        'bar': {'color': "darkred"},
        'steps': [
            {'range': [0, 50], 'color': "lightgreen"},
            {'range': [50, 75], 'color': "orange"},
            {'range': [75, 100], 'color': "red"},
        ],
    }
))
st.plotly_chart(gauge_fig, use_container_width=True)

# 2️⃣ CLV vs Average Comparison
st.subheader("💸 CLV Comparison with Average")
clv_bar = go.Figure(data=[
    go.Bar(name='Selected Customer', x=["CLV"], y=[row['Predicted_CLV']], marker_color='dodgerblue'),
    go.Bar(name='Average CLV', x=["CLV"], y=[data["Predicted_CLV"].mean()], marker_color='gray')
])
clv_bar.update_layout(barmode='group', yaxis_title="CLV ($)")
st.plotly_chart(clv_bar, use_container_width=True)

# 3️⃣ CLV vs Churn Quadrant
st.subheader("🧮 Customer Position in Risk/Value Quadrant")
scatter_fig = px.scatter(
    data,
    x="Predicted_CLV",
    y="Churn_Prob",
    opacity=0.3,
    color_discrete_sequence=["lightgray"],
    labels={"Predicted_CLV": "Predicted CLV", "Churn_Prob": "Churn Probability"},
)
scatter_fig.add_trace(go.Scatter(
    x=[row["Predicted_CLV"]],
    y=[row["Churn_Prob"]],
    mode="markers+text",
    name="Selected Customer",
    marker=dict(color="red", size=10),
    text=["📍 You"],
    textposition="top center"
))
scatter_fig.add_vline(x=data["Predicted_CLV"].mean(), line_dash="dot", line_color="black")
scatter_fig.add_hline(y=data["Churn_Prob"].mean(), line_dash="dot", line_color="black")
scatter_fig.update_layout(height=500, yaxis_tickformat=".0%", title="CLV vs Churn Risk")
st.plotly_chart(scatter_fig, use_container_width=True)
