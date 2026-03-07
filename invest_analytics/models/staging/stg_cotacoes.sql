with source as (
    select * from {{ source('bronze', 'historico_acoes') }}
),

renamed as (
    select
        cast(date as date) as data_pregao,
        upper(ticker) as ticker,
        -- NUMERIC para garantir precisão em valores monetários
        cast(open as numeric) as preco_abertura,
        cast(high as numeric) as preco_maximo,
        cast(low as numeric) as preco_minimo,
        cast(close as numeric) as preco_fechamento,
        cast(volume as int64) as volume_negociado
    from source
)

select * from renamed