# This script prints top 20 most watched creators from your youtube history

import re
import requests
import random
from concurrent.futures import ThreadPoolExecutor

PATTERN = r'https://www\.youtube\.com/watch\?v=([a-zA-Z0-9._]{11})'

API = ["https://invidious.projectsegfau.lt/api/v1/videos/{}", 
    "https://invidious.slipfox.xyz/api/v1/videos/{}", 
    "https://vid.priv.au/api/v1/videos/{}",
    "https://iv.ggtyler.dev/api/v1/videos/{}", 
    "https://anontube.lvkaszus.pl/api/v1/videos/{}", 
    "https://invidious.nerdvpn.de/api/v1/videos/{}",
    "https://inv.in.projectsegfau.lt/api/v1/videos/{}", 
    "https://invidious.io.lol/api/v1/videos/{}", 
    "https://inv.tux.pizza/api/v1/videos/{}",
    "https://inv.zzls.xyz/api/v1/videos/{}"]

def get_video_info(video_id):
    api_url = API[random.randrange(0, len(API))].format(video_id)
    response = requests.get(api_url)
    if response.status_code == 200:
        video_info = response.json()
        author = video_info["author"]
        return author

with open('watch-history.html', 'r', encoding='utf-8') as file:
    content = file.read()

matches = re.findall(PATTERN, content)
unique_matches = set(matches)

author_count = {}

with ThreadPoolExecutor() as executor: 
    results = list(executor.map(get_video_info, unique_matches))

for author in results:
    if author != "":
        author_count[author] = author_count.get(author, 0) + 1

sorted_authors = sorted(author_count.items(), key=lambda x: x[1], reverse=True)

for author, count in sorted_authors[:20]: # change number if you want bigger list
    print(f"{author}: {count}")