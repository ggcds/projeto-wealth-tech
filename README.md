# 📈 Wealth Tech Pipeline - B3 Investment Data

Este projeto implementa um pipeline de dados ponta a ponta para análise de ativos da B3 (RENT3, PETR4, VALE3, ITUB4, WEGE3). A solução automatiza desde a extração de dados brutos até a modelagem de indicadores de performance financeira, utilizando a arquitetura medalhão.

## 🏗️ Arquitetura e Tecnologias

O projeto foi desenhado focando em escalabilidade e baixo custo de processamento no Google Cloud:

* **Ingestão (Bronze):** Script Python otimizado que extrai apenas o último ano de dados (Yahoo Finance), mantendo a tabela enxuta no BigQuery.
* **Transformação (Silver):** dbt para limpeza e tipagem de dados (`NUMERIC` para precisão financeira).
* **Inteligência (Gold):** Modelagem de KPIs (Variação Diária e Médias Móveis) via dbt.
* **Orquestração:** Apache Airflow rodando em Docker para automação do fluxo.
* **Data Warehouse:** Google BigQuery.



## 🛠️ Como Executar com Docker (Recomendado)

A stack completa está conteinerizada, facilitando a demonstração em qualquer ambiente:

1.  **Pré-requisitos:** Docker Desktop instalado.
2.  **Configuração:** Coloque sua chave do GCP em `credentials/gcp_key.json`.
3.  **Subir Ambiente:**
    ```bash
    docker-compose up -d
    ```
4.  **Acessar Orquestrador:** Vá para `localhost:8080` (admin/admin) para disparar o pipeline manualmente.

## 📊 Estrutura de Dados

* **Bronze:** `historico_acoes` (Dados brutos, janela de 1 ano).
* **Silver:** `stg_cotacoes` (Camada padronizada e limpa).
* **Gold:** `fct_performance_diaria` (Dataset final com indicadores para BI).

## 💡 Diferenciais Técnicos
- **Otimização de Custos:** Lógica de `replace` na Bronze e filtros temporais para reduzir processamento no BigQuery.
- **Governança:** Testes de dados integrados (dbt tests) para garantir integridade de preços e tickers.
- **DevOps:** Ambiente 100% isolado via Docker Compose.