# check.py — run this to diagnose dashboard issues
import sqlite3
from database import DB_PATH

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# Check if channel exists
channels = cursor.execute("SELECT channel_id, title, video_count FROM channels").fetchall()
print("\n=== CHANNELS IN DB ===")
for c in channels:
    print(f"  {c[0]} | {c[1]} | {c[2]} videos")

# Check total videos
total = cursor.execute("SELECT COUNT(*) FROM videos").fetchone()[0]
print(f"\n=== TOTAL VIDEOS IN DB: {total} ===")

# Check date range of videos
date_range = cursor.execute("""
    SELECT MIN(published_at), MAX(published_at) FROM videos
""").fetchone()
print(f"\n=== VIDEO DATE RANGE ===")
print(f"  Earliest : {date_range[0]}")
print(f"  Latest   : {date_range[1]}")

# Check videos in 2026
vids_2026 = cursor.execute("""
    SELECT COUNT(*) FROM videos
    WHERE date(published_at) >= '2026-01-01'
""").fetchone()[0]
print(f"\n=== VIDEOS FROM 2026 ONWARDS: {vids_2026} ===")

# Check videos from 2020 onwards
vids_2020 = cursor.execute("""
    SELECT COUNT(*) FROM videos
    WHERE date(published_at) >= '2020-01-01'
""").fetchone()[0]
print(f"=== VIDEOS FROM 2020 ONWARDS: {vids_2020} ===")

conn.close()