import re
from config import STRICT_CLEANING,dataset_name
import logging
logger = logging.getLogger(__name__)

def dataset_preprocessor(row:str):
    return custom_preprocessing(row)

#takes a dictionary row and turn it to a string in format of:
#key1:val1
#
# ---
#
#key2:val2...
def dict_to_text(row: dict) -> str:
    parts = []

    for key, val in row.items():
        if val is None:
            continue

        key = key.strip()
        val = val.strip()
        parts.append(f"{key}: {val}")

    if not parts:
        return ""

    text = " | ".join(parts)
    return clean_text(text)

def list_to_text(row: dict) -> str:
    parts = []

    for  val in row:
        if val is None:
            continue

        val = val.strip()
        parts.append(f"{val}")

    if not parts:
        return ""

    text = " \n ".join(parts)
    return clean_text(text)

def clean_text(text:str):
    #remove control chars (not including tab and new line)
    text = re.sub(r'[\x00-\x08\x0b-\x1f\x7f]', ' ', text)
    # remove special characters
    if STRICT_CLEANING:
        text = re.sub(r'[^a-zA-Z0-9\s|:?!]', ' ', text)
    # remove extra whitespace
    text = re.sub(r'\s+', ' ', text)
    # convert to lowercase and remove trailing and starting white spaces
    text = text.lower().strip()
    return text

#since each dataset and data input in general is different you need to define
#a custom format fit for each dataset to get the maximum results so thats why
#i added this function
def custom_preprocessing(row:dict):
    if(dataset_name == "Software Questions.csv"):
        #creates a dict with text:question and answer,Difficulty:Difficulty,catagory:catagory,Question Number:Question Number
        text=dict_to_text({"Question": row["Question"],"Answer":row["Answer"]})
        full_data = {"text":text,"Category":row["Category"],"Difficulty":row["Difficulty"],"Question Number":row["Question Number"]}
        return full_data
    else:
         return row