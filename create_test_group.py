import os
import shutil

PHOTO_ROOT = "PhotoboothPublic"
GROUP_NAME = "TestGroupe"
PHOTOS = ["photo1.jpg", "photo2.jpg", "photo3.jpg"]

# Créer le dossier du groupe
group_path = os.path.join(PHOTO_ROOT, GROUP_NAME)
os.makedirs(group_path, exist_ok=True)

# Copier des photos de test (tu peux remplacer par des vraies photos)
for photo in PHOTOS:
    # Ici on copie un fichier existant, sinon tu peux juste créer un fichier vide
    with open(os.path.join(group_path, photo), "wb") as f:
        f.write(b"FAKE PHOTO DATA")

print(f"Groupe '{GROUP_NAME}' créé avec 3 photos dans {group_path}")