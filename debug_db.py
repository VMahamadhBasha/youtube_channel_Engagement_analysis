# debug_db.py
# Run this anytime to print data stored in your SQLite database

import sqlite3
from database import DB_PATH

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# ── CHANNELS ──────────────────────────────────────────
print("\n" + "="*50)
print("📺 CHANNELS")
print("="*50)

channels = cursor.execute("SELECT channel_id, title, subscriber_count, view_count, video_count FROM channels").fetchall()

if not channels:
    print("No channel data found.")
else:
    for row in channels:
        print(f"  Channel ID   : {row[0]}")
        print(f"  Title        : {row[1]}")
        print(f"  Subscribers  : {row[2]:,}")
        print(f"  Total Views  : {row[3]:,}")
        print(f"  Total Videos : {row[4]:,}")
        print()

# ── PLAYLISTS ─────────────────────────────────────────
print("="*50)
print("📋 PLAYLISTS (first 5)")
print("="*50)

playlists = cursor.execute("SELECT playlist_id, channel_id, title FROM playlists LIMIT 5").fetchall()

if not playlists:
    print("No playlist data found.")
else:
    for row in playlists:
        print(f"  Playlist ID : {row[0]}")
        print(f"  Channel ID  : {row[1]}")
        print(f"  Title       : {row[2]}")
        print()

# ── VIDEOS ────────────────────────────────────────────
print("="*50)
print("🎬 VIDEOS (first 10)")
print("="*50)

videos = cursor.execute("""
    SELECT video_id, title, views, likes, comments, duration_seconds
    FROM videos
    LIMIT 10
""").fetchall()

if not videos:
    print("No video data found.")
else:
    for row in videos:
        print(f"  Video ID  : {row[0]}")
        print(f"  Title     : {row[1]}")
        print(f"  Views     : {row[2]:,}")
        print(f"  Likes     : {row[3]:,}")
        print(f"  Comments  : {row[4]:,}")
        print(f"  Duration  : {row[5]} seconds")
        print()

# ── COUNTS ────────────────────────────────────────────
print("="*50)
print("📊 SUMMARY COUNTS")
print("="*50)

total_channels  = cursor.execute("SELECT COUNT(*) FROM channels").fetchone()[0]
total_playlists = cursor.execute("SELECT COUNT(*) FROM playlists").fetchone()[0]
total_videos    = cursor.execute("SELECT COUNT(*) FROM videos").fetchone()[0]

print(f"  Total Channels  : {total_channels}")
print(f"  Total Playlists : {total_playlists}")
print(f"  Total Videos    : {total_videos}")
print("="*50)

conn.close()