from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from controllers import rag_controller
from core.vector_store import view_collection
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

class QueryRequest(BaseModel):
    query: str


@router.post("/retrieve")
async def retrieve_chunks(request: QueryRequest):
    try:
        results = rag_controller.retrieve_chunks_controller(request)
        return {"results": results}
    except Exception as e:
        logger.exception("Error during retrieval")
        raise HTTPException(status_code=500, detail="Internal Server Error during retrieval")

@router.get("/view_database")
async def view_database():
    try:
        return view_collection()
    except Exception as e:
        logger.exception("Error during retrieval")
        raise HTTPException(status_code=500, detail="Internal Server Error during retrieval")
