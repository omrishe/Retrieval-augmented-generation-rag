from core import tokenize,detokenize
from config import chunk_overlap,chunk_size


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