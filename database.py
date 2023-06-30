import os
from dotenv import load_dotenv
import mysql.connector

load_dotenv('env/.env')

connection = mysql.connector.connect(
    host=os.getenv("HOST"),
    database=os.getenv("DATABASE"),
    user=os.getenv("USERNAME"),
    password=os.getenv("PASSWORD"),
    ssl_ca=os.getenv("SSL_CERT")
)

cursor = connection.cursor()

# Execute a SELECT query
query = "SELECT * FROM courses"
cursor.execute(query)

# Fetch all rows from the result
rows = cursor.fetchall()

# Get column names from the cursor description
columns = [column[0] for column in cursor.description]

# Process the fetched data
result_dicts = []
for row in rows:
    result_dict = dict(zip(columns, row))
    result_dicts.append(result_dict)

# Print the result
print(result_dicts)

# Close the cursor and the connection
cursor.close()
connection.close()


  
