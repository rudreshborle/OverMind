import os
import chromadb
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Settings
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.core import StorageContext
from llama_index.embeddings.huggingface import HuggingFaceEmbedding

# Configure LlamaIndex to use a local, open-source embedding model
# Using all-MiniLM-L6-v2 with a short cache path to avoid Windows long path issues
def setup_local_embeddings():
    # Set a short cache directory to avoid Windows MAX_PATH (260 char) issues
    short_cache = os.path.join(os.getcwd(), ".hf_cache")
    os.environ["HF_HOME"] = short_cache
    os.environ["SENTENCE_TRANSFORMERS_HOME"] = short_cache
    
    embed_model = HuggingFaceEmbedding(
        model_name="all-MiniLM-L6-v2",
        cache_folder=short_cache
    )
    Settings.embed_model = embed_model
    # We only use LlamaIndex for retrieval/indexing, not generation.
    Settings.llm = None

def get_chroma_client():
    # Use a local persistent directory for ChromaDB at the project root
    db_path = os.path.join(os.getcwd(), ".chroma_db")
    return chromadb.PersistentClient(path=db_path)

def index_codebase(source_dir: str = "src"):
    """Reads the source directory, embedded it using a local model, and indexes it into ChromaDB."""
    print(f"Indexing codebase at {source_dir} using local embeddings...")
    setup_local_embeddings()
    
    # Load documents from the directory (only Python/txt/md files usually for codebases)
    documents = SimpleDirectoryReader(
        source_dir, 
        recursive=True, 
        required_exts=[".py", ".md", ".txt"]
    ).load_data()
    
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

def query_codebase(query: str, top_k: int = 3) -> str:
    """Query the indexed codebase using Semantic Search."""
    setup_local_embeddings()
    
    db = get_chroma_client()
    chroma_collection = db.get_or_create_collection("codebase_index")
    vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
    
    index = VectorStoreIndex.from_vector_store(
        vector_store,
    )
    
    # We use a retriever instead of a query engine because we only want the raw text 
    # context chunks back, not an LLM-synthesized answer (our Architect does that).
    retriever = index.as_retriever(similarity_top_k=top_k)
    nodes = retriever.retrieve(query)
    
    context = "\n\n".join([f"--- File/Context Snippet ({n.metadata.get('file_name', 'Unknown')}) ---\n{n.get_text()}" for n in nodes])
    return context if context else "No relevant context found in the codebase."

if __name__ == "__main__":
    # Test indexing
    index_codebase("src")
    print(query_codebase("Where are the crewai agents defined?"))
