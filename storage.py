# storage.py
# Saves and loads YouTube channel data to/from a local JSON file

import json
import os

STORAGE_DIR = "local_data"


def save_to_local(channel_id, youtube_channel_data):
    """
    Saves the fetched YouTube data dict to a local JSON file.
    Uses atomic write (temp file + rename) to prevent corruption on interrupted saves.
    """
    if not youtube_channel_data or not youtube_channel_data.get("channel_info"):
        raise ValueError("Cannot save empty or invalid YouTube channel data.")

    os.makedirs(STORAGE_DIR, exist_ok=True)
    file_path = os.path.join(STORAGE_DIR, f"{channel_id}.json")
    tmp_path  = file_path + ".tmp"

    try:
        with open(tmp_path, "w", encoding="utf-8") as f:
            json.dump(youtube_channel_data, f, indent=4, ensure_ascii=False)
        os.replace(tmp_path, file_path)   # atomic rename — safe on all OS
    except Exception as e:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)
        raise IOError(f"Failed to save data for channel '{channel_id}': {e}")

    print(f"✅ Data saved locally to: {file_path}")
    return file_path


def load_from_local(channel_id):
    """
    Loads the previously saved JSON file for the given channel_id.
    Raises FileNotFoundError if no file exists, ValueError if file is corrupted.
    """
    file_path = os.path.join(STORAGE_DIR, f"{channel_id}.json")

    if not os.path.exists(file_path):
        raise FileNotFoundError(
            f"No local data found for channel: '{channel_id}'. "
            f"Please fetch the channel data first."
        )

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        raise ValueError(
            f"The saved JSON file for channel '{channel_id}' is corrupted. "
            f"Delete '{file_path}' and re-fetch the channel. Details: {e}"
        )