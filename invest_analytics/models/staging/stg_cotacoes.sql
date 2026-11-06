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

WITH raw_source AS (
    SELECT * FROM {{ source('bronze', 'historico_acoes') }}
),

final_transformation AS (
    SELECT
        CAST(date AS DATE) as data_pregao,
        UPPER(ticker) as ticker,
        CAST(open AS NUMERIC) as preco_abertura,
        CAST(high AS NUMERIC) as preco_maximo,
        CAST(low AS NUMERIC) as preco_minimo,
        CAST(close AS NUMERIC) as preco_fechamento,
        CAST(volume AS INT64) as volume_negociado
    FROM raw_source
    WHERE TRUE  -- o BigQuery exige WHERE, GROUP BY ou HAVING junto do QUALIFY
    -- Garante um registro por ativo e pregão, mesmo que a bronze receba cargas repetidas
    QUALIFY ROW_NUMBER() OVER (PARTITION BY UPPER(ticker), CAST(date AS DATE) ORDER BY date DESC) = 1
)

SELECT * FROM final_transformation