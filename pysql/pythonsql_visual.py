import pandas as pd
import matplotlib.pyplot as plt
import pyodbc

#connecting to the sql server
conn = pyodbc.connect(
   "DRIVER = {ODBC Driver 17 for SQL Server};"
   "SERVER = your_server_name"
   "DATABASE = Name_of_your_database"
   "UID = your_username"
   "PASSWORD = your_password"
)

#Selecting a querry for data loading
query = "SELECT * FROM your_table"
df = pd.read_sql(query, conn)

#the plotting
fig = plt.figure()
df['your_column'].value_counts().plot(kind='bar')
plt.title("My SQL Data Plot")
plt.show()