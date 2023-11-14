import os
import shutil
import time
import urllib.request

# Installer les modules nécessaires
os.system("pip install pytube tqdm ")

# Créer le dossier de téléchargement et le fichier url.txt
download_dir = os.path.join(os.path.expanduser("~"), "Downloads", "Youtube download")
if not os.path.exists(download_dir):
    os.mkdir(download_dir)
    os.mkdir(os.path.join(download_dir, "data"))
    with open(os.path.join(download_dir, "url.txt"), "w") as f:
        f.write("https://www.youtube.com/watch?v=dQw4w9WgXcQ\n")
else:
    if not os.path.exists(os.path.join(download_dir, "data")):
        os.mkdir(os.path.join(download_dir, "data"))

# Télécharger le fichier Python à partir de GitHub
url = "https://raw.githubusercontent.com/MrFlappy0/Youtube-downloader/main/download.py"
filename = os.path.join(download_dir, "download.py")
urllib.request.urlretrieve(url, filename)

# Vérifier que tous les fichiers sont bien présents
if os.path.exists(os.path.join(download_dir, "download.py")) and os.path.exists(os.path.join(download_dir, "url.txt")):
    print("Tous les fichiers ont été installés dans la rubrique téléchargement de l'explorateur.")
    time.sleep(5)
    # Demander à l'utilisateur s'il souhaite désinstaller le fichier setup.py
    response = input("Souhaitez-vous désinstaller le fichier setup.py ? (y/n) ")
    if response.lower() == "y":
        os.remove(os.path.join(os.path.dirname(os.path.abspath(__file__)), "setup.py"))
    else:
        exit()
else:
    print("Erreur : tous les fichiers n'ont pas été installés correctement.")
