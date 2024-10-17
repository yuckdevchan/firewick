from flask import Flask, render_template, request, session, send_from_directory
import iv_api

app = Flask(__name__)
app.config['TESTING'] = True
app.secret_key = b'\x83\xc7\x91\xb7\xfc\x16\t\xc1\xc2\xad\xc6\xf1'

branding = {
    "name": "firewick"
}

iv_instance = "https://inv.nadeko.net"

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html", branding_name=branding["name"]), 404

@app.route("/favicon.ico")
def favicon():
    return send_from_directory("static", "favicon.ico", mimetype="image/vnd.microsoft.icon")

@app.route("/")
def index():
    popular_videos = iv_api.get_videos(iv_instance, "popular")
    return render_template("videos.html", branding_name=branding["name"], videos=popular_videos, accurate_view_counts=session.get("accurate_view_counts"))

@app.route("/popular")
def popular():
    return index()

@app.route("/trending")
def trending():
    trending_videos = iv_api.get_videos(iv_instance, "trending")
    return render_template("videos.html", branding_name=branding["name"], videos=trending_videos, accurate_view_counts=session.get("accurate_view_counts"))

@app.route("/search")
def search():
    query = request.args.get("q")
    if query in (None, ""):
        return index()
    search_results = iv_api.get_videos(iv_instance, f"search?q={query}")
    return render_template("videos.html", branding_name=branding["name"], videos=search_results, query=query, accurate_view_counts=session.get("accurate_view_counts"))

@app.route("/watch")
def watch():
    video_id = request.args.get("v")
    video = iv_api.get_video(iv_instance, video_id)
    return render_template("watch.html", branding_name=branding["name"], video=video, accurate_view_counts=session.get("accurate_view_counts"))

@app.route("/settings")
def settings():
    return render_template("settings.html", branding_name=branding["name"], settings=settings, instances=iv_api.get_instances(), accurate_view_counts=session.get("accurate_view_counts"), instance=session.get("instance"))

@app.route("/stats")
def stats():
    stats = iv_api.get_stats(iv_instance)
    return render_template("stats.html", branding_name=branding["name"], stats=stats)

@app.route("/api/settings/accurateViewCounts", methods=["POST"])
def api_settings_accurate_view_counts():
    value = True if request.form.get("Accurate View Counts") == "on" else False
    print(value)
    session["accurate_view_counts"] = value
    return "true"

@app.route("/api/settings/instance", methods=["POST"])
def api_settings_instance():
    instance = request.form.get("Invidious Instance")
    session["instance"] = instance
    return "true"

@app.route("/api/settings/showDislikes", methods=["POST"])
def api_settings_show_dislikes():
    value = True if request.form.get("Show Dislikes") == "on" else False
    session["show_dislikes"] = value
    return "true"

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
