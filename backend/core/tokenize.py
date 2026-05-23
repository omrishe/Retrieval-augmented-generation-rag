import logging
logger = logging.getLogger(__name__)
import tiktoken
from config import  tokenizer_encoding,chunk_size,chunk_overlap

enc = tiktoken.get_encoding(tokenizer_encoding)

# Token utils
def tokenize(text: str) -> list[int]:
    return enc.encode(text)

def detokenize(tokens: list[int]) -> str:
    return enc.decode(tokens)

def chunk_text(text: str) -> list[str]:
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