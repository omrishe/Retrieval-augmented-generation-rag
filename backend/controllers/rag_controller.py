from services import rag_service 
from config import top_k,similarity_threshold,vector_collection_name

def retrieve_chunks_controller(request):
    return rag_service.retrieve_related_chunks(query=request.query,
        top_k=top_k,
        similarity_threshold=similarity_threshold,
        collection_name=vector_collection_name)