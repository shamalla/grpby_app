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
        drop_cols_df = st.multiselect("Select columns to DROP rows with missing values:",df.columns.tolist(),key = f"drop_col_{label}")
        if drop_cols_df:
            before = df.shape[0]
            df = df.dropna(subset = drop_cols_df)
            after = df.shape[0]
            st.warning(f"{before - after} rows droped in {label} due to nulls in selected columns.")
    with tab2a:
        st.subheader("Replace Missing Values")
        replace_cols_df = st.multiselect(f"Select columns to REPLACE missing values in - {label}:", df.columns.tolist(),key = f"replace_col_{label}")
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
                    st.success(f"Nulls replaced with '{custom_value_df}' in {label}.")
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
    st.subheader(f"Analytics for {label}")
    with st.expander(f"Groupby Analytics for {label}"):
        grpby_col = st.multiselect(f"Select column(s) to group by in {label}", df.columns, key = f"gr_col_{label}")
        grp_aggf = st.multiselect(f"Select aggregatation function in {label}",["mean", "sum", "count","min", "max"],key = f"gr_ag_{label}")
    #Select only numeric columns
        numeric_cols = df.select_dtypes(include = "number").columns
        selected_cols = []
        if len(numeric_cols) == 0:
            st.warning(f"No numeric columns available for aggregation in {label}.")
        elif grpby_col:
            selected_cols = st.multiselect(f"Select numeric columns to aggregate in {label}", numeric_cols, default = list(numeric_cols),key = f"gr_sel_cl_{label}")
        if selected_cols and grp_aggf and grpby_col:
            try:
                grouped_df = df.groupby(grpby_col)[selected_cols].agg(grp_aggf)
                grouped_df.columns = ['_'.join(col).strip() if isinstance(col, tuple) else col for col in grouped_df.columns.values]
                grouped_df.reset_index(inplace=True)
                st.subheader("Grouped Result")
                num_rows = st.slider("Select number of rows to preview ", min_value = 5, max_value = 1000, value = 10 )
                st.dataframe(grouped_df)
            except Exception as e:
                st.error(f"Error during grouping in {label}: {e}")
        else:
            st.info("Please select at least one numeric column and one aggregate function to aggregate")  
            


    with st.expander(f"Pivot Table for{label}"):
        pv_idx_col = st.multiselect(f"Select columns to use as index in {label}",df.columns, key = f"pv_id_{label}")
        pv_col = st.multiselect(f"Select columns to split horizontally in {label}",df.columns, key = f"pv_cl_{label}")
        pv_aggf = st.multiselect(f"Select an aggregate function to aggrgate in {label}",["mean","sum","count","min","max"], key = f"pv_n_cl_{label}")
        pv_numeric_val = df.select_dtypes(include = "number").columns
        if len(pv_numeric_val) == 0:
            st.warning(f"No numeric columns availlable for aggregation in {label}.") 
            pv_values = []
        else:
            pv_values = st.multiselect(f"Select numeric columns to aggregate in {label}",pv_numeric_val, default = list(pv_numeric_val))
        if  pv_idx_col and pv_values and pv_aggf:
            try:
                pv_table = df.pivot_table(index =pv_idx_col ,columns = pv_col if pv_col else None,values= pv_values,aggfunc = pv_aggf if len(pv_aggf) > 1 else pv_aggf[0], fill_value = 0)
                pv_table.columns = ['_'.join(map(str, col)).strip() if isinstance(col, tuple) else col for col in pv_table.columns]
                pv_table.reset_index(inplace = True)
                st.dataframe(pv_table)
            except Exception as e:
                st.error(f"Error during pivot_tabling in {label}: {e}")
        else:
            st.info("Please select at least one index column,one numeric column and one aggregate function to aggregate")
    return df
