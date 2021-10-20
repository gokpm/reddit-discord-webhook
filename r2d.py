import json
import asyncpraw
import asyncio
from discord_webhook import DiscordWebhook, DiscordEmbed

class Database:
    def __init__(self, path) -> None:
        self.path = path
        if os.path.isfile(path):
            self.read()
        else:
            self.write([])
        return
        
    def __call__(self) -> list:
        return self.data
    
    def read(self) -> None:
        with open(self.path, 'r') as file:
            self.data = json.load(file)
        return
        
    def write(self, data) -> None:
        self.data = data
        with open(self.path, 'w') as file:
            json.dump(self.data, file, indent = 4)
        return
        
class Bot:
    def __init__(self, subreddit, post_count):
        self.subreddit = subreddit
        self.webhook = webhook
        self.cache = Database(subreddit+'.json')
        return
        
    async def get_submissions(self):
        while True:
            try:
                self.reddit = asyncpraw.Reddit(client_id=<CLIENT_ID>,
                                          client_secret=<CLIENT_SECRET>,
                                          user_agent=<USER_AGENT>)
                self.reddit.read_only = True
                break
            except:
                pass
        return
        
        
    
    

         

async def cache(cacheMode):
    cache_fp = r'archive.json'
    global archive
    if cacheMode == 'r':
        try:
            with open(cache_fp, 'r') as archive_file:
                archive = json.load(archive_file)
        except:
            with open(cache_fp, 'w') as archive_file:
                json.dump([], archive_file, indent = 4)   
            with open(cache_fp, 'r') as archive_file:
                archive = json.load(archive_file)
    elif cacheMode == 'r+':
        archive.append(post.id)
        with open(cache_fp, 'r+') as archive_file:
                json.dump(archive, archive_file, indent = 4)
    return
           
async def execWebhook(webhookUrl):
    webhook = DiscordWebhook(url=webhookUrl)
    embed = DiscordEmbed(title=post.title,
            description=post.selftext,
            color = '9966cc',
            url = post.url)
    if not post.is_self:
        embed.set_image(url=post.url)
    webhook.add_embed(embed)
    webhook.execute()
    await asyncio.sleep(sleep_time*3)

async def send(postList, webhookUrl):
    global post
    async for post in postList:
        if not post.id in archive:
            await cache('r+')
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
    client_id=<CLIENT_ID>
    client_secret=<CLIENT_SECRET>,
    user_agent=<USER_AGENT>)
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
        time_taken = time_end - time_start
        print('Cycle {0}: {1:.2f}s'.format(i, time_taken))
    return
          
if __name__ == '__main__':
    asyncio.run(main())
    
