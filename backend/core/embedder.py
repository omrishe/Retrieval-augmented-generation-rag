import logging
logger = logging.getLogger(__name__)
import os
from config import embedding_mode
from openai import OpenAI
import random
import time


#function to embed the chunks
def embed_chunks(chunks,retry_attempt=2):
    # Use mock embeddings if embedding_mode config variable is set to 'true'
    if embedding_mode == "mock":
        logger.info("Using mock embeddings.")
        return embed_chunks_mock(chunks)
    if embedding_mode == "local":
        logger.info("Using local embeddings.")
        return local_chunks_embed(chunks)
    try:
        client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
        # Send all chunks in a single call
        logger.info(f"Trying to send {len(chunks)} chunks for embedding.")
        if not isinstance(chunks, list):
            chunks = [chunks]
        resp = client.embeddings.create(
            model="text-embedding-3-small",
            input=chunks)
        embeddings = [e.embedding for e in resp.data]
        return embeddings
    except Exception as e:
        logger.warning(f"Retrying to send chunks... attempts left: {retry_attempt}. Error: {e}")
        if(retry_attempt>0):
            time.sleep(3)
            return embed_chunks(chunks,retry_attempt-1)
        else:
            logger.error("Failed to embed chunks after multiple retries.")
            raise RuntimeError("Embedding generation failed")
            
def embed_chunks_mock(chunks):
    embeddings = []
    for chunk in chunks:
        # generate a fake vector of length 1536 (like text-embedding-3-small)
        embeddings.append([random.random() for _ in range(1536)])
    return embeddings


def local_chunks_embed(chunks):
    from sentence_transformers import SentenceTransformer
    # Cache the model on the function to avoid reloading it on every call
    if not hasattr(local_chunks_embed, "model"):
        logger.info("Loading local SentenceTransformer model...")
        # 'all-MiniLM-L6-v2' outputs 384-dimensional embeddings. 
        local_chunks_embed.model = SentenceTransformer("all-MiniLM-L6-v2")
        
    if not isinstance(chunks, list):
        chunks = [chunks]
        
    logger.info(f"Generating local embeddings for {len(chunks)} chunks.")
    embeddings = local_chunks_embed.model.encode(chunks)
    
    return embeddings.tolist()
