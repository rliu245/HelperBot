import discord
import requests
from bs4 import BeautifulSoup
import datetime

client = discord.Client()

"""
Description:
    helper function for formatting the news obtained from Maplestory 2 into format
        Title1:
        Category1:
        Date1:
        Link of Website1:
            
        Title2:
        Category2:
        ...

Parameters:
    links - a list of tuples/lists with 4 indices
    
Returns:
    String with proper formatting
"""
def print_news(links):
    result = []
    for tuples in links:
        result.append(' Title: {} \n Category: {} \n Date: {} \n Link: {} \n'.format(tuples[0], tuples[1], tuples[2], tuples[3]))
    
    result_string = '\n'.join(result)
    return result_string

"""
Description:
    scrapes maplestory 2 news website for news and saves the title, category, date, and link of each news item.

Parameters:
    url - website to be scraped(in this case, maplestory2's news website)
    
Returns:
    list of tuples(where each tuple has 4 elements)
"""
def retrieve_news(url = 'http://maplestory2.nexon.net/en/news'):
    USER_AGENT = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}
    page = requests.get(url, headers = USER_AGENT)
    # can use html.parser or lxml
    soup = BeautifulSoup(page.text, 'html.parser')
    
    # scrape all the news listings on the website
    all_news = soup.find(class_ = 'news-list')
    important_news = all_news.find_all('figure', attrs = {'class': 'news-item'})

    links = []

    for item in important_news:
        title = item.find('h2').text
        
        # Each news category has a different class name for scraping(nc-events, nc-announcements, nc-updates, nc-sales, and nc-maintenances)
        category = item.find('span', class_ = 'news-category-tag nc-events')
        if category is None:
            category = item.find('span', class_ = 'news-category-tag nc-announcements')
        if category is None:
            category = item.find('span', class_ = 'news-category-tag nc-updates')
        if category is None:
            category = item.find('span', class_ = 'news-category-tag nc-sales')
        if category is None:
            category = item.find('span', class_ = 'news-category-tag nc-maintenances')
        # In case news category doesnt fall under the 5 listed, categorize it as None and come back to it later
        category = 'Unknown' if category is None else category.text
        
        time = item.find('time').text
        
        # must add maplestory2.nexon.net to the beginning of the links
        link = 'maplestory2.nexon.net' + item.find('a', {'class': 'news-item-link', 'href': True})['href']
    
        links.append((title, category, time, link))
        
    return links

@client.event
async def on_ready():
    print("{} is in".format(client.user))

@client.event
async def on_message(message):
    if message.author != client.user:
        if message.content.lower() == 'time':
            '''
            await client.send_message(message.channel,
                                      'This one is for tommy_troll :smirk:\n' + 'If event starts on Saturday Maple time, then for people in the US it starts at: \nPDT (UTC -7): 5:00 PM on Friday \nEDT (UTC-7): 8:00 PM on Friday \n')
            '''
            # Prints the Time in format: (Tue, 16 October 2018 04:41:32 PM)
            await client.send_message(message.channel, 'For tommy_troll who loves to troll really hard :smirk: :joy:\nMaplestory 2 time is currently: {}'.format(datetime.datetime.utcnow().strftime('%a, %d %B %Y %I:%M:%S %p %z')))
        
        if message.content.lower() == 'news':
            await client.send_message(message.channel, print_news(retrieve_news('http://maplestory2.nexon.net/en/news')))

token = open('token_key').readline().strip()
client.run(token)