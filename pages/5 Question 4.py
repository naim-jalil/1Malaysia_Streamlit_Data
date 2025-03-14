from component.filter import filter
from component.reverse_mapping import reverse_mapping
import streamlit as st
import plotly.express as px
import pandas as pd
import os


st.set_page_config(
    page_icon=":shark:", layout="wide"
)

st.title("What are the common diseases that the deceased patients had?")

df = pd.read_csv(os.path.join("assets", "mapped_data.csv"))

# Filter here
df = filter(df)

df = reverse_mapping(df)

tab1, tab2 = st.tabs(["Bar Chart", "Data Set"])

with tab1:
    total_selected = len(df)
    st.write(f"📌 **Total Selected Cases**: {total_selected:,}")
    # Filter deceased patients (assuming DATE_OF_DEATH is not NaN when a patient is deceased)
    deceased_patients = df[df["DATE_OF_DEATH"].notna()]

    # Define disease columns
    disease_columns = ['DIABETES', 'COPD', 'ASTHMA', 'INMUSUPR', 'HYPERTENSION',
                       'CARDIOVASCULAR', 'OBESITY', 'CHRONIC_KIDNEY', 'TOBACCO']

    # Convert disease values: 1 (YES), else 0 (NO)
    disease_counts = deceased_patients[disease_columns].applymap(
        lambda x: 1 if x == 1 else 0).sum()

    # 🔹 Convert Series to DataFrame
    disease_counts_df = disease_counts.reset_index()
    disease_counts_df.columns = ['Disease', 'Count']  # Rename columns properly

    # 🔹 Create bar chart
    fig = px.bar(disease_counts_df,
                 x="Count",
                 y="Disease",
                 title="Common Diseases Among Deceased Patients",
                 labels={"Count": "Number of Deceased Patients",
                         "Disease": "Disease"},
                 color="Disease",  # Different colors for each disease
                 color_discrete_sequence=px.colors.qualitative.Set1)

    # Rotate x-axis labels for readability
    fig.update_xaxes(tickangle=45)

    st.plotly_chart(fig)

with tab2:
    total_selected = len(df)
    st.write(f"📌 **Total Selected Cases**: {total_selected:,}")
    st.dataframe(df)


# # Load dataset
# df = pd.read_csv("dataset.csv")
# df.columns = map(str.upper, df.columns)  # Ensure column names are uppercase
