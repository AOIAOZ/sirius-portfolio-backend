import os
import sys
import json
import logging

from ..models.prompt import Prompt

def create_logger(name: str = ""):
    # Create a logger
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)  # Set desired level

    # Make sure the "logs" directory exists
    if not os.path.exists("logs"):
        os.makedirs("logs")

    # Create a StreamHandler that writes log entries to stdout
    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setLevel(logging.DEBUG)

    # Create a FileHandler that writes log entries to "logs/<name>.log"
    log_file_path = f"logs/{name}.log" if name else "logs/default.log"
    file_handler = logging.FileHandler(log_file_path)
    file_handler.setLevel(logging.DEBUG)

    # Create a log formatter and add it to both handlers
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    stream_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)

    # Add handlers to the logger
    logger.addHandler(stream_handler)
    logger.addHandler(file_handler)

    return logger


def parse_config(config_path:str=None):
    if not config_path:
        raise ValueError("Empty config path provided")
    with open(config_path, "r", encoding='utf-8') as f:
        data = json.load(f)
    model_id = data["prediction"]["model_id"]
    prompt = Prompt(data["prediction"]["prompt"])
    temperature = data["prediction"]["temperature"]
    thinking_budget = data["prediction"]["thinking_budget"]
    proxies = (d for d in data["proxies"])
    return model_id, prompt, temperature, thinking_budget, proxies
