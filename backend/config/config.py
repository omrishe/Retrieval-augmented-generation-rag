# Configuration for the RAG
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

PROJECT_ROOT = Path(__file__).parent.parent.absolute()
MIN_ENCODING_CONFIDENCE = float(os.getenv("MIN_ENCODING_CONFIDENCE", "0.5"))
STRICT_CLEANING = os.getenv("STRICT_CLEANING", "False").lower() == "true"
SOURCE_TYPE = os.getenv("SOURCE_TYPE","dataset")
chunk_size = 300
chunk_overlap = 50
batch_threshold = 5
dataset_name = "Software Questions.csv"
chromadb_collection_name = "rag_chunks"
top_k = 3
similarity_threshold = 0.7
tokenizer_encoding = os.getenv("TOKENIZER_ENCODING", "cl100k_base")

