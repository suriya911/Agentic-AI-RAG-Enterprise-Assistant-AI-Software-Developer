from typing import List, Dict
import weaviate
from langchain.embeddings import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Weaviate
from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from ..config import settings

class RAGEngine:
    def __init__(self):
        # Initialize Weaviate client
        self.client = weaviate.Client(
            url=settings.WEAVIATE_URL,
            auth_client_secret=weaviate.AuthApiKey(api_key=settings.WEAVIATE_API_KEY) if settings.WEAVIATE_API_KEY else None
        )
        
        # Initialize OpenAI embeddings
        self.embeddings = OpenAIEmbeddings(openai_api_key=settings.OPENAI_API_KEY)
        
        # Initialize text splitter
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len,
        )
        
        # Initialize vector store
        self.vectorstore = Weaviate(
            client=self.client,
            index_name="Document",
            text_key="content",
            embedding=self.embeddings,
            by_text=False
        )
        
        # Initialize LLM
        self.llm = ChatOpenAI(
            temperature=0,
            model_name="gpt-4",
            openai_api_key=settings.OPENAI_API_KEY
        )
        
        # Initialize memory
        self.memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True
        )
        
        # Initialize QA chain
        self.qa_chain = ConversationalRetrievalChain.from_llm(
            llm=self.llm,
            retriever=self.vectorstore.as_retriever(),
            memory=self.memory,
            return_source_documents=True
        )

    async def get_relevant_documents(self, query: str) -> List[Dict]:
        """Retrieve relevant documents from the vector store."""
        docs = self.vectorstore.similarity_search(query, k=3)
        return [{"content": doc.page_content, "metadata": doc.metadata} for doc in docs]

    async def generate_answer(self, question: str, context_docs: List[Dict]) -> str:
        """Generate an answer using GPT-4 with the provided context."""
        # Format context
        context = "\n\n".join([doc["content"] for doc in context_docs])
        
        # Generate answer
        result = self.qa_chain({"question": question, "chat_history": []})
        return result["answer"]

    async def add_document(self, content: str, metadata: Dict) -> None:
        """Add a document to the vector store."""
        # Split text into chunks
        chunks = self.text_splitter.split_text(content)
        
        # Add chunks to vector store
        for chunk in chunks:
            self.vectorstore.add_texts(
                texts=[chunk],
                metadatas=[metadata]
            ) 