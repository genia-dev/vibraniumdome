import ast
import json
import logging
import os
from datetime import datetime
from uuid import uuid4

import yaml
from pydantic import BaseModel
import requests

logger = logging.getLogger(__name__)


def safe_loads_dictionary_string(dictionary_string: str = ""):
    parsed_dictionary = {}
    try:
        if dictionary_string:
            parsed_dictionary = ast.literal_eval(dictionary_string)
    except Exception:
        logger.error("dictionary_string could not be parser: %s", dictionary_string)
    return parsed_dictionary


def safe_loads_json(json_string: str):
    try:
        parsed_json = json.loads(json_string)
    except json.JSONDecodeError:
        logger.warn("json_string could not be parser: %s", json_string)
        parsed_json = {}
    return parsed_json


def safe_loads_yaml(full_path: str):
    with open(full_path, "r") as f:
        return yaml.safe_load(f)


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
        return obj.model_dump()
    return obj

def check_api_token(vibranium_dome_base_url, vibranium_dome_api_key) -> bool:
    full_url = f"{vibranium_dome_base_url}/api/trpc/validateAPIToken"
    headers = {"Authorization": f"Bearer {vibranium_dome_api_key}"}
    try:
        response = requests.get(full_url, headers=headers)
        logger.debug(response)
        return response.ok
    except Exception:
        logger.exception("failed to check_api_token")
        return False
