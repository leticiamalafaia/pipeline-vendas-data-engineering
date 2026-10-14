# Pipeline de Vendas — Engenharia de Dados

[![Testes automatizados](https://github.com/leticiamalafaia/pipeline-vendas-data-engineering/actions/workflows/tests.yml/badge.svg)](https://github.com/leticiamalafaia/pipeline-vendas-data-engineering/actions/workflows/tests.yml)

Projeto de portfólio de Engenharia de Dados que implementa um pipeline para processar dados de vendas, realizar transformações com Python e Pandas e armazenar os resultados em um banco de dados PostgreSQL.

A execução é automatizada com Apache Airflow, utilizando Docker para o ambiente de execução e Pytest para verificar a qualidade dos dados antes do processamento.

## Objetivos

- Ler dados de vendas a partir de arquivos CSV.
- Inspecionar e transformar os dados com Python e Pandas.
- Validar a qualidade dos dados por meio de testes automatizados.
- Armazenar os dados tratados no PostgreSQL.
- Automatizar a execução das etapas com Apache Airflow.
- Implementar uma carga idempotente para evitar duplicações.
- Realizar análises de vendas utilizando SQL.
- Automatizar a execução dos testes com GitHub Actions.

## Tecnologias utilizadas

- **Python:** processamento e transformação dos dados.
- **Pandas:** manipulação dos dados tabulares.
- **PostgreSQL:** armazenamento dos dados.
- **SQL:** criação de tabelas e análises de vendas.
- **Apache Airflow:** orquestração do pipeline.
- **Docker e Docker Compose:** execução dos serviços em containers.
- **Pytest:** testes automatizados de qualidade e integração.
- **Git e GitHub:** versionamento e publicação do projeto.
- **GitHub Actions:** integração contínua (CI).

## Estrutura do Projeto

```text
projeto-pipeline-vendas/
├── .github/
│   └── workflows/
│       └── tests.yml
├── dags/
│   └── pipeline_vendas.py
├── data/
│   └── vendas.csv
├── sql/
│   ├── create_tables.sql
│   └── analise_vendas.sql
├── src/
│   └── tratamento.py
├── tests/
│   ├── test_idempotencia.py
│   └── test_qualidade_dados.py
├── requirements.txt
├── README.md
└── .gitignore
```

O arquivo `data/vendas_tratadas.csv` é gerado durante a execução do pipeline e não é versionado no Git.

## Pré-requisitos

Antes de executar o projeto, tenha instalado e configurado:

- Python e pip.
- Docker e Docker Compose.
- PostgreSQL acessível pelo pipeline.
- Git.

## Funcionamento do pipeline

O pipeline executa as seguintes etapas:

1. Lê os dados de vendas do arquivo `data/vendas.csv`.
2. Executa os testes automatizados de qualidade dos dados.
3. Converte a coluna `data` para o tipo de data.
4. Calcula o faturamento de cada venda, multiplicando a quantidade pelo preço.
5. Salva os dados transformados em `data/vendas_tratadas.csv`.
6. Carrega os dados na tabela `vendas` do PostgreSQL.
7. Disponibiliza os dados para análises por meio de consultas SQL.

O Apache Airflow coordena as tarefas por meio da DAG `pipeline_vendas`.

### Tarefas da DAG

- **`testar_qualidade`:** executa os testes automatizados antes do processamento.
- **`executar_pipeline`:** realiza o tratamento e a carga dos dados após a aprovação dos testes.

A DAG foi executada com sucesso no ambiente local do Airflow.

## Transformação dos dados

O processamento é implementado em `src/tratamento.py`, utilizando Python, Pandas e Psycopg.

As principais operações são:

- Leitura do CSV de origem.
- Conversão e tratamento dos tipos de dados.
- Cálculo do faturamento de cada venda.
- Geração do CSV tratado.
- Carga dos dados no PostgreSQL.

O faturamento é calculado pela seguinte regra:

`faturamento = quantidade * preco`

## Carga idempotente no PostgreSQL

A carga utiliza a instrução SQL:

```sql
ON CONFLICT (id_venda) DO UPDATE
```

Essa estratégia utiliza o identificador da venda para evitar registros duplicados. Quando uma venda com o mesmo `id_venda` já existe, os dados correspondentes são atualizados.

A função `carregar_no_postgres(df, conn=None)` permite receber uma conexão existente ou criar uma conexão usando variáveis de ambiente.

As variáveis utilizadas para a conexão são:

- `POSTGRES_HOST`
- `POSTGRES_DB`
- `POSTGRES_USER`
- `POSTGRES_PASSWORD`

A implementação da carga e das transformações está em `src/tratamento.py`.

## Testes automatizados

O projeto utiliza Pytest para verificar a qualidade dos dados e o comportamento da carga no banco de dados.

### Testes de qualidade

Arquivo: `tests/test_qualidade_dados.py`

- **`test_id_venda_unico`:** verifica se os identificadores das vendas são únicos.
- **`test_dados_sem_nulos`:** verifica se existem valores nulos.
- **`test_quantidade_valida`:** verifica se as quantidades são positivas.
- **`test_preco_valido`:** verifica se os preços são positivos.
- **`test_faturamento_valido`:** verifica se o faturamento corresponde à multiplicação da quantidade pelo preço.

### Teste de integração

Arquivo: `tests/test_idempotencia.py`

- **`test_idempotencia_carga`:** verifica se uma segunda carga atualiza a venda existente sem gerar duplicatas.

O teste utiliza o identificador `999999` e uma transação com rollback, evitando que o registro de teste permaneça no banco de dados.

### Executar os testes no container do Airflow

Na pasta do projeto, a suíte completa pode ser executada com:

```bash
cd "$HOME/Área de trabalho/Airflow"

docker compose exec airflow-worker bash -lc \
'cd /opt/airflow/projeto-vendas && PYTHONPATH=. pytest tests/ -v'
```

Na última execução registrada, os seis testes foram aprovados no container do Airflow Worker.

## Integração contínua com GitHub Actions

O projeto possui um workflow em `.github/workflows/tests.yml`.

O workflow é configurado para executar em eventos de `push` e `pull_request` direcionados à branch `main`, além de permitir execução manual.

As etapas incluem:

1. Obtenção do código do repositório.
2. Configuração do Python 3.12.
3. Inicialização de um serviço PostgreSQL 16 para os testes.
4. Instalação das dependências do projeto.
5. Criação da tabela utilizando `sql/create_tables.sql`.
6. Execução dos testes automatizados.

O banco de dados utilizado no CI é configurado separadamente do ambiente local, com variáveis de ambiente próprias para os testes.

O status da execução pode ser consultado na aba **Actions** do repositório.

## Análises SQL

O arquivo `sql/analise_vendas.sql` contém seis consultas analíticas:

1. Faturamento por produto.
2. Faturamento por cidade.
3. Faturamento e quantidade de vendas por categoria.
4. Cidades com faturamento superior a R$ 5.000.
5. Quantidade de vendas por cidade.
6. Ticket médio das vendas.

### Resultados das análises

Com base nos dados utilizados no projeto, foram obtidos os seguintes resultados:

- **Produto com maior faturamento:** Notebook, com R$ 14.000,00.
- **Cidade com maior faturamento:** Olinda, com R$ 8.360,00.
- **Cidade com mais vendas:** Recife, com 5 vendas.
- **Categoria com maior faturamento:** Eletrônicos, com R$ 16.400,00.
- **Ticket médio:** R$ 1.775,00.

## Verificação dos dados no PostgreSQL

Após a execução do pipeline, é possível verificar a quantidade de vendas, a unicidade dos identificadores e o faturamento total com a consulta:

```sql
SELECT
    COUNT(*) AS total_vendas,
    COUNT(DISTINCT id_venda) AS ids_unicos,
    SUM(faturamento) AS faturamento_total
FROM vendas;
```

Na última verificação registrada, o resultado foi:

- Total de vendas: 10.
- Identificadores únicos: 10.
- Faturamento total: R$ 17.750,00.

## Aprendizados e práticas aplicadas

Este projeto reúne práticas importantes de Engenharia de Dados:

- Construção de um pipeline de transformação e carga de dados.
- Validação de dados com testes automatizados.
- Integração entre Python, Pandas e PostgreSQL.
- Orquestração de tarefas com Apache Airflow.
- Implementação de carga idempotente.
- Análises de dados utilizando SQL.
- Uso de containers com Docker Compose.
- Versionamento de código com Git e GitHub.
- Automação de testes com GitHub Actions.

## Repositório

Código-fonte: [pipeline-vendas-data-engineering](https://github.com/leticiamalafaia/pipeline-vendas-data-engineering)
