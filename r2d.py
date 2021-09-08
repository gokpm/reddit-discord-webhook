'''
Version:            0.4
Date last modified: 08-09-2021
Modified by:        icemelting
Contributed by:     icemelting
'''

import asyncpraw, time
from discord_webhook import DiscordWebhook, DiscordEmbed
import asyncio

async def cache(cacheMode):
    cache_fp = <CACHE_FILEPATH>
    global archive
    if cacheMode == 'r':
        cache = open(cache_fp, 'a+')
        cache.close()
        cache = open(cache_fp, 'r')
        archive = cache.read().split()
        cache.close()
    elif cacheMode == 'a+':
        cache = open(cache_fp, 'a+')
        cache.write(post.id+'\n')
        cache.close()
        archive.append(post.id)
    return
           
async def execWebhook(webhookUrl):
    webhook = DiscordWebhook(url=webhookUrl)
    embed = DiscordEmbed(title=post.title, description=post.selftext, color = '9966cc', url = post.url)
    if not post.is_self:
        embed.set_image(url=post.url)
    webhook.add_embed(embed)
    webhook.execute()
    await asyncio.sleep(sleep_time)

async def send(postList, webhookUrl):
    global post
    async for post in postList:
        if not post.id in archive:
            await cache('a+')
            await execWebhook(webhookUrl)
    return    

async def notify(subReddit, sortBy, postLimit):
    webhookDictionary = {
    'opencv': <WEBHOOK_URL>,
    'jokes': <WEBHOOK_URL>,
    'dankmemes': <WEBHOOK_URL>,
    'python': <WEBHOOK_URL>,
    'fountainpens': <WEBHOOK_URL>}
    webhookUrl = webhookDictionary[subReddit]
    sub = await reddit.subreddit(subReddit)
    if sortBy.lower() == 'new':
        new = sub.new(limit = postLimit)
        await send(new, webhookUrl)
    elif sortBy.lower() == 'hot':
        hot = sub.hot(limit = postLimit)
        await send(hot, webhookUrl)
    return
   
async def main():
    global sleep_time, reddit
    sleep_time = 1.618
    reddit = asyncpraw.Reddit(
    client_id=<CLIENT_ID>,
    client_secret=<CLIENT_SECRET>,
    user_agent=<BOT_NAME>)
    reddit.read_only = True
    i = 0
    await cache('r')
    while True:
        time_start = time.perf_counter()
        await notify('opencv', 'new', 50)
        await notify('jokes', 'hot', 50)
        await notify('dankmemes', 'hot', 50)
        await notify('python', 'new', 50)
        await notify('fountainpens', 'new', 50)
        i += 1
        time_end = time.perf_counter()
        time_min = int((time_end - time_start)/60)
        time_sec = int((time_end - time_start)%60)
        print(f'Cycle {i} Ping: {time_min}m {time_sec}s')
    return
          
if __name__ == '__main__':
    asyncio.run(main())