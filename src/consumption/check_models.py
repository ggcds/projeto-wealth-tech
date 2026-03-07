import google.generativeai as genai
import os

# O Docker já injetou essa chave para você
api_key = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=api_key)

print("--- Modelos Disponíveis no seu AI Studio ---")
for m in genai.list_models():
    if 'generateContent' in m.supported_generation_methods:
        print(f"Nome: {m.name}")