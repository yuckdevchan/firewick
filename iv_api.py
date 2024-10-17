import requests, humanize

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
}

def get_instances() -> dict:
    instances = requests.get("https://api.invidious.io/instances.json?pretty=1&sort_by=type,users")
    return instances.json()

def get_stats(invidious_instance: str) -> dict:
    stats = requests.get(f"{invidious_instance}/api/v1/stats")
    return stats.json()

def get_videos(invidious_instance: str, feed: str) -> dict:
    videos = requests.get(f"{invidious_instance}/api/v1/{feed}").json()
    for video in videos:
        try:
            video["viewCountCommas"] = humanize.intcomma(video["viewCount"])
            video["viewCountText"] = humanize.intword(video["viewCount"]).replace(" thousand", "K").replace(" million", "M").replace(" billion", "B").replace(" trillion", "T")
        except KeyError:
            pass
    return videos

def get_video(invidious_instance: str, video_id: str) -> dict:
    try:
        video = requests.get(f"{invidious_instance}/api/v1/videos/{video_id}", headers=headers).json()
        video["viewCountCommas"] = humanize.intcomma(video["viewCount"])
        video["likeCountCommas"] = humanize.intcomma(video["likeCount"])
    except:
        return {"error": "Video not found or unsupported type / feature."}
    return video

def get_comments(invidious_instance: str, video_id: str) -> dict:
    try:
        comments = requests.get(f"{invidious_instance}/api/v1/comments/{video_id}", headers=headers).json()
    except:
        return {"error": "Comments not found or unsupported type / feature."}
    return comments
