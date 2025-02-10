from flask import Flask, render_template_string, request, send_file
import yt_dlp

app = Flask(__name__)

# HTML কন্টেন্ট
index_html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>YouTube Video Downloader</title>
</head>
<body>
    <h1>YouTube Video Downloader</h1>
    <form method="POST" action="/download">
        <label for="url">Enter YouTube URL:</label>
        <input type="text" name="url" id="url" required>
        <button type="submit">Download</button>
    </form>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(index_html)

@app.route('/download', methods=['POST'])
def download():
    video_url = request.form['url']
    
    ydl_opts = {
        'format': 'best',
        'outtmpl': 'downloads/%(title)s.%(ext)s',  # ভিডিও যেখানে সেভ হবে
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(video_url, download=True)
        filename = ydl.prepare_filename(info_dict)

    # ভিডিও ফাইল পাঠানো হচ্ছে
    return send_file(filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)