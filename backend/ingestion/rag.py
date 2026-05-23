import logging
from config import  chunk_size,chunk_overlap
from core import tokenize,detokenize

logger = logging.getLogger(__name__)

#atm this slicing based on token length which can cause lost of
#semantic,maybe add recursive chunking while not the perfect solution might be good
#for non sample csv
def ingestion_chunk_text(text: str) -> list[str]:
    #turns text into tokens eg: [15496, 995] = tokenize("Hello world")
    tokens = tokenize(text)
    chunks = []
    start = 0
    while start < len(tokens):
        end = start + chunk_size
        chunk_tokens = tokens[start:end]
        chunks.append(detokenize(chunk_tokens))
        start = end - chunk_overlap
    return chunks

