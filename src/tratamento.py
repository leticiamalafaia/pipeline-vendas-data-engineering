import pandas as pd

df = pd.read_csv("data/vendas.csv")

print(df.head())

print("\nTipos das colunas:")
print(df.dtypes)

print("\nValores nulos:")
print(df.isnull().sum())

df["data"] = pd.to_datetime(df["data"], format="%Y-%m-%d")

print("\nTipos após tratamento:")
print(df.dtypes)