import subprocess

modules_to_install = ['praw', 'requests', 'colorama', 'rich', 'inquirer', 'Pillow', 'tqdm']

def check_and_install_modules():
    for module in modules_to_install:
        try:
            __import__(module)
        except ImportError:
            subprocess.call(['pip', 'install', module])

check_and_install_modules()


import os
import praw
import time
import requests
import json
from colorama import Fore, Style
from rich.console import Console
import inquirer


console = Console()

def get_credentials():

    config_file = os.path.join(os.path.expanduser("~"), "Documents", "Reddit Crawler", "config.json")
    if not os.path.exists(os.path.dirname(config_file)):
        os.makedirs(os.path.dirname(config_file))
    if os.path.exists(config_file):
        with open(config_file, "r") as f:
            config = json.load(f)
    else:
        config = {}
        with open(config_file, "w") as f:
            json.dump(config, f)
    if "client_id" not in config:
        config["client_id"] = input("Entrez votre identifiant client Reddit: ")
    if "client_secret" not in config:
        config["client_secret"] = input("Entrez votre secret client Reddit: ")
    if "user_agent" not in config:
        config["user_agent"] = input("Entrez votre agent utilisateur Reddit: ")
    with open(config_file, "w") as f:
        json.dump(config, f)
    return config["client_id"], config["client_secret"], config["user_agent"]

client_id, client_secret, user_agent = get_credentials()

from rich.console import Console

# Créer une instance de la classe Console pour afficher des messages à l'utilisateur
console = Console()

# Afficher un message de bienvenue et des instructions pour l'utilisateur
console.print("[bold][purple]Bienvenue dans le programme de téléchargement de Reddit ![/purple][/bold]")
console.print("Ce programme vous permet de télécharger des images à partir de subreddits spécifiques.")
console.print("Assurez-vous que le subreddit que vous souhaitez télécharger est public et autorise le téléchargement de ses images.\n")

while True:
    questions = [
        inquirer.List('choice',
                      message="Que voulez-vous faire ?",
                      choices=['Télécharger un subreddit', 'Obtenir toutes les informations d\'un subreddit', 'Télécharger des posts à partir d\'un utilisateur', 'Télécharger des posts à partir d\'un mot-clé'],
                      ),
    ]
    answers = inquirer.prompt(questions)

    if answers['choice'] == "Télécharger un subreddit":
    
        subreddit_name = input("\n" + Fore.BLUE + "Entrez le nom du subreddit que vous souhaitez télécharger: " + Style.RESET_ALL)
        time_filter = "all"
        max_posts = int(input("\n" + Fore.BLUE + "Entrez le nombre de posts à télécharger: " + Style.RESET_ALL))

        from tqdm.autonotebook import tqdm

        def download_subreddit_posts(subreddit_name, max_posts):
            reddit = praw.Reddit(client_id=client_id,
                                 client_secret=client_secret,
                                 user_agent=user_agent)

            subreddit = reddit.subreddit(subreddit_name)
            subreddit_posts = subreddit.new(limit=max_posts)

            pbar = tqdm(total=max_posts, desc="Downloading", dynamic_ncols=True)

            from PIL import Image
            from io import BytesIO

            def is_valid_image(image_bytes):
                try:
                    img = Image.open(BytesIO(image_bytes))
                    img.verify()
                    return True
                except:
                    return False

            for post in subreddit_posts:
                if post.is_self:
                    continue
                if post.url.endswith(('.m1v', '.mpeg', ".webm", '.mov', '.qt', '.mpa', '.mpg', '.mpe', '.avi', '.movie', '.mp4', '.ra', '.aif', '.aiff', '.aifc', '.wav', '.au', '.snd', '.mp3', '.mp2', '.ras', '.xwd', '.bmp', '.jpe', '.jpg', '.jpeg', '.xpm', '.ief', '.pbm', '.tif', '.gif', '.ppm', '.xbm', '.tiff', '.rgb', '.pgm', '.png', '.pnm')):
                    response = requests.get(post.url)
                    if is_valid_image(response.content):
                        filename = clean_filename(post.title) + post.url[-4:]
                        if download_media(post.url, filename, pbar):
                            print(f"\nTéléchargement réussi: {filename}\n")
                        time.sleep(1)
                    else:
                        print(f"\nImage invalide: {post.url}\n")
                elif post.url.endswith(('.mp4', '.mov', '.avi', '.webm')):
                    filename = clean_filename(post.title) + post.url[-4:]
                    if download_media(post.url, filename, pbar):
                        print(f"\nTéléchargement réussi: {filename}\n")
                    time.sleep(1)
                else:
                    continue
                pbar.update()

        def download_media(media_url, filename, pbar):
            directory = os.path.join(os.path.expanduser("~"), "Downloads", "Reddit Crawler", "downloads", subreddit_name)
            if not os.path.exists(directory):
                os.makedirs(directory)
            file_path = os.path.join(directory, filename)
            if os.path.exists(file_path):
                print(f"  Le fichier {filename} existe déjà, il ne sera pas re-téléchargé.")
                return False
            try:
                response = requests.get(media_url, stream=True)
                response.raise_for_status()
                total_length = int(response.headers.get('content-length'))
                pbar.set_postfix(file=filename[-10:], refresh=True)
                with open(file_path, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)
                return True
            except Exception as e:
                print(f"\nErreur lors du téléchargement de {filename}: {e}\n")
                return False

        def clean_filename(filename):
            keepcharacters = (' ','.','_')
            return "".join(c for c in filename if c.isalnum() or c in keepcharacters).rstrip()

        download_subreddit_posts(subreddit_name, max_posts)

        # Add the following line to disable the live display
        os.environ["WDM_LOG_LEVEL"] = "0"

    elif answers['choice'] == "Obtenir toutes les informations d'un subreddit":
        subreddit_name = input("Entrez le nom du subreddit dont vous souhaitez obtenir les informations: ")
        import praw
        import urllib

        reddit = praw.Reddit(client_id=client_id, client_secret=client_secret, user_agent=user_agent)

        subreddit = reddit.subreddit(subreddit_name)

        image_count = 0
        gif_count = 0

        for submission in subreddit.top(limit=1000):  # change to the desired number of posts
            url = submission.url
            if url.endswith(('.jpg', '.png', '.jpeg')):
                image_count += 1
            elif url.endswith(('.gif', '.gifv')):
                gif_count += 1

        subreddit_info = {
            "name": subreddit.display_name,
            "title": subreddit.title,
            "description": subreddit.description,
            "subscribers": subreddit.subscribers,
            "created_utc": subreddit.created_utc,
            "over18": subreddit.over18,
            "public_description": subreddit.public_description,
            "submission_type": subreddit.submission_type,
            "url": subreddit.url,
            "icon_img": subreddit.icon_img,
            "header_img": subreddit.header_img,
            "created": subreddit.created,
            "subreddit_type": subreddit.subreddit_type,
            "lang": subreddit.lang,
            "whitelist_status": subreddit.whitelist_status,
            "quarantine": subreddit.quarantine,
            "name": subreddit.name,
            "public_traffic": subreddit.public_traffic,
            "title": subreddit.title,
            "url": subreddit.url,
            "user_is_banned": subreddit.user_is_banned,
            "user_is_contributor": subreddit.user_is_contributor,
            "user_is_moderator": subreddit.user_is_moderator,
            "user_is_subscriber": subreddit.user_is_subscriber,
            "image_count": image_count,
            "gif_count": gif_count
        }

        directory = os.path.join(os.path.expanduser("~"), "Downloads", "Reddit Crawler", "info subreddit", subreddit_name)
        if not os.path.exists(directory):
            os.makedirs(directory)
        with open(os.path.join(directory, f"{subreddit_name}.json"), "w") as f:
            json.dump(subreddit_info, f, indent=4)

    elif answers['choice'] == "Télécharger des posts à partir d'un utilisateur":
        username = input("Entrez le nom d'utilisateur dont vous souhaitez télécharger les posts: ")
        max_posts = int(input("\n" + Fore.BLUE + "Entrez le nombre de posts à télécharger: " + Style.RESET_ALL))

        from tqdm.autonotebook import tqdm

        def download_user_posts(username, max_posts):
            reddit = praw.Reddit(client_id=client_id,
                                 client_secret=client_secret,
                                 user_agent=user_agent)

            user = reddit.redditor(username)
            user_posts = user.submissions.new(limit=max_posts)

            pbar = tqdm(total=max_posts, desc="Downloading", dynamic_ncols=True)

            from PIL import Image
            from io import BytesIO

            def is_valid_image(image_bytes):
                try:
                    img = Image.open(BytesIO(image_bytes))
                    img.verify()
                    return True
                except:
                    return False

            for post in user_posts:
                if post.is_self:
                    continue
                if post.url.endswith(('.m1v', '.mpeg', ".webm", '.mov', '.qt', '.mpa', '.mpg', '.mpe', '.avi', '.movie', '.mp4', '.ra', '.aif', '.aiff', '.aifc', '.wav', '.au', '.snd', '.mp3', '.mp2', '.ras', '.xwd', '.bmp', '.jpe', '.jpg', '.jpeg', '.xpm', '.ief', '.pbm', '.tif', '.gif', '.ppm', '.xbm', '.tiff', '.rgb', '.pgm', '.png', '.pnm')):
                    response = requests.get(post.url)
                    if is_valid_image(response.content):
                        filename = clean_filename(post.title) + post.url[-4:]
                        if download_media(post.url, filename, pbar):
                            print(f"\nTéléchargement réussi: {filename}\n")
                        time.sleep(1)
                    else:
                        print(f"\nImage invalide: {post.url}\n")
                elif post.url.endswith(('.mp4', '.mov', '.avi', '.webm')):
                    filename = clean_filename(post.title) + post.url[-4:]
                    if download_media(post.url, filename, pbar):
                        print(f"\nTéléchargement réussi: {filename}\n")
                    time.sleep(1)
                else:
                    continue
                pbar.update()

        def download_media(media_url, filename, pbar):
            directory = os.path.join(os.path.expanduser("~"), "Downloads", "Reddit Crawler", "downloads", "user", username)
            if not os.path.exists(directory):
                os.makedirs(directory)
            file_path = os.path.join(directory, filename)
            if os.path.exists(file_path):
                print(f"  Le fichier {filename} existe déjà, il ne sera pas re-téléchargé.")
                return False
            try:
                response = requests.get(media_url, stream=True)
                response.raise_for_status()
                total_length = int(response.headers.get('content-length'))
                pbar.set_postfix(file=filename[-10:], refresh=True)
                with open(file_path, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)
                return True
            except Exception as e:
                print(f"\nErreur lors du téléchargement de {filename}: {e}\n")
                return False

        def clean_filename(filename):
            keepcharacters = (' ','.','_')
            return "".join(c for c in filename if c.isalnum() or c in keepcharacters).rstrip()

        download_user_posts(username, max_posts)

        # Add the following line to disable the live display
        os.environ["WDM_LOG_LEVEL"] = "0"

    elif answers['choice'] == "Télécharger des posts à partir d'un mot-clé":
        keyword = input("Entrez le mot-clé dont vous souhaitez télécharger les posts: ")
        max_posts = int(input("\n" + Fore.BLUE + "Entrez le nombre de posts à télécharger: " + Style.RESET_ALL))

        from tqdm.autonotebook import tqdm

        def download_keyword_posts(keyword, max_posts):
            reddit = praw.Reddit(client_id=client_id,
                                 client_secret=client_secret,
                                 user_agent=user_agent)

            keyword_posts = reddit.subreddit("all").search(keyword, limit=max_posts)

            pbar = tqdm(total=max_posts, desc="Downloading", dynamic_ncols=True)

            from PIL import Image
            from io import BytesIO

            def is_valid_image(image_bytes):
                try:
                    img = Image.open(BytesIO(image_bytes))
                    img.verify()
                    return True
                except:
                    return False

            for post in keyword_posts:
                if post.is_self:
                    continue
                if post.url.endswith(('.m1v', '.mpeg', ".webm", '.mov', '.qt', '.mpa', '.mpg', '.mpe', '.avi', '.movie', '.mp4', '.ra', '.aif', '.aiff', '.aifc', '.wav', '.au', '.snd', '.mp3', '.mp2', '.ras', '.xwd', '.bmp', '.jpe', '.jpg', '.jpeg', '.xpm', '.ief', '.pbm', '.tif', '.gif', '.ppm', '.xbm', '.tiff', '.rgb', '.pgm', '.png', '.pnm')):
                    response = requests.get(post.url)
                    if is_valid_image(response.content):
                        filename = clean_filename(post.title) + post.url[-4:]
                        if download_media(post.url, filename, pbar):
                            print(f"\nTéléchargement réussi: {filename}\n")
                        time.sleep(1)
                    else:
                        print(f"\nImage invalide: {post.url}\n")
                elif post.url.endswith(('.mp4', '.mov', '.avi', '.webm')):
                    filename = clean_filename(post.title) + post.url[-4:]
                    if download_media(post.url, filename, pbar):
                        print(f"\nTéléchargement réussi: {filename}\n")
                    time.sleep(1)
                else:
                    continue
                pbar.update()

        def download_media(media_url, filename, pbar):
            directory = os.path.join(os.path.expanduser("~"), "Downloads", "Reddit Crawler", "downloads", "keyword", keyword)
            if not os.path.exists(directory):
                os.makedirs(directory)
            file_path = os.path.join(directory, filename)
            if os.path.exists(file_path):
                print(f"  Le fichier {filename} existe déjà, il ne sera pas re-téléchargé.")
                return False
            try:
                response = requests.get(media_url, stream=True)
                response.raise_for_status()
                total_length = int(response.headers.get('content-length'))
                pbar.set_postfix(file=filename[-10:], refresh=True)
                with open(file_path, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)
                return True
            except Exception as e:
                print(f"\nErreur lors du téléchargement de {filename}: {e}\n")
                return False

        def clean_filename(filename):
            keepcharacters = (' ','.','_')
            return "".join(c for c in filename if c.isalnum() or c in keepcharacters).rstrip()

        download_keyword_posts(keyword, max_posts)

        # Add the following line to disable the live display
        os.environ["WDM_LOG_LEVEL"] = "0"

    else:
        console.print("Choix invalide.", style="red")

    print("\n")
    questions = [
        inquirer.List('answer',
                      message="Voulez-vous effectuer une autre action ?",
                      choices=['o', 'n'],
                      ),
    ]
    answer = inquirer.prompt(questions)

    if answer['answer'] != "o":
        break

console.print("Merci d'avoir utilisé le programme de téléchargement de Reddit !", style="bold blue")

