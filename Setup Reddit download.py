import requests
import os
import subprocess
import os

modules_to_install = ['praw', 'requests', 'wget', 'Pillow', 'io', 'json', 'os', 'time', 'datetime', 'subprocess']

def check_and_install_modules():
    """
    Cette fonction vérifie si les modules requis sont installés. Si ce n'est pas le cas, il les installe automatiquement.
    """
    for module in modules_to_install:
        try:
            __import__(module)
        except ImportError:
            subprocess.call(['pip', 'install', module])

check_and_install_modules()

downloads_path = os.path.join(os.path.expanduser("~"), "Downloads")
reddit_crawler_path = os.path.join(downloads_path, "Reddit Crawler")
if not os.path.exists(reddit_crawler_path):
    os.mkdir(reddit_crawler_path)

downloads_folder_path = os.path.join(reddit_crawler_path, "downloads")
if not os.path.exists(downloads_folder_path):
    os.mkdir(downloads_folder_path)

url = "https://raw.githubusercontent.com/MrFlappy0/Reddit-Crawler/main/Reddit%20download.py"
response = requests.get(url)

with open(os.path.join(reddit_crawler_path, "Reddit download.py"), "wb") as f:
    f.write(response.content)

    os.remove("C:/Users/theov/Downloads/Setup Reddit Crawler.py")
