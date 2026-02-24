# main.py
# Entry point — run this to execute the full pipeline

from config import get_channel_id
from database import create_database
from api import build_youtube_channel_data
from storage import save_to_local, load_from_local
from db_insert import push_to_database

def main():
    # Step 1: Get Channel ID from user
    channel_id = get_channel_id()

    # Step 2: Create DB and tables (safe if already exists)
    create_database()

    # Step 3: Fetch data from YouTube API
    print(f"\n📡 Fetching data for channel: {channel_id} ...")
    youtube_channel_data = build_youtube_channel_data(channel_id)

    # Step 4: Save to local JSON storage
    save_to_local(channel_id, youtube_channel_data)

    # Step 5: Load from local and push to SQLite
    data = load_from_local(channel_id)
    push_to_database(channel_id, data)

if __name__ == "__main__":
    main()