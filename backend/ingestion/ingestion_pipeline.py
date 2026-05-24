import logging
from .loader import retrieve_dataset
from core import  embed_chunks, add_chunks_to_database
from .rag import ingestion_chunk_text
from .preprocessor import dataset_preprocessor
from config import  batch_threshold, dataset_name,SOURCE_TYPE

#Sets up logging to see messages in console
logger = logging.getLogger(__name__)

def initialize_rag_pipeline():
    #dataset_name = input("Enter your file name(with File extension): ")#will be changed next update
    
    if( SOURCE_TYPE== "dataset"):
        # retrieve dataset
        dataset = retrieve_dataset(dataset_name=dataset_name)
        batch = []
        batch_ids = []
        batch_metadatas = []
        
        for i, row in enumerate(dataset):
            #preprocessing(text cleaning and format)
            record=dataset_preprocessor(row[0])
            logger.info(f"Processing text: {record} \n")
            text_chunks = ingestion_chunk_text(record["text"])
            
            # Extract metadata
            metadata = record.copy()
            #deletes field "text" from metadata
            metadata.pop("text", None)
            
            # assign unique id to each chunk eg:1-2
            for j, chunk in enumerate(text_chunks):
                batch.append(chunk)
                batch_ids.append(f"{i}-{j}")
                batch_metadatas.append(metadata)
            
            # if batch number >= threshold send all of them to the embedder
            if(batch_threshold <= len(batch)):
                batch_embeddings = embed_chunks(batch)
                add_chunks_to_database(batch_ids, batch, batch_embeddings, metadatas=batch_metadatas)
                # clear batches
                batch = []
                batch_ids = []
                batch_metadatas = []
        
        # Process remaining chunks
        if batch:
            batch_embeddings = embed_chunks(batch)
            add_chunks_to_database(batch_ids, batch, batch_embeddings, metadatas=batch_metadatas)
            
        logger.info("all chunks embedded and mapped to IDs")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='\n%(asctime)s - %(levelname)s - %(message)s\n')
    try:
        initialize_rag_pipeline()
    except RuntimeError:
        logger.exception("RAG pipeline init failed")
    except FileNotFoundError:
        logger.exception("file was not found")
    except Exception:
        logger.exception("An unexpected error occurred during RAG pipeline initialization")
