import pandas as pd
import psycopg

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

def carregar_no_postgres(df):
    with psycopg.connect("host=host.docker.internal dbname=pipeline_vendas user=leticia") as conn:
        with conn.cursor() as cursor:
            for _, linha in df.iterrows():
                cursor.execute(
                    """
                    INSERT INTO vendas (
                        id_venda, data, produto, categoria,
                        quantidade, preco, cidade, faturamento
                    )
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT (id_venda) DO NOTHING
                    """,
                    (
                        int(linha["id_venda"]),
                        linha["data"].date(),
                        linha["produto"],
                        linha["categoria"],
                        int(linha["quantidade"]),
                        float(linha["preco"]),
                        linha["cidade"],
                        float(linha["faturamento"]),
                    ),
                )

    print("Carga no PostgreSQL concluída!")

def main():
    df = carregar_dados()
    validar_dados(df)
    df = transformar_dados(df)
    salvar_dados(df)
    carregar_no_postgres(df)


if __name__ == "__main__":
    main()