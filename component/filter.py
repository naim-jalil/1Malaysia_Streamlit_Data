import streamlit as st
import pandas as pd


def filter(df):
    df['DATE_OF_FIRST_SYMPTOM'] = pd.to_datetime(
        df['DATE_OF_FIRST_SYMPTOM'], format='%Y-%m-%d')

    df['ADMISSION DATE'] = pd.to_datetime(
        df['ADMISSION DATE'], format='%Y-%m-%d')

    df['DATE_OF_DEATH'] = pd.to_datetime(
        df['DATE_OF_DEATH'], format='%Y-%m-%d')

    # Filter the dataset below
    # st.write("Filter")
    with st.expander("Filter"):
        st.write("Demographics")

        # Create columns
        col1, col2 = st.columns(2)

        with col1:
            sex = st.multiselect(
                "Sex", ["FEMALE", "MALE", "UNKNOWN"])

            if sex:
                df = df[df['SEX'].isin(sex)]

        with col2:
            max_age = df['AGE'].max()
            min_age = df['AGE'].min()
            age = st.slider("AGE",
                            min_age, max_age, (min_age, max_age))

            df = df[(df['AGE'] >= age[0]) & (df['AGE'] <= age[1])]

        col3, col12, col13 = st.columns(3)

        with col3:
            speak_native = st.selectbox(
                "Speaks Native Language", ["All", "YES", "NO"])
            if speak_native != "All":
                df = df[df['SPEAKS_NATIVE_LANGUAGE'] == speak_native]

        with col12:
            origin = st.selectbox(
                "Origin", ["All"] + list(df['ORIGIN'].unique()))

            if origin != "All":
                df = df[df['ORIGIN'] == origin]

        with col13:
            migrant = st.selectbox("Migrant", ["All", "YES", "NO"])
            if migrant != "All":
                df = df[df['MIGRANT'] == migrant]

        sector = st.multiselect(
            "Sector", list(df['SECTOR'].unique()))

        if sector:
            df = df[df['SECTOR'].isin(sector)]

        st.divider()
        st.write("Symptoms")

        col4, col5, col6 = st.columns(3)

        with col4:
            pneumonia = st.selectbox("Pneumonia", ["All", "YES", "NO"])
            if pneumonia != "All":
                df = df[df['PNEUMONIA'] == pneumonia]

            copd = st.selectbox("COPD", ["All", "YES", "NO"])
            if copd != "All":
                df = df[df['COPD'] == copd]

            cardiovascular = st.selectbox(
                "Cardiovascular", ["All", "YES", "NO"])
            if cardiovascular != "All":
                df = df[df['CARDIOVASCULAR'] == cardiovascular]

            obesity = st.selectbox("Obesity", ["All", "YES", "NO"])
            if obesity != "All":
                df = df[df['OBESITY'] == obesity]

        with col5:
            pregnancy = st.selectbox("Pregnancy", ["All", "YES", "NO"])
            if pregnancy != "All":
                df = df[df['PREGNANCY'] == pregnancy]

            asthma = st.selectbox("Asthma", ["All", "YES", "NO"])
            if asthma != "All":
                df = df[df['ASTHMA'] == asthma]

            chronic_kidney = st.selectbox(
                "Chronic Kidney", ["All", "YES", "NO"])
            if chronic_kidney != "All":
                df = df[df['CHRONIC_KIDNEY'] == chronic_kidney]

            tobacco = st.selectbox("Tobacco", ["All", "YES", "NO"])
            if tobacco != "All":
                df = df[df['TOBACCO'] == tobacco]

        with col6:
            diabetes = st.selectbox("Diabetes", ["All", "YES", "NO"])
            if diabetes != "All":
                df = df[df['DIABETES'] == diabetes]

            inmusupr = st.selectbox("Inmunosuppression", ["All", "YES", "NO"])
            if inmusupr != "All":
                df = df[df['INMUSUPR'] == inmusupr]

            hypertension = st.selectbox("Hypertension", ["All", "YES", "NO"])
            if hypertension != "All":
                df = df[df['HYPERTENSION'] == hypertension]

            other_disease = st.selectbox("Other Disease", ["All", "YES", "NO"])
            if other_disease != "All":
                df = df[df['OTHER_DISEASE'] == other_disease]

        col9, col10 = st.columns(2)
        with col9:
            another_case = st.selectbox("Another Case", ["All", "YES", "NO"])
            if another_case != "All":
                df = df[df['ANOTHER_CASE'] == another_case]

        with col10:
            # get date range
            min_date = df['DATE_OF_FIRST_SYMPTOM'].min()
            max_date = df['DATE_OF_FIRST_SYMPTOM'].max()

            date_range = st.date_input(
                "Date of First Symptoms", (min_date, max_date))

            if date_range:
                df = df[(df['DATE_OF_FIRST_SYMPTOM'] >= pd.to_datetime(date_range[0])) &
                        (df['DATE_OF_FIRST_SYMPTOM'] <= pd.to_datetime(date_range[1]))]

        death = st.selectbox("Death", ["All", "YES", "NO"])
        if death == "YES":
            death_date_min = df['DATE_OF_DEATH'].min()
            death_date_max = df['DATE_OF_DEATH'].max()
            death_date = st.date_input(
                "Death Date", (death_date_min, death_date_max))
            if death_date:
                df = df[(df['DATE_OF_DEATH'] >= pd.to_datetime(death_date[0])) &
                        (df['DATE_OF_DEATH'] <= pd.to_datetime(death_date[1]))]
        elif death == "NO":
            df = df[df['DATE_OF_DEATH'].isnull()]

        st.divider()
        st.write("Hospitalization")

        col7, col8 = st.columns(2)

        with col7:
            hospitalized = st.selectbox("Hospitalized", ["All", "YES", "NO"])
            if hospitalized != "All":
                df = df[df['HOSPITALIZED'] == hospitalized]

            addmission_date_min = df['ADMISSION DATE'].min()
            addmission_date_max = df['ADMISSION DATE'].max()
            addmission_date = st.date_input(
                "Admission Date", (addmission_date_min, addmission_date_max
                                   ))
            if addmission_date:
                df = df[(df['ADMISSION DATE'] >= pd.to_datetime(addmission_date[0])) &
                        (df['ADMISSION DATE'] <= pd.to_datetime(addmission_date[1]))]

        with col8:
            icu = st.selectbox("ICU", ["All", "YES", "NO"])
            if icu != "All":
                df = df[df['ICU'] == icu]

            intubar = st.selectbox("Intubated", ["All", "YES", "NO"])
            if intubar != "All":
                df = df[df['INTUBATED'] == intubar]

        st.divider()
        st.write("Outcome")

        outcome = st.selectbox(
            "Outcome", ["All", "POSITIVE", "NEGATIVE", "PENDING"])
        if outcome != "All":
            df = df[df['OUTCOME'] == outcome]

        return df
