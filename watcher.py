import os
import time
import json
from dotenv import load_dotenv

load_dotenv()

PHOTO_ROOT = os.getenv("PHOTO_ROOT")
INTERFACE_DIR = os.getenv("INTERFACE_DIR")
GROUPS_JSON = os.path.join(INTERFACE_DIR, "groups.json")
MAX_GROUPS = int(os.getenv("MAX_GROUPS", "5"))
SCAN_INTERVAL_SECONDS = int(os.getenv("SCAN_INTERVAL_SECONDS", "5"))
BASE_ONEDRIVE_URL = os.getenv("BASE_ONEDRIVE_URL")

def get_photos(group_path):
    return [f for f in os.listdir(group_path) if f.lower().endswith(".jpg")]

def update_groups_json(group_name, photos, link):
    if os.path.exists(GROUPS_JSON):
        with open(GROUPS_JSON, "r", encoding="utf-8") as f:
            groups = json.load(f)
    else:
        groups = []

    groups = [g for g in groups if g["name"] != group_name]
    groups.insert(0, {
        "name": group_name,
        "link": link,
        "photos": photos[:3]
    })
    groups = groups[:MAX_GROUPS]

    with open(GROUPS_JSON, "w", encoding="utf-8") as f:
        json.dump(groups, f, indent=2, ensure_ascii=False)

    print(f"[OK] Groupe ajouté : {group_name}")

def main():
    print(f"📡 Surveillance du dossier : {PHOTO_ROOT}")
    seen = set()

    while True:
        for group_name in os.listdir(PHOTO_ROOT):
            group_path = os.path.join(PHOTO_ROOT, group_name)
            if not os.path.isdir(group_path) or group_name in seen:
                continue

            photos = get_photos(group_path)
            if len(photos) < 3:
                continue

            # Génère le lien public basé sur le lien racine
            link = f"{BASE_ONEDRIVE_URL}&group={group_name}"

            update_groups_json(group_name, photos, link)
            seen.add(group_name)

        time.sleep(SCAN_INTERVAL_SECONDS)

if __name__ == "__main__":
    main()
