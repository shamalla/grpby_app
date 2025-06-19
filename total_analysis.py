import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
st.title = ("Total Analysis")
st.subheader("Upload your file(s)")
file1 = st.file_uploader("Upload file 1", type = ["xlsx","xlx","txt","csv"])
file2 = st.file_uploader("Uploade your file (optional)", type = ["xlsx","xlx","txt","csv"])
dfi , df2 = None, None

#Loaded files
if file1 :
    df1 = pd.read_excel(file1)
    st.success("file 1 has been loaded successfully")
    #preview of the data we have loaded
    st.subheader("File 1 preview")
    num_rows1 = st.slider("Select number of rows to preview", min_value = 5, max_value = 100, value = 10 )
    st.dataframe(df1.head(num_rows))
    #To check columns present
    if "Unnamed:0" in df1.columns:
        st.info("Please prepare your file one with Column names as your first row and load again.")
    else:
        with st.expander("Columns present"):
            st.write(df1.columns.tolist())
    #Checking for duplicated entries  
    st.subheader("Duplicated Rows")
    df1_dup = df1.duplicated()
    st.write(df1[df1_dup].head(10))
    #Drop duplicates if the checkbox is selected
    if st.checkbox("Drop all exact duplicate rows"):
        df1 = df1.drop_duplicates()
        st.success("Duplicated rows are removed")
    #Showing null entries per column
    st.subheader("Missing values per column")
    st.write(df1.isnull().sum())
    #Dealing with the null values
    #Using tabs to separete our options for null values
    tab1a,tab2a = st.tabs(["Drop Nulls", "Replace Nulls"])
    with tab1a:
        st.subheader("Drop Rows with Nulls")
        drop_cols_df1 = st.multiselect("Select columns to DROP rows with missing values:",df1.columns.tolist())
        if drop_cols_df1:
            before = df1.shape[0]
            df1 = df1.dropna(subset = drop_cols_df1)
            after = df1.shape[0]
            st.warning(f"{before - after} rows droped due to nulls in selected columns.")
    with tab2a:
        st.subheader("Replace Missing Values")
        replace_cols_df1 = st.multiselect("Select columns to REPLACE missing values:", df1.columns.tolist())
        if replace_cols_df1:
            strategy = st.selectbox("Choose a replacement strategy:",["Replace with 0", "Replace with Custom Text", "Replace with Mean", "Replace with Median","Replace with Mode"]
                                    )
            if strategy == "Replace with 0":
                df1[replace_cols_df1] = df1[replace_cols_df1].fillna(0)
                st.success(f"Replace nulls in {replace_cols_df1} with 0.")
            elif strategy == "Replace with Custom Text":
                custom_value_df1 = st.text_input("Enter the custom value to use:")
                if custom_value_df1:
                    df1[replace_cols_df1] = df1[replace_cols_df1].fillna(custom_value_df1)
                    st.success(f"Replace nulls in {replace_cols_df1} with '{custom_value_df1}'.")
            elif strategy in ["Replace with Mean", "Replace with Median", "Replace with Mode"]:
                skipped = []
                for col1 in replace_cols_df1:
                    if pd.api.types.is_numeric_dtype(df1[col1]):
                        if strategy == "Replace with Mean":
                            value = df1[col1].mean()
                        elif strategy == "Replace with Median":
                            value = df1[col1].median()
                        elif strategy == "Replace with Mode":
                            Value = df1[col1].mode()[0] if not df1[col1].mode().empty else None
                        if value is not None:
                            df1[col1] == df1[col1].fillna(value)
                    else:
                        skipped.append(col)
                if skipped:
                    st.warning(f"Skipped non_numeric columns: {','.join(skipped)}")
                else:
                    st.success(f"Replace nulls with {strategy.split()[-1].lower()} values in selected numeric columns.")
    with st.expander("Preview Cleaned Data"):
        st.dataframe(df1.head(10))
    #Show summary statistic
    st.subheader("Summary statistic")
    with st.expander("A copy of summary statisic"):
        st.write(df1.describe(include = "all"))
    #Group by function
    st.subheader("Group by statistics")
    grpby_col1 = st.multiselect("Select column(s) to group by", df1.columns)
    aggf1 = st.multiselect("Select aggregatation function",["mean", "sum", "count","min", "max"])
    #Select only numeric columns
    numeric_cols1 = df1.select_dtype(include = "number").columns
    if len(numeric_cols1) == 0:
        st.warning("No numeric columns available")
    elif grpby_col1:
        selected_cols1 = st.multiselect("Select numeric columns to aggregate", numeric_cols1, default = (numeric_cols1))
    if selected_cols1:
        grouped_df1 = df1.groupby(grpby_col1)[selected_cols1].agg(aggf1)
        st.subheader("Grouped Result")
        st.dataframe(grouped_df1)
    else:
        st.info("Please select at least one numeric column to aggregate")
else:
    st.info("Please load your data to begin.")

#Operations to be undertaken on the second file if uploaded
if file2:
    df2.read_excel(file2)   
    st.success("File2 uploaded successfully")
    #Previw of the second dataset that has been loaded 
    st.subheader("File 2 Data preview")
    num_rows2 = st.slider("Select number of rows", min_value = 5, max_value = 100, value = 10)
    st.dataframe(df2.head(num_rows2))
    #To check all present columns
    if "Unnamed:0" in df2.columns:
        st.info("Please prepare your file two with Column names as your first row and load again.")
    else:
        with st.expander("Here is your file two columns"):
            st.write(df2.columns.tolist())
    #Checking for duplicated values
    st.subheader("Duplicated Rows")
    df2_dup = df2.duplicated()
    st.write(df2[df2_dup].head(10))
    #Dealing with duplicated values
    if st.checkbox("Drop all exact duplicate rows"):
        df2 = df2.drop_duplicates()
        st.success("Duplicate rows are removed")
    #Dealing with missing values
    st.subheader("Missing Values per column")
    st.write(df2.isnull().sum())
    #Dealing with null values
    #Using tabs to separate our options
    tab1b,tab2b = st.tabs(["Drop Nulls", "Replace Nulls"])
    with tab1b:
        st.subheader("Drop Rows with Nulls")
        drop_cols_df2 = st.multiselect("Select columns to DROP rows with missing values:",df2.columns.tolist())
        if drop_cols_df2:
            before = df2.shape[0]
            df2 = df2.dropna(subset = drop_cols_df2)
            after = df2.shape[0]
            st.warning(f"{before - after} rows droped due to nulls in selected columns.")
    with tab2b:
        st.subheader("Replace Missing Values")
        replace_cols_df2 = st.multiselect("Select columns to REPLACE missing values:", df2.columns.tolist())
        if replace_cols_df2:
            strategy = st.selectbox("Choose a replacement strategy:",["Replace with 0", "Replace with Custom Text", "Replace with Mean", "Replace with Median","Replace with Mode"]
                                    )
            if strategy == "Replace with 0":
                df2[replace_cols_df2] = df2[replace_cols_df2].fillna(0)
                st.success(f"Replace nulls in {replace_cols_df2} with 0.")
            elif strategy == "Replace with Custom Text":
                custom_value_df2 = st.text_input("Enter the custom value to use:")
                if custom_value_df2:
                    df2[replace_cols_df2] = df2[replace_cols_df2].fillna(custom_value_df2)
                    st.success(f"Replace nulls in {replace_cols_df2} with '{custom_value_df2}'.")
            elif strategy in ["Replace with Mean", "Replace with Median", "Replace with Mode"]:
                skipped = []
                for col2 in replace_cols_df2:
                    if pd.api.types.is_numeric_dtype(df2[col2]):
                        if strategy == "Replace with Mean":
                            value = df2[col2].mean()
                        elif strategy == "Replace with Median":
                            value = df2[col2].median()
                        elif strategy == "Replace with Mode":
                            Value = df2[col2].mode()[0] if not df2[col2].mode().empty else None
                        if value is not None:
                            df2[col2] == df2[col2].fillna(value)
                    else:
                        skipped.append(col2)
                if skipped:
                    st.warning(f"Skipped non_numeric columns: {','.join(skipped)}")
                else:
                    st.success(f"Replace nulls with {strategy.split()[-1].lower()} values in selected numeric columns.")
    with st.expander("Preview Cleaned Data"):
        st.dataframe(df2.head(10))
    #Group by function
    st.subheader("Group by statistics")
    grpby_col1 = st.multiselect("Select column(s) to group by", df1.columns)
    aggf1 = st.multiselect("Select aggregatation function",["mean", "sum", "count","min", "max"])
    #Select only numeric columns
    numeric_cols1 = df1.select_dtype(include = "number").columns
    if len(numeric_cols1) == 0:
        st.warning("No numeric columns available")
    elif grpby_col1:
        selected_cols1 = st.multiselect("Select numeric columns to aggregate", numeric_cols1, default = (numeric_cols1))
    if selected_cols1:
        grouped_df1 = df1.groupby(grpby_col1)[selected_cols1].agg(aggf1)
        st.subheader("Grouped Result")
        st.dataframe(grouped_df1)
    else:
        st.info("Please select at least one numeric column to aggregate")
else:
    st.info("Please load your data to begin.")

    
    


        




      
    


