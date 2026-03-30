# ⚽🧉 Agente Gaúcho de Regras de Futebol

RAG com LangChain + Gemini + Streamlit para consultar regras do futebol em PDF.
Porém um pouco personalizado e usando one-shot para quando não souber a resposta.

## Tecnologias
- LangChain
- Google Gemini (LLM + Embeddings) | model="gemini-2.5-flash-lite"
- Chroma (banco vetorial)
- Streamlit

## Como rodar
1. Instale as dependências: `pip install -r requirements.txt`
2. Copie o `.env.example` e renomeie para `.env` preencha `GOOGLE_API_KEY=` com sua chave
3. Coloque os PDFs na pasta `pdfs/`
4. Rode: `streamlit run app.py`
5. E adicione um `.gitignore` para não subir arquivos desnecessários:

```
.env
chroma_db/
.venv/
__pycache__/
*.pyc
```

## Fontes dos PDFs
[fundamentos_futebol](https://crefsc.org.br/)

[regras_futebol](https://futebolpaulista.com.br/)
