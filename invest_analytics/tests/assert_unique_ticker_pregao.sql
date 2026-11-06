-- Falha se algum ativo tiver mais de um registro no mesmo pregão
SELECT
    ticker,
    data_pregao,
    COUNT(*) AS registros
FROM {{ ref('fct_performance_diaria') }}
GROUP BY ticker, data_pregao
HAVING COUNT(*) > 1
