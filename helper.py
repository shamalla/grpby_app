import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st

def analyze_file(df,label = "File"):
    st.subheader(f"{label} preview")
    num_rows = st.slider(f"Select number of rows to preview - {label}", min_value = 5, max_value = 100, value = 10 )
    st.dataframe(df.head(num_rows))
    #To check columns present
    if "Unnamed:0" in df.columns:
        st.info(f"Please prepare your {label} with Column names as your first row and load again.")
    else:
        with st.expander(f"Columns in {label} present"):
            st.write(df.columns.tolist())
    #Checking for duplicated entries  
    st.subheader(f"Duplicated Rows in {label}")
    df_dup = df.duplicated()
    st.write(df[df_dup].head(10))
    #Drop duplicates if the checkbox is selected
    if st.checkbox(f"Drop all exact duplicate rows in {label}"):
        df = df.drop_duplicates()
        st.success(f"Duplicated rows in {label} are removed")
    #Showing null entries per column
    st.subheader("Missing values per column")
    st.write(df.isnull().sum())
    #Dealing with the null values
    #Using tabs to separete our options for null values
    tab1a,tab2a = st.tabs(["Drop Nulls", "Replace Nulls"])
    with tab1a:
        st.subheader(f"Drop Rows in {label} with Nulls")
        drop_cols_df = st.multiselect("Select columns to DROP rows with missing values:",df.columns.tolist())
        if drop_cols_df:
            before = df.shape[0]
            df = df.dropna(subset = drop_cols_df)
            after = df.shape[0]
            st.warning(f"{before - after} rows droped in {label} due to nulls in selected columns.")
    with tab2a:
        st.subheader("Replace Missing Values")
        replace_cols_df = st.multiselect(f"Select columns to REPLACE missing values in - {label}:", df.columns.tolist())
        if replace_cols_df:
            strategy = st.selectbox("Choose a replacement strategy:",["Replace with 0", "Replace with Custom Text", "Replace with Mean", "Replace with Median","Replace with Mode"]
                                    )
            if strategy == "Replace with 0":
                df[replace_cols_df] = df[replace_cols_df].fillna(0)
                st.success(f"Nulls replaced with 0 in {label}.")
            elif strategy == "Replace with Custom Text":
                custom_value_df = st.text_input("Enter the custom value to use:")
                if custom_value_df:
                    df[replace_cols_df] = df[replace_cols_df].fillna(custom_value_df)
                    st.success(f"Nulls replaced with '{custom_value_df1}' in {label}.")
            elif strategy in ["Replace with Mean", "Replace with Median", "Replace with Mode"]:
                skipped = []
                for col in replace_cols_df:
                    if pd.api.types.is_numeric_dtype(df[col]):
                        if strategy == "Replace with Mean":
                            value = df[col].mean()
                        elif strategy == "Replace with Median":
                            value = df[col].median()
                        elif strategy == "Replace with Mode":
                            Value = df[col].mode()[0] if not df[col].mode().empty else None
                        if value is not None:
                            df[col] == df[col].fillna(value)
                    else:
                        skipped.append(col)
                if skipped:
                    st.warning(f"Skipped non_numeric columns in {label}: {','.join(skipped)}")
                else:
                    st.success(f"Replaced nulls in {label} with {strategy.split()[-1].lower()} values in selected numeric columns.")
    with st.expander(f"Preview Cleaned Data in {label}"):
        st.dataframe(df.head(10))
    #Show summary statistic
    st.subheader(f"Summary statistic - {label}")
    with st.expander(f"A copy of {label} summary statisic"):
        st.write(df.describe(include = "all"))
    #Group by function
    st.subheader(f"Group by statistics for {label}")
    grpby_col = st.multiselect(f"Select column(s) to group by in {label}", df.columns)
    aggf = st.multiselect(f"Select aggregatation function in {label}",["mean", "sum", "count","min", "max"])
    #Select only numeric columns
    numeric_cols = df.select_dtypes(include = "number").columns
    selected_cols = []
    if len(numeric_cols) == 0:
        st.warning(f"No numeric columns available for aggregation in {label}.")
    elif grpby_col:
        selected_cols = st.multiselect(f"Select numeric columns to aggregate in {label}", numeric_cols, default = (numeric_cols))
    if selected_cols and aggf:
        try:
            grouped_df = df.groupby(grpby_col)[selected_cols].agg(aggf)
            st.subheader("Grouped Result")
            st.dataframe(grouped_df)
        except Exception as e:
            st.error(f"Error during grouping in {label}: {e}")
    else:
        st.info("Please select at least one numeric column and one aggregate function to aggregate")
    return df
