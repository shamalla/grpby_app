import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import pyodbc
import plotly.express as px

#setting the title of the page
st.set_page_config(page_title = "SQL Server Dashboard")
st.title("SQL Server Data viewer")

server = st.text_input("SQL Server",value="localhost")
database = st.text_input("Database",value="database_name")
#user_name = st.text_input("User_name", value = "your user_name")
#password = st.text_input("Password", type = "password")


#A button is placed so that the app can only run if the credentials have been entrered
if st.button("Connect and load your Data"):
    try:
        conn = pyodbc.connect(
            f"DRIVER={{ODBC Driver 17 for SQL Server}};"
            f"SERVER=127.0.0.1,1433;"
            f"DATABASE={database};"
            f"Trusted_Connection=yes;"
            #f"UID={user_name};"
            #f"PWD={password}"
        )

        #sql query to load the data
        query = st.text_area("Enter SQL Query", "SELECT TOP 100 * FROM your_table")

        #Load the data from our question
        df = pd.read_sql(query,conn)
        st.success("Your data has been loaded successfully")

        with st.expander("View your data"):
            st.dataframe(df)

        if not df.empty:
            st.subheader("Plot options")
        #Selecting numeric columns to use for plotting
            numeric_columns = st.select_dtypes(include = ["number"]).column_tolist()
            all_columns = df.columns.to_list()

            x_cols = st.selectbox("Select X_axis columns", all_columns)
            y_cols = st.selectbox("Select Y_axis columns", numeric_columns)

            chart_type = st.radio("Select Chart type",["Line","Bar","Scatter","Histogram"])

            if x_cols and y_cols:
                if chart_type == "Line":
                    fig = px.line(df, x=x_cols, y=y_cols, title=f"{y_cols} vs {x_cols}")
                elif chart_type == "Bar":
                    fig = px.bar(df, x = x_cols, y = y_cols, title = f"{y_cols} vs{x_cols}")
                elif chart_type == "scatter":
                    fig = px.scatter(df, x = x_cols, y = y_cols, title = f"{y_cols} vs{x_cols}")
                elif chart_type == "Histogram":
                    fig = px.histogram(df, x = x_cols, y = y_cols, title = f"{y_cols} vs{x_cols}")
                st.plotly_chart(fig,use_container_width = True)
            else:
                st.warning("Please select both X and Y labels to plot.")
    except Exception as e:
        st.error(f"connection error or query failure\n{e}")    
