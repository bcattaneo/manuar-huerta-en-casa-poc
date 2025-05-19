
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Literal, Union
import os
import logging
__import__("pysqlite3")
import sys

sys.modules["sqlite3"] = sys.modules.pop("pysqlite3")
import chromadb
from chromadb import Settings
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_chroma import Chroma
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.chat_history import BaseChatMessageHistory
from langchain.chains import create_history_aware_retriever, create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from dotenv import load_dotenv
import requests
import uvicorn

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Load environment variables from .env file
load_dotenv()

# Configurar puerto para Azure
port = int(os.getenv("PORT", 8000))

# Get OpenAI API key from environment variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY environment variable is not set")

# Configure FastAPI app
app = FastAPI(title="RAG Query API", 
              description="API for querying documents with memory of previous conversations")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods including OPTIONS
    allow_headers=["*"],  # Allows all headers
    expose_headers=["*"]  # Exposes all headers
)

# Initialize ChromaDB connection
def init_chroma_client(
    collection_name: str = "pdf_documents"
):
    try:
        # Initialize OpenAI embeddings
        embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)
        
        # Connect to ChromaDB with HTTP client
        db = Chroma(
            # client=chroma_client,
            persist_directory="./chroma_db",
            collection_name=collection_name,
            embedding_function=embeddings,
            client_settings=Settings(anonymized_telemetry=False)
        )
        
        # Check if we have documents in the database
        doc_count = db._collection.count()
        logger.info(f"Number of documents in ChromaDB: {doc_count}")
        
        if doc_count == 0:
            logger.warning("No documents found in the database. Make sure to run store.py first.")
        
        return db
    except Exception as e:
        logger.error(f"Error connecting to ChromaDB: {str(e)}")
        raise

# Initialize the LLM and retriever
def init_llm_retriever(db):
    # Initialize GPT model
    llm = ChatOpenAI(
        openai_api_key=OPENAI_API_KEY,
        model="gpt-4o-mini",
        temperature=2
    )
    
    # Get the retriever from the ChromaDB
    retriever = db.as_retriever(search_kwargs={"k": 3})
    
    return llm, retriever

# def init_llm_images():
#     # Initialize GPT model
#     llm = ChatOpenAI(
#         openai_api_key=OPENAI_API_KEY,
#         model="gpt-4o", # TODO: change all this to use gpt image or something else
#         temperature=0
#     )
    
#     return llm

# Custom chat message history class
class CustomChatMessageHistory(BaseChatMessageHistory):
    def __init__(self, messages):
        self.messages = []
        # Convert messages to LangChain format
        for msg in messages:
            if msg["role"] == "user":
                self.messages.append(HumanMessage(content=msg["content"]))
            elif msg["role"] == "assistant":
                self.messages.append(AIMessage(content=msg["content"]))
    
    def add_message(self, message):
        self.messages.append(message)
    
    def clear(self):
        self.messages = []

# Initialize database connection and models
db = init_chroma_client()
llm, retriever = init_llm_retriever(db)
# llm_images = init_llm_images()

@app.post("/class")
async def get_class(request: Request):
    try:
        payload = await request.json()

        image = payload["image"]

        # OpenAI API endpoint for chat completions
        api_url = "https://api.openai.com/v1/chat/completions"
        
        # Prepare headers with API key
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {OPENAI_API_KEY}"
        }
        
        prompt = """
        Tu única función es identificar plantas, como frutas y verduras.

        Responde con el nombre de la clase identificada.

        Si no encuentras una clase a identificar, responde con "ERROR".
        """

        payload = {
            "model": "gpt-4o",
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"{image}"
                            }
                        }
                    ]
                }
            ],
        }
        
        # Send the request to OpenAI API
        response = requests.post(api_url, headers=headers, json=payload)
        
        # Check if the request was successful
        if response.status_code == 200:
            result = response.json()
            analysis_text = result["choices"][0]["message"]["content"]
            return {"answer": analysis_text}
        else:
            raise HTTPException(
                status_code=response.status_code,
                detail=f"Error from OpenAI API: {response.text}"
            )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# @app.post("/class")
# async def get_class(request: Request):
#     try:
#         payload = await request.json()

#         image = payload["image"]

#         print(">>>>>>> CLASS")
#         print(payload)
#         print("<<<<<<< CLASS")

#         prompt = ChatPromptTemplate.from_template("""
#         Tu única función es identificar plantas, como frutas y verduras.

#         Responde con el nombre en mayúsculas de la clase identificada
        
#         La imagen es:
#         {image}
#         """)

#         chain = prompt | llm_images
        
#         response = chain.invoke({
#             "image": image,
#         })
        
#         return {
#             "answer": response.content,
#         }
    
#     except Exception as e:
#         logger.error(f"Error processing query: {str(e)}")
#         raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

@app.post("/query")
async def query_documents(request: Request):
    try:
        payload = await request.json()

        print(">>>>>>> QUERY")
        print(payload)
        print("<<<<<<< QUERY")

        messages = payload["messages"]
        doc_class = payload.get("class", None)

        # Create chat history from the messages
        chat_history = CustomChatMessageHistory(messages)
        
        # Get the last user message
        last_message = None
        for msg in reversed(messages):
            if msg["role"] == "user":
                last_message = msg["content"]
                break
        
        if not last_message:
            raise HTTPException(status_code=400, detail="No user message found in the provided messages")
        
        docs_and_scores = db.similarity_search_with_score(last_message, k=2)
        print(docs_and_scores)

        context = "\n".join(map(lambda doc: doc[0].page_content, docs_and_scores))

        print(context)

        # OpenAI API endpoint for chat completions
        api_url = "https://api.openai.com/v1/chat/completions"
        
        # Prepare headers with API key
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {OPENAI_API_KEY}"
        }
        
        prompt = f"""
        You are a helpful assistant that provides accurate information for kids and teens, based ONLY on the provided context. 
        If the answer cannot be found in the context, politely say so without making up information.
              
        Be kind, it's for a kid or teen.
                                                  
        Always respond in spanish.

        Your information should be valid for plants, fruits or vegetables in Uruguay.

        This query is related to the class: {doc_class}. 
        Focus your answer specifically on this topic area when relevant and when class is defined.

        Never say stuff like 'Based on the provided information' or anything related to your context documents as an assistant.
        
        Context information is below:
        {context}
        
        Chat History:
        {chat_history.messages}
                                                  
        Given the context information and not prior knowledge, answer the query.
        """

        payload = {
            "model": "gpt-4o",
            "messages": [
                {
                    "role": "system",
                    "content": [
                        {"type": "text", "text": prompt},
                    ]
                },
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": last_message},
                    ]
                }
            ],
        }
        
        # Send the request to OpenAI API
        response = requests.post(api_url, headers=headers, json=payload)
        
        # Check if the request was successful
        if response.status_code == 200:
            result = response.json()
            analysis_text = result["choices"][0]["message"]["content"]
            return {"answer": analysis_text} # TODO: add sources
        else:
            raise HTTPException(
                status_code=response.status_code,
                detail=f"Error from OpenAI API: {response.text}"
            )
    
    except Exception as e:
        logger.error(f"Error processing query: {str(e)}")
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

if __name__ == "__main__":
    # Ejecutar la aplicación con uvicorn
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=port)