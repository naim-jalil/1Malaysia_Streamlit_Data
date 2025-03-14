import streamlit as st
import pandas as pd
import os
import plotly.express as px

st.set_page_config(page_title="COVID-19 Data Dashboard",
                   page_icon=":shark:", layout="wide")

st.title("📊 Data Overview")

# Load dataset
df = pd.read_csv(os.path.join("assets", "mapped_data.csv"))

# Convert AGE to numeric (handle missing values)
df["AGE"] = pd.to_numeric(df["AGE"], errors="coerce")
df = df.dropna(subset=["AGE"])  # Remove NaN ages
df["AGE"] = df["AGE"].astype(int)

# ---- DASHBOARD METRICS ----
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("📝 Total Cases", f"{len(df):,}")

with col2:
    total_hospitalized = df[df["HOSPITALIZED"] == "YES"].shape[0]
    st.metric("🏥 Total Hospitalized", f"{total_hospitalized:,}")

with col3:
    total_male = df[df["SEX"] == "MALE"].shape[0]
    total_female = df[df["SEX"] == "FEMALE"].shape[0]
    st.metric("👨 Male vs 👩 Female", f"{total_male:,} / {total_female:,}")

# ---- FILTERING DATA ----
st.sidebar.header("🔍 Filter Data")
sex_filter = st.sidebar.multiselect(
    "Select Sex", df["SEX"].unique(), default=df["SEX"].unique())
age_range = st.sidebar.slider("Select Age Range", int(df["AGE"].min()), int(
    df["AGE"].max()), (int(df["AGE"].min()), int(df["AGE"].max())))
outcome_filter = st.sidebar.selectbox(
    "Select Outcome", ["All"] + df["OUTCOME"].unique().tolist())

filtered_df = df[df["SEX"].isin(sex_filter)]
filtered_df = filtered_df[(filtered_df["AGE"] >= age_range[0]) & (
    filtered_df["AGE"] <= age_range[1])]

if outcome_filter != "All":
    filtered_df = filtered_df[filtered_df["OUTCOME"] == outcome_filter]

st.divider()
st.write(f"📌 **Filtered Cases Count**: {len(filtered_df):,}")
st.dataframe(filtered_df)

# ---- DASHBOARD VISUALIZATIONS ----
st.divider()
st.markdown("## 📊 Data Visualizations")

tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "👥 Gender Distribution",
    "🏥 Hospitalization Rate",
    "🩺 Outcome Distribution",
    "📅 Admission Months Count",
    "☠️ Death Month Counts",
    "📊 Comparative Analysis"
])

# Gender Distribution Pie Chart
with tab1:
    st.subheader("👥 Gender Distribution (Pie Chart)")
    fig1 = px.pie(df, names="SEX", title="Gender Distribution",
                  color_discrete_sequence=["#ff9999", "#66b3ff"])
    st.plotly_chart(fig1, use_container_width=True)

# Hospitalization Rate Bar Chart
with tab2:
    st.subheader("🏥 Hospitalization Rate (Bar Chart)")
    hospital_counts = df["HOSPITALIZED"].value_counts().reset_index()
    hospital_counts.columns = ["Hospitalized", "Count"]
    fig2 = px.bar(hospital_counts, x="Hospitalized", y="Count", title="Hospitalization Rate",
                  color="Hospitalized", color_discrete_sequence=["#ff9999", "#66b3ff"])
    st.plotly_chart(fig2, use_container_width=True)

# Outcome Distribution Bar Chart
with tab3:
    st.subheader("🩺 Outcome Distribution (Bar Chart)")
    outcome_counts = df["OUTCOME"].value_counts().reset_index()
    outcome_counts.columns = ["Outcome", "Count"]
    fig3 = px.bar(outcome_counts, x="Outcome", y="Count", title="Outcome Distribution",
                  color="Outcome", color_discrete_sequence=["#4CAF50", "#FFA07A", "#4682B4"])
    st.plotly_chart(fig3, use_container_width=True)

# Admission Months Count (Line Chart)
with tab4:
    st.subheader("📅 Admission Trends Over Time (Line Chart)")
    if "ADMISSION DATE" in df.columns:
        df["ADMISSION_DATETIME"] = pd.to_datetime(
            df["ADMISSION DATE"], errors='coerce')
        df["ADMISSION_YEAR"] = df["ADMISSION_DATETIME"].dt.year
        df["ADMISSION_MONTH"] = df["ADMISSION_DATETIME"].dt.strftime("%b")

        admission_counts = df.groupby(
            ["ADMISSION_YEAR", "ADMISSION_MONTH"]).size().reset_index(name="Count")

        month_order = ["Jan", "Feb", "Mar", "Apr", "May",
                       "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
        admission_counts["ADMISSION_MONTH"] = pd.Categorical(
            admission_counts["ADMISSION_MONTH"], categories=month_order, ordered=True)
        admission_counts = admission_counts.sort_values(
            ["ADMISSION_YEAR", "ADMISSION_MONTH"])

        fig4 = px.line(admission_counts, x="ADMISSION_MONTH", y="Count", color="ADMISSION_YEAR", labels={
                       "ADMISSION_YEAR": "Year"}, title="Monthly Admission Trends Over the Years", markers=True)
        st.plotly_chart(fig4, use_container_width=True)
    else:
        st.warning("⚠️ 'ADMISSION DATE' column not found in dataset.")

# Death Month Counts (Line Chart)
with tab5:
    st.subheader("☠️ Death Trends Over Time (Line Chart)")
    if "DATE_OF_DEATH" in df.columns:
        df["DEATH_DATETIME"] = pd.to_datetime(
            df["DATE_OF_DEATH"], errors='coerce')
        df["DEATH_YEAR"] = df["DEATH_DATETIME"].dt.year
        df["DEATH_MONTH"] = df["DEATH_DATETIME"].dt.strftime("%b")

        death_counts = df.groupby(
            ["DEATH_YEAR", "DEATH_MONTH"]).size().reset_index(name="Count")

        death_counts["DEATH_MONTH"] = pd.Categorical(
            death_counts["DEATH_MONTH"], categories=month_order, ordered=True)
        death_counts = death_counts.sort_values(["DEATH_YEAR", "DEATH_MONTH"])

        fig5 = px.line(death_counts, x="DEATH_MONTH", y="Count", color="DEATH_YEAR", labels={
                       "DEATH_YEAR": "Year"}, title="Monthly Death Trends Over the Years", markers=True)
        st.plotly_chart(fig5, use_container_width=True)
    else:
        st.warning("⚠️ 'DATE_OF_DEATH' column not found in dataset.")

# ---- NEW COMPARATIVE ANALYSIS TAB ----
with tab6:
    st.subheader("📊 Comparative Analysis & Trends")

    # Age vs. Hospitalization Status (Box Plot)
    st.markdown(
        "### 🏥 Age Distribution of Hospitalized vs. Non-Hospitalized Cases")
    fig6_1 = px.box(df, x="HOSPITALIZED", y="AGE", color="HOSPITALIZED",
                    title="Age Distribution by Hospitalization Status")
    st.plotly_chart(fig6_1, use_container_width=True)
