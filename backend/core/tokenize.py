import logging
logger = logging.getLogger(__name__)
import tiktoken
from config import  tokenizer_encoding

enc = tiktoken.get_encoding(tokenizer_encoding)

# Token utils
def tokenize(text: str) -> list[int]:
    return enc.encode(text)

def detokenize(tokens: list[int]) -> str:
    return enc.decode(tokens)

