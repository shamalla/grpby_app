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
    #preview the rows the user chooses with expander
    num_rows = st.slider("Select number of rows to preview", min_value = 5, max_value = 100, value = 10 )
    with st.expander("File 1 Data preview"):
    st.dataframe(df1.head(num_rows))
    #To check columns present
    if "Unnamed:0" in df1.columns:
        st.info("Please prepare your file two with Column names as your first row and load again.")
    else:
        with st.expander("Columns present"):
        st.write(df1.columns.tolist())
    #Checking for duplicated entries  
    st.subheader("Duplicated entries")
    df1_dup = df1.duplicated()
    st.write(df1[df1_dup].head(10))
    #Drop duplicates if the checkbox is selected
    if st.checkbox("Drop all exact duplicate rows"):
        df1 = df1.drop_duplicates()
        st.info("Duplicated rows are removed")
    #Showing null entries per column
    st.subheader("Missing values per column")
    st.write(df1.isnull().sum())
    #Dealing with the null values
    #Using tabs to separete our options for null values
    tab1,tab2 = st.tabs(["Drop Nulls", "Replace Nulls"])
    with tab1:
        st.subheader("Drop Rows with Nulls")
        drop_cols_df1 = st.multiselect("Select columns to DROP rows with missing values:",df1.columns.tolist())
        if drop_cols_df1:
            before = df1.shape[0]
            df1 = df1.dropna(subset = drop_cols_df1)
            after = df1.shape[0]
            st.warning(f"{before - after} rows droped due to nulls in selected columns.")
    with table2:
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
                    dfi[replace_cols_df1] = df1[replace_cols_df1].fillna(custom_value_df1)
                    st.success(f"Replace nulls in {replace_cols_df1} with '{custom_value_df1}'.")
            elif strategy in ["Replace with Mean", "Replace with Median", "Replace with Mode"]:
                skipped = []
                for col in replace_cols_df1:
                    if pd.api.types.is_numeric_dtype(df1[col]):
                        if strategy == "Replace with Mean":
                            value = df1[col].mean()
                        elif strategy == "Replace with Median":
                            value = df1[col].median()
                        elif strategy == "Replace with Mode":
                            Value = df1[col].mode()[0] if not df1[col].mode().empty else None
                        if value is not None:
                            df1[col] == df1[col].fillna(value)
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
    st.dataframe(df2.head())
    #To check all present columns
    if "Unnamed:0" in df2.columns:
        st.info("Please prepare your file two with Column names as your first row and load again.")
    else:
        st.write(df2.columns.tolist())
    Checking for duplicated values
    

        




      
    


