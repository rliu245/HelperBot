import discord
import requests
from bs4 import BeautifulSoup
import datetime
import json
import _thread
import asyncio
import random

client = discord.Client()
news_db = 0

def read_newsfile(filename):
    with open(filename) as f_in:
        return json.load(f_in)

def write_newsfile(data, filename):
    with open(filename, 'w') as f_out:
        json.dump(data, f_out)

async def reset_timer():
    now = datetime.datetime.now()
    await 'Work in Progress'
    pass

# simulation of a mutex lock since only 1 person per wash
washing_machine_in_use = False

def start_laundry(author):
    global washing_machine_in_use
    if washing_machine_in_use:
        # wait for washing machine to finish
        pass
    
    washing_machine_in_use = True
    msg = '{} is using the washing machine'.format(author.mention)
    print(msg)
    return msg

async def finish_laundry(author):
    global washing_machine_in_use
    wait_time = random.randint(60, 300)
    print('{} has to wait {}'.format(author, wait_time))
    await asyncio.sleep(wait_time)
    
    washing_machine_in_use = False
    msg = '{} has finished washing their clothes'.format(author.mention)
    print(msg)
    return msg

"""
Description:
    
Parameter:
    
Return:

"""
def check_for_new_news(url = 'http://maplestory2.nexon.net/en/news'):
    USER_AGENT = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}
    page = requests.get(url, headers = USER_AGENT)
    # can use html.parser or lxml
    soup = BeautifulSoup(page.text, 'html.parser')
    
    # scrape all the news listings on the website
    all_news = soup.find(class_ = 'news-list')
    important_news = all_news.find_all('figure', attrs = {'class': 'news-item'})

    links = []
    # Create a dict to hold all the patches. Keys are Time(String), Values are News_Titles(List)
    change = False

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
        
        if time in news_db:
            if title in news_db[time]:
                continue
            else:
                news_db[time].append(title)
                change = True
                
                links.append((title, category, time, link))
        else:
            news_db[time] = [title]
            change = True
            
            links.append((title, category, time, link))
    
    if change:
        write_newsfile(news_db, 'news_db.json')
    
    return links

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
        result.append('Title: {}\nCategory: {}\nDate: {}\nLink: {}\n'.format(tuples[0], tuples[1], tuples[2], tuples[3]))
    
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
    # Create a dict to hold all the patches. Keys are Time(String), Values are News_Titles(List)
    change = False

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
        link = 'http://maplestory2.nexon.net' + item.find('a', {'class': 'news-item-link', 'href': True})['href']
    
        links.append((title, category, time, link))
        
        if time in news_db:
            if title in news_db[time]:
                continue
            else:
                news_db[time].append(title)
                change = True
        else:
            news_db[time] = [title]
            change = True
    
    if change:
        write_newsfile(news_db, 'news_db.json')
        
    return links

@client.event
async def on_ready():
    print("{} is in".format(client.user))
    
    for server in client.servers:
        print('Joined Server {}'.format(server))
    
    '''
    try:
        _thread.start_new_thread(check_for_news, ())
    except Exception as e:
        print("Error unable to start thread")
        print(e)
    '''

@client.event
async def on_message(message):
    if message.author != client.user:
        # Create variable to hold the message so it's easier to create if/elif statements
        msg = message.content.lower()
        if msg == 'time':
            '''
            await client.send_message(message.channel,
                                      'This one is for tommy_troll :smirk:\n' + 'If event starts on Saturday Maple time, then for people in the US it starts at: \nPDT(West Coast) (UTC -7): 5:00 PM on Friday \nEDT(East Coast) (UTC-7): 8:00 PM on Friday \n')
            '''
            # Prints the Time in format: (Tue, 16 October 2018 04:41:32 PM)
            await client.send_message(message.channel, 'For Tommy_troll who is a super troll :smirk: :joy:\nMaplestory 2 time is currently: {}'.format(datetime.datetime.utcnow().strftime('%a, %d %B %Y %I:%M:%S %p %z')))
 
        elif msg == 'time reset':
            await client.send_message(message.channel, reset_timer())

        elif msg == 'news':
            await client.send_message(message.channel, print_news(retrieve_news('http://maplestory2.nexon.net/en/news')))
            
        elif msg == 'setlaundry':
            start = start_laundry(message.author)
            await client.send_message(message.channel, start)
            await client.send_message(message.channel, await finish_laundry(message.author))

async def check_for_news():
    await client.wait_until_ready()
    
    while(True):
        news = check_for_new_news()
        if not news == []:
            await client.send_message(client.get_channel('499717504726335518'), print_news(news))
        else:
            print('Waiting.....')
            await client.send_message(client.get_channel('501450681270534183'), 'hello world')
            
        await asyncio.sleep(300)               

if __name__ == "__main__":
    token = open('token_key').readline().strip()
    news_db = read_newsfile('news_db.json')
    client.loop.create_task(check_for_news())
    client.run(token)
    '''
    loop = asyncio.get_event_loop()
    loop.run_until_complete(check_for_news())
    '''