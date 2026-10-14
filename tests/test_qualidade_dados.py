import pandas as pd

from src.tratamento import transformar_dados

def test_id_venda_unico():
    df = pd.read_csv("data/vendas.csv")
    assert df["id_venda"].is_unique


def test_dados_sem_nulos():
    df = pd.read_csv("data/vendas.csv")
    assert df.isnull().sum().sum() == 0


def test_quantidade_valida():
    df = pd.read_csv("data/vendas.csv")
    assert (df["quantidade"] > 0).all()


def test_preco_valido():
    df = pd.read_csv("data/vendas.csv")
    assert (df["preco"] > 0).all()

def test_faturamento_valido():
    df = pd.read_csv("data/vendas.csv")
    df_tratado = transformar_dados(df)

    faturamento_esperado = (
        df_tratado["quantidade"] * df_tratado["preco"]
    )

    assert (
        df_tratado["faturamento"] == faturamento_esperado
    ).all()
