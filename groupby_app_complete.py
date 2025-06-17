import pandas as pd
import streamlit as st
st.title = ("Groupby analysis")
uploaded_file = st.file_uploader("Upload your file", type = ["xlsx", "xls"])
if uploaded_file is not None:
    df = pd.read_excel(uploaded_file,  header=1)
    st.success("File loaded successfully")
    #Preview of the data we have loaded
    st.subheader("Data Preview")
    st.dataframe(df.head())
    if "Unnamed:0" in df.columns:
        df = df.drop(columns = ["Unnamed:0"])
        st.write(df.columns.tolist())
    #Show missing values
    st.subheader("Missing values per Column")
    st.write(df.isnull().sum())
    #show describe statistics
    st.subheader("Summary statistics")
    st.write(df.describe(include = "all"))
    #Group by Function
    st.subheader("Group by Analysis")
    group_column = st.multiselect("Select a column to group by", df.columns)
    agg_function = st.selectbox("Select aggregation function", ["mean", "sum", "count", "min", "max"])
    #Select only numeric columns
    numeric_cols = df.select_dtypes(include = "number").columns
    if len(numeric_cols) == 0:
        st.warning("No numeric columns available for aggregation.")
    elif group_column:
        selected_cols = st.multiselect("Select numeric columns to aggregate", numeric_cols, default = list(numeric_cols))
    if selected_cols:
        grouped_df = df.groupby(group_column)[selected_cols].agg(agg_function)
        st.subheader("Grouped Result")
        st.dataframe(grouped_df)
else:
    st.info("Please select at least one numeric column to aggregate.")