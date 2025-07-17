import pandas as pd
import matplotlib.pyplot as plt

# Load CSV file
df = pd.read_csv('sales_email.csv')


print(df)
# Display first few rows
print("Data Preview:")
print(df.head())

# Basic statistics
print("\nSummary Statistics:")
print(df.describe())
print(df.plot(kind='bar', x='Month', y='Sales'))
print(df)

# Visualization: Line Chart for Sales Trend
plt.figure(figsize=(8, 5))
#plt.plot(df['Month'], df['Sales'], marker='o', linestyle='-', color='blue')
plt.title('Monthly Sales Trend')
plt.xlabel('Month')
plt.ylabel('Sales')
plt.grid(True)
plt.show()
