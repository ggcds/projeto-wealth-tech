{{
  config(
    materialized='table',
    partition_by={
      "field": "data_pregao",
      "data_type": "date",
      "granularity": "day"
    },
    cluster_by=['setor', 'ticker']
  )
}}

WITH silver_data AS (
    SELECT * FROM {{ ref('stg_cotacoes') }}
    WHERE data_pregao >= DATE_SUB(CURRENT_DATE(), INTERVAL 1 YEAR)
),

depara AS (
    SELECT * FROM {{ ref('depara_tickers') }}
),

market_indicators AS (
    SELECT
        s.*,
        -- Cálculo de variação
        ROUND(SAFE_DIVIDE((s.preco_fechamento - s.preco_abertura), s.preco_abertura) * 100, 2) AS variacao_diaria_pct,
        
        -- Média móvel aritmética (SMA)
        AVG(s.preco_fechamento) OVER (
            PARTITION BY s.ticker 
            ORDER BY s.data_pregao 
            ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
        ) AS media_movel_7d
    FROM silver_data s
)

-- O SELECT final agora processa o lote completo com ordem lógica de colunas
SELECT 
    -- 1. Eixo Temporal e Identificação
    m.data_pregao,
    m.ticker,
    
    -- 2. Contexto da Entidade (Enriquecimento via Seed)
    d.nome_empresa,
    d.setor,
    d.sub_setor,
    d.tipo_ativo,

    -- 3. Métricas de Mercado (Dados Brutos)
    m.preco_abertura,
    m.preco_fechamento,
    m.preco_maximo,
    m.preco_minimo,
    m.volume_negociado,

    -- 4. Indicadores de Performance (KPIs Calculados)
    m.variacao_diaria_pct,
    m.media_movel_7d

FROM market_indicators m
LEFT JOIN depara d ON m.ticker = d.ticker