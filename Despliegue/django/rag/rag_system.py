# rag/rag_system.py
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings  # Actualizado
from langchain_ollama import ChatOllama  # Actualizado
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from django.conf import settings

class RAGSystem:
    def __init__(self):
        self.llm = ChatOllama(
            model=settings.LLM_MODEL_NAME,
            temperature=0
        )
        
        self.embeddings = HuggingFaceEmbeddings(
            model_name=settings.EMBEDDINGS_MODEL_NAME
        )
        
        self.vector_db = Chroma(
            persist_directory=settings.VECTORDB_DIR,
            embedding_function=self.embeddings
        )
        
        self.prompt_template = ChatPromptTemplate.from_messages([
            ("system", self._get_system_prompt()),
            ("human", "{input}"),
        ])
        
        self.chain = self._create_chain()

    def _get_system_prompt(self):
        return """Eres un asistente para tareas de respuesta a preguntas.
        Usa los siguientes fragmentos de contexto recuperado para responder 
        la pregunta. Si no sabes la respuesta, di que no sabes. 
        Usa un máximo de tres oraciones y mantén la respuesta concisa.
        {context}"""

    def _create_chain(self):
        retriever = self.vector_db.as_retriever()
        document_chain = create_stuff_documents_chain(self.llm, self.prompt_template)
        return create_retrieval_chain(retriever, document_chain)

    def get_response(self, question: str) -> str:
        try:
            response = self.chain.invoke({"input": question})
            return response['answer']
        except Exception as e:
            return f"Error procesando la pregunta: {str(e)}"

# Singleton para evitar múltiples inicializaciones
rag_instance = RAGSystem()
