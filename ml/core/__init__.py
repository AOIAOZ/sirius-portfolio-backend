import os
from pathlib import Path
from .config import create_logger, parse_config

config_file_path = os.environ.get("CONFIG_PATH")
if not config_file_path:
    config_file_path = Path(__file__).parent.parent / 'config.json'

model_id, model_prompt, model_temperature, model_thinking_budget, proxies = parse_config(config_file_path)
logger = create_logger("Prediction")
