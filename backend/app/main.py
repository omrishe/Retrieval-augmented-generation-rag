from fastapi import FastAPI
import logging
from dotenv import load_dotenv
from app.api import router
from fastapi.middleware.cors import CORSMiddleware
load_dotenv() # Load environment variables from .env file

# Sets up logging to see messages in console
logging.basicConfig(level=logging.INFO, format='\n%(asctime)s - %(levelname)s - %(message)s\n')
logger = logging.getLogger(__name__)
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)

#if collection is empty start ingesting
@app.on_event("startup")
def startup():
    from services import start_rag_ingestion
    start_rag_ingestion()

if __name__ == "__main__":
    import uvicorn
    logger.info("Starting FastAPI server...")
    uvicorn.run(app, host="127.0.0.1", port=8000)
