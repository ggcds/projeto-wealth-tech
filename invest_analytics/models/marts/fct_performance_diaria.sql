{{
  config(
    materialized='incremental',
    partition_by={
      "field": "data_pregao",
      "data_type": "date",
      "granularity": "day"
    },
    incremental_strategy='insert_overwrite',
    cluster_by=['ticker']
  )
}}

WITH silver_data AS (
    SELECT * FROM {{ ref('stg_cotacoes') }}
    
    {% if is_incremental() %}
    -- Garante que temos dados suficientes (7 dias) para calcular a média móvel sem lacunas
    WHERE data_pregao >= DATE_SUB(
        (SELECT MAX(data_pregao) FROM {{ this }}), 
        INTERVAL 10 DAY
    )
    {% else %}
    -- Carga inicial limitada a 1 ano para performance
    WHERE data_pregao >= DATE_SUB(CURRENT_DATE(), INTERVAL 1 YEAR)
    {% endif %}
),

market_indicators AS (
    SELECT
        *,
        -- Cálculo de volatilidade diária (fechamento vs abertura)
        ROUND(SAFE_DIVIDE((preco_fechamento - preco_abertura), preco_abertura) * 100, 2) AS variacao_diaria_pct,
        
        -- Média móvel aritmética (SMA) de 7 períodos
        AVG(preco_fechamento) OVER (
            PARTITION BY ticker 
            ORDER BY data_pregao 
            ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
        ) AS media_movel_7d
    FROM silver_data
)

SELECT * FROM market_indicators
{% if is_incremental() %}
-- Filtra para inserir apenas os dias que foram de fato atualizados/novos
WHERE data_pregao >= DATE_SUB((SELECT MAX(data_pregao) FROM {{ this }}), INTERVAL 3 DAY)
{% endif %}