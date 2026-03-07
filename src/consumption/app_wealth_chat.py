import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits import create_sql_agent

# 1. Conexão com o BigQuery (Dataset Gold)
db = SQLDatabase.from_uri("bigquery://projeto-wealth-tech/gold")

# 2. Inicialização do Gemini 2.0 Flash Lite
llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash-lite", 
    temperature=0
)

# 3. Criação do Agente SQL com "Modo de Economia" Ativo
agent_executor = create_sql_agent(
    llm, 
    db=db, 
    agent_type="openai-tools", 
    verbose=True,
    # Restringe a visão do agente apenas ao necessário
    include_tables=['fct_performance_diaria'], 
    # Instrução crucial: impede a IA de fazer consultas de "amostra" que gastam cota
    extra_context="Não peça exemplos de linhas. Use apenas o schema das tabelas para gerar o SQL.",
    # Limita o raciocínio a 3 iterações para evitar loops caros
    max_iterations=3 
)

if __name__ == "__main__":
    print("\n📈 Wealth Tech Chat")
    
    while True:
        user_query = input("\nPergunta sobre seus ativos: ")
        if user_query.lower() in ["sair", "exit"]: break
            
        try:
            # O agente agora será mais direto e econômico no uso da API
            response = agent_executor.invoke({"input": user_query})
            print(f"\nResposta: {response['output']}")
        except Exception as e:
            # Se ainda der 429, o erro será capturado aqui
            print(f"\nNota: Se aparecer 'Quota Exceeded', aguarde 60s. Erro: {e}")