from core.vector_store import query_db
from core import embed_chunks
from services import chunk_text
import logging
logger = logging.getLogger(__name__)



def retrieve_related_chunks(query, top_k, similarity_threshold, collection_name):
    logger.info(f"Retrieving related chunks for query: {query}")
    #if query is too big chunk it
    if len(query) > 100000:
        query_chunks = chunk_text(query)
    else:
        query_chunks = [query]
    logger.info(f"testing text:{query}")
    query_embeddings = embed_chunks(query_chunks) # Embed all query chunks in one go
    
    
    results = query_db(query_embeddings, top_k, collection_name)
    
    formated_data = format_data(results,similarity_threshold)
    return formated_data

def format_data(results,similarity_threshold):
    # Filter results by similarity_threshold if needed, but ChromaDB's query already returns most similar
    # The 'distances' field in results can be used for this if filtering by an absolute threshold is required.
    # For now, we'll return the top_k directly.
    
    retrieved_documents = results['documents']
    retrieved_distances = results['distances']
    retrieved_ids = results['ids']

    #flatten the list of lists returned by ChromaDB query
    flat_documents = [item for sublist in retrieved_documents for item in sublist]
    flat_distances = [item for sublist in retrieved_distances for item in sublist]
    flat_ids = [item for sublist in retrieved_ids for item in sublist]
    
    #combine into a list of tuples (id, similarity, document)
    formatted_results = []
    for i in range(len(flat_documents)):
        similarity = 1 - flat_distances[i]
        logger.info(f"similiarity is:{similarity}")
        if similarity >= similarity_threshold: # we are using cosine similarity
            formatted_results.append((flat_ids[i], similarity, flat_documents[i]))
    
    logger.info(f"Found {len(formatted_results)} related chunks.")
    return formatted_results

def start_rag_ingestion():
    from core import collection
    from ingestion import ingestion_pipeline
    print("number of collections is:",collection.count())
    if collection.count() == 0:
        ingestion_pipeline.initialize_rag_pipeline()