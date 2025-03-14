# import streamlit as st

def reverse_mapping(df):
    # Define the reverse mappings in a dictionary
    reverse_mappings = {
        "SEX": {"FEMALE": 1, "MALE": 2, "UNKNOWN": 99},
        "HOSPITALIZED": {"NO": 1, "YES": 2, "UNKNOWN": 99},
        "INTUBATED": {"YES": 1, "NO": 2, "DOES NOT APPLY": 97, "IGNORED": 98, "UNKNOWN": 99},
        "PNEUMONIA": {"YES": 1, "NO": 2, "DOES NOT APPLY": 97, "IGNORED": 98, "UNKNOWN": 99},
        "PREGNANCY": {"YES": 1, "NO": 2, "DOES NOT APPLY": 97, "IGNORED": 98, "UNKNOWN": 99},
        "SPEAKS_NATIVE_LANGUAGE": {"YES": 1, "NO": 2, "DOES NOT APPLY": 97, "IGNORED": 98, "UNKNOWN": 99},
        "DIABETES": {"YES": 1, "NO": 2, "DOES NOT APPLY": 97, "IGNORED": 98, "UNKNOWN": 99},
        "COPD": {"YES": 1, "NO": 2, "DOES NOT APPLY": 97, "IGNORED": 98, "UNKNOWN": 99},
        "ASTHMA": {"YES": 1, "NO": 2, "DOES NOT APPLY": 97, "IGNORED": 98, "UNKNOWN": 99},
        "INMUSUPR": {"YES": 1, "NO": 2, "DOES NOT APPLY": 97, "IGNORED": 98, "UNKNOWN": 99},
        "HYPERTENSION": {"YES": 1, "NO": 2, "DOES NOT APPLY": 97, "IGNORED": 98, "UNKNOWN": 99},
        "OTHER_DISEASE": {"YES": 1, "NO": 2, "DOES NOT APPLY": 97, "IGNORED": 98, "UNKNOWN": 99},
        "CARDIOVASCULAR": {"YES": 1, "NO": 2, "DOES NOT APPLY": 97, "IGNORED": 98, "UNKNOWN": 99},
        "OBESITY": {"YES": 1, "NO": 2, "DOES NOT APPLY": 97, "IGNORED": 98, "UNKNOWN": 99},
        "CHRONIC_KIDNEY": {"YES": 1, "NO": 2, "DOES NOT APPLY": 97, "IGNORED": 98, "UNKNOWN": 99},
        "TOBACCO": {"YES": 1, "NO": 2, "DOES NOT APPLY": 97, "IGNORED": 98, "UNKNOWN": 99},
        "ANOTHER CASE": {"YES": 1, "NO": 2, "DOES NOT APPLY": 97, "IGNORED": 98, "UNKNOWN": 99},
        "MIGRANT": {"YES": 1, "NO": 2, "DOES NOT APPLY": 97, "IGNORED": 98, "UNKNOWN": 99},
        "ICU": {"YES": 1, "NO": 2, "DOES NOT APPLY": 97, "IGNORED": 98, "UNKNOWN": 99},
        "OUTCOME": {"POSITIVE": 1, "NEGATIVE": 2, "PENDING": 3},
        "NATIONALITY": {"MEXICAN": 1, "FOREIGN": 2, "UNKNOWN": 99}
    }

    # Apply reverse mapping to each column in the DataFrame
    for column, mapping in reverse_mappings.items():
        if column in df.columns:  # Check if the column exists in the DataFrame
            df[column] = df[column].map(mapping)

    return df
