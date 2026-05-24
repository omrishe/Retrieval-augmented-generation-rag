import logging
from config import vector_collection_name
import chromadb

logger = logging.getLogger(__name__)

def get_chroma_collection(collection_name=vector_collection_name):
    try:
        chroma_client = chromadb.PersistentClient(path="./chroma_db")
        #collection_exists = any(c.name == collection_name for c in chroma_client.list_collections())
        #from ingestion.ingestion_pipeline import initialize_rag_pipeline
        #initialize_rag_pipeline()
        collection = chroma_client.get_or_create_collection(name=collection_name, metadata={"hnsw:space": "cosine"})
        return collection
    except Exception as e:
        logger.error(f"Error getting or creating Chroma collection {collection_name}: {e}")
        raise
    

collection = get_chroma_collection()

def query_db(embeddings, top_k, collection_name):
    return collection.query(
        query_embeddings=embeddings,
        n_results=top_k)


def add_chunks_to_database(chunk_ids, chunks, embeddings, metadatas=None, collection_name=vector_collection_name):
    collection.add(
        ids=chunk_ids,
        documents=chunks,
        embeddings=embeddings,
        metadatas=metadatas
    )
    
    logger.info(f"Successfully Added {len(chunks)} chunks to Chroma collection '{collection_name}'.")
    return collection

def view_collection(collection_name=vector_collection_name):
    print("\ndatabase count is:", collection.count(), "\n")
    
    peek_data = collection.peek()
    
    #excluding embeddings column cause they are huge so they cause a crash and clutter the response
    safe_data = {
        "ids": peek_data.get("ids"),
        "documents": peek_data.get("documents"),
        "metadatas": peek_data.get("metadatas")
    }
    
    return {"database": safe_data}
