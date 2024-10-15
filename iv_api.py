import requests

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
}

def get_stats(invidious_instance: str) -> dict:
    stats = requests.get(f"{invidious_instance}/api/v1/stats")
    return stats.json()

def get_videos(invidious_instance: str, feed: str) -> dict:
    videos = requests.get(f"{invidious_instance}/api/v1/{feed}").json()
    return videos

def get_video(invidious_instance: str, video_id: str) -> dict:
    video = requests.get(f"{invidious_instance}/api/v1/videos/{video_id}", headers=headers).json()
    return video
