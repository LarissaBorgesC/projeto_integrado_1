# Projeto Integrado — Inteligência de Mercado e Análise de Dados

Projeto acadêmico desenvolvido para o componente de **Inteligência de mercado e análise de dados**, com foco em agronegócio. O objetivo é simular um fluxo completo de dados, desde a geração e análise estatística até a criação de um pipeline ETL, modelagem de banco de dados, testes automatizados e um modelo de regressão linear para previsão de produtividade.

## Objetivos

O projeto cobre os seguintes passos:

1. **Probabilidade e Estatística**  
   Simulação de dados de 50 propriedades agrícolas e análise de média, desvio padrão, correlação, intervalo de confiança e normalidade.

2. **Banco de Dados**  
   Criação de um banco relacional em PostgreSQL com tabelas para fazendas, clima e produtividade.

3. **Engenharia de Dados**  
   Implementação de um pipeline ETL em Python para ler, limpar e integrar os arquivos CSV gerados.

4. **Projeto de Software**  
   Organização da arquitetura em MVC e validação do fluxo com testes automatizados.

5. **Machine Learning**  
   Treinamento de um modelo de regressão linear para prever produtividade com base em chuva e temperatura.

## Estrutura do projeto

```bash
.
├── analise_estatistica.py
├── db_schema.sql
├── etl_pipeline.py
├── main.py
├── model_ml.py
├── test_pipeline.py
├── requirements.txt
├── README.md
└── .gitignore
```

## Descrição dos arquivos

- `main.py`  
  Simula os dados agrícolas, gera os arquivos base (`clima.csv` e `produtividade.csv`), executa a análise estatística e treina o modelo de regressão linear.

- `analise_estatistica.py`  
  Script voltado à análise estatística dos dados simulados.

- `db_schema.sql`  
  Script SQL com a estrutura do banco de dados PostgreSQL e consulta para produtividade média por região e safra.

- `etl_pipeline.py`  
  Pipeline ETL que lê os arquivos CSV, faz limpeza, integra os dados e gera `dataset_unificado.csv`.

- `model_ml.py`  
  Script que carrega o dataset unificado, divide em treino e teste, treina o modelo e exibe `R²` e `MAE`.

- `test_pipeline.py`  
  Testes automatizados para validar a geração dos arquivos e o funcionamento do ETL.

## Requisitos

Instale as dependências com:

```bash
pip install -r requirements.txt
```

## Dependências

- pandas
- numpy
- scipy
- scikit-learn
- pytest

## Como executar

### 1. Gerar os dados e análises
```bash
python main.py
```

### 2. Executar o ETL
```bash
python etl_pipeline.py
```

### 3. Treinar o modelo
```bash
python model_ml.py
```

### 4. Executar os testes
```bash
pytest test_pipeline.py -v
```

## Resultados esperados

Ao executar o projeto, serão gerados:

- `clima.csv`
- `produtividade.csv`
- `dataset_unificado.csv`

Além disso, o console exibirá:

- média da produtividade;
- desvio padrão;
- correlação entre chuva e produtividade;
- intervalo de confiança;
- teste de normalidade;
- métricas do modelo (`R²` e `MAE`).

## Arquitetura

A solução foi organizada em uma estrutura inspirada no padrão MVC:

- **Model**: arquivos de dados e banco relacional.
- **Controller**: scripts que processam, integram e treinam os dados.
- **View**: relatórios e métricas exibidos no console e no relatório final.
- **QA/Testes**: validação automatizada com `pytest`.

## Observações

- O projeto foi desenvolvido com fins acadêmicos.
- Os dados foram simulados para atender ao contexto proposto.
- O relatório final deve ser entregue em formato Word ou PDF, conforme solicitado no AVA.

## Autor

Larissa Borges
