import pandas as pd


def carregar_dados():
    return pd.read_csv("data/vendas.csv")


def validar_dados(df):
    print(df.head())

    print("\nTipos das colunas:")
    print(df.dtypes)

    print("\nValores nulos:")
    print(df.isnull().sum())


def transformar_dados(df):
    df["data"] = pd.to_datetime(df["data"], format="%Y-%m-%d")
    df["faturamento"] = df["quantidade"] * df["preco"]

    return df


def salvar_dados(df):
    df.to_csv("data/vendas_tratadas.csv", index=False)


def main():
    df = carregar_dados()
    validar_dados(df)
    df = transformar_dados(df)
    salvar_dados(df)


if __name__ == "__main__":
    main()