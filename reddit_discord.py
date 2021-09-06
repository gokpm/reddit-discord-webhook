import praw, time
from discord_webhook import DiscordWebhook, DiscordEmbed

sleep_time = 1.618
cache_fp = <CACHE_FILEPATH>

webhookDictionary = {
'opencv': <WEBHOOK_URL>,
'jokes': <WEBHOOK_URL>,
'dankmemes': <WEBHOOK_URL>,
'python': <WEBHOOK_URL>,
'fountainpens': <WEBHOOK_URL>}

reddit = praw.Reddit(
client_id=<CLIENT_ID>,
client_secret=<CLIENT_SECRET>,
user_agent=<BOT_NAME>)
reddit.read_only = True

def cache(cacheMode):
    if cacheMode == 'r':
        global archive
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
    return archive
    
def notify(subReddit, sortBy, postLimit):
    webhookUrl = webhookDictionary[subReddit]
    sub = reddit.subreddit(subReddit)
    if sortBy.lower() == 'new':
        new = list(sub.new(limit = postLimit))
        new.reverse()
        send(new, webhookUrl)
    elif sortBy.lower() == 'hot':
        hot = sub.hot(limit = postLimit)
        send(hot, webhookUrl)
        
def send(postList, webhookUrl):
    global post
    for post in postList:
        if not post.id in archive:
            cache('a+')
            execWebhook(webhookUrl)
    return archive
            
def execWebhook(webhookUrl):
    webhook = DiscordWebhook(url=webhookUrl)
    embed = DiscordEmbed(title=post.title, description=post.selftext, color = '9966cc', url = post.url)
    if not post.is_self:
        embed.set_image(url=post.url)
    webhook.add_embed(embed)
    webhook.execute()
    time.sleep(sleep_time*3)
   
def main():
    i = 0
    cache('r')
    while True:
        time_start = time.perf_counter()
        notify('opencv', 'new', 100)
        notify('jokes', 'hot', 100)
        notify('dankmemes', 'hot', 100)
        notify('python', 'new', 100)
        notify('fountainpens', 'new', 100)
        i += 1
        time_end = time.perf_counter()
        time_min = int((time_end - time_start)/60)
        time_sec = int((time_end - time_start)%60)
        print(f'Cycle {i} Ping: {time_min}m {time_sec}s')
          
if __name__ == '__main__':
    main()