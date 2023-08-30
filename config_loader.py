import json

def load_config():
    try:
        with open('config.json', 'r') as f:
            config = json.load(f)
        return config
    except FileNotFoundError:
        print("config.json file not found")
        return None
    except json.JSONDecodeError:
        print("Error decoding config.json")
        return None
