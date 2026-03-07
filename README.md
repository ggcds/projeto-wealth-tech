# Projeto Wealth Tech - Pipeline de Dados de Investimentos

Este projeto automatiza a recolha, transformação e modelação de dados do mercado financeiro brasileiro (B3) utilizando uma arquitetura moderna de dados.

## 🛠 Tecnologias Utilizadas
- **Python**: Extração de dados via `yfinance`.
- **Google BigQuery**: Data Warehouse (Camadas Bronze, Silver, Gold).
- **dbt (data build tool)**: Transformação e modelação de dados.
- **Arquitetura**: Medalhão (Bronze/Silver/Gold).

## 🚀 Como Executar
1. Configure o ambiente virtual: `python -m venv .env`
2. Ative o ambiente e instale as dependências: `pip install -r requirements.txt`
3. Execute a extração: `python main.py` (em breve)
4. Execute as transformações dbt: `cd invest_analytics && dbt run`

## 📊 Estrutura do Pipeline
- **Bronze**: Dados brutos extraídos do Yahoo Finance.
- **Silver**: Limpeza e padronização (dbt).
- **Gold**: KPIs e agregados prontos para análise.