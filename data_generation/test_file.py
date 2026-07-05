import pandas as pd 
 
df = pd.read_csv("data/products/product.csv")
print(df.head())
print(df.shape)
print(df.info())
print(df.describe())