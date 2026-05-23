import logging
from config import top_k,similarity_threshold,chromadb_collection_name
import chromadb
logger = logging.getLogger(__name__)

def get_chroma_collection(collection_name=chromadb_collection_name):
    chroma_client = chromadb.PersistentClient(path="./chroma_db")
    try:
        collection = chroma_client.get_or_create_collection(name=collection_name)
    except Exception as e:
        logger.error(f"Error getting or creating Chroma collection {collection_name}: {e}")
        raise
    return collection

collection = get_chroma_collection()


def retrieve_related_chunks(query, top_k=top_k, similarity_threshold=similarity_threshold, collection_name=chromadb_collection_name):
    logger.info(f"Retrieving related chunks for query: {query}")
    #if query is too big chunk it
    if len(query) > 100000:
        query_chunks = chunk_text(query)
    else:
        query_chunks = [query]
    query_embeddings = embed_chunks(query_chunks) # Embed all query chunks in one go
    
    collection = get_chroma_collection(collection_name)
    
    results = collection.query(
        query_embeddings=query_embeddings,
        n_results=top_k
    )

    # Filter results by similarity_threshold if needed, but ChromaDB's query already returns most similar
    # The 'distances' field in results can be used for this if filtering by an absolute threshold is required.
    # For now, we'll return the top_k directly.
    
    retrieved_documents = results['documents']
    retrieved_distances = results['distances']
    retrieved_ids = results['ids']

    # Flatten the list of lists returned by ChromaDB query
    flat_documents = [item for sublist in retrieved_documents for item in sublist]
    flat_distances = [item for sublist in retrieved_distances for item in sublist]
    flat_ids = [item for sublist in retrieved_ids for item in sublist]
    
    # Combine into a list of tuples (id, similarity, document)
    formatted_results = []
    for i in range(len(flat_documents)):
        if 1 - flat_distances[i] >= similarity_threshold: # Assuming distance is L2, 1-distance approximates cosine similarity
            formatted_results.append((flat_ids[i], 1 - flat_distances[i], flat_documents[i]))
    
    logger.info(f"Found {len(formatted_results)} related chunks.")
    return formatted_results

def add_chunks_to_database(chunk_ids, chunks, embeddings, metadatas=None, collection_name=chromadb_collection_name):
    collection = get_chroma_collection(collection_name)
    
    collection.add(
        ids=chunk_ids,
        documents=chunks,
        embeddings=embeddings,
        metadatas=metadatas
    )
    
    logger.info(f"Successfully Added {len(chunks)} chunks to Chroma collection '{collection_name}'.")
    return collection
