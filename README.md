# Pipeline de Vendas — Engenharia de Dados

Projeto de portfólio de Engenharia de Dados que implementa um pipeline para processar dados de vendas, realizar transformações com Python e Pandas e armazenar os resultados em um banco de dados PostgreSQL.

A execução é automatizada com Apache Airflow, utilizando Docker para o ambiente de execução e Pytest para verificar a qualidade dos dados antes do processamento.

## Objetivos

* Ler dados de vendas a partir de arquivos CSV.
* Inspecionar e transformar os dados com Python e Pandas.
* Calcular o faturamento de cada venda.
* Armazenar os dados tratados no PostgreSQL.
* Automatizar as etapas com Apache Airflow.
* Validar a qualidade dos dados com testes automatizados.
* Realizar análises SQL para extrair informações sobre as vendas.

## Arquitetura do Pipeline

O pipeline é composto pelas seguintes etapas:

1. **Entrada de dados:** leitura dos dados de vendas do arquivo `data/vendas.csv`.
2. **Qualidade dos dados:** execução de testes automatizados com Pytest.
3. **Transformação:** conversão de datas e cálculo do faturamento com Python e Pandas.
4. **Armazenamento intermediário:** gravação dos dados tratados em `data/vendas_tratadas.csv`.
5. **Carga no banco:** inserção dos dados na tabela `vendas`, no PostgreSQL.
6. **Análise:** execução de consultas SQL para analisar faturamento, produtos, categorias e cidades.

### Fluxo de execução

```text
Arquivo CSV
    |
    v
Testes de qualidade (Pytest)
    |
    v
Tratamento com Python e Pandas
    |
    v
CSV tratado
    |
    v
PostgreSQL
    |
    v
Análises SQL
```

O Apache Airflow coordena as tarefas de qualidade e execução do pipeline. A carga utiliza o identificador da venda para evitar inserir novamente registros já existentes.

## Tecnologias Utilizadas

* **Python:** lógica de processamento e transformação dos dados.
* **Pandas:** leitura, validação inicial e manipulação dos dados.
* **PostgreSQL:** armazenamento dos dados de vendas.
* **Psycopg 3:** conexão entre Python e PostgreSQL.
* **Apache Airflow 3.1.0:** orquestração das tarefas do pipeline.
* **Docker e Docker Compose:** execução dos serviços em containers.
* **Pytest:** testes automatizados de qualidade dos dados.
* **SQL:** criação da tabela e consultas analíticas.
* **Git e GitHub:** versionamento e publicação do projeto.

## Estrutura do Projeto

```text
projeto-pipeline-vendas/
├── dags/
│   └── pipeline_vendas.py
├── data/
│   ├── vendas.csv
│   └── vendas_tratadas.csv
├── sql/
│   ├── create_tables.sql
│   └── analise_vendas.sql
├── src/
│   └── tratamento.py
├── tests/
│   └── test_qualidade_dados.py
├── requirements.txt
├── README.md
└── .gitignore
```

## Pré-requisitos

Antes de executar o projeto, tenha instalado e configurado:

* Python e pip.
* Docker e Docker Compose.
* PostgreSQL acessível pelo pipeline.
* Git.

O Apache Airflow deste projeto é executado em um ambiente Docker.

## Configuração do Ambiente

O script Python utiliza variáveis de ambiente para se conectar ao PostgreSQL:

| Variável            | Descrição                       |
| ------------------- | ------------------------------- |
| `POSTGRES_HOST`     | Endereço do servidor PostgreSQL |
| `POSTGRES_DB`       | Nome do banco de dados          |
| `POSTGRES_USER`     | Usuário do banco                |
| `POSTGRES_PASSWORD` | Senha do banco                  |

Configure essas variáveis no ambiente de execução antes de executar o pipeline. Não coloque senhas diretamente no código nem publique credenciais no GitHub.

O arquivo `.env` está listado no `.gitignore` para evitar que seja versionado acidentalmente.

## Testes Automatizados

O projeto utiliza Pytest para validar a qualidade dos dados e verificar o comportamento idempotente da carga no PostgreSQL.

A suíte possui seis testes automatizados:

**Testes de qualidade dos dados**
- Unicidade dos identificadores das vendas.
- Ausência de valores nulos.
- Quantidades maiores que zero.
- Preços maiores que zero.
- Cálculo correto do faturamento.

**Teste de integração**
- Verificação da idempotência da carga no PostgreSQL, garantindo que um mesmo identificador seja atualizado sem gerar registros duplicados. O teste utiliza uma transação com rollback para não manter os dados temporários no banco.

### Executar os testes

Para executar os cinco testes de qualidade localmente:

```bash
pytest tests/test_qualidade_dados.py -v
```

O teste de integração requer acesso ao PostgreSQL e as variáveis de ambiente de conexão configuradas.

No ambiente Docker/Airflow do projeto, a suíte completa pode ser executada com:

```bash
docker compose exec airflow-worker bash -lc 'cd /opt/airflow/projeto-vendas && pytest tests/ -v'
```

A DAG `pipeline_vendas` executa os testes antes do processamento. A tarefa `executar_pipeline` só começa depois do sucesso da tarefa `testar_qualidade`.

## Análises SQL

O arquivo `sql/analise_vendas.sql` contém seis consultas analíticas executadas no PostgreSQL:

1. Faturamento por produto.
2. Faturamento por cidade.
3. Faturamento e quantidade de vendas por categoria.
4. Cidades com faturamento superior a R$ 5.000.
5. Quantidade de vendas por cidade.
6. Ticket médio das vendas.

### Principais resultados

* **Produto de maior faturamento:** Notebook, com R$ 14.000.
* **Cidade com maior faturamento:** Olinda, com R$ 8.360.
* **Cidade com mais vendas:** Recife, com 5 vendas.
* **Categoria de maior faturamento:** Eletrônicos, com R$ 16.400.
* **Ticket médio:** R$ 1.775,00.

Essas consultas permitem comparar o desempenho dos produtos, das categorias e das cidades, transformando os dados de vendas em informações úteis para análise.

## Como Executar o Projeto

### Pré-requisito do ambiente

O projeto utiliza um ambiente Apache Airflow executado com Docker Compose. Na configuração de desenvolvimento utilizada para validar este pipeline, o arquivo `docker-compose.yaml` do Airflow fica fora deste repositório.

Para reproduzir a execução, configure um ambiente compatível com Apache Airflow 3.1.0, PostgreSQL e as dependências do projeto. O repositório deve estar montado no container em `/opt/airflow/projeto-vendas`, com as variáveis de ambiente de conexão ao PostgreSQL configuradas.

### 1. Iniciar o ambiente

Entre na pasta que contém o arquivo `docker-compose.yaml` do Airflow e execute:

```bash
docker compose up -d
```

### 2. Executar o pipeline

A DAG `pipeline_vendas` pode ser executada pela interface web do Airflow, disponível em `http://localhost:8080`, ou pelo terminal:

```bash
docker compose exec airflow-scheduler airflow dags trigger pipeline_vendas
```

A DAG possui duas tarefas principais:

1. `testar_qualidade`: executa os testes automatizados.
2. `executar_pipeline`: realiza o tratamento e a carga dos dados no PostgreSQL após o sucesso dos testes.

### 3. Executar os testes manualmente

Para executar a suíte completa no container do Airflow Worker:

```bash
docker compose exec airflow-worker bash -lc 'cd /opt/airflow/projeto-vendas && pytest tests/ -v'
```

O teste de integração da idempotência requer acesso ao PostgreSQL e as variáveis de ambiente de conexão configuradas.

### 4. Consultar os resultados

Após a execução, os dados tratados ficam disponíveis no arquivo `data/vendas_tratadas.csv` e na tabela `vendas` do PostgreSQL.

As consultas analíticas estão disponíveis em `sql/analise_vendas.sql`.

Para verificar a quantidade de vendas, os identificadores únicos e o faturamento total, execute no ambiente PostgreSQL:

```sql
SELECT
    COUNT(*) AS total_vendas,
    COUNT(DISTINCT id_venda) AS ids_unicos,
    SUM(faturamento) AS faturamento_total
FROM vendas;
```

Na execução validada durante o desenvolvimento, o resultado foi de 10 vendas, 10 identificadores únicos e faturamento total de R$ 17.750,00.
