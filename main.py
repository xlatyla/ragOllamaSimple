
import pandas as pd
from langchain_core.output_parsers import StrOutputParser
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.llms import Ollama
from langchain_core.prompts import ChatPromptTemplate
from langchain.memory import ConversationBufferMemory
from langchain_core.runnables import RunnablePassthrough


contexto = [
    """
    Si te hacen preguntas sobre _______, escribe el contexto.
    """
]


def setup_rag():
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
    documents = text_splitter.create_documents(contexto)
    embeddings = OllamaEmbeddings(model="mistral")
    vectorstore = FAISS.from_documents(documents, embeddings)
    return vectorstore.as_retriever()

    RAG_PROMPT_TEMPLATE = """
    Eres un asistente amable y servicial. Responde de manera natural y conversacional, siguiendo estas reglas:

    1. Para saludos o preguntas generales (hola, cómo estás, etc.): responde de forma breve y amistosa sin usar el contexto.
    2. Si la pregunta claramente requiere información del contexto (como preguntas sobre ________): usa el texto de referencia.
    3. En otros casos: responde de manera general con un tono amigable.

    Historial de conversación:
    {history}

    PREGUNTA: '{question}'
    TEXTO DE REFERENCIA: '{context}'

    RESPUESTA:
    """



def start():
    llm = Ollama(model="mistral")
    retriever = setup_rag()
    memory = ConversationBufferMemory(memory_key="history", return_messages=True)
    prompt = ChatPromptTemplate.from_template(RAG_PROMPT_TEMPLATE)
    chain = (
        RunnablePassthrough.assign(
            context=lambda x: "\n\n".join(doc.page_content for doc in retriever.get_relevant_documents(x["question"])),
            history=lambda x: memory.load_memory_variables({})["history"]
        )
        | prompt
        | llm
        | StrOutputParser()
    )
    
    while True:
        pregunta = input("\nTú: ")
        if pregunta.lower() in ["salir", "exit", "quit"]:
            break
            
        respuesta = chain.invoke({"question": pregunta})
        memory.save_context({"question": pregunta}, {"answer": respuesta})
        
        print("\nBot:", respuesta)




if __name__ == "__main__":
    start()
