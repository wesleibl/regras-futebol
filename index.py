import os
import streamlit as st
from dotenv import load_dotenv
import glob

# Imports devem vir antes de tudo
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()

CAMINHO_PDF = "./regras_futebol.pdf"
CHROMA_DIR = "./chroma_db"

@st.cache_resource
def carregar_chain():
    documents = []
    for caminho in glob.glob("./pdfs/*.pdf"):
        loader = PyPDFLoader(caminho)
        documents.extend(loader.load())
        print(f"Carregado: {caminho}")
        
    print(f"Páginas carregadas: {len(documents)}")

    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks = splitter.split_documents(documents)
    print(f"Blocos gerados: {len(chunks)}")

    embeddings = GoogleGenerativeAIEmbeddings(
        model="models/gemini-embedding-001"
    )

    if os.path.exists(CHROMA_DIR) and os.listdir(CHROMA_DIR):
        vectorstore = Chroma(
            persist_directory=CHROMA_DIR,
            embedding_function=embeddings
        )
        print("Banco vetorial carregado do disco.")
    else:
        vectorstore = Chroma.from_documents(
            chunks,
            embeddings,
            persist_directory=CHROMA_DIR
        )
        print("Banco vetorial criado e salvo.")

    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash-lite",
    )

    prompt = ChatPromptTemplate.from_template("""
        Responda a pergunta abaixo com base apenas no contexto fornecido.
        Explique para um leigo. 
        Fale com sotaque e gíria gaúcha.
        Caso não saiba, nao quero uma resposta nesse jeito:
        Resposta errada:Bah, tchê! O texto que me deram não explica bem o que é carrinho, sabe? Não fala nada sobre isso. Não lembro de ter visto essa palavra aqui.
        Reposta esperada: Bah, tchê! Pior que agora eu não to me lembrando, mas vou ver e te aviso 😅
                                              
    Contexto: {context}
    Pergunta: {input}
    """)

    retriever = vectorstore.as_retriever()

    def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)

    chain = (
        {"context": retriever | format_docs, "input": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )

    return chain

# Interface Streamlit
st.title("⚽🧉 Agente Gaúcho de Regras de Futebol")
st.write("Faça perguntas sobre as regras oficiais do futebol.")

chain = carregar_chain()

if "historico" not in st.session_state:
    st.session_state.historico = []

for msg in st.session_state.historico:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

pergunta = st.chat_input("Digite sua pergunta...")

if pergunta:
    with st.chat_message("user"):
        st.write(pergunta)
    st.session_state.historico.append({"role": "user", "content": pergunta})

    with st.chat_message("assistant"):
        with st.spinner("Buscando nas regras..."):
            resposta = chain.invoke(pergunta)
        st.write(resposta)
    st.session_state.historico.append({"role": "assistant", "content": resposta})