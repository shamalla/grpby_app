import pandas as pd
import numpy as np
import streamlit as st
import matplotlib.pyplot as plt
from helper import analyze_file

st.title = ("Total Analytics")
st.subheader("Upload your file(s)")
file1 = st.file_uploader("Upload file 1(Required)", type = ["xlsx","xlx","csv"], key = "file1")
file2 = st.file_uploader("Upload your file (optional)", type = ["xlsx","xlx","csv"], key = "file2")
df1 , df2 = None, None

#Loaded files
if file1 :
    xls1 = pd.ExcelFile(file1)
    sheet_names1 = xls1.sheet_names
    selected_sheet1 = st.selectbox("Select sheet to analyze for File 1", sheet_names1, key = "f1")
    df1 = pd.read_excel(file1, sheet_name=selected_sheet1) if file1.name.endswith("xlsx") else pd.read_csv(file1)
    st.success(f"Loaded: {selected_sheet1} from File 1")
if file2:
    xls2 = pd.ExcelFile(file2)
    sheet_names2 = xls2.sheet_names
    selected_sheet2 = st.selectbox("Select sheet to analyze for File 2", sheet_names2,key = "f2")
    df2 = pd.read_excel(file2, sheet_name=selected_sheet2) if file2.name.endswith("xlsx") else pd.read_csv(file2)
    st.success(f"Loaded: {selected_sheet2} from File 2")
if df1 is not None:
    options = ["Analyze File 1 only"]
    if df2 is not None:
        options.extend(["Analyze File 2 only", "Analyze File 1 and File 2 separetly", "Merge File 1 and File 2, then analyze"])
    choice = st.radio("What analysis do you want?",options)

    if choice == "Analyze File 1 only":
        df1 = analyze_file(df1, label="File 1")

    elif choice == "Analyze File 2 only":
        df2 = analyze_file(df2, label ="File 2")

    elif choice == "Analyze File 1 and File 2 separetly":
        st.header("Analysis for File 1")
        df1 = analyze_file(df1, label = "File 1")

        st.markdown("---")

        st.header("Analysis for File 2")
        df2 = analyze_file(df2, label = "File 2")

    elif choice == "Merge File 1 and File 2, then analyze" and df2 is not None:
        #Merging the two data and doing analysis on them
        st.subheader("Clean files before merging")
        #Drop duplicates if user wants
        st.markdown("***Remove duplicates**")
        if st.checkbox("Drop duplicates in File 1"):
            before = df1.shape[0]
            df1 = df1.drop_duplicates()
            after = df1.shape[0]
            st.success(f"{before - after} duplicate rows removed from File 1.")
        if st.checkbox("Drop duplicates in File2"):
            before = df2.shape[0]
            df2 = df2.drop_duplicates()
            after = df2.shape[0]
            st.success(f"{before - after} duplicate rows romeved in File 2.")
        #Drop rows with null values
        st.markdown("**Drop rows with null values**")
        cols1 = st.multiselect("Drop rows in File 1 with null in selected columns:",df1.columns.tolist(),key = "dropna1")
        if cols1:
            before = df1.shape[0]
            df1 = df1.dropna(subset = cols1)
            after = df1.shape[0]
            st.warning(f"{before - after} rows droped from File 1 due to nulls.")
        cols2 = st.multiselect("Drop rows in File 2 with null in selected columns:", df2.columns.tolist(),key ="dropna2")
        if cols2:
            before = df2.shape[0]
            df2 = df2.dropna(subset = cols2)
            after = df2.shape[0]
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
            merged_df = pd.merge(left= df1_subset, right= df2_subset, left_on= merge_col_df1, right_on= merge_col_df2, how= how,suffixes=('_fl1', '_fl2'),indicator=True)
            st.success(f"Successfully merged!Resulting shape{merged_df.shape}")
            st.dataframe(merged_df.head(10))

            both_files = merged_df[merged_df["_merge"] == "both"]
            left_only = merged_df[merged_df["_merge"] == "left_only"]
            right_only = merged_df[merged_df["_merge"] == "right_only"]

            with st.expander("Rows from both files"):
                st.write(f"Shape:{both_files.shape}")
                st.dataframe(both_files.head())
                with st.expander("Summary of Both rows"):
                    st.write(both_files.describe(include = "all"))
                with st.expander("Add or subtract Two numeric columns"):
                    numeric_columns = both_files.select_dtypes(include = "number").columns.tolist()
                    
                    if len(numeric_columns) < 2:
                        st.warning("Need atleast two numeric columns to add or subtract.")

                    else:
                        col1 = st.selectbox("Select first column", numeric_columns,key = "arith_col1")
                        col2 = st.selectbox("Select second column", numeric_columns, key = "arith_col2")
                        operation = st.radio("Choose operation",["Add","Subtract"], key = "arith_oper")

                        if col1 and col2:
                            if "Result" in both_files.columns:
                                both_files.drop(columns =["Result"], inplace=True)
                            if operation == "Add":
                                both_files["Result"] = both_files[col1] + both_files[col2]
                                st.success(f"{col1} + {col2}")
                            else:
                                both_files["Result"] = both_files[col1] - both_files[col2]
                                st.success(f"{col1} - {col2}")

                            with st.expander("Preview of Result"):
                                st.dataframe(both_files[[col1, col2, "Result"]].head(10))
                
            with st.expander("Rows from File 1 only"):
                st.write(f"Shape:{left_only.shape}")
                st.dataframe(left_only.head())
                with st.expander("Summary of files from File 1"):
                    st.write(left_only.describe(include = "all"))

            with st.expander("Rows from File 2 only"):
                st.write(f"Shape:{right_only.shape}")
                st.dataframe(right_only.head())
                with st.expander("Summary of files from File 2"):
                    st.write(right_only.describe(include = "all"))

        except Exception as e:
            st.error(f"Merger failed: {e}")
            
else:
    st.info("Please load your data to begin.")





        

    

        
    


    
    

    

    




