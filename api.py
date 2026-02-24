# api.py
# Fetches channel, playlist, and video data from YouTube API

from googleapiclient.discovery import build
import isodate
from config import API_KEY

# Guard: ensure API key exists before making any requests
if not API_KEY:
    raise EnvironmentError(
        "API_KEY is missing or empty in config.py. "
        "Please add your YouTube Data API v3 key."
    )


def safe_get(data, key, default=None):
    value = data.get(key, default)
    return value if value not in [None, ""] else default


def to_int(value, default=0):
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def duration_to_seconds(duration):
    """Converts ISO 8601 duration string to total seconds. Returns 0 on any failure."""
    try:
        return int(isodate.parse_duration(duration).total_seconds())
    except (isodate.isoerror.ISO8601Error, AttributeError, TypeError, ValueError):
        return 0


def build_youtube_client():
    return build("youtube", "v3", developerKey=API_KEY)


def fetch_channel_details(youtube, channel_id):
    """
    Fetches channel snippet, statistics, and contentDetails.
    Raises ValueError if the channel ID is invalid or not found.
    """
    response = youtube.channels().list(
        part="snippet,statistics,contentDetails",
        id=channel_id
    ).execute()

    items = response.get("items", [])
    if not items:
        raise ValueError(
            f"No channel found for ID: '{channel_id}'. "
            "Check the Channel ID and try again."
        )

    channel_data = {}
    for channel in items:
        uploads_playlist_id = channel["contentDetails"]["relatedPlaylists"]["uploads"]
        channel_data[channel_id] = {
            "title":                safe_get(channel["snippet"], "title", "Unknown"),
            "description":          safe_get(channel["snippet"], "description", ""),
            "published_at":         safe_get(channel["snippet"], "publishedAt"),
            "custom_url":           safe_get(channel["snippet"], "customUrl"),
            "country":              safe_get(channel["snippet"], "country"),
            "subscriber_count":     to_int(channel["statistics"].get("subscriberCount")),
            "view_count":           to_int(channel["statistics"].get("viewCount")),
            "video_count":          to_int(channel["statistics"].get("videoCount")),
            "uploads_playlist_id":  uploads_playlist_id,
        }
    return channel_data


def fetch_playlists(youtube, channel_id):
    """Fetches all playlists for the channel, handling pagination."""
    playlists_data = {}
    next_page_token = None

    while True:
        response = youtube.playlists().list(
            part="snippet",
            channelId=channel_id,
            maxResults=50,
            pageToken=next_page_token
        ).execute()

        for playlist in response.get("items", []):
            playlists_data[playlist["id"]] = {
                "title":        safe_get(playlist["snippet"], "title", "Untitled"),
                "description":  safe_get(playlist["snippet"], "description", ""),
                "published_at": safe_get(playlist["snippet"], "publishedAt"),
            }

        next_page_token = response.get("nextPageToken")
        if not next_page_token:
            break

    return playlists_data


def process_video(video, snippet, playlist_id, playlist_info):
    """
    Builds the video dict from the API response.
    JSON keys:
        video_title, video_description, duration, duration_seconds
    These are mapped to DB columns by db_insert.py.
    """
    stats   = video.get("statistics", {})
    content = video.get("contentDetails", {})

    return {
        "video_title":       safe_get(snippet, "title", "No Title"),
        "video_description": safe_get(snippet, "description", ""),
        "published_at":      safe_get(snippet, "publishedAt"),
        "views":             to_int(stats.get("viewCount")),
        "likes":             to_int(stats.get("likeCount")),
        "comments":          to_int(stats.get("commentCount")),
        "duration":          safe_get(content, "duration", "PT0S"),  # → DB 'duration_iso'
        "duration_seconds":  duration_to_seconds(content.get("duration", "PT0S")),
        "playlist_id":       playlist_id,
        "playlist_title":    safe_get(playlist_info, "title", "Unknown Playlist"),
    }


def fetch_videos_from_playlists(youtube, playlists_data):
    """
    Fetches all videos from all playlists, handling pagination.
    Skips deleted/private videos that are missing from the snippet map.
    """
    all_videos = {}

    for playlist_id, playlist_info in playlists_data.items():
        next_page_token = None

        while True:
            response = youtube.playlistItems().list(
                part="snippet,contentDetails",
                playlistId=playlist_id,
                maxResults=50,
                pageToken=next_page_token
            ).execute()

            video_ids   = []
            snippet_map = {}

            for item in response.get("items", []):
                video_id = item["contentDetails"]["videoId"]
                snippet_map[video_id] = item["snippet"]
                video_ids.append(video_id)

            if video_ids:
                videos_response = youtube.videos().list(
                    part="statistics,contentDetails",
                    id=",".join(video_ids)
                ).execute()

                for video in videos_response.get("items", []):
                    vid = video["id"]

                    # Skip deleted or private videos missing from the snippet map
                    if vid not in snippet_map:
                        print(f"⚠️  Skipping video '{vid}' — deleted or private.")
                        continue

                    snippet = snippet_map[vid]
                    all_videos[vid] = process_video(video, snippet, playlist_id, playlist_info)

            next_page_token = response.get("nextPageToken")
            if not next_page_token:
                break

    return all_videos


def build_youtube_channel_data(channel_id):
    """
    Full pipeline: builds YouTube client, fetches channel info,
    playlists, and all videos. Returns a single data dict.
    """
    youtube      = build_youtube_client()
    channel_info = fetch_channel_details(youtube, channel_id)
    playlists    = fetch_playlists(youtube, channel_id)
    videos       = fetch_videos_from_playlists(youtube, playlists)

    return {
        "channel_info": channel_info,
        "playlists":    playlists,
        "videos":       videos,
    }