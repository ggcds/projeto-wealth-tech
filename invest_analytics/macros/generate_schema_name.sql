{% macro generate_schema_name(custom_schema_name, node) -%}
    {# Define o schema padrão configurado no seu profile (ex: 'silver') #}
    {%- set default_schema = target.schema -%}

    {# Se não houver um schema customizado no dbt_project, usa o padrão #}
    {%- if custom_schema_name is none -%}
        {{ default_schema }}
    {%- else -%}
        {# Se houver (ex: 'gold'), usa apenas o nome customizado, sem prefixos #}
        {{ custom_schema_name | trim }}
    {%- endif -%}
{%- endmacro %}