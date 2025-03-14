import plotly.express as px
from component.filter import filter
import streamlit as st
import pandas as pd
import os

st.set_page_config(
    page_icon=":shark:", layout="wide"
)

st.title("How many patients required intubation?")

df = pd.read_csv(os.path.join("assets", "mapped_data.csv"))
df = filter(df)

total_selected = len(df)
st.toast(f"Total Selected Cases: {total_selected:,}")

tab1, tab2 = st.tabs(["Bar Chart", "Data Set"])

analysis = df.copy()

# Define age bins
bins = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
labels = ["0-10", "10-20", "20-30", "30-40", "40-50",
          "50-60", "60-70", "70-80", "80-90", "90-100"]

# Bin the AGE column
analysis["AGE_GROUP"] = pd.cut(
    analysis["AGE"], bins=bins, labels=labels, right=False)

with tab1:
    st.write(f"📌 **Total Selected Cases**: {total_selected:,}")
    # Count intubated patients
    intubated_counts = analysis["INTUBATED"].value_counts().reset_index()
    intubated_counts.columns = ["INTUBATED", "COUNT"]

    # Bar chart for patients requiring intubation
    # Plotting the horizontal bar chart
    fig4 = px.bar(
        intubated_counts,
        x="COUNT",
        y="INTUBATED",
        labels={"INTUBATED": "Intubation Status",
                "COUNT": "Number of Patients"},
        color="INTUBATED",
        color_discrete_sequence=px.colors.qualitative.Set2
    )
    st.plotly_chart(fig4)


with tab2:
    st.write(f"📌 **Total Selected Cases**: {total_selected:,}")
    st.dataframe(df)
