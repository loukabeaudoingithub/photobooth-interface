from flask import Flask, send_from_directory, send_file, render_template_string, jsonify, abort
import os
import json
import urllib.parse
import random
selected_photos = []

app = Flask(__name__)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PHOTO_ROOT = "C:/Users/beaud/OneDrive/PhotoboothPublic"
GROUPS_JSON = os.path.join(BASE_DIR, "groups.json")

@app.route('/')
def home():
    return send_from_directory('.', 'photobooth.html')

@app.route('/ipad')
def ipad():
    return send_from_directory('.', 'ipad.html')

@app.route('/groups.json')
def serve_groups():
    return send_from_directory('.', 'groups.json')

@app.route('/group/<group_name>')
def group_page(group_name):
    try:
        with open(GROUPS_JSON, "r", encoding="utf-8") as f:
            groups = json.load(f)
    except:
        return "groups.json introuvable", 500

    group = next((g for g in groups if g["name"] == group_name), None)
    if not group:
        return f"Groupe '{group_name}' introuvable", 404

    link = group.get("link", "#")
    qr_url = f"https://api.qrserver.com/v1/create-qr-code/?size=150x150&data={link}"
    safe_link = urllib.parse.quote(link, safe=':/?=&')

    page_html = f"""
<!DOCTYPE html>
<html lang="fr">
<head>
    <script type="text/javascript" src="https://cdn.jsdelivr.net/npm/@emailjs/browser@4/dist/email.min.js"></script>
    <script type="text/javascript">
      (function() {{
        emailjs.init({{ publicKey: "_esvw5Sq81yyz3Tkl" }});
      }})();
    </script>
    <meta charset="UTF-8">
    <title>{group_name}</title>

    <style>
        body {{
            font-family: 'Segoe UI', sans-serif;
            text-align: center;
            padding: 40px;
            background: url('https://images.unsplash.com/photo-1529333166437-7750a6dd5a70?auto=format&fit=crop&w=1600&q=80') no-repeat center center fixed;
            background-size: cover;
            color: #fff;
        }}
        h1 {{
            font-size: 3em;
            margin-bottom: 30px;
            text-shadow: 2px 2px 5px rgba(0,0,0,0.5);
        }}
        .photo-container {{
            display: flex;
            flex-wrap: wrap;
            justify-content: center;
            gap: 20px;
        }}
        .photo-container img {{
            width: 300px;
            border: 5px solid white;
            border-radius: 15px;
            box-shadow: 0 0 15px rgba(0,0,0,0.6);
        }}
        .qr {{
            margin-top: 30px;
        }}
        .qr img {{
            width: 150px;
        }}
        .back-button {{
            margin-top: 40px;
            font-size: 2em;
            padding: 12px 24px;
            background-color: #ffffff;
            color: #333;
            border: none;
            border-radius: 8px;
            box-shadow: 0 0 10px rgba(0,0,0,0.3);
        }}
        .back-button:hover {{
            background-color: #f0f0f0;
        }}
        .share-buttons {{
            margin-top: 30px;
        }}
        .share-buttons button {{
            font-size: 1.2em;
            padding: 12px 24px;
            margin: 10px;
            border: none;
            border-radius: 8px;
            background-color: #ffd700;
            color: #333;
            box-shadow: 0 0 10px rgba(0,0,0,0.3);
            cursor: pointer;
        }}
        .share-buttons button:hover {{
            background-color: #ffcc00;
        }}
        .modal {{
            position: fixed;
            top: 0; left: 0;
            width: 100%; height: 100%;
            background: rgba(0,0,0,0.6);
            display: none;
            justify-content: center;
            align-items: center;
            z-index: 999;
        }}
        .modal.active {{
            display: flex;
        }}
        .modal-content {{
            background: white;
            padding: 30px;
            border-radius: 10px;
            width: 90%;
            max-width: 500px;
            color: #333;
        }}
        .close {{
            float: right;
            cursor: pointer;
            font-size: 1.5em;
        }}
        a {{
            color: #ffd700;
            font-weight: bold;
        }}
    </style>
</head>
<body>
    <h1>{group_name}</h1>

    <div class="photo-container">
        {"".join([f'<img src="/photo/{group_name}/{p}" alt="Photo {i}">' for i, p in enumerate(group["photos"], 1)])}
    </div>

    <div class="qr">
        <p><strong>Lien OneDrive :</strong> <a href="{link}" target="_blank">{link}</a></p>
        <img src="{qr_url}" alt="QR Code">
    </div>

    <div class="share-buttons">
        <button onclick="shareNative()">📤 Partager</button>
        <button onclick="openModal('email')">✉️ Par courriel</button>
        <button onclick="openModal('whatsapp')">📱 WhatsApp</button>
        <button onclick="openModal('messenger')">💬 Messenger</button>
    </div>

    <button class="back-button" onclick="window.location.href='/ipad'">⬅️ Retour à la recherche</button>

    <div id="modal" class="modal">
      <div class="modal-content">
        <span class="close" onclick="closeModal()">❌</span>
        <div id="modal-body"></div>
      </div>
    </div>

    <script>
    const link = decodeURIComponent("{safe_link}");

    function shareNative() {{
        if (navigator.share) {{
            navigator.share({{
                title: "Vos photos du Photobooth",
                text: "Voici le lien vers vos photos :",
                url: link
            }}).catch(function(err) {{
                alert("Le partage a échoué : " + err);
            }});
        }} else {{
            document.querySelector("button[onclick='shareNative()']").style.display = "none";
        }}
    }}

    function openModal(type) {{
        const modal = document.getElementById('modal');
        const body = document.getElementById('modal-body');
        modal.classList.add('active');

        if (type === 'email') {{
            body.innerHTML = `
                <h2>Envoyer par courriel</h2>
                <form id="emailForm">
                    <input type="email" name="to_email" placeholder="Adresse courriel" required style="width: 100%; padding: 10px; margin-bottom: 10px;">
                    <button type="submit">📤 Envoyer</button>
                </form>
            `;
        }} else if (type === 'whatsapp') {{
            body.innerHTML = `
                <h2>Partager via WhatsApp</h2>
                <button onclick="window.open('https://api.whatsapp.com/send?text=${{encodeURIComponent(link)}}', '_blank')">Ouvrir WhatsApp</button>
            `;
        }} else if (type === 'messenger') {{
            body.innerHTML = `
                <h2>Partager via Messenger</h2>
                <button onclick="window.open('https://www.facebook.com/dialog/send?link=${{encodeURIComponent(link)}}&app_id=123456789&redirect_uri=${{encodeURIComponent(link)}}', '_blank')">Ouvrir Messenger</button>
            `;
        }}
    }}

    function closeModal() {{
        document.getElementById('modal').classList.remove('active');
    }}

    document.addEventListener("submit", function(e) {{
        if (e.target && e.target.id === "emailForm") {{
            e.preventDefault();
            const formData = new FormData(e.target);
            const toEmail = formData.get("to_email");

            if (!toEmail) {{
                alert("Veuillez entrer une adresse courriel.");
                return;
            }}

            emailjs.send("service_15qdwy9", "template_6rwue2o", {{
                to_email: toEmail,
                message: link
            }}).then(() => {{
                alert("Courriel envoyé !");
                closeModal();
            }}, (err) => {{
                alert("Erreur : " + err.text);
            }});
        }}
    }});
    </script>
</body>
</html>
"""
    return render_template_string(page_html)

@app.route('/photo/<group>/<filename>')
def photo(group, filename):
    path = os.path.join(PHOTO_ROOT, group)
    if not os.path.exists(os.path.join(path, filename)):
        abort(404)
    return send_from_directory(path, filename)

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

    print("Photos trouvées :", all_photos)  # ← ajoute cette ligne

    selected_photos = random.sample(all_photos, min(3, len(all_photos)))
    return jsonify([f'/random-photo/{i}' for i in range(len(selected_photos))])

@app.route('/random-photo/<int:index>')
def serve_random_photo(index):
    if 0 <= index < len(selected_photos):
        return send_file(selected_photos[index], mimetype='image/jpeg')
    return "Image not found", 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)