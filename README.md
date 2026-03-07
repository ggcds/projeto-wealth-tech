# 📈 Wealth Tech Pipeline - B3 Investment Data

Este projeto implementa um pipeline de dados ponta a ponta para análise de ativos da B3 (RENT3, PETR4, VALE3, ITUB4, WEGE3). A solução automatiza desde a extração de dados brutos até a modelagem de indicadores de performance financeira, utilizando a arquitetura medalhão.

## 🏗️ Arquitetura e Tecnologias

O projeto foi desenhado focando em escalabilidade, organização e conformidade com o **BigQuery Sandbox (Free Tier)**:

* **Ingestão (Bronze):** Script Python com `yfinance` e autenticação via Service Account, extraindo 1 ano de histórico para o BigQuery.
* **Transformação (Silver):** dbt para limpeza, renomeação e tipagem rigorosa (uso de `NUMERIC` para precisão em valores monetários).
* **Inteligência (Gold):** Modelagem de KPIs financeiros como **Variação Diária %** e **Média Móvel de 7 dias** utilizando Window Functions.
* **Orquestração:** Apache Airflow rodando em Docker para gestão do fluxo de trabalho.
* **Data Warehouse:** Google BigQuery.



---

## 🖥️ Guia da Demonstração

Para validar o pipeline, siga este roteiro:

### 1. Preparação da Infraestrutura
* **Docker:** Execute `docker-compose up -d`. O ambiente isolado garante que o dbt e o Airflow comuniquem-se sem conflitos locais.
* **Segurança:** As credenciais e logs estão protegidos via `.gitignore` para evitar exposição de chaves do GCP.

### 2. Orquestração no Airflow (`localhost:8080`)
* **Ativação:** Ligue a DAG `pipeline_wealth_tech`.
* **Disparo:** Inicie o fluxo manualmente. O Airflow executará a extração Python, seguida pelo `dbt run` e `dbt test`.

### 3. Validação no Google BigQuery
* **Camada Gold:** Acesse a tabela `gold.fct_performance_diaria`.
* **Diferencial:** Note o uso de `SAFE_DIVIDE` e `ROWS BETWEEN` para garantir cálculos precisos mesmo em feriados ou dias sem pregão.

---

## 🛠️ Como Executar

1.  **Credenciais:** Crie a pasta `credentials/` e coloque sua chave do GCP em `gcp_key.json`.
2.  **Configuração Local:** Crie as pastas `logs/` e `airflow/logs/` (ignoradas pelo Git).
3.  **Deploy:**
    ```bash
    docker-compose up -d
    ```

## 💡 Notas Técnicas (Sandbox Compatibility)
* **Estratégia de Carga:** Devido às restrições de DML na conta gratuita do BigQuery, os modelos dbt utilizam `materialized='table'`, garantindo o processamento completo sem erros de permissão.
* **Performance:** Uso de `partition_by` e `cluster_by` para otimizar o custo de consulta na camada Gold.