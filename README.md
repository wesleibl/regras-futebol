# ⚽🧉 Agente Gaúcho de Regras de Futebol

Chatbot que responde perguntas sobre regras do futebol com sotaque gaúcho, usando RAG (Retrieval-Augmented Generation) para consultar documentos PDF oficiais.

Construído com **LangChain**, **Google Gemini**, **ChromaDB** e **Streamlit**.

---

## Arquitetura

```
PDFs (regras oficiais)
        │
        ▼
   PyPDFLoader ──► Extração de texto por página
        │
        ▼
RecursiveCharacterTextSplitter ──► Chunks (1000 chars, 200 overlap)
        │
        ▼
Google Embeddings (gemini-embedding-001) ──► Vetores
        │
        ▼
    ChromaDB ──► Armazenamento e busca vetorial
        │
        ▼
  Retriever ──► Contexto relevante
        │
        ▼
 ChatPromptTemplate + Gemini 2.5 Flash Lite ──► Resposta em gauchês
```

**Fluxo:** os PDFs são divididos em blocos de texto, convertidos em embeddings e armazenados no ChromaDB. Quando o usuário faz uma pergunta, o retriever busca os trechos mais relevantes e os passa como contexto para o Gemini, que gera a resposta — sempre em linguagem acessível e com sotaque gaúcho.

---

## Decisões técnicas

- **One-shot prompting** no template: em vez de deixar o modelo inventar respostas genéricas quando não encontra a informação no contexto, o prompt inclui um exemplo concreto de resposta esperada vs. indesejada. Isso mantém o tom consistente mesmo em cenários de fallback.
- **Cache com `@st.cache_resource`**: o pipeline de embeddings e carregamento do banco vetorial roda apenas uma vez por sessão, evitando reprocessamento a cada interação.
- **Persistência do ChromaDB em disco**: na primeira execução os embeddings são gerados e salvos. Nas seguintes, o banco é carregado direto do disco sem recalcular.

---

## Stack

| Camada | Tecnologia |
|---|---|
| LLM | Google Gemini 2.5 Flash Lite |
| Embeddings | Google `gemini-embedding-001` |
| Orquestração | LangChain (LCEL chains) |
| Banco vetorial | ChromaDB |
| Interface | Streamlit (chat UI) |
| Leitura de PDFs | PyPDF |

---

## Como rodar

```bash
# 1. Clone o repositório
git clone https://github.com/wesleibl/regras-futebol.git
cd regras-futebol

# 2. Crie e ative um ambiente virtual
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# .venv\Scripts\activate   # Windows

# 3. Instale as dependências
pip install -r requirements.txt

# 4. Configure sua chave de API
cp .env.example .env
# Edite o .env e preencha: GOOGLE_API_KEY=sua_chave_aqui

# 5. Coloque os PDFs na pasta pdfs/

# 6. Rode a aplicação
streamlit run index.py
```

---

## Fontes dos PDFs

- [Fundamentos do Futebol](https://crefsc.org.br/) — CREF/SC
- [Regras do Futebol](https://futebolpaulista.com.br/) — Federação Paulista de Futebol

---

## Estrutura do projeto

```
regras-futebol/
├── index.py            # App principal (pipeline RAG + interface Streamlit)
├── pdfs/               # PDFs com regras oficiais do futebol
├── chroma_db/          # Banco vetorial persistido (gerado na 1ª execução)
├── requirements.txt
├── .env.example
└── .gitignore
```
