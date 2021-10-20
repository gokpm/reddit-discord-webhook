import os
import json
import asyncio
import asyncpraw
from dotenv import load_dotenv
from discord_webhook import DiscordWebhook, DiscordEmbed

load_dotenv()

class Database:
    def __init__(self, path) -> None:
        self.path = path
        if os.path.isfile(self.path):
            self.read()
        else:
            self.data = []
            self.write()
        return
    
    def read(self) -> None:
        with open(self.path, 'r') as file:
            self.data = json.load(file)
        return
        
    def write(self) -> None:
        with open(self.path, 'w') as file:
            json.dump(self.data, file, indent = 4)
        return
        
class Bot:
    def __init__(self, subreddit_name, post_count, webhook_url):
        self.subreddit = subreddit_name
        self.count = post_count
        self.webhook_url = webhook_url
        self.cache = Database(self.subreddit+'.json')
        return
        
    async def run(self):
        while True:
            try:
                reddit = asyncpraw.Reddit(
                    client_id = os.environ['CLIENT_ID'],
                    client_secret = os.environ['CLIENT_SECRET'],
                    user_agent = os.environ['USER_AGENT'])
                reddit.read_only = True
                self.sub = await reddit.subreddit(self.subreddit)
                self.posts = self.sub.hot(limit = self.count)
                break
            except:
                pass       
        async for post in self.posts:
            if post.id in self.cache.data:
                continue
            else:
                self.cache.data.append(post.id)
                self.cache.write()
                self.webhook = DiscordWebhook(url=self.webhook_url)
                embed = DiscordEmbed(title=post.title,
                    description=post.selftext,
                    color = '9966cc',
                    url = post.url)
                if post.is_self:
                    pass
                else:
                    embed.set_image(url=post.url)
                self.webhook.add_embed(embed)
                self.webhook.execute()
                await asyncio.sleep(1) 
        return
        
async def main():
    instance = []    
    instance.append(Bot('jokes', 100, os.environ['jokes']))
    instance.append(Bot('dankmemes', 100, os.environ['dankmemes']))
    instance.append(Bot('python', 100, os.environ['python']))
    instance.append(Bot('linux', 100, os.environ['linux']))
    tasks = []
    for i in range(len(instance)):
        tasks.append(asyncio.create_task(instance[i].run()))  
    while True:
        await asyncio.wait(tasks)
    return
   
if __name__=='__main__':
    asyncio.run(main())
