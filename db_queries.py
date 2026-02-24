# db_queries.py
# SQL helper functions used by the Streamlit dashboard (app.py).

import sqlite3
from database import DB_PATH


def _connect():
    return sqlite3.connect(DB_PATH)


def get_channel_summary(channel_id: str) -> dict | None:
    """Return a dictionary of channel metadata or None if not found."""
    conn = _connect()
    cursor = conn.cursor()
    row = cursor.execute(
        """
        SELECT title, description, published_at, custom_url, country,
               subscriber_count, view_count, video_count
        FROM channels
        WHERE channel_id = ?
        """,
        (channel_id,)
    ).fetchone()
    conn.close()
    if not row:
        return None
    keys = [
        "title",
        "description",
        "published_at",
        "custom_url",
        "country",
        "subscriber_count",
        "view_count",
        "video_count",
    ]
    return dict(zip(keys, row))


def get_filtered_videos(channel_id: str, date_from: str, date_to: str) -> list:
    """Return video rows for the given channel and date range.

    Each tuple matches the layout used by app.py:
    (video_id, title, views, likes, comments, duration_seconds)
    """
    conn = _connect()
    cursor = conn.cursor()
    rows = cursor.execute(
        """
        SELECT video_id, title, views, likes, comments, duration_seconds
        FROM videos
        WHERE channel_id = ?
          AND date(published_at) BETWEEN date(?) AND date(?)
        ORDER BY published_at ASC
        """,
        (channel_id, date_from, date_to),
    ).fetchall()
    conn.close()
    return rows


def get_top_videos(channel_id: str, date_from: str, date_to: str, limit: int = 10) -> list:
    """Return the top videos ordered by views within the date window."""
    conn = _connect()
    cursor = conn.cursor()
    rows = cursor.execute(
        """
        SELECT video_id, title, views, likes, comments, duration_seconds
        FROM videos
        WHERE channel_id = ?
          AND date(published_at) BETWEEN date(?) AND date(?)
        ORDER BY views DESC
        LIMIT ?
        """,
        (channel_id, date_from, date_to, limit),
    ).fetchall()
    conn.close()
    return rows


def get_videos_by_month(channel_id: str, date_from: str, date_to: str) -> list:
    """Return list of (month,label),count tuples sorted by month.

    The month string format is YYYY-MM and matches how the app uses it
    for labels/values.
    """
    conn = _connect()
    cursor = conn.cursor()
    rows = cursor.execute(
        """
        SELECT strftime('%Y-%m', published_at) AS month, COUNT(*)
        FROM videos
        WHERE channel_id = ?
          AND date(published_at) BETWEEN date(?) AND date(?)
        GROUP BY month
        ORDER BY month
        """,
        (channel_id, date_from, date_to),
    ).fetchall()
    conn.close()
    return rows
