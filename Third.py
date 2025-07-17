from tabulate import tabulate
import pandas as pd
import matplotlib.pyplot as plt
from pandasql import sqldf

df = pd.read_csv('Sales_email.csv')
print(df)

query = "SELECT * FROM df WHERE email LIKE '%@gmail.com%'"
result = sqldf(query)

# Create a new column to classify emails
# df['email_type'] = df['email'].apply(lambda x: 'Gmail' if '@gmail.com' in str(x) else 'Other')
# counts = df['email_type'].value_counts()

# plt.figure(figsize=(6, 6))
# #plt.pie(counts, labels=counts.index.astype(str).tolist(), autopct='%1.1f%%', startangle=90, colors=['#66b3ff', '#ff9999'])
# plt.title('Email Distribution: Gmail vs Other')
# plt.show()

# Pretty-print with tabulate
if result is not None:
    print(tabulate(result, headers='keys', tablefmt='grid', showindex=False))
else:
    print("No results found.")

