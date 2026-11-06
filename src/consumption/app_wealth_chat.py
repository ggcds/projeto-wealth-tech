import os
import re
import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from google.cloud import bigquery

# ==========================================
# ⚙️ CONFIGURAÇÃO DA PÁGINA WEB
# ==========================================
st.set_page_config(page_title="Wealth Tech AI", page_icon="📈", layout="centered")
st.title("📈 Wealth Tech Chat")
st.caption("Seu assistente financeiro inteligente integrado ao BigQuery.")

# ==========================================
# 🔌 INICIALIZAÇÃO DE SERVIÇOS (COM CACHE)
# ==========================================
# O @st.cache_resource impede que o BQ e o Gemini reiniciem a cada clique na tela
# Limite de bytes processados por consulta gerada pela IA (padrão: 1 GB)
MAX_BYTES_BILLED = int(os.getenv("MAX_BYTES_BILLED", 1_000_000_000))

FORBIDDEN_SQL = re.compile(
    r"\b(INSERT|UPDATE|DELETE|MERGE|CREATE|DROP|ALTER|TRUNCATE|GRANT|REVOKE|CALL|EXECUTE)\b",
    re.IGNORECASE,
)


def validate_sql(sql: str) -> str:
    """Aceita apenas uma única consulta de leitura (SELECT/WITH)."""
    sql = sql.strip().rstrip(";").strip()
    if ";" in sql:
        raise ValueError("Apenas uma consulta por vez é permitida.")
    if not re.match(r"^(SELECT|WITH)\b", sql, re.IGNORECASE):
        raise ValueError("Apenas consultas de leitura (SELECT) são permitidas.")
    if FORBIDDEN_SQL.search(sql):
        raise ValueError("A consulta gerada contém um comando não permitido.")
    return sql


@st.cache_resource
def load_services():
    # Recomendado: apontar BQ_READONLY_CREDENTIALS para uma service account
    # apenas com BigQuery Data Viewer + Job User, separada da conta do dbt.
    readonly_key = os.getenv("BQ_READONLY_CREDENTIALS")
    if readonly_key:
        bq = bigquery.Client.from_service_account_json(readonly_key, project="projeto-wealth-tech")
    else:
        bq = bigquery.Client(project="projeto-wealth-tech")
    llm = ChatGoogleGenerativeAI(model="gemini-flash-lite-latest", temperature=0)
    return bq, llm

bq_client, llm = load_services()

# ==========================================
# 🧠 CHAINS (PROMPTS)
# ==========================================
template_sql = """
Você é um engenheiro de dados. Converta a pergunta do usuário em SQL válido para o BigQuery.
Retorne APENAS o código SQL. Sem markdown (```sql). Use ALIAS nas funções de agregação.

Schema de `projeto-wealth-tech.gold.fct_performance_diaria`:
- data_pregao (DATE)
- ticker (STRING): Ex: "RENT3.SA", "VALE3.SA", "PETR4.SA", "ITUB4.SA", "WEGE3.SA"
- preco_abertura, preco_fechamento, preco_maximo, preco_minimo (NUMERIC)
- volume_negociado (INT64)
- variacao_intradia_pct (NUMERIC): variação % entre fechamento e abertura do mesmo pregão
- retorno_diario_pct (NUMERIC): variação % do fechamento contra o pregão anterior
- media_movel_7d (NUMERIC)
- setor (STRING): Ex: "Consumo Cíclico", "Materiais Básicos", "Bens de Capital", "Energia", "Financeiro"
- sub_setor (STRING): Ex: "Aluguel de Carros", "Mineração", "Máquinas e Equipamentos", "Petróleo e Gás", "Bancos"
- nome_empresa (STRING): Ex: "Localiza Rent a Car S.A.", "Vale S.A.", "WEG S.A.", "Petróleo Brasileiro S.A."

Gere somente uma consulta SELECT. Nunca use INSERT, UPDATE, DELETE, MERGE, CREATE, DROP ou ALTER.

Nota: Para filtros textuais, prefira usar as colunas 'setor' e 'sub_setor' com os valores exatos listados acima (usando = ou IN).

Pergunta: {pergunta}
SQL:
"""
chain_sql = PromptTemplate.from_template(template_sql) | llm | StrOutputParser()

template_resposta = """
Você é o assistente virtual financeiro do aplicativo 'Wealth Tech'.
Sua função é responder à pergunta do usuário de forma natural, profissional, objetiva e elegante.

Regras:
1. Use EXATAMENTE os dados fornecidos abaixo. Não invente informações.
2. Formate os valores monetários no padrão brasileiro (ex: R$ 45,79).
3. Seja direto, não explique como você buscou os dados.

Pergunta do Usuário: {pergunta}
Dados extraídos do banco de dados: {dados}

Resposta profissional:
"""
chain_resposta = PromptTemplate.from_template(template_resposta) | llm | StrOutputParser()

# ==========================================
# 💬 INTERFACE DE CHAT
# ==========================================
# 1. Cria a memória do chat se for a primeira vez que a página carrega
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Olá! Sou o assistente do Wealth Tech. Como posso analisar seus ativos da B3 hoje?"}
    ]

# 2. Desenha o histórico de mensagens na tela
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# 3. Caixa de texto para o usuário digitar
if user_query := st.chat_input("Ex: Qual a média da Localiza no último mês?"):
    
    # Salva a pergunta e mostra na tela
    st.session_state.messages.append({"role": "user", "content": user_query})
    with st.chat_message("user"):
        st.markdown(user_query)

    # Inicia a resposta do assistente
    with st.chat_message("assistant"):
        # Mostra um ícone de carregamento enquanto o BigQuery trabalha
        with st.spinner("Consultando o BigQuery..."):
            try:
                # 1. Gera o SQL
                sql_query = chain_sql.invoke({"pergunta": user_query})
                sql_limpo = sql_query.replace("```sql", "").replace("```", "").strip()
                sql_limpo = validate_sql(sql_limpo)

                # 2. Executa no banco, com teto de custo por consulta
                job_config = bigquery.QueryJobConfig(maximum_bytes_billed=MAX_BYTES_BILLED)
                query_job = bq_client.query(sql_limpo, job_config=job_config)
                resultados = query_job.result()
                dados_brutos = [dict(row) for row in resultados]
                
                # 3. Gera a resposta humanizada
                resposta_final = chain_resposta.invoke({
                    "pergunta": user_query,
                    "dados": str(dados_brutos)
                })
                
                # 4. Escreve a resposta na tela
                st.markdown(resposta_final)
                
                # Bônus: Esconde a query em um botão expansível para não poluir o chat
                with st.expander("🛠️ Ver query executada"):
                    st.code(sql_limpo, language="sql")
                
                # Salva a resposta do bot na memória
                st.session_state.messages.append({"role": "assistant", "content": resposta_final})
                
            except Exception as e:
                erro_msg = f"Desculpe, ocorreu um erro ao buscar os dados. Detalhes: {e}"
                st.error(erro_msg)
                st.session_state.messages.append({"role": "assistant", "content": erro_msg})