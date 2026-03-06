import os
import chromadb
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.core import StorageContext

def get_chroma_client():
    # Use a local persistent directory for ChromaDB
    db_path = os.path.join(os.getcwd(), ".chroma_db")
    return chromadb.PersistentClient(path=db_path)

def index_codebase(source_dir: str = "src"):
    """Reads the source directory and indexes it into ChromaDB."""
    print(f"Indexing codebase at {source_dir}...")
    
    # Load documents from the directory
    documents = SimpleDirectoryReader(source_dir, recursive=True).load_data()
    
    # Initialize Chroma client and get/create collection
    db = get_chroma_client()
    chroma_collection = db.get_or_create_collection("codebase_index")
    
    # Set up LlamaIndex storage context with Chroma
    vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
    storage_context = StorageContext.from_defaults(vector_store=vector_store)
    
    # Create the index
    index = VectorStoreIndex.from_documents(
        documents, storage_context=storage_context
    )
    
    print("Codebase indexing complete.")
    return index

def query_codebase(query: str):
    """Query the indexed codebase."""
    db = get_chroma_client()
    chroma_collection = db.get_or_create_collection("codebase_index")
    vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
    
    index = VectorStoreIndex.from_vector_store(
        vector_store,
    )
    
    query_engine = index.as_query_engine()
    response = query_engine.query(query)
    return str(response)

if __name__ == "__main__":
    # Test indexing
    index_codebase()
