import sys
sys.path.append(r'e:\infosys springboard 6.0\Youtube _analytics')
from db_queries import get_channel_summary, get_filtered_videos, get_videos_by_month, get_top_videos
print(get_channel_summary('UC4a-Gbdw7vOaccHmFo40b9g'))
print('filtered count', len(get_filtered_videos('UC4a-Gbdw7vOaccHmFo40b9g','2020-01-01','2026-12-31')))
print('months sample', get_videos_by_month('UC4a-Gbdw7vOaccHmFo40b9g','2020-01-01','2020-12-31')[:2])
print('top3', get_top_videos('UC4a-Gbdw7vOaccHmFo40b9g','2020-01-01','2026-12-31', limit=3))
