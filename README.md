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

## Testes de Qualidade

O projeto utiliza Pytest para verificar a qualidade dos dados antes da execução do processamento.

Os testes automatizados verificam:

* Unicidade dos identificadores das vendas.
* Ausência de valores nulos.
* Quantidades maiores que zero.
* Preços maiores que zero.
* Cálculo correto do faturamento.

Para executar os testes localmente, utilize:

```bash
pytest tests/test_qualidade_dados.py
```

A DAG do Apache Airflow executa os testes antes de iniciar o processamento. Se a tarefa de qualidade falhar, a tarefa seguinte não será executada.

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

### 1. Iniciar o ambiente Docker

Acesse a pasta do Apache Airflow:

```bash
cd ~/Área\ de\ trabalho/Airflow
```

Inicie os serviços:

```bash
docker compose up -d
```

### 2. Executar o pipeline pelo Airflow

Com os serviços iniciados:

1. Acesse a interface web do Airflow em `http://localhost:8080`.
2. Localize a DAG `pipeline_vendas`.
3. Acione a execução manual da DAG.
4. Acompanhe as tarefas `testar_qualidade` e `executar_pipeline`.

A tarefa de processamento depende do sucesso dos testes de qualidade.

### 3. Consultar os resultados

Após a execução, os dados tratados ficam disponíveis no arquivo `data/vendas_tratadas.csv` e na tabela `vendas` do PostgreSQL.

As consultas analíticas estão disponíveis em `sql/analise_vendas.sql`.
