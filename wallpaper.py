import praw
import re
import urllib.request
import os
import time
from PIL import Image


#Enter your own Reddit OAuth credentials
#Instructions on how-to here:
#https://praw.readthedocs.io/en/latest/getting_started/authentication.html

reddit = praw.Reddit(client_id="",
                     client_secret="",
                     user_agent="")


#Gets the top pictures of the week from a subreddit your choice.
#A few other conditions are added to ensure that the image is a good resolution.

def getPicsFrom(subreddit, amount):
    count = 1
    subreddit = reddit.subreddit(subreddit)
    hot_wallpaper = subreddit.top('week', limit=None)
    print(f"Getting pictures from {subreddit}...")
    for submission in hot_wallpaper:
        try:
            url = str(submission.url)
            resolution = re.findall(r"[\[\(]\d+\s*[x×]\s*\d+[\]\)]", submission.title)
            if not resolution:
                continue
            resolution = re.findall(r"\d+", resolution[0])
            if float(resolution[0]) > 1.7 * float(resolution[1]) and float(resolution[0]) < 7000:
                image = Image.open(urllib.request.urlopen(url))
                width, height = image.size
                if((width > 1.7*height) and (width < 7000) and (height > 800) and (width > 1000)):
                    print(f"Downloading ({count}/{amount}): {url}")
                    urllib.request.urlretrieve(url, f"RedditWallpaperApp {submission.title}.{url[-3:]}")
                    count += 1
            if count == amount+1:
                break
        except:
            count -= 1
            continue


#Deletes old Pictures after a given number of days
#Only deletes pictures that have names that start with "RedditWallpaperApp"
#If you don't want an image to be deleted change the title so that it doesn't start with "RedditWallpaperApp"

def deletePicsAfter(days):
    current_time = time.time()
    for f in os.listdir():
        creation_time = os.path.getctime(f)
        if (current_time - creation_time) // (24 * 3600) >= days and (str(f).split()[0] == "RedditWallpaperApp"):
            os.unlink(f)
            print('{} removed'.format(f))


deletePicsAfter(2)
print()
getPicsFrom('EarthPorn', 10)
print()
getPicsFrom('wallpaper', 4)
print()
getPicsFrom('wallpapers', 4)
print("\nDone!")
