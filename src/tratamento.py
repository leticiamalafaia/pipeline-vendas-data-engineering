import pandas as pd

df = pd.read_csv("data/vendas.csv")

print(df.head())

print("\nTipos das colunas:")
print(df.dtypes)

print("\nValores nulos:")
print(df.isnull().sum())

df["data"] = pd.to_datetime(df["data"], format="%Y-%m-%d")

df["faturamento"] = df["quantidade"] * df["preco"]

df.to_csv("data/vendas_tratadas.csv", index=False)

print("\nDados com faturamento:")
print(df[["produto", "quantidade", "preco", "faturamento"]])

print("\nTipos após tratamento:")
print(df.dtypes)