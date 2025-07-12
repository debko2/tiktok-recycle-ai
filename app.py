from flask import Flask, request, jsonify
import whisper, uuid, os, subprocess

app = Flask(__name__)
model = whisper.load_model("base")

@app.route("/edit", methods=["POST"])
def edit_video():
    video = request.files["video"]
    hook = request.form.get("hook", "WAIT FOR IT")
    file_id = str(uuid.uuid4())
    video_path = f"/tmp/{file_id}.mp4"
    output_path = f"/tmp/{file_id}_final.mp4"
    video.save(video_path)
    ffmpeg_command = [
        "ffmpeg", "-i", video_path,
        "-vf", f"drawtext=text='{hook}':fontcolor=white:fontsize=60:x=50:y=50",
        "-y", output_path
    ]
    subprocess.run(ffmpeg_command)
    return jsonify({"finalVideoUrl": f"https://your-cdn.com/videos/{file_id}_final.mp4"})