from flask import Flask, send_from_directory
import os

app = Flask(__name__, static_folder='frontend', static_url_path='')

@app.route('/')
def index():
    return send_from_directory('frontend', 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    if os.path.exists(os.path.join('frontend', path)):
        return send_from_directory('frontend', path)
    return send_from_directory('frontend', 'index.html')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=False)
