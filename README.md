# 📈 Wealth Tech Pipeline - B3 Investment Data

Este projeto implementa um ecossistema de dados completo para análise de ativos estratégicos da B3 (RENT3, PETR4, VALE3, ITUB4, WEGE3), integrando Engenharia de Dados, Analytics Engineering e IA Generativa.

## 🏗️ Arquitetura e Tecnologias

A solução foi desenhada com foco em escalabilidade e automação utilizando o BigQuery Sandbox:

* **Orquestração (Docker)**: Ambiente multi-container isolado com Apache Airflow e PostgreSQL para metadados.
* **Ingestão (Bronze)**: Scripts Python utilizando `yfinance` para extração de histórico de ativos.
* **Transformação (Silver/Gold)**: dbt para limpeza de dados e modelagem de KPIs financeiros como Variação % e Média Móvel.
* **Enriquecimento (Seeds)**: Uso de tabelas de referência (`depara_tickers`) para mapeamento setorial das empresas.
* **Consumo (IA)**: Chatbot desenvolvido com LangChain e Gemini para análise de portfólio via linguagem natural.

---

## 📁 Estrutura do Projeto

Organização baseada em padrões de mercado para separação de responsabilidades:

```text
PROJETO_WEALTH_TECH/
├── airflow/                # Configurações do Orquestrador Airflow
│   ├── dags/               # Pipelines automatizados
│   ├── logs/               # Histórico de execuções (ignorado pelo Git)
│   └── plugins/            # Componentes customizados
├── credentials/            # Chaves de segurança (GCP Service Account)
├── invest_analytics/       # Projeto dbt (Transformação)
│   ├── models/             # SQLs de Staging e Marts
│   ├── seeds/              # Dados mestres (depara_tickers.csv)
│   └── dbt_project.yml     # Configurações do dbt
├── src/                    # Código fonte da aplicação
│   ├── consumption/        # Camada de IA (Chatbot)
│   └── ingestion/          # Scripts de extração (Yahoo Finance)
├── Dockerfile              # Imagem customizada com dbt e libs de IA
├── docker-compose.yaml     # Orquestração de serviços locais
└── requirements.txt        # Dependências Python
```



---

## 🖥️ Guia da Demonstração

Para validar o pipeline e a camada de inteligência, siga este roteiro:

### 1. Preparação da Infraestrutura
* **Docker:** Execute `docker-compose up -d --build`. O uso da flag `--build` garante que a imagem customizada seja montada com o `dbt` e as libs de IA pré-instaladas, evitando erros de execução.
* **Automação de Acesso:** O ambiente já inicializa o banco de dados e cria o usuário **admin** (senha: `admin`) automaticamente no boot.

### 2. Enriquecimento e Transformação (CLI)
Como você agora utiliza uma arquitetura profissional, execute os comandos diretamente no container do **scheduler**:
* **Seeds:** `docker exec -it airflow_scheduler bash -c "cd invest_analytics && dbt seed"` (carrega o depara de empresas e setores).
* **Run & Test:** `docker exec -it airflow_scheduler bash -c "cd invest_analytics && dbt run && dbt test"` (processa a camada Gold e valida a integridade dos dados).

### 3. Validação no Google BigQuery
* **Camada Gold:** Acesse a tabela `gold.fct_performance_diaria`.
* **Diferencial:** Note que os dados agora estão enriquecidos com `nome_empresa` e `setor`, permitindo análises granulares pelo Chatbot.

---

## 🛠️ Como Executar

1. **Credenciais:** Coloque sua chave do GCP em `credentials/gcp_key.json`.
2. **Ambiente:** Certifique-se de que o arquivo `requirements.txt` e o `Dockerfile` estão na raiz do projeto.
3. **Deploy:**
   ```bash
   docker-compose up -d --build
    ```

## 💡 Notas Técnicas

Este projeto foi construído seguindo padrões de engenharia de software aplicados a dados, garantindo robustez e facilidade de manutenção:

* **Infraestrutura Imutável**: O uso do `Dockerfile` para pré-instalar o `dbt-bigquery` e bibliotecas de IA elimina o erro de "Permission Denied" e garante que o ambiente seja idêntico em qualquer máquina.
* **Resiliência Analítica**: Os modelos SQL utilizam `SAFE_DIVIDE` para evitar erros de divisão por zero e Window Functions (`ROWS BETWEEN`) para garantir médias móveis consistentes, mesmo com lacunas de dados em feriados.
* **Sandbox Optimization**: Devido às restrições de DML na conta gratuita do BigQuery, os modelos utilizam `materialized='table'`, garantindo o processamento completo sem falhas de permissão de escrita.
* **Eficiência de Custo**: Implementação de `partition_by` por dia e `cluster_by` por setor/ticker na camada Gold, reduzindo drasticamente o volume de dados escaneados por consulta da IA.
* **Automação de Setup**: O `docker-compose` gerencia o ciclo de vida completo: desde a prontidão do banco Postgres até a criação automática do usuário administrador do Airflow.

---
Desenvolvido por **Guilherme Caldas**
