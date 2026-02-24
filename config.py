# config.py
# Central configuration — Channel ID entered once, used everywhere

API_KEY = "AIzaSyAnIQ1aAqGbCnJml1R9QfKQ1qf3yPvNZq8"

def get_channel_id():
    channel_id = input("Enter YouTube Channel ID: ").strip()
    if not channel_id:
        raise ValueError("Channel ID cannot be empty.")
    return channel_id