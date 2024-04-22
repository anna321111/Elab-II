import pandas as pd


mydf = pd.read_csv('supermarketnew.csv', header=0)
print(len(mydf))
describe = mydf.describe()
print(describe)
print(mydf.head(5))

num_columns = len(mydf.columns)

# Display the DataFrame
print(mydf.head())