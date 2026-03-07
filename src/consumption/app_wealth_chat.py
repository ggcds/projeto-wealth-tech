import os
from google.oauth2 import service_account
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits import create_sql_agent

# 1. Caminho da chave dentro do Docker
key_path = "/opt/airflow/credentials/gcp_key.json"
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = key_path

# 2. Carrega credenciais com o ESCOPO correto para Cloud Platform
creds = service_account.Credentials.from_service_account_file(
    key_path,
    scopes=['https://www.googleapis.com/auth/cloud-platform'] # Adicione esta linha
)

# 3. Conexão com o BigQuery
db = SQLDatabase.from_uri("bigquery://projeto-wealth-tech/gold")

# 4. Inicialização do Gemini 1.5 Pro
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-pro", 
    temperature=0,
    credentials=creds
)

# 5. Criação do Agente SQL
agent_executor = create_sql_agent(llm, db=db, agent_type="openai-tools", verbose=True)

if __name__ == "__main__":
    print("\n📈 Wealth Tech Chat - IA Analytics Ativa!")
    while True:
        user_query = input("\nPergunta sobre seus ativos: ")
        if user_query.lower() in ["sair", "exit"]: break
        try:
            response = agent_executor.invoke({"input": user_query})
            print(f"\nResposta: {response['output']}")
        except Exception as e:
            print(f"\nErro no processamento: {e}")