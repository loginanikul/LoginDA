import sqlite3
import pandas as pd

# Connect to SQLite Database
conn = sqlite3.connect('sales.db')

# SQL Query
query = """
SELECT region, SUM(sales_amount) AS total_sales
FROM sales_data
GROUP BY region
ORDER BY total_sales DESC
"""

# Execute Query & Load to DataFrame
df = pd.read_sql_query(query, conn)

print(df)
