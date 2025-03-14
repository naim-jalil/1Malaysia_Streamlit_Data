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

# Total Cases
with col1:
    st.metric("📝 Total Cases", f"{len(df):,}")

# Total Hospitalized Cases
with col2:
    total_hospitalized = df[df["HOSPITALIZED"] == "YES"].shape[0]
    st.metric("🏥 Total Hospitalized", f"{total_hospitalized:,}")

# Male vs Female Count
with col3:
    total_male = df[df["SEX"] == "MALE"].shape[0]
    total_female = df[df["SEX"] == "FEMALE"].shape[0]
    st.metric("👨 Male vs 👩 Female", f"{total_male:,} / {total_female:,}")

# ---- FILTERING DATA ----
st.sidebar.header("🔍 Filter Data")
sex_filter = st.sidebar.multiselect(
    "Select Sex", df["SEX"].unique(), default=df["SEX"].unique())
age_range = st.sidebar.slider("Select Age Range", int(df["AGE"].min()), int(df["AGE"].max()),
                              (int(df["AGE"].min()), int(df["AGE"].max())))
outcome_filter = st.sidebar.selectbox(
    "Select Outcome", ["All"] + df["OUTCOME"].unique().tolist())

# Apply filters
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

# Create tabs for visualizations
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "👥 Gender Distribution",
    "🏥 Hospitalization Rate",
    "🩺 Outcome Distribution",
    "📅 Admission Months Count",
    "☠️ Death Month Counts"
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

# Admission Months Count
with tab4:
    st.subheader("📅 Admission Months Count (Bar Chart)")

    if "ADMISSION DATE" in df.columns:
        df["ADMISSION_MONTH"] = pd.to_datetime(
            df["ADMISSION DATE"], errors='coerce').dt.month

        # Convert month numbers to month names
        month_mapping = {1: "Jan", 2: "Feb", 3: "Mar", 4: "Apr", 5: "May", 6: "Jun",
                         7: "Jul", 8: "Aug", 9: "Sep", 10: "Oct", 11: "Nov", 12: "Dec"}
        df["ADMISSION_MONTH"] = df["ADMISSION_MONTH"].map(month_mapping)

        admission_counts = df["ADMISSION_MONTH"].value_counts().reindex(
            month_mapping.values(), fill_value=0)

        fig4 = px.bar(
            x=admission_counts.index,
            y=admission_counts.values,
            labels={"x": "Month", "y": "Number of Admissions"},
            title="Admissions per Month",
            color=admission_counts.index,
            color_discrete_sequence=px.colors.sequential.Blues
        )
        st.plotly_chart(fig4, use_container_width=True)
    else:
        st.warning("⚠️ 'ADMISSION DATE' column not found in dataset.")

# Death Month Counts
with tab5:
    st.subheader("☠️ Death Month Counts (Bar Chart)")

    if "DATE_OF_DEATH" in df.columns:
        df["DEATH_MONTH"] = pd.to_datetime(
            df["DATE_OF_DEATH"], errors='coerce').dt.month

        # Convert month numbers to month names
        df["DEATH_MONTH"] = df["DEATH_MONTH"].map(month_mapping)

        death_counts = df["DEATH_MONTH"].value_counts().reindex(
            month_mapping.values(), fill_value=0)

        fig5 = px.bar(
            x=death_counts.index,
            y=death_counts.values,
            labels={"x": "Month", "y": "Number of Deaths"},
            title="Deaths per Month",
            color=death_counts.index,
            color_discrete_sequence=px.colors.sequential.Reds
        )
        st.plotly_chart(fig5, use_container_width=True)
    else:
        st.warning("⚠️ 'DATE_OF_DEATH' column not found in dataset.")
