# database.py
# Creates the SQLite database and all tables

import sqlite3

DB_PATH = "youtube_analytics.db"


def create_database():
    """
    Creates all tables if they don't already exist.
    Safe to call repeatedly — uses IF NOT EXISTS throughout.
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("PRAGMA foreign_keys = ON;")

    # ── Channels ──────────────────────────────────────────────────────────────
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS channels (
            channel_id          TEXT PRIMARY KEY,
            title               TEXT NOT NULL,
            description         TEXT,
            published_at        TEXT,
            custom_url          TEXT,
            country             TEXT,
            subscriber_count    INTEGER DEFAULT 0,
            view_count          INTEGER DEFAULT 0,
            video_count         INTEGER DEFAULT 0,
            uploads_playlist_id TEXT
        );
    """)

    # ── Playlists ─────────────────────────────────────────────────────────────
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS playlists (
            playlist_id  TEXT PRIMARY KEY,
            channel_id   TEXT NOT NULL,
            title        TEXT NOT NULL,
            description  TEXT,
            published_at TEXT,
            FOREIGN KEY (channel_id) REFERENCES channels(channel_id)
        );
    """)

    # ── Videos ───────────────────────────────────────────────────────────────
    # NOTE: column is 'title' (NOT 'video_title') and 'duration_iso' (NOT 'duration')
    # This matches the live DB schema exactly — do not rename these columns.
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS videos (
            video_id         TEXT PRIMARY KEY,
            channel_id       TEXT NOT NULL,
            playlist_id      TEXT,
            title            TEXT NOT NULL,
            description      TEXT,
            published_at     TEXT,
            views            INTEGER DEFAULT 0,
            likes            INTEGER DEFAULT 0,
            comments         INTEGER DEFAULT 0,
            duration_iso     TEXT,
            duration_seconds INTEGER DEFAULT 0,
            FOREIGN KEY (channel_id)  REFERENCES channels(channel_id),
            FOREIGN KEY (playlist_id) REFERENCES playlists(playlist_id)
        );
    """)

    conn.commit()
    conn.close()
    print("✅ Database & Tables Ready:", DB_PATH)