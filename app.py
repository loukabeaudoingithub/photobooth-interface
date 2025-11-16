from flask import Flask, render_template, send_file, jsonify
import os
import random

app = Flask(__name__)

PHOTO_ROOT = r"C:\Users\beaud\OneDrive\PhotoboothPublic"
selected_photos = []

@app.route('/')
def home():
    return render_template('photobooth.html')

@app.route('/random-group-photos')
def random_group_photos():
    global selected_photos
    all_photos = []

    for group_folder in os.listdir(PHOTO_ROOT):
        group_path = os.path.join(PHOTO_ROOT, group_folder)
        if os.path.isdir(group_path):
            for file in os.listdir(group_path):
                if file.lower().endswith(('.jpg', '.jpeg', '.png')):
                    full_path = os.path.join(group_path, file)
                    all_photos.append(full_path)

    selected_photos = random.sample(all_photos, min(3, len(all_photos)))
    return jsonify([f'/photo/{i}' for i in range(len(selected_photos))])

@app.route('/photo/<int:index>')
def serve_photo(index):
    if 0 <= index < len(selected_photos):
        return send_file(selected_photos[index], mimetype='image/jpeg')
    return "Image not found", 404

if __name__ == '__main__':
    app.run(debug=True)