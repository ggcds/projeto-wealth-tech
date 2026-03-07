with silver_data as (
    select * from {{ ref('stg_cotacoes') }}
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