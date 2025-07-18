import pandas as pd
import matplotlib.pyplot as plt 


data = {
    'Name': ['Anirudha', 'Ambika', None, 'Tejas', 'Padmakar'],
    'Age': [27, None, 28, 21, 58],
    'Department': ['Sales', 'HR', 'Finance', 'Sales', 'HR']
    
}


df = pd.DataFrame(data)

df.rename(columns={'OldColumnName': 'NewColumnName'}, inplace=False)
# Read the CSV file
#df = pd.read_csv('test_data.csv')

# Remove any row with a null (NaN) value
df_cleaned = df.dropna()
df = df.dropna(subset=['Name'])

#df['Name']=df['Name'].fillna('unknown')

# Display the cleaned DataFrame
print(df_cleaned)

pivot_table = pd.pivot_table(
    df_cleaned,
    values='Age',
    index='Department',
    aggfunc='max'
)

print("\nPivot Table (Average Age by Department):\n")
print(pivot_table)


plt.plot(df['Name'], df['Age'])
plt.title('Kulkarni Family Age Difference')
plt.show()



#print(df)


# (Optional) Save the cleaned data to a new CSV file
df_cleaned.to_csv('cleaned_test_data.csv', index=True)
 