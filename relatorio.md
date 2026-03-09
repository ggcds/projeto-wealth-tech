# Wealth Tech Pipeline - B3 Investment Data

## 1. Identificação do Projeto

**Título do Projeto:**  
Wealth Tech Pipeline - Ecossistema de Dados para Análise de Ativos da B3

**Autoria:**  
Guilherme Barros Caldas

**Empresa / contexto de aplicação:**  
Este projeto foi desenvolvido no contexto de uma empresa fictícia do setor Wealth Tech, com foco em análise de investimentos e suporte à tomada de decisão baseada em dados. A proposta consiste em estruturar um ecossistema de dados completo para análise de ativos estratégicos da B3, integrando Engenharia de Dados, Analytics Engineering e Inteligência Artificial Generativa.

---

## 2. Problema e Objetivos

### Descrição do problema de negócio
No mercado financeiro, a análise de ativos depende de dados confiáveis, organizados e acessíveis. Em muitos contextos, essas informações estão distribuídas em diferentes fontes, exigindo tratamento manual, padronização e esforço técnico para serem transformadas em insumos analíticos. Esse cenário reduz a eficiência operacional, dificulta a geração de insights e limita a escalabilidade da análise.

### Justificativa
O projeto se justifica pela necessidade de construir uma arquitetura moderna e automatizada para coleta, transformação e consumo de dados financeiros. Além disso, a incorporação de uma camada de IA generativa permite democratizar o acesso às informações, facilitando consultas em linguagem natural e reduzindo a dependência de conhecimento técnico em SQL.

### Objetivo geral
Desenvolver um pipeline de dados ponta a ponta para ingestão, transformação, enriquecimento e consumo analítico de dados de ativos da B3, com foco em automação, qualidade e apoio à decisão.

### Objetivos específicos
- Automatizar a ingestão de dados históricos de ativos estratégicos da B3.
- Estruturar os dados em camadas analíticas seguindo o modelo Bronze, Silver e Gold.
- Garantir qualidade e consistência com o uso de dbt, testes e padronização.
- Enriquecer os dados com tabelas de referência para classificação setorial.
- Disponibilizar uma interface analítica com IA generativa para consultas em linguagem natural.
- Criar uma base escalável para futuras aplicações em analytics e inteligência de mercado.

---

## 3. Dados

### Fontes de dados
A principal fonte de dados do projeto é a biblioteca `yfinance`, utilizada para extração do histórico de ativos selecionados da B3: `RENT3`, `PETR4`, `VALE3`, `ITUB4` e `WEGE3`.

Como fonte complementar de enriquecimento, são utilizadas tabelas de referência no dbt, especialmente a seed `depara_tickers`, responsável por mapear os ativos para seus respectivos setores.

### Descrição das variáveis
As principais variáveis coletadas incluem:
- Data de negociação
- Ativo
- Preço de abertura
- Preço de fechamento
- Preço máximo
- Preço mínimo
- Volume negociado

Após o enriquecimento, o dataset passa a incluir também atributos categóricos, como setor econômico e classificação da empresa.

### Processo de coleta e tratamento
A coleta é realizada por scripts Python localizados na camada de ingestão do projeto. Esses scripts extraem os dados históricos dos ativos e os disponibilizam na camada Bronze, preservando a estrutura original.

Na sequência, o dbt executa as transformações para as camadas Silver e Gold, promovendo limpeza, padronização, modelagem e testes de qualidade. O fluxo é executado por meio do comando:

```bash
docker exec -it airflow_scheduler bash -c "cd invest_analytics && dbt build --profiles-dir ."
```

Esse processo garante a execução integrada de seeds, models e tests, mantendo consistência e idempotência no pipeline.

### Limitações
Algumas limitações identificadas no projeto são:
- Dependência de uma fonte pública de dados, sujeita a indisponibilidades ou variações.
- Escopo limitado a cinco ativos estratégicos.
- Ausência, nesta versão, de dados fundamentalistas, macroeconômicos ou de notícias.
- Necessidade de evolução da governança e segurança para uso em ambiente corporativo.

---

## 4. Metodologia e Modelagem

### Abordagem adotada
O projeto adota uma abordagem descritiva e analítica com forte ênfase em automação. A solução foi desenhada para integrar Engenharia de Dados, transformação analítica e consumo inteligente por meio de IA generativa.

A arquitetura segue o padrão de separação em camadas:
- **Bronze:** ingestão bruta dos dados.
- **Silver:** limpeza e padronização.
- **Gold:** modelagem analítica para consumo final.

### Etapas técnicas
1. Provisionamento da infraestrutura com Docker e Docker Compose.
2. Inicialização do ambiente com Airflow e PostgreSQL.
3. Extração dos dados históricos via Python e `yfinance`.
4. Armazenamento inicial na camada Bronze.
5. Transformação e testes com dbt nas camadas Silver e Gold.
6. Enriquecimento com seeds de referência.
7. Disponibilização no BigQuery Sandbox.
8. Integração com agente SQL desenvolvido com LangChain + Gemini.

### Ferramentas utilizadas
- Python
- SQL
- BigQuery Sandbox
- dbt
- Apache Airflow
- Docker
- Docker Compose
- PostgreSQL
- LangChain
- Gemini

### Métricas de avaliação
As métricas consideradas para avaliação do projeto incluem:
- Taxa de sucesso da ingestão
- Tempo de execução do pipeline
- Quantidade de testes aprovados no dbt
- Percentual de registros válidos após transformação
- Tempo médio de resposta para consultas
- Efetividade do agente SQL na interpretação de perguntas em linguagem natural

---

## 5. Resultados e Discussão

### Principais descobertas
O projeto demonstrou que é possível construir um pipeline moderno e escalável para análise de ativos da B3, integrando ingestão automatizada, transformação estruturada e consumo analítico inteligente.

A arquitetura em camadas permitiu melhor organização dos dados, maior rastreabilidade e mais facilidade de manutenção. O uso do dbt contribuiu para a padronização das transformações e para a validação da qualidade dos dados por meio de testes integrados.

Outro resultado relevante foi a criação de uma camada de consumo com IA generativa, permitindo que consultas analíticas fossem realizadas em linguagem natural. Isso amplia o acesso aos dados e reduz a barreira técnica para usuários de negócio.

### Performance dos modelos
A performance do projeto pode ser analisada sob dois aspectos:
1. **Modelos de dados no dbt**, avaliados pela consistência, rastreabilidade e organização da camada analítica.
2. **Agente SQL com IA**, avaliado pela capacidade de interpretar perguntas e gerar consultas coerentes com a estrutura do BigQuery.

Exemplo de tabela para apresentação dos resultados:

| Componente | Indicador sugerido | Resultado |
|---|---|---|
| Ingestão Python | Taxa de sucesso das cargas | [preencher] |
| dbt Models | Testes aprovados / executados | [preencher] |
| Pipeline | Tempo total de execução | [preencher] |
| BigQuery | Tempo médio de consulta | [preencher] |
| Agente SQL | Taxa de perguntas respondidas corretamente | [preencher] |

### Interpretação dos resultados
Os resultados indicam que a solução atende adequadamente ao objetivo de estruturar uma base confiável para análise de ativos e geração de insights. A arquitetura proposta apresenta aderência a boas práticas de Engenharia de Dados, especialmente em modularidade, automação e separação entre camadas.

Do ponto de vista de negócio, o ganho principal está na redução do tempo entre a coleta de dados e a geração de informação analítica. Além disso, a camada de IA generativa agrega valor ao permitir exploração mais intuitiva da base de dados.

### Limitações e riscos identificados
Entre as principais limitações e riscos, destacam-se:
- Dependência de fonte pública para dados financeiros.
- Possíveis inconsistências ou atrasos na disponibilidade dos dados.
- Dependência de boa modelagem e metadados para funcionamento eficiente do agente SQL.
- Necessidade de evolução em segurança, governança de acesso e gerenciamento de credenciais.
- Risco de interpretações ambíguas em perguntas complexas feitas ao agente de IA.

---

## 6. Conclusões e Recomendações

### Resultado
O projeto alcançou o objetivo de construir um ecossistema de dados completo para análise de ativos estratégicos da B3, integrando ingestão automatizada, transformação analítica, enriquecimento semântico e consumo por IA generativa.

A solução demonstra potencial para ser expandida para cenários mais robustos e corporativos, servindo como base para aplicações futuras em analytics, monitoramento de carteira e inteligência financeira.

### Sugestões práticas
- Expandir o número de ativos monitorados.
- Incorporar novas fontes de dados, como fundamentos, dividendos e indicadores macroeconômicos.
- Criar dashboards analíticos com Power BI ou Looker Studio sobre a camada Gold.
- Adicionar monitoramento operacional e alertas automáticos no pipeline.
- Evoluir os testes de qualidade e observabilidade de dados.
- Melhorar o agente SQL com memória contextual e validação automática de respostas.
- Preparar a solução para um ambiente produtivo com governança corporativa.

### Impacto esperado
O impacto esperado é a melhoria da eficiência analítica, a redução de esforço manual e o aumento da autonomia dos usuários no consumo de informações financeiras. Em um contexto organizacional, o projeto também contribui para a maturidade de dados e para a padronização de processos analíticos.

---

## 7. Anexos

Podem ser incluídos como anexos:
- Estrutura de pastas do projeto
- Prints do Airflow em execução
- Evidências do `dbt build`
- Código dos scripts Python de ingestão
- Código dos modelos dbt
- Seeds utilizadas no enriquecimento
- Prints do BigQuery com tabelas geradas
- Exemplos de perguntas feitas ao agente SQL
- Respostas geradas pela camada de IA
- Tabelas complementares com métricas de qualidade e execução
