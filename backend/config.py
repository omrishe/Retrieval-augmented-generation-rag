# Configuration for the RAG demo
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

PROJECT_ROOT = Path(__file__).parent.absolute()
MIN_ENCODING_CONFIDENCE = float(os.getenv("MIN_ENCODING_CONFIDENCE", "0.5"))

chunk_size = 100
chunk_overlap = 25
batch_size = 5
dataset_name = "Software Questions.csv"
chromadb_collection_name = "rag_chunks"
top_k = 3
similarity_threshold = 0.7
