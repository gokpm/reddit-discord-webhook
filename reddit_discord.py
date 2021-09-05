title = '''
Title              : Reddit to Discord
Date Created       : 01-09-2021
Date Last Modified : 04-09-2021
Modification       : GitHub Ready
Created by         : Gokul PM a.k.a icemelting
'''

print(title)

import praw
from discord_webhook import DiscordWebhook, DiscordEmbed
import time

wait_time = 1.618
cache_filepath = <CACHE_FILE_PATH>
subreddit_list = [<SUBREDDIT_NAMES>]
webhook_url = [<RESPECTIVE_WEBHOOK_URL>]
switcher = {}
for i in range(len(webhook_url)):
    switcher.update({subreddit_list[i]: webhook_url[i]})

cache = open(cache_filepath, 'a+')
cache.close()
cache = open(cache_filepath, 'r')
already_seen = cache.read().split()
cache.close()

reddit = praw.Reddit(
    client_id=<CLIENT_ID>,
    client_secret=<CLIENT_SECRET>,
    user_agent=<BOT_NAME>)
reddit.read_only = True

def to_discord(subreddit_name: str, post_limit: int):
    webhook_url = switcher.get(subreddit_name, "nothing")
    sub = reddit.subreddit(subreddit_name)
    latest = sub.hot(limit = post_limit)
    for post in latest:
        if not post.id in already_seen:
            time.sleep(wait_time)
            cache = open(cache_filepath, 'a+')
            cache.write(post.id+'\n')
            cache.close()
            already_seen.append(post.id)
            webhook = DiscordWebhook(url=webhook_url)
            embed = DiscordEmbed(title=post.title, description=post.selftext, color = '9966cc', url = post.url)
            if not post.is_self:
                embed.set_image(url=post.url)
            webhook.add_embed(embed)
            webhook.execute()
    time.sleep(wait_time*5)

while True:
    for r in subreddit_list:
        to_discord(r, 50)
