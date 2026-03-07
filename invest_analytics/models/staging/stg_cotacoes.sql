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
)

SELECT * FROM final_transformation