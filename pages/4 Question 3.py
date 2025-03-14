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

total_selected = len(df)
st.toast(f"Total Selected Cases: {total_selected:,}")

tab1, tab2 = st.tabs(["Bubble Chart", "Data Set"])

with tab1:
    st.write(f"📌 **Total Selected Cases**: {total_selected:,}")
    # Select the relevant columns
    columns_of_interest = ['DIABETES', 'COPD', 'ASTHMA', 'INMUSUPR', 'HYPERTENSION',
                           'CARDIOVASCULAR', 'OBESITY', 'CHRONIC_KIDNEY', 'TOBACCO', 'ICU']

    # Filter the DataFrame to only include those columns
    df_selected = df[columns_of_interest]

    # Rows where ICU is "YES"
    df_filtered = df_selected[df_selected['ICU'] == 'YES']

    # Drop the ICU column
    df_filtered = df_filtered.drop(columns=['ICU'])

    # Count the number of "YES" for each disease
    yes_counts = (df_filtered == 'YES').sum()

    # Create a DataFrame for plotting
    disease_counts = yes_counts.reset_index()
    disease_counts.columns = ['Disease', 'YES_Count']

    # Create the bubble plot
    fig = px.scatter(disease_counts,
                     x='Disease',
                     y='YES_Count',
                     size='YES_Count',  # Use YES_Count to determine the bubble size
                     title="ICU admitted patients",
                     labels={'YES_Count': "With the disease"},
                     color='YES_Count',
                     color_continuous_scale='Viridis',  # Color scale for bubbles
                     hover_name='Disease',  # Tooltip on hover
                     size_max=60)  # Maximum bubble size

    # Show the plot
    st.plotly_chart(fig)


with tab2:
    st.write(f"📌 **Total Selected Cases**: {total_selected:,}")
    st.dataframe(df)
