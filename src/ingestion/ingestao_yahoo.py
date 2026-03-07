import yfinance as yf
import pandas as pd
import pandas_gbq
import os

# ==========================================
# 1. Configurações Iniciais
# ==========================================
# Aponta para o seu arquivo JSON (o caminho funciona se você rodar na raiz do projeto)
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "credentials/gcp_key.json"

# ATENÇÃO: Confirme se o ID do projeto é exatamente esse na linha 3 do seu JSON
PROJECT_ID = "projeto-wealth-tech" 
DESTINATION_TABLE = "bronze.historico_acoes" 

# Ativos brasileiros da nossa carteira
TICKERS = ["RENT3.SA", "PETR4.SA", "VALE3.SA", "ITUB4.SA", "WEGE3.SA"]

# ==========================================
# 2. Extração de Dados (API Yahoo)
# ==========================================
dados_coletados = []
print("Iniciando extração do Yahoo Finance...\n")

for ticker in TICKERS:
    print(f"Extraindo dados de: {ticker}")
    acao = yf.Ticker(ticker)
    df = acao.history(period="1y") 
    
    if not df.empty: # Garante que só adiciona se houver dados
        df.reset_index(inplace=True)
        df['Ticker'] = ticker
        df = df[['Date', 'Ticker', 'Open', 'High', 'Low', 'Close', 'Volume']]
        dados_coletados.append(df)

tabela_final = pd.concat(dados_coletados, ignore_index=True)
tabela_final.columns = [col.replace(' ', '_').lower() for col in tabela_final.columns]
tabela_final = tabela_final.dropna(subset=['close']) # Remove nulos para não sujar a Silver
print(f"\nExtração concluída: {len(tabela_final)} linhas.")

# ==========================================
# 3. Carga de Dados (BigQuery)
# ==========================================
print("\nIniciando o envio para o BigQuery...")

# Padronização: O BigQuery prefere colunas sem espaços e em minúsculo
tabela_final.columns = [col.replace(' ', '_').lower() for col in tabela_final.columns]

# Tratamento de Data: Remove o fuso horário para evitar erro de incompatibilidade no BigQuery
if tabela_final['date'].dt.tz is not None:
    tabela_final['date'] = tabela_final['date'].dt.tz_localize(None)

# Envia os dados para a nuvem
pandas_gbq.to_gbq(
    tabela_final, 
    destination_table=DESTINATION_TABLE, 
    project_id=PROJECT_ID, 
    if_exists='replace' # Cria a tabela se não existir, ou substitui se já existir
)

print(f"\nSucesso! Dados carregados na tabela: {DESTINATION_TABLE} no GCP.")