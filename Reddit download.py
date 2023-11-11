import os
import praw
import wget
import time
from PIL import Image
from io import BytesIO
import requests
import json

def get_credentials():

    config_file = os.path.join(os.path.expanduser("~"), "Downloads", "Reddit Crawler", "config.json")
    if os.path.exists(config_file):
        with open(config_file, "r") as f:
            config = json.load(f)
    else:
        config = {}
    if "client_id" not in config:
        config["client_id"] = input("Enter your Reddit client ID: ")
    if "client_secret" not in config:
        config["client_secret"] = input("Enter your Reddit client secret: ")
    if "user_agent" not in config:
        config["user_agent"] = input("Enter your Reddit user agent: ")
    with open(config_file, "w") as f:
        json.dump(config, f)
    return config["client_id"], config["client_secret"], config["user_agent"]

client_id, client_secret, user_agent = get_credentials()

subreddit_name = input("Enter the subreddit name: ")
time_filter = "all"
max_posts = int(input("Enter the number of posts to download: "))

def download_media(media_url, filename):
    directory = os.path.join(os.path.expanduser("~"), "Downloads", "Reddit Crawler", "downloads", subreddit_name)
    if not os.path.exists(directory):
        os.makedirs(directory)

    filename = clean_filename(filename)
    try:
        wget.download(media_url, os.path.join(directory, filename), bar=wget.bar_adaptive)
    except Exception as e:
        print(f"Error downloading {filename}: {e}")

def clean_filename(filename):
    keepcharacters = (' ','.','_')
    return "".join(c for c in filename if c.isalnum() or c in keepcharacters).rstrip()

def is_valid_image(image_bytes):
    try:
        img = Image.open(BytesIO(image_bytes))
        img.verify()
        return True
    except:
        return False


def download_subreddit_posts(subreddit_name, max_posts):
    reddit = praw.Reddit(client_id=client_id,
                     client_secret=client_secret,
                     user_agent=user_agent)

    subreddit = reddit.subreddit(subreddit_name)
    subreddit_posts = subreddit.new(limit=max_posts)

    for post in subreddit_posts:
        if post.is_self:
            continue
        if post.url.endswith(('.m1v', '.mpeg', ".webm", '.mov', '.qt', '.mpa', '.mpg', '.mpe', '.avi', '.movie', '.mp4', '.ra', '.aif', '.aiff', '.aifc', '.wav', '.au', '.snd', '.mp3', '.mp2', '.ras', '.xwd', '.bmp', '.jpe', '.jpg', '.jpeg', '.xpm', '.ief', '.pbm', '.tif', '.gif', '.ppm', '.xbm', '.tiff', '.rgb', '.pgm', '.png', '.pnm')):
            response = requests.get(post.url)
            if is_valid_image(response.content):
                filename = post.title + post.url[-4:]
                download_media(post.url, filename)
                time.sleep(1)
            else:
                print(f"Invalid image: {post.url}")
        else:
            continue


download_subreddit_posts(subreddit_name, max_posts)

