import json
import os
from pathlib import Path

CONFIG_DIR = Path("D:/自制连点器/config")
CONFIG_FILE = CONFIG_DIR / "config.json"

DEFAULT_CONFIG = {
    "click_type": "left",
    "click_action": "single",
    "interval": 1.0,
    "random_offset": 0.2,
    "click_count": 0,
    "stop_condition": "none",
    "stop_count": 100,
    "stop_time": 300,
    "hotkey_start": "f9",
    "hotkey_stop": "f10",
    "hotkey_pause": "f11",
    "theme": "dark",
    "targets": [],
    "color_monitor": {
        "enabled": False,
        "x": 0,
        "y": 0,
        "width": 50,
        "height": 50,
        "target_color": [255, 0, 0],
        "tolerance": 30
    }
}


def load_config():
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    if CONFIG_FILE.exists():
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                return {**DEFAULT_CONFIG, **json.load(f)}
        except:
            return DEFAULT_CONFIG.copy()
    return DEFAULT_CONFIG.copy()


def save_config(config):
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=4, ensure_ascii=False)


def export_config(config, path):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=4, ensure_ascii=False)


def import_config(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)
