{{
  config(
    materialized='table',
    partition_by={
      "field": "data_pregao",
      "data_type": "date",
      "granularity": "day"
    },
    cluster_by=['ticker']
  )
}}

WITH silver_data AS (
    SELECT * FROM {{ ref('stg_cotacoes') }}
    
    -- Filtro fixo de 1 ano para garantir performance e relevância dos dados
    WHERE data_pregao >= DATE_SUB(CURRENT_DATE(), INTERVAL 1 YEAR)
),

market_indicators AS (
    SELECT
        *,
        -- Cálculo de volatilidade diária resiliente a erros (SAFE_DIVIDE)
        ROUND(SAFE_DIVIDE((preco_fechamento - preco_abertura), preco_abertura) * 100, 2) AS variacao_diaria_pct,
        
        -- Média móvel aritmética (SMA) de 7 períodos baseada em janelas de tempo
        AVG(preco_fechamento) OVER (
            PARTITION BY ticker 
            ORDER BY data_pregao 
            ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
        ) AS media_movel_7d
    FROM silver_data
)

-- O SELECT final agora processa o lote completo de 1 ano
SELECT * FROM market_indicators