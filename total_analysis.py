import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
st.title = ("Total Analysis")
st.subheader("Upload your file(s)")
file1 = st.file_uploader("Upload file 1(Required)", type = ["xlsx","xlx","txt","csv"], key = "file1")
file2 = st.file_uploader("Uploade your file (optional)", type = ["xlsx","xlx","txt","csv"], key = "file2")
df1 , df2 = None, None

#Loaded files
if file1 :
    df1 = pd.read_excel(file1) if file1.name.endswith["xlsx", "xls"] else pd.read_csv(file1)
if file2:
    df2 = pd.read_excel(file2) if file.name.endswith["xlsx", "xls"] else pd.read_csv(file2)
if df1 is not None:
    st.success("file 1 has been loaded successfully")
    analysis_option = ["Analyze file 1 only"]
    if df2 is not None:
        st.success("file 2 has been loaded successfully")
        analysis_option.extend(["Analyze file 2 only", "Analyze file 1 and file 2 separetly", "Merge file 1 and file 2, then analyze "])

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
        st.warning("No numeric columns available for aggregation.")
    elif grpby_col1:
        selected_cols1 = st.multiselect("Select numeric columns to aggregate", numeric_cols1, default = (numeric_cols1))
    if selected_cols1 and aggf1:
        try:
            grouped_df1 = df1.groupby(grpby_col1)[selected_cols1].agg(aggf1)
            st.subheader("Grouped Result")
            st.dataframe(grouped_df1)
        except Exception as e:
            st.error(f"Error while grouping: {e}")
    else:
        st.info("Please select at least one numeric column and one aggregate function to aggregate")
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
    grpby_col2 = st.multiselect("Select column(s) to group by", df2.columns)
    aggf2 = st.multiselect("Select aggregatation function",["mean", "sum", "count","min", "max"])
    #Select only numeric columns
    numeric_cols2 = df2.select_dtype(include = "number").columns
    if len(numeric_cols2) == 0:
        st.warning("No numeric columns available for aggregation")
    elif grpby_col2:
        selected_cols2 = st.multiselect("Select numeric columns to aggregate", numeric_cols2, default = (numeric_cols2))
    if selected_cols2 and aggf2:
        try:
            grouped_df2 = df2.groupby(grpby_col2)[selected_cols2].agg(aggf2)
            st.subheader("Grouped Result")
            st.dataframe(grouped_df2)
        except Exception as e1:
            st.error(f"error while grouping: {e1}")
    else:
        st.info("Please select at least one numeric column and one ggregate function to aggregate")
else:
    st.info("Please load your second data to begin.")
    
    #Merging the two data and doing analysis on them
    st.subheader("Clean files before merging")
    #Drop duplicates if user wants
    st.markdown("***Remove duplicates**")
    if st.checkbox("Drop duplicates in File 1"):
        before = df1.shape[]
        df1 = df1.drop_duplicates()
        after = df1.shape[]
        st.success(f"{befor - after} duplicate rows removed from File 1.")

    if st.checkbox("Drop duplicates in File2"):
        before = df2.shape[]
        df2 = df2.drop_duplicates()
        after = df2.shape[]
        st.success(f"{before - after} duplicate rows romeved in File 2.")

    #Drop rows with null values
    st.markdown("**Drop rows with null values**")
    cols1 = st.multiselect("Drop rows in File 1 with null in selected columns:",df1.columns.tolist(),key = "dropna1")
    if cols1:
        before = df1.shape[]
        df1 = df1.dropna(subset = cols1)
        after = df2.shape[]
        st.warning(f"{before - after} rows droped frop File 1 due to nulls.")
    cols2 = st.multiselect("Drop rows in File 2 with null in selected columns:", df2.columns.tolist(),key ="dropna2")
    if cols2:
        before = df1.shape[]
        df2 = df2.dropna(subset = cols2)
        st.warning(f"{before - after} rows droped from File 2 due to nulls.")

    st.subheader("Merging analysis")

    #Select columns to merge on which have same data in each file1
    merge_col_df1 = st.selectbox("Select column to merge on from File 1",df1.columns, key = "merge_col1")
    merge_col_df2 = st.selectbox("Select column to mergr on from File 2",df2.columns, key = "merge_col2")

    #How do you want to merge your data
    how = st.selectbox("Choose merge type:",["inner","outer","left","right"])

    #Columns to be included in our merge
    cols_inc = st.radio("Columns to include in the merge analysis",["Use all colums","Select specific_columns"])
    if cols_inc == "Select specific_columns":
        cols_df1 = st.multiselect("Select columns to be included from df1",df1.columns.tolist(), default = [merge_col_df1], key = "col_d_f1")
        cols_df2 = st.multiselect("Select columns to be included from File 2",df2.columns.tolist(), default = [merge_col_df2], key = "col_d_f2")
        #Ensuring merged columns are included
        if merge_col_df1 not in cols_df1:
            cols_df1.append(merge_col_df1)
        if merge_col_df2 not in cols_df2:
            cols_df2.append(merge_col_df2)
        df1_subset = df1[cols_df1]
        df2_subset = df2[cols_df2]
    else:
        df1_subset = df1
        df2_subset = df2

    #perform the merge function
    try:
        merged_df = pd.merge(left= df1_subset, right= df2_subset, left_on= merge_col_df1, right_on= merge_col_df2, how= how,indicator=True)
        st.success(f"Successfully merged!Resulting shape{merged_df.shape}")
        st.dataframe(merged_df.head(10))

        both_files = merged_df[merged_df["_merge"] == "both"]
        left_only = merged_df[merged_df["_merge"] == "left_only"]
        right_only = merged_df[merged_df["_merge"] == "right_only"]

        with st.expander("Rows from both files"):
            st.write(f"Shape:{both_files}")
            st.dataframe(both_files.head())
            with st.expander("Summary of Both rows"):
                st.write(both_files.describe(include = "all"))

        with st.expander("Rows from File 1 only"):
            st.write(f"Shape:{left_only}")
            st.dataframe(left_only.head())
            with st.expander("Summary of files from File 1"):
                st.write(left_only.describe(include = "all"))

        with st.expander("Rows from File 2 only"):
            st.write(f"Shape:{right_only}")
            st.dataframe(right_only.head())
            with st.expander("Summary of files from File 2"):
                st.write(right_only.describe(include = "all"))

    except Exception as e:
        st.error(f"Merge faile: {e}")



        with st.expander("Insight of analysed data"):
            st.subheader()
     
     
        #df1_subset = safe_rename_columns(df1_subset, merge_col_df1, "fl1")
        #df2_subset = safe_rename_columns(df2_subset, merge_col_df2, "fl2")

        #common_cols = set(df1_subset.columns) & set(df2_subset.columns)
        #if common_cols:
            #st.error(f" Merge failed: Still found duplicate columns: {list(common_cols)}")
        #else:


    #dirty linen
    st.subheader(f"Analytics for {label}")
    with st.expander(f"Groupby Analytics for {label}")
    grpby_col = st.multiselect(f"Select column(s) to group by in {label}", df.columns)
    aggf = st.multiselect(f"Select aggregatation function in {label}",["mean", "sum", "count","min", "max"])
    #Select only numeric columns
    numeric_cols = df.select_dtypes(include = "number").columns
    selected_cols = []
    if len(numeric_cols) == 0:
        st.warning(f"No numeric columns available for aggregation in {label}.")
    elif grpby_col:
        selected_cols = st.multiselect(f"Select numeric columns to aggregate in {label}", numeric_cols, default = list(numeric_cols))
    if selected_cols and aggf and grpby_col:
        try:
            grouped_df = df.groupby(grpby_col)[selected_cols].agg(aggf)
            grouped_df.columns = ['_'.join(col).strip() if isinstance(col, tuple) else col for col in grouped_df.columns.values]
            grouped_df.reset_index(inplace=True)
            st.subheader("Grouped Result")
            num_rows = st.slider("Select number of rows to preview ", min_value = 5, max_value = 1000, value = 10 )
            st.dataframe(grouped_df)
        except Exception as e:
            st.error(f"Error during grouping in {label}: {e}")
    else:
        st.info("Please select at least one numeric column and one aggregate function to aggregate")
    return df

        



    

    
    


        




      
    


