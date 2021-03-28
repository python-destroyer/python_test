import yaml

from data_base import BASE_DIR

config_path = BASE_DIR / 'test2' / 'The_task' / 'config.yaml'

def get_config(path):
    with open(path) as f:
        config = yaml.safe_load(f)
    return config

config = get_config(config_path)