import pandas as pd
import numpy as np
import streamlit as st
import matplotlib.pyplot as plt
from helper import analyze_file

st.title = ("Total Analytics")
st.subheader(f"Karibu. Welcome. Bienvenue... Please upload your file(s).")
st.markdown("**Note:** Please ensure the first row of your file contains the column headers before uploading.")
file1 = st.file_uploader("Upload file 1(Required)", type = ["xlsx","xlx","csv"], key = "file1")
file2 = st.file_uploader("Upload your file (optional)", type = ["xlsx","xlx","csv"], key = "file2")
df1 , df2 = None, None

#---optional: Let the user select which row to use as header---
#st.markdown("(Experimental) Choose which row to use as column header:")
#header_row = st.number_input("Row number(starting from 0)",min_value = 0,step=1,value=0)
# if file1:
#     df1 = pd.read_excel(file1, sheet_name=selected_sheet1, header=header_row)
# if file2:
#     df2 = pd.read_excel(file2, sheet_name=selected_sheet2, header=header_row)

#option2
#select_custom_header = st.checkbox("Manually select header row",value = False)
# if use_custom_header:
#     header_row = st.number_input("Select header row index (0-based)", min_value=0, value=0)
#     df1 = pd.read_excel(file1, sheet_name=selected_sheet1, header=header_row)
# else:
#     df1 = pd.read_excel(file1, sheet_name=selected_sheet1)

#Loaded files
if file1 :
    xls1 = pd.ExcelFile(file1)
    sheet_names1 = xls1.sheet_names
    selected_sheet1 = st.selectbox("Select sheet to analyze for File 1", sheet_names1, key = "f1")
    df1 = pd.read_excel(file1, sheet_name=selected_sheet1,header=0) if file1.name.endswith("xlsx") else pd.read_csv(file1,header=0)
    st.success(f"Loaded: {selected_sheet1} from File 1")
if file2:
    xls2 = pd.ExcelFile(file2)
    sheet_names2 = xls2.sheet_names
    selected_sheet2 = st.selectbox("Select sheet to analyze for File 2", sheet_names2,key = "f2")
    df2 = pd.read_excel(file2, sheet_name=selected_sheet2,header=0) if file2.name.endswith("xlsx") else pd.read_csv(file2,header=0)
    st.success(f"Loaded: {selected_sheet2} from File 2")
if df1 is not None:
    options = ["Analyze File 1 only"]
    if df2 is not None:
        options.extend(["Analyze File 2 only", "Analyze File 1 and File 2 separetly", "Reconcile File 1 and File 2"])
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

    elif choice == "Reconcile File 1 and File 2" and df2 is not None:
        #Merging the two data and doing analysis on them
        st.subheader("Clean files before merging")
        #Drop duplicates if user wants
        st.markdown("**Deaaling with duplicates**")
        with st.expander("Duplicate rows in File 1"):
            df1_dup = df1.duplicated()
            st.write(df1[df1_dup].head(10))
        with st.expander("Duplicate rows in File 2"):
            df2_dup = df2.duplicated()
            st.write(df2[df2_dup].head(10))

        st.markdown("***Remove duplicated rows**")
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
        st.markdown("**Dealing with Null values**")
        with st.expander("Missing values per column"):
            st.write(df1.isnull().sum())
            st.write(df2.isnull().sum())
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

        use_pivot = st.checkbox("Use Pivot Tables to get unique entries")
        if use_pivot:
            st.markdown("### Pivot Table for File 1")
            with st.expander("Create Pivot Table for File 1"):
                pv_idx_df1 = st.multiselect(f"Select columns to use as index in df1",df1.columns, key = "pv_id_df1")
                pv_col_df1 = st.multiselect(f"Select columns to split horizontally in df1 (optional)",df1.columns, key = "pv_cl_df1")
                pv_aggf_df1 = st.selectbox(f"Select an aggregate function to aggregate in df1",["mean","sum","count","min","max"], key = "pv_agg_df1") 
                pv_numeric_val_df1 = df1.select_dtypes(include = "number").columns
                if len(pv_numeric_val_df1) == 0:
                    st.warning(f"No numeric columns availlable for aggregation in df1.") 
                    pv_values_df1 = []
                else:
                    pv_values_df1 = st.multiselect(f"Select numeric columns to aggregate in df1",pv_numeric_val_df1, default = list(pv_numeric_val_df1), key ="pv_num_df1")
                if  pv_idx_df1 and pv_values_df1 and pv_aggf_df1:
                    try:
                        pv_table_df1 = df1.pivot_table(index =pv_idx_df1 ,columns = pv_col_df1 if pv_col_df1 else None,values= pv_values_df1,aggfunc = pv_aggf_df1, fill_value = 0)
                        pv_table_df1.columns = ['_'.join(map(str, col)).strip() if isinstance(col, tuple) else col for col in pv_table_df1.columns]
                        pv_table_df1.reset_index(inplace = True)
                        with st.expander(f"Review your File 1 pivot table"):
                            num_rows = st.slider("Select number of rows to preview ", min_value = 5, max_value = 1000, value = 10,key = "pv_df1" )
                            st.dataframe(pv_table_df1)   
                            st.write(f"Pivot table shape: {pv_table_df1.shape}")
                    except Exception as e:
                        st.error(f"Error during pivot_tabling in File 1: {e}")

            st.markdown("### Pivot Table for File 2")
            with st.expander("Create Pivot Table for File 2"):
                pv_idx_df2 = st.multiselect(f"Select columns to use as index in df1",df2.columns, key = "pv_id_df2")
                pv_col_df2 = st.multiselect(f"Select columns to split horizontally in df1 (optional)",df2.columns, key = "pv_cl_df2")
                pv_aggf_df2 = st.selectbox(f"Select an aggregate function to aggregate in df2",["mean","sum","count","min","max"], key = "pv_agg_df2") 
                pv_numeric_val_df2 = df2.select_dtypes(include = "number").columns
                if len(pv_numeric_val_df2) == 0:
                    st.warning(f"No numeric columns availlable for aggregation in df2.") 
                    pv_values_df2 = []
                else:
                    pv_values_df2 = st.multiselect(f"Select numeric columns to aggregate in df2",pv_numeric_val_df2, default = list(pv_numeric_val_df2),key = "pv_num_df2")
                if  pv_idx_df2 and pv_values_df2 and pv_aggf_df2:
                    try:
                        pv_table_df2 = df2.pivot_table(index =pv_idx_df2 ,columns = pv_col_df2 if pv_col_df2 else None,values= pv_values_df2,aggfunc = pv_aggf_df2, fill_value = 0)
                        pv_table_df2.columns = ['_'.join(map(str, col)).strip() if isinstance(col, tuple) else col for col in pv_table_df2.columns]
                        pv_table_df2.reset_index(inplace = True)
                        with st.expander(f"Review your File 2 pivot table"):
                            num_rows = st.slider("Select number of rows to preview ", min_value = 5, max_value = 1000, value = 10, key = "pv_df2" )
                            st.dataframe(pv_table_df2)   
                            st.write(f"Pivot table shape: {pv_table_df2.shape}")
                    except Exception as e:
                        st.error(f"Error during pivot_tabling in File 2: {e}")  

            
        st.subheader("Reconciliation analysis")
        base_df1 = pv_table_df1 if use_pivot and "pv_table_df1" in locals() else df1
        base_df2 = pv_table_df2 if use_pivot and "pv_table_df2" in locals() else df2
        #Select columns to merge on which have same data in each file1
        merge_col_df1 = st.selectbox("Select column to merge on from File 1",base_df1.columns, key = "merge_col1")
        merge_col_df2 = st.selectbox("Select column to merge on from File 2",base_df2.columns, key = "merge_col2")

        #How do you want to merge your data
        how = st.selectbox("Choose merge type:",["inner","outer","left","right"])
        #To input a function that now removes duplicate by inputing a suffix 
        #def safe_rename_columns(df, merge_col,suffix):
            #cols = df.columns.tolist()
            #seen = {}
            #new_base_cols = []
            #for col in cols:
                #if col not in seen:
                    #seen[col] = 1
                    #new_base_cols.append(col)
                #else:
                    #count = seen[col]
                    #new_name = f"{col}_{count}"
                    #while new_name in seen:
                        #count += 1
                        #new_name = f"{col}_{count}"
                    #seen[col] = count + 1
                    #seen[new_name] = 1
                    #new_base_cols.append(new_name)
            #df.columns = new_base_cols

            # Step 2: Add suffix except for merge column
            #final_cols = []
            #for col in df.columns:
                #if col == merge_col:
                    #final_cols.append(col)
                #else:
                    #final_cols.append(f"{col}_{suffix}")
            #df.columns = final_cols
            #return df


        #Columns to be included in our merge
        cols_inc = st.radio("Columns to include in the reconciliation",["Use all columns","Select specific_columns"])
        default_df1 = list(set([merge_col_df1]) | set(base_df1.columns.tolist()))
        default_df2 = list(set([merge_col_df2]) | set(base_df2.columns.tolist()))
        if cols_inc == "Select specific_columns":
            cols_df1 = st.multiselect("Select columns to be included from df1",options=base_df1.columns.tolist(), default=[col for col in default_df1 if col in base_df1.columns],key="col_d_f1")
            cols_df2 = st.multiselect("Select columns to be included from File 2",options=base_df2.columns.tolist(),default=[col for col in default_df2 if col in base_df2.columns],key="col_d_f2")
            #Ensuring merged columns are included
            if merge_col_df1 not in cols_df1:
                cols_df1.append(merge_col_df1)
            if merge_col_df2 not in cols_df2:
                cols_df2.append(merge_col_df2)
            df1_subset = base_df1[cols_df1].copy()
            df2_subset = base_df2[cols_df2].copy()

        else:
            df1_subset = base_df1.copy()
            df2_subset = base_df2.copy()
            #perform the merge function
        try:
            merged_df = pd.merge(left= df1_subset, right= df2_subset, left_on= merge_col_df1, right_on= merge_col_df2, how= how,suffixes=('_fl1', '_fl2'),indicator=True)
            st.success(f"Successfully merged!Resulting shape{merged_df.shape}")
            st.dataframe(merged_df.head(10))

            both_files = merged_df[merged_df["_merge"] == "both"]
            left_only = merged_df[merged_df["_merge"] == "left_only"]
            right_only = merged_df[merged_df["_merge"] == "right_only"]

                #Rows from all the tables
            with st.expander("Rows from both files"):
                st.write(f"Shape:{both_files.shape}")
                st.dataframe(both_files.head())
                with st.expander("Summary of Both rows"):
                    st.write(both_files.describe(include = "all"))

                    #result_df = both_files.copy()
                with st.expander("Add or subtract Two numeric columns"):
                    numeric_columns = both_files.select_dtypes(include = "number").columns.tolist()
                    all_columns = both_files.columns.tolist()
                    
                    if len(numeric_columns) < 2:
                        st.warning("Need atleast two numeric columns to add or subtract.")

                    else:
                        col1 = st.selectbox("Select first column", numeric_columns,key = "arith_col1")
                        col2 = st.selectbox("Select second column", numeric_columns, key = "arith_col2")

                        id_column_option = [col for col in all_columns if col not in [col1,col2]]
                        id_col = st.selectbox("select an identifier column to include", id_column_option, key= "id_col")
                        operation = st.radio("Choose operation",["Add","Subtract"], key = "arith_oper")

                            #merge_key_col = merge_col_df1 if merge_col_df1 in both_files.columns else merge_col_df2
                        selected_columns = [id_col,col1,col2]     
                        result_df = both_files[selected_columns].copy()
                            #possible_merge_cols = [merge_col_df1, merge_col_df2, f"{merge_col_df1}_fl1", f"{merge_col_df2}_fl2"]
                            #merge_key_col = next((col for col in possible_merge_cols if col in both_files.columns), None)
                        if col1 !=col2:   
                                #if merge_key_col: #= merge_col_df1 if merge_col_df1 in both_files.columns else merge_col_df2
                                    #selected_columns = [merge_key_col,col1,col2]     
                                #result_df = both_files[selected_columns].copy()  
                                #result_df = both_files[[merge_col_df1,col1,col2]].copy()
                                #result_df = both_files.copy()
                            if "Result" in result_df.columns:
                                result_df.drop(columns =["Result"], inplace=True)
                            if operation == "Add":
                                result_df["Result"] = result_df[col1] + result_df[col2]
                                st.success(f"Successfully added:{col1} + {col2}")
                            else:
                                result_df["Result"] = result_df[col1] - result_df[col2]
                                st.success(f"Successfully subtracted:{col1} - {col2}")

                            num_rows = st.slider("Select number of rows to preview ", min_value = 5, max_value = 1000, value = 10 )
                            st.dataframe(result_df[[id_col,col1, col2, "Result"]].head(num_rows))
                            with st.expander("Summary of the Result"):
                                st.write(result_df.describe(include="all"))

                            between_df_files = result_df[result_df["Result"].between(-10 , 10)]
                            outside_result = result_df[~result_df["Result"].between(-10 , 10)]              
                            with st.expander(f"Data from both Files that reconciliation is between (-10 and 10)"):
                                num_rows = st.slider("Select number of rows to preview ", min_value = 5, max_value = 1000, value = 10,key ="preview_between" )
                                st.dataframe(between_df_files[[id_col, col1, col2,"Result"]].head(num_rows))

                            with st.expander(f"Data from both Files that reconcilliation is greater than (-10 and 10)"):
                                num_rows = st.slider("Select number of rows to preview ", min_value = 5, max_value = 1000, value = 10,key = "preview_outside" )
                                st.dataframe(outside_result[[id_col,col1,col2,"Result"].head(num_rows)])                

                                    #with st.expander("Preview of Result"):
                                        #st.dataframe(result_df[[col1, col2, "Result"]].head(10))
                
                #Rows from Left table only
            with st.expander("Rows from File 1 only"):
                st.write(f"Shape:{left_only.shape}")
                st.dataframe(left_only.head())
                with st.expander("Summary of files from File 1"):
                    st.write(left_only.describe(include = "all"))

                #Rows from right Table only
            with st.expander("Rows from File 2 only"):
                st.write(f"Shape:{right_only.shape}")
                st.dataframe(right_only.head())
                with st.expander("Summary of files from File 2"):
                    st.write(right_only.describe(include = "all"))

        except Exception as e:
            st.error(f"Merger failed: {e}")
            
else:
    st.info("Please load your data to begin.")





        

    

        
    


    
    

    

    




