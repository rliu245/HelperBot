# washingtonshiao@gmail.com
import discord
import os
import requests
from bs4 import BeautifulSoup

client = discord.Client()

def print_news(links):
    result = []
    for tuples in links:
        result.append(' Title: {} \n Category: {} \n Time: {} \n Link: {} \n'.format(tuples[0], tuples[1], tuples[2], tuples[3]))
    
    result_string = '\n'.join(result)
    return result_string

def retrieve_news():
    USER_AGENT = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}
    url = 'http://maplestory2.nexon.net/en/news'
    page = requests.get(url, headers = USER_AGENT)
    # can use html.parser or lxml
    soup = BeautifulSoup(page.text, 'html.parser')
    
    all_news = soup.find(class_ = 'news-list')
    important_news = all_news.find_all('figure', attrs = {'class': 'news-item'})

    links = []

    for item in important_news:
        # must add maplestory2.nexon.net to the beginning of the links
        link = 'maplestory2.nexon.net' + item.find('a', {'class': 'news-item-link', 'href': True})['href']
        time = item.find('time').text
    
        category = item.find('span', class_ = 'news-category-tag nc-events')
        if category is None:
            category = item.find('span', class_ = 'news-category-tag nc-announcements')
        if category is None:
            category = item.find('span', class_ = 'news-category-tag nc-updates')
        if category is None:
            category = item.find('span', class_ = 'news-category-tag nc-sales')
        if category is None:
            category = item.find('span', class_ = 'news-category-tag nc-maintenances')
        
        category = 'Unknown' if category is None else category.text
        title = item.find('h2').text
    
        links.append((title, category, time, link))
        
    return links

@client.event
async def on_ready():
    print("I'm in")
    print(client.user)

@client.event
async def on_message(message):
    if message.author != client.user:
        if message.content.lower() == 'time':
            await client.send_message(message.channel,
                                      'This one is for tommy_troll :smirk:\n' + 'If event starts on Saturday Maple time, then for people in the US it starts at: \n PDT (UTC -7): 5:00 PM on Friday \n EDT (UTC-7): 8:00 PM on Friday \n')
        
        if message.content.lower() == 'test':
            await client.send_message(message.channel, print_news(retrieve_news()))

# token = os.environ.get("DISCORD_BOT_SECRET")
# Client ID: 501445905296130068
token = 'NTAxNDQ1OTA1Mjk2MTMwMDY4.DqZftg.n0Ro1QgBOR9QPCe9yUDbcazkBhw'
client.run(token)