import os
import chardet
import logging
import csv
from config import MIN_ENCODING_CONFIDENCE, PROJECT_ROOT
logger = logging.getLogger(__name__)


#loader purpose is to turn data into text

def retrieve_dataset(dataset_name="Software Questions.csv",path="datasets",chunk_size=1000):
    dataset_path=retrieve_path (dataset_name, path)
    result=detect_encoding(path=dataset_path)
    
    if(result["confidence"]>MIN_ENCODING_CONFIDENCE):
        logger.info(f"Successfully created iterator in dataset: {dataset_path}")
        # return an iteratable of the dataset
        return stream_csv(dataset_path, result["encoding"], batch_size=1)
    else:
        raise RuntimeError("Low encoding confidence, cannot safely read file")
        
def retrieve_path (dataset_name:str, path:str):
    BASE_DIR = os.getenv("DATASET_DIR", path)
    dataset_path = PROJECT_ROOT / BASE_DIR / dataset_name  # path to the dataset
    #check valid path
    if not dataset_path.exists():
        logger.error(f"Dataset not found at: {dataset_path}")
        raise FileNotFoundError(f"Dataset not found: {dataset_path}")
    return str(dataset_path)


def detect_encoding(path:str):
    encoding = None
    confidence = None
    try:
        #detecting encoding with probablitiy
        with open(path, "rb") as f:
            result = chardet.detect(f.read(10000))
            encoding = result["encoding"]
            confidence = result.get("confidence", 0)

        if(not encoding):
            raise RuntimeError(f"Encoding detection failed: encoding={encoding}, confidence={confidence}")
        
        logger.info(f"Detected encoding: {encoding} with confidence: {confidence * 100}%")
        return {"encoding":encoding,"confidence":confidence}

    except (OSError, UnicodeError) as e:
        logger.exception("Failed to detect encoding or load dataset")
        raise RuntimeError(f"Failed to load dataset: {e}")


def stream_csv(file_path:str, encoding:str, batch_size:int):
    with open(file_path, "r", encoding=encoding, newline="",errors="replace") as f:
        reader = csv.DictReader(f)#creates an iterator

        batch = []

        for row in reader:
            batch.append(row)
            batch_len=len(batch)
            if batch_len == batch_size:
                    yield batch
                    batch = []

        if batch:
            yield batch