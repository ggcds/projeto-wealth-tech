# 📈 Wealth Tech Pipeline - B3 Investment Data

Este projeto implementa um pipeline de dados ponta a ponta para análise de ativos da B3 (RENT3, PETR4, VALE3, ITUB4, WEGE3). A solução automatiza desde a extração de dados brutos até a modelagem de indicadores de performance financeira, utilizando a arquitetura medalhão.

## 🏗️ Arquitetura e Tecnologias

O projeto foi desenhado focando em escalabilidade, organização e baixo custo de processamento no Google Cloud:

* **Ingestão (Bronze):** Script Python otimizado que extrai apenas o último ano de dados via `yfinance`, mantendo a tabela enxuta no BigQuery.
* **Transformação (Silver):** dbt para limpeza e tipagem rigorosa de dados (uso de `NUMERIC` para precisão financeira).
* **Inteligência (Gold):** Modelagem de KPIs financeiros (Variação Diária % e Médias Móveis) via dbt.
* **Orquestração:** Apache Airflow rodando em Docker para automação e gestão do fluxo.
* **Data Warehouse:** Google BigQuery.

[Image of Data engineering medallion architecture bronze silver gold]

---

## 🖥️ Guia da Demonstração (Step-by-Step)

Para validar o pipeline durante a apresentação, siga este roteiro:

### 1. Preparação da Infraestrutura
* **Subida do Ambiente:** Ao executar `docker-compose up -d`, demonstramos a portabilidade da solução através de containers. O ambiente isolado garante que o pipeline rode sem conflitos de dependências locais.

### 2. Orquestração no Airflow (`localhost:8080`)
* **Acesso e Login:** Credenciais padrão (`admin`/`admin`).
* **Ativação (Unpause):** Ative a DAG `pipeline_wealth_tech`.
* **Disparo (Trigger):** Clique no botão **Play** para iniciar o fluxo manual.
* **Monitoramento (Graph View):** Acompanhe a execução sequencial:
    1.  `extrair_dados_yahoo`: Script Python popula a camada **Bronze** com 1 ano de histórico.
    2.  `dbt_run_gold_silver`: O dbt processa as transformações e cálculos de indicadores.
    3.  `dbt_test`: Execução de testes de qualidade para garantir integridade dos dados finais.

### 3. Validação no Google BigQuery
* **Camada Gold:** No console do GCP, valide a tabela `gold.fct_performance_diaria`.
* **Insight de Negócio:** Destaque os campos de **Variação Diária (%)** e **Média Móvel de 7 dias**, que alimentam o produto de Wealth Tech.

---

## 🛠️ Como Executar

1.  **Configuração:** Coloque sua chave do GCP em `credentials/gcp_key.json`.
2.  **Subir Ambiente:**
    ```bash
    docker-compose up -d
    ```
3.  **Executar Pipeline:** Acesse o Airflow em `localhost:8080` e dispare a DAG manualmente.

## 💡 Diferenciais Técnicos
* **Otimização de Custos:** Lógica de `replace` na Bronze e janelas temporais fixas para reduzir o faturamento no BigQuery.
* **Governança:** Testes automatizados via dbt para evitar nulos e inconsistências.