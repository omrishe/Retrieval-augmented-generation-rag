import logging
logger = logging.getLogger(__name__)
import os
from openai import OpenAI
import random


#function to embed the chunks
def embed_chunks(chunks,retry_attempt=2):
    # Use mock embeddings if MOCK_EMBEDDINGS environment variable is set to 'true'
    if os.environ.get("MOCK_EMBEDDINGS", "false").lower() == "true":
        logger.info("Using mock embeddings.")
        return embed_chunks_mock(chunks)

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
            return embed_chunks(chunks,retry_attempt-1)
        else:
            logger.error("Failed to embed chunks after multiple retries.")
            raise Exception("failed to embed chunks")
            
def embed_chunks_mock(chunks):
    embeddings = []
    for chunk in chunks:
        # generate a fake vector of length 1536 (like text-embedding-3-small)
        embeddings.append([random.random() for _ in range(1536)])
    return embeddings

