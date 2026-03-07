FROM apache/airflow:2.10.0-python3.12

# Instala dependências de sistema necessárias para o dbt e git
USER root
RUN apt-get update && apt-get install -y git && apt-get clean

# Volta para o usuário airflow para instalar as bibliotecas Python
USER airflow
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt