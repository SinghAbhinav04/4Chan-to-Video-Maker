import os
import json

CONFIG_FILE = os.path.join(os.path.dirname(__file__), "config.json")

DEFAULT_CONFIG = {
    "llm_model": "accounts/fireworks/models/minimax-m2p7",
    "llm_temperature": 0.3,
    "llm_provider": "router",
    "gemini_api_key": "",
    "router_host": "127.0.0.1",
    "router_port": 3456,
    "video_fps": 30,
    "video_preset": "fast"
}

def load_config():
    if not os.path.exists(CONFIG_FILE):
        save_config(DEFAULT_CONFIG)
        return DEFAULT_CONFIG
    
    try:
        with open(CONFIG_FILE, "r") as f:
            config = json.load(f)
            # Merge with defaults to ensure all keys exist
            return {**DEFAULT_CONFIG, **config}
    except Exception as e:
        print(f"Error loading config: {e}")
        return DEFAULT_CONFIG

def save_config(config):
    try:
        with open(CONFIG_FILE, "w") as f:
            json.dump(config, f, indent=4)
    except Exception as e:
        print(f"Error saving config: {e}")

def update_config(new_data):
    current = load_config()
    current.update(new_data)
    save_config(current)
    return current
