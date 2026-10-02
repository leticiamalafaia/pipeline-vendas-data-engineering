CREATE TABLE IF NOT EXISTS vendas (
    id_venda INTEGER PRIMARY KEY,
    data DATE,
    produto VARCHAR(100),
    categoria VARCHAR(100),
    quantidade INTEGER,
    preco NUMERIC(10,2),
    cidade VARCHAR(100),
    faturamento NUMERIC(10,2)
);
