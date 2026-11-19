from flask import Flask, send_from_directory
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
app = Flask(__name__)

@app.route('/')
def home():
    return send_from_directory(BASE_DIR, 'index.html')

@app.route('/<path:path>')
def static_files(path):
    return send_from_directory(BASE_DIR, path)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
