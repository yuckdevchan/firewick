from flask import Flask, render_template, request
import iv_api

app = Flask(__name__)
app.config['TESTING'] = True

branding = {
    "name": "firewick"
}

iv_instance = "https://inv.nadeko.net"

@app.route("/")
def index():
    popular_videos = iv_api.get_videos(iv_instance, "popular")
    return render_template("videos.html", branding_name=branding["name"], videos=popular_videos)

@app.route("/popular")
def popular():
    return index()

@app.route("/trending")
def trending():
    trending_videos = iv_api.get_videos(iv_instance, "trending")
    return render_template("videos.html", branding_name=branding["name"], videos=trending_videos)

@app.route("/search")
def search():
    query = request.args.get("q")
    search_results = iv_api.get_videos(iv_instance, f"search?q={query}")
    return render_template("videos.html", branding_name=branding["name"], videos=search_results, query=query)

@app.route("/watch")
def watch():
    video_id = request.args.get("v")
    video = iv_api.get_video(iv_instance, video_id)
    return render_template("watch.html", branding_name=branding["name"], video=video)

@app.route("/stats")
def stats():
    stats = iv_api.get_stats(iv_instance)
    return render_template("stats.html", branding_name=branding["name"], stats=stats)

if __name__ == "__main__":
    app.run(debug=True)
