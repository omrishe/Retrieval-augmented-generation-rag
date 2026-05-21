import os
from rag import retrieve_related_chunks
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import logging
from dotenv import load_dotenv
from config import top_k
from ingest import initialize_rag_pipeline

load_dotenv() # Load environment variables from .env file

# Sets up logging to see messages in console
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
initialize_rag_pipeline()
app = FastAPI()

class QueryRequest(BaseModel):
    query: str
    top_k: int = top_k

#listening
@app.post("/retrieve")
async def retrieve(request: QueryRequest):
    try:
        results = retrieve_related_chunks(request.query, top_k=request.top_k)
        return {"results": results}
    except Exception as e:
        logger.exception("Error during retrieval")
        raise HTTPException(status_code=500, detail="Internal Server Error during retrieval")
