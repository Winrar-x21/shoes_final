import json
import os

user_configs = os.path.join(os.path.dirname(__file__), 'configs')


def user_exists(user_id: str):
    return f'{user_id}.json' in os.listdir(user_configs)


def write_user_config(user_id: str, config: dict):
    with open(os.path.join(user_configs, f'{user_id}.json'), 'w+') as f:
        json.dump(config, f)


def read_user_config(user_id: str):
    with open(os.path.join(user_configs, f'{user_id}.json'), 'r') as f:
        return json.load(f)


def update_user_config(user_id: str, keys_to_update: dict):
    old_config = read_user_config(user_id=user_id)
    for key in keys_to_update:
        if key in old_config:
            old_config[key] = keys_to_update[key]
    write_user_config(user_id=user_id, config=old_config)