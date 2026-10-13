import os
import pandas as pd
import psycopg
from src.tratamento import carregar_no_postgres


def test_idempotencia_carga():
    conn = psycopg.connect(
        host=os.getenv("POSTGRES_HOST"),
        dbname=os.getenv("POSTGRES_DB"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD"),
    )
    id_teste = 999999

    try:
        # 1. Garante que o ID de teste não existe antes de começar
        with conn.cursor() as cur:
            cur.execute("DELETE FROM vendas WHERE id_venda = %s;", (id_teste,))

        # 2. Primeira carga: inserção de nova venda
        df_novo = pd.DataFrame(
            [
                {
                    "id_venda": id_teste,
                    "data": pd.to_datetime("2026-01-01"),
                    "produto": "Produto Teste",
                    "categoria": "Eletrônicos",
                    "quantidade": 1,
                    "preco": 100.0,
                    "cidade": "São Paulo",
                    "faturamento": 100.0,
                }
            ]
        )
        carregar_no_postgres(df_novo, conn=conn)

        # 3. Segunda carga: atualização da mesma venda (idempotência)
        df_atualizado = pd.DataFrame(
            [
                {
                    "id_venda": id_teste,
                    "data": pd.to_datetime("2026-01-01"),
                    "produto": "Produto Teste Atualizado",
                    "categoria": "Eletrônicos",
                    "quantidade": 2,
                    "preco": 100.0,
                    "cidade": "São Paulo",
                    "faturamento": 200.0,
                }
            ]
        )
        carregar_no_postgres(df_atualizado, conn=conn)

        # 4. Verificação: confirma se atualizou sem duplicar
        with conn.cursor() as cur:
            cur.execute(
                "SELECT quantidade, faturamento FROM vendas WHERE id_venda = %s;",
                (id_teste,),
            )
            resultado = cur.fetchone()

            assert resultado is not None, "A venda de teste não foi encontrada."
            assert resultado[0] == 2, "A quantidade não foi atualizada."
            assert resultado[1] == 200.0, "O faturamento não foi atualizado."

    finally:
        # Garante o rollback para NUNCA persistir dados de teste no banco
        conn.rollback()
        conn.close()
