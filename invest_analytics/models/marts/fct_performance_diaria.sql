with silver_data as (
    select * from {{ ref('stg_cotacoes') }}
    -- Filtra para processar apenas os últimos 365 dias
    where data_pregao >= date_sub(current_date(), interval 1 year)
),
calculos as (
    select
        *,
        -- Variação percentual entre fechamento e abertura
        round(((preco_fechamento - preco_abertura) / preco_abertura) * 100, 2) as variacao_diaria_pct,
        
        -- Média móvel de 7 dias do fechamento
        avg(preco_fechamento) over (
            partition by ticker 
            order by data_pregao 
            rows between 6 preceding and current row
        ) as media_movel_7d
    from silver_data
)

select * from calculos
order by data_pregao desc, ticker asc