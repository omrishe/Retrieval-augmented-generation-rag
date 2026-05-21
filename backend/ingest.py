import os
import logging
from dotenv import load_dotenv
import utils.fileRetrieve as fr
from rag import row_to_text, chunk_text, embed_chunks, add_chunks_to_database
from config import chunk_size, chunk_overlap, batch_size, dataset_name

load_dotenv() #Load environment variables from .env file

#Sets up logging to see messages in console
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def initialize_rag_pipeline():
    dataset = fr.retrieve_file(dataset_name=dataset_name)  # retrieve dataset
    all_chunks = []
    chunk_ids = []
    chunk_embeddings = {}  # dictionary key: chunk_id, value: embedding
    for i, row in enumerate(dataset):
        text=row_to_text(row[0])
        logger.info(f"Processing text: {text} \n")
        chunks = chunk_text(text, chunk_size, overlap=chunk_overlap)
        # note: its extend not append - causes flat list not list of lists
        all_chunks.extend(chunks)
        # assign unique id to each chunk eg:1-2
        chunk_ids.extend([f"{i}-{j}" for j in range(len(chunks))])
    for start in range(0, len(all_chunks), batch_size):
        batch = all_chunks[start:start + batch_size]
        batch_ids = chunk_ids[start:start + batch_size]
        batch_embeddings = embed_chunks(batch)

        for cid, emb in zip(batch_ids, batch_embeddings):
            chunk_embeddings[cid] = emb
    add_chunks_to_database(chunk_ids, all_chunks, list(chunk_embeddings.values()))
    logger.info("all chunks embedded and mapped to IDs")

if __name__ == "__main__":
    try:
        initialize_rag_pipeline()
    except RuntimeError:
        logger.exception("RAG pipeline init failed")
    except FileNotFoundError:
        logger.exception("file was not found")
    except Exception:
        logger.exception("An unexpected error occurred during RAG pipeline initialization")
