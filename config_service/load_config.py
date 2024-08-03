import json

def load_config(config_name: str):
    with open(f'config_service/config/config_{config_name}.json') as f:
        return json.load(f)