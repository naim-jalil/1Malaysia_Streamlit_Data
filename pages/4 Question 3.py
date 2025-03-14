import plotly.express as px
import streamlit as st
import pandas as pd
import os
from component.filter import filter
from component.reverse_mapping import reverse_mapping

st.title("Any correlations between other diseases and ICU admission?")

df = pd.read_csv(os.path.join("assets", "mapped_data.csv"))

# Filter here
df = filter(df)

df = reverse_mapping(df)

tab1, tab2 = st.tabs(["Chart", "Data Set"])

with tab1:
    st.subheader("Chart")
    # Select only numeric columns from the relevant disease and ICU columns
    disease_columns = [
        "DIABETES", "COPD", "ASTHMA", "INMUSUPR", "HYPERTENSION",
        "CARDIOVASCULAR", "OBESITY", "CHRONIC_KIDNEY", "TOBACCO", "ICU"
    ]

    # Filter the dataframe to only include the specified columns and ensure they are numeric
    correlation_df = df[disease_columns].corr(numeric_only=True)

    # Plotting the heatmap
    fig = px.imshow(
        correlation_df,
        text_auto=True,
        color_continuous_scale='Viridis',
        title='Correlation between Diseases and ICU Admission'
    )

    # Show the heatmap
    st.plotly_chart(fig)

with tab2:
    st.subheader("Data Set")
    st.dataframe(df)
