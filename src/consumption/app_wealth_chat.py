import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits import create_sql_agent

# 1. Autenticação (Caminho fixo do Docker)
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/opt/airflow/credentials/gcp_key.json"

# 2. Conexão com o BigQuery
# Substitua 'projeto-wealth-tech' pelo ID real do seu projeto se for diferente
db = SQLDatabase.from_uri("bigquery://projeto-wealth-tech/gold")

# 3. Inicialização do Gemini 1.5 Pro (Nova biblioteca)
llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro", temperature=0)

# 4. Criação do Agente SQL
agent_executor = create_sql_agent(
    llm, 
    db=db, 
    agent_type="openai-tools", 
    verbose=True
)

if __name__ == "__main__":
    print("\n📈 Wealth Tech Chat - IA Analytics Ativa!")
    while True:
        user_query = input("\nPergunta sobre seus ativos: ")
        if user_query.lower() in ["sair", "exit"]: break
        
        try:
            # O agente usará os metadados do dbt para entender o SQL
            response = agent_executor.invoke({"input": user_query})
            print(f"\nResposta: {response['output']}")
        except Exception as e:
            print(f"\nErro no processamento: {e}")