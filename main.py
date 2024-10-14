from flask import Flask, render_template, request
import iv_api

app = Flask(__name__)
app.config['TESTING'] = True

branding = {
    "name": "firewick"
}

@app.route("/")
def index():
    popular_videos = iv_api.get_videos("https://inv.nadeko.net", "trending")
    return render_template("videos.html", branding_name=branding["name"], videos=popular_videos)

@app.route("/search")
def search():
    query = request.args.get("q")
    search_results = iv_api.get_videos("https://inv.nadeko.net", f"search?q={query}")
    return render_template("videos.html", branding_name=branding["name"], videos=search_results, query=query)

@app.route("/watch")
def watch():
    video_id = request.args.get("v")
    video = iv_api.get_video("https://inv.nadeko.net", video_id)
    return render_template("watch.html", branding_name=branding["name"], video=video)

if __name__ == "__main__":
    app.run(debug=True)
