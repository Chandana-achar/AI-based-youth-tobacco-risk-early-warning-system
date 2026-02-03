import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# ---------------- Page config ----------------
st.set_page_config(page_title="Youth Tobacco Risk Dashboard", layout="wide")

st.title("🚨 AI-Based Youth Tobacco Risk Early Warning System")
st.markdown("Using **GYTS-4 Government Dataset (IndiaAI / data.gov.in)**")

# ---------------- Load data ----------------
@st.cache_data
def load_data():
    file_path = os.path.join(os.getcwd(), "GYTS4.xlsx")
    return pd.read_excel(file_path)

data = load_data()

# ---------------- Clean column names ----------------
data.columns = data.columns.str.strip()

# ---------------- Sidebar ----------------
st.sidebar.header("🔍 Filters")

area = st.sidebar.selectbox(
    "Select Area",
    data['Area'].unique()
)

filtered_data = data[data['Area'] == area]

# ---------------- Correct feature columns ----------------
features = [
    'Current tobacco users (%)',
    'Current tobacco smokers (%)',
    'Current cigarette users (%)',
    'Current smokeless tobacco users (%)'
]

filtered_data = filtered_data[['State/UT', 'Area'] + features]

# ---------------- Risk Score ----------------
filtered_data['Risk_Score'] = (
    filtered_data['Current tobacco users (%)'] * 0.35 +
    filtered_data['Current tobacco smokers (%)'] * 0.30 +
    filtered_data['Current cigarette users (%)'] * 0.20 +
    filtered_data['Current smokeless tobacco users (%)'] * 0.15
)

# ---------------- Risk Level ----------------
def label_risk(score):
    if score >= 20:
        return "High"
    elif score >= 10:
        return "Medium"
    else:
        return "Low"

filtered_data['Risk_Level'] = filtered_data['Risk_Score'].apply(label_risk)

# ---------------- Metrics ----------------
st.subheader("📊 Key Insights")

c1, c2, c3 = st.columns(3)
c1.metric("States Analyzed", filtered_data.shape[0])
c2.metric("High Risk States", (filtered_data['Risk_Level'] == "High").sum())
c3.metric("Low Risk States", (filtered_data['Risk_Level'] == "Low").sum())

# ---------------- Risk Distribution ----------------
st.subheader("⚠️ Risk Distribution")

fig1, ax1 = plt.subplots()
sns.countplot(
    x=filtered_data['Risk_Level'],
    order=["Low", "Medium", "High"],
    ax=ax1
)
st.pyplot(fig1)

# ---------------- Top High-Risk States ----------------
st.subheader("🔥 Top High-Risk States")

top_states = filtered_data.sort_values(
    'Risk_Score',
    ascending=False
).head(10)

fig2, ax2 = plt.subplots(figsize=(10, 5))
sns.barplot(
    x='Risk_Score',
    y='State/UT',
    data=top_states,
    ax=ax2
)
st.pyplot(fig2)

# ---------------- Table ----------------
st.subheader("📄 State-wise Risk Table")

st.dataframe(
    filtered_data[['State/UT', 'Risk_Score', 'Risk_Level']]
    .sort_values('Risk_Score', ascending=False),
    use_container_width=True
)

# ---------------- Footer ----------------
st.markdown("---")
st.markdown(
    "💡 This dashboard uses GYTS-4 government data to identify "
    "high-risk regions and support preventive youth health policies."
)
