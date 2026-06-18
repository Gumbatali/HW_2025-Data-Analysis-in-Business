import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Business Analytics", layout="wide", page_icon="📈")

# Premium Custom CSS
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(180deg, #18181b 0%, #27272a 100%);
        color: #f4f4f5;
        font-family: 'Inter', sans-serif;
    }
    h1, h2, h3 {
        color: #fcd34d !important;
        font-weight: 700 !important;
    }
    .stDataFrame {
        border-radius: 12px;
        border: 1px solid #52525b;
        background-color: rgba(39, 39, 42, 0.8);
    }
    div[data-testid="stMetricValue"] {
        color: #fbbf24;
        font-weight: 800;
        font-size: 2.5rem !important;
    }
    div[data-testid="stMetricDelta"] {
        font-size: 1.1rem !important;
    }
    .stPlotlyChart {
        border-radius: 12px;
        overflow: hidden;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.2);
    }
</style>
""", unsafe_allow_html=True)

st.title("📈 Business Data Analytics Dashboard")
st.markdown("*A professional dashboard for tracking sales, conversion rates, and revenue metrics.*")
st.markdown("---")

@st.cache_data
def get_business_data():
    np.random.seed(42)
    dates = pd.date_range(start="2024-01-01", periods=180)
    
    # Generate mock sales data
    base_sales = np.linspace(100, 300, 180) + np.random.normal(0, 30, 180)
    sales = np.clip(base_sales, a_min=50, a_max=None)
    
    # Generate mock revenue
    revenue = sales * np.random.uniform(15, 30, 180)
    
    # Traffic
    traffic = sales * np.random.uniform(5, 15, 180)
    
    df = pd.DataFrame({
        "Date": dates,
        "Sales": sales.astype(int),
        "Revenue ($)": revenue.round(2),
        "Website Traffic": traffic.astype(int)
    })
    
    df["Conversion Rate (%)"] = (df["Sales"] / df["Website Traffic"] * 100).round(2)
    return df

df = get_business_data()

# Top KPIs
col1, col2, col3, col4 = st.columns(4)
total_rev = df["Revenue ($)"].sum()
avg_conv = df["Conversion Rate (%)"].mean()
col1.metric("Total Revenue", f"${total_rev:,.0f}", "+15.2%")
col2.metric("Total Sales", f"{df['Sales'].sum():,}", "+8.4%")
col3.metric("Avg Conversion Rate", f"{avg_conv:.2f}%", "+1.1%")
col4.metric("Active Users", "12,450", "+500")

st.markdown("---")

# Charts
c1, c2 = st.columns([2, 1])

with c1:
    st.subheader("💵 Revenue Trend")
    fig_rev = px.area(df, x="Date", y="Revenue ($)", 
                      template="plotly_dark", color_discrete_sequence=["#fbbf24"])
    fig_rev.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig_rev, use_container_width=True)

with c2:
    st.subheader("Funnel Analysis")
    funnel_data = dict(
        number=[10000, 4000, 2000, 500],
        stage=["Website Visits", "Added to Cart", "Initiated Checkout", "Purchased"]
    )
    fig_funnel = px.funnel(funnel_data, x='number', y='stage', template="plotly_dark",
                           color_discrete_sequence=["#fcd34d", "#f59e0b", "#d97706", "#b45309"])
    fig_funnel.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig_funnel, use_container_width=True)

st.subheader("📋 Raw Performance Data")
st.dataframe(df.sort_values("Date", ascending=False).head(10), use_container_width=True)
