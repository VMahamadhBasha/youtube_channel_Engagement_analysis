# db_insert.py
# Reads local JSON and inserts all data into SQLite.
# Column names MUST match the DB schema in database.py exactly.

import sqlite3
from database import DB_PATH


def insert_channel(cursor, channel_id, channel_info):
    """Upserts the channel row. channel_info is keyed by channel_id."""
    info = channel_info[channel_id]
    cursor.execute("""
        INSERT OR REPLACE INTO channels (
            channel_id, title, description, published_at,
            custom_url, country, subscriber_count,
            view_count, video_count, uploads_playlist_id
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        channel_id,
        info.get("title"),
        info.get("description"),
        info.get("published_at"),
        info.get("custom_url"),
        info.get("country"),
        info.get("subscriber_count", 0),
        info.get("view_count", 0),
        info.get("video_count", 0),
        info.get("uploads_playlist_id"),
    ))


def insert_playlists(cursor, channel_id, playlists):
    """Upserts all playlist rows for the channel."""
    for playlist_id, pl in playlists.items():
        cursor.execute("""
            INSERT OR REPLACE INTO playlists (
                playlist_id, channel_id, title, description, published_at
            ) VALUES (?, ?, ?, ?, ?)
        """, (
            playlist_id,
            channel_id,
            pl.get("title"),
            pl.get("description"),
            pl.get("published_at"),
        ))


def insert_videos(cursor, channel_id, videos):
    """
    Upserts all video rows for the channel.

    JSON key mapping → DB column:
        video_title       → title        (DB uses 'title', JSON uses 'video_title')
        video_description → description
        duration          → duration_iso (DB uses 'duration_iso', JSON uses 'duration')
        duration_seconds  → duration_seconds
    """
    for video_id, vid in videos.items():
        cursor.execute("""
            INSERT OR REPLACE INTO videos (
                video_id, channel_id, playlist_id,
                title, description, published_at,
                views, likes, comments,
                duration_iso, duration_seconds
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            video_id,
            channel_id,
            vid.get("playlist_id"),
            vid.get("video_title"),        # JSON key → DB column 'title'
            vid.get("video_description"),  # JSON key → DB column 'description'
            vid.get("published_at"),
            vid.get("views", 0),
            vid.get("likes", 0),
            vid.get("comments", 0),
            vid.get("duration"),           # JSON key → DB column 'duration_iso'
            vid.get("duration_seconds", 0),
        ))


def push_to_database(channel_id, youtube_channel_data):
    """
    Main entry point called by app.py.
    Inserts channel, playlists, and videos into the DB in a single transaction.
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("PRAGMA foreign_keys = ON;")

    try:
        insert_channel(cursor, channel_id, youtube_channel_data["channel_info"])
        print("✅ Channel inserted.")

        insert_playlists(cursor, channel_id, youtube_channel_data["playlists"])
        print("✅ Playlists inserted.")

        insert_videos(cursor, channel_id, youtube_channel_data["videos"])
        print("✅ Videos inserted.")

        conn.commit()
        print("🎉 All data pushed to SQLite successfully!")
    except Exception as e:
        conn.rollback()
        raise RuntimeError(f"Database insert failed and was rolled back: {e}")
    finally:
        conn.close()