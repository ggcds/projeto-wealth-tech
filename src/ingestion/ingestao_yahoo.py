import os
import logging
import yfinance as yf
import pandas as pd
import pandas_gbq
from google.oauth2 import service_account

# Configuração de Logging para monitoramento no Airflow
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Configurações de Ambiente
PROJECT_ID = "projeto-wealth-tech" 
DATASET_ID = "bronze"
TABLE_NAME = "historico_acoes"
KEY_PATH = "/opt/airflow/credentials/gcp_key.json"

TICKERS = ["RENT3.SA", "PETR4.SA", "VALE3.SA", "ITUB4.SA", "WEGE3.SA"]

def get_credentials(path):
    """Carrega credenciais de forma segura para o ambiente Docker."""
    if not os.path.exists(path):
        raise FileNotFoundError(f"Chave GCP não encontrada em: {path}")
    return service_account.Credentials.from_service_account_file(path)

def fetch_market_data(tickers, period="1y"):
    """Extrai e padroniza dados do Yahoo Finance."""
    collected_data = []
    logging.info(f"Iniciando extração para {len(tickers)} ativos...")

    for ticker in tickers:
        try:
            df = yf.Ticker(ticker).history(period=period)
            if df.empty:
                logging.warning(f"Nenhum dado encontrado para {ticker}")
                continue
                
            df = df.reset_index()
            df['ticker'] = ticker.upper()
            # Seleção e padronização de colunas
            df = df[['Date', 'ticker', 'Open', 'High', 'Low', 'Close', 'Volume']]
            df.columns = [col.lower() for col in df.columns]
            
            # Tratamento de fuso horário para compatibilidade com BigQuery
            if df['date'].dt.tz is not None:
                df['date'] = df['date'].dt.tz_localize(None)
                
            collected_data.append(df)
            logging.info(f"Dados de {ticker} extraídos com sucesso.")
        except Exception as e:
            logging.error(f"Erro ao extrair {ticker}: {e}")

    return pd.concat(collected_data, ignore_index=True) if collected_data else pd.DataFrame()

def load_to_bigquery(df, project_id, dataset, table, credentials):
    """Realiza a carga no BigQuery com tratamento de erros."""
    if df.empty:
        logging.error("Dataframe vazio. Abortando carga.")
        return

    destination = f"{dataset}.{table}"
    try:
        logging.info(f"Enviando {len(df)} linhas para {destination}...")
        pandas_gbq.to_gbq(
            dataframe=df,
            destination_table=destination,
            project_id=project_id,
            credentials=credentials,
            if_exists='append',
            progress_bar=False
        )
        logging.info("Carga concluída com sucesso!")
    except Exception as e:
        logging.error(f"Falha na carga para o BigQuery: {e}")
        raise

if __name__ == "__main__":
    # Execução do Pipeline
    try:
        creds = get_credentials(KEY_PATH)
        data = fetch_market_data(TICKERS)
        load_to_bigquery(data, PROJECT_ID, DATASET_ID, TABLE_NAME, creds)
    except Exception as e:
        logging.critical(f"Falha crítica no pipeline: {e}")
        exit(1)