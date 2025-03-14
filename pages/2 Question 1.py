import plotly.express as px
import streamlit as st
import pandas as pd
import os
from component.filter import filter


st.set_page_config(
    page_icon=":shark:", layout="wide"
)


st.title("Which age groups are most susceptible to COVID-19?")

df = pd.read_csv(os.path.join("assets", "mapped_data.csv"))

df = filter(df)


tab1, tab2, tab3 = st.tabs(["Bar Chart", "Histogram", "Data Set"])

with tab1:
    st.subheader("Bar Chart")
    analysis = df.copy()
    # Define the bins and labels
    bins = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
    labels = ['0-10', '10-20', '20-30', '30-40', '40-50',
              '50-60', '60-70', '70-80', '80-90', '90-100']

    # Create the binned AGE column
    analysis['AGE_BIN'] = pd.cut(
        analysis['AGE'], bins=bins, labels=labels, right=False)

    # Count the occurrences of each age bin
    age_group_counts = analysis['AGE_BIN'].value_counts().sort_index()
    fig1 = px.bar(
        x=age_group_counts.values,
        y=age_group_counts.index,
        labels={"x": "Number of Cases",
                "y": "Age Group",  "color": "Age Group"},
        title="COVID-19 Cases by Age Group",
        color=age_group_counts.index,
        color_discrete_sequence=px.colors.sequential.Viridis
    )
    st.plotly_chart(fig1)


with tab2:
    st.subheader("Histogram")

    fig2 = px.histogram(
        analysis,
        x="AGE",
        nbins=20,
        labels={"AGE": "Age", "count": "Number of Cases"},
        title="Distribution of COVID-19 Cases by Age",
        color_discrete_sequence=["#636EFA"]
    )

    st.plotly_chart(fig2)

with tab3:
    st.subheader("Data Set")
    st.dataframe(df)
