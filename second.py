from os import preadv
import pandas as pd
import matplotlib.pyplot as plt

test_data =[
    {'Month': 'Jan', 'Sales': 100},
    {'Month': 'Feb', 'Sales': 120},
    {'Month': 'Mar', 'Sales': 90},
    {'Month': 'Apr', 'Sales': 150},
    {'Month': 'May', 'Sales': 130},
]

df = pd.DataFrame(test_data)
print(df.head(1))

print(df.tail(1))

print(df.info())

print(df.describe())

print(df.plot(kind='line', x='Month', y='Sales'))

plt.show()  
