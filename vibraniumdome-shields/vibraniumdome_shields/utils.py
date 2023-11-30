import json
import ast
import logging
import os
from datetime import datetime
from uuid import uuid4

from pydantic import BaseModel


logger = logging.getLogger(__name__)

def safe_loads_dictionary_string(dictionary_string: str):
    try:
        parsed_dictionary = ast.literal_eval(dictionary_string)
    except json.JSONDecodeError:
        logger.error("dictionary_string could not be parser: %s", dictionary_string)
        parsed_dictionary = {}
    return parsed_dictionary


def safe_loads_json(json_string: str):
    try:
        parsed_json = json.loads(json_string)
    except json.JSONDecodeError:
        logger.warn("json_string could not be parser: %s", json_string)
        parsed_json = {}
    return parsed_json


def is_blank(input: str):
    return not is_not_blank(input)


def is_not_blank(input: str):
    return input and input.strip()


def load_vibranium_home():
    if os.environ.get("VIBRANIUM_HOME") is not None:
        return os.environ.get("VIBRANIUM_HOME")
    else:
        return os.path.join(os.getcwd(), "")


def uuid4_str():
    return str(uuid4())


def timestamp_str():
    return datetime.isoformat(datetime.utcnow())


# Define a custom encoding function to handle Pydantic objects
def pydantic_json_encoder(obj):
    if isinstance(obj, BaseModel):
        return obj.dict()
    return obj
