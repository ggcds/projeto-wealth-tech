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

WITH raw_source AS (
    SELECT * FROM {{ ref('bronze_historico_acoes') }}
    
    {% if is_incremental() %}
    -- Mantém a integridade dos dados reprocessando os últimos 3 dias (lookback window)
    WHERE CAST(date AS DATE) >= DATE_SUB(
        (SELECT MAX(data_pregao) FROM {{ this }}), 
        INTERVAL 3 DAY
    )
    {% endif %}
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