-- 1. Faturamento total por produto
SELECT
    produto,
    SUM(faturamento) AS faturamento_total
FROM vendas
GROUP BY produto
ORDER BY faturamento_total DESC;


-- 2. Faturamento total por cidade
SELECT
    cidade,
    SUM(faturamento) AS faturamento_total
FROM vendas
GROUP BY cidade
ORDER BY faturamento_total DESC;


-- 3. Faturamento e quantidade de vendas por categoria
SELECT
    categoria,
    SUM(faturamento) AS faturamento_total,
    COUNT(*) AS total_vendas
FROM vendas
GROUP BY categoria
ORDER BY faturamento_total DESC;


-- 4. Cidades com faturamento acima de R$ 5.000
SELECT
    cidade,
    SUM(faturamento) AS faturamento_total
FROM vendas
GROUP BY cidade
HAVING SUM(faturamento) > 5000
ORDER BY faturamento_total DESC;


-- 5. Quantidade de vendas por cidade
SELECT
    cidade,
    COUNT(*) AS total_vendas
FROM vendas
GROUP BY cidade
ORDER BY total_vendas DESC;
-- 6. Ticket médio das vendas
SELECT
    AVG(faturamento) AS ticket_medio
FROM vendas;
