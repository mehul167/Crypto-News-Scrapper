from bs4 import BeautifulSoup
import requests
import sys
from pymongo import MongoClient
import os
from dotenv import load_dotenv
sys.stdout.reconfigure(encoding='utf-8')

def coindesk(url):
    
    html_text = requests.get(url).text

    load_dotenv()
    mongo_url = os.getenv("MONGODB_URL")
    client = MongoClient(mongo_url)
    db = client['Scrapped_Data']
    collection = db['coindesk']

    soup = BeautifulSoup(html_text, 'lxml')
    articles = soup.find_all('div', class_ = "article-cardstyles__StyledWrapper-sc-q1x8lc-0 eJFoEa article-card default")
    data_list=[]
    for article in articles:
        title_outer = article.find('div',class_="article-cardstyles__Block-sc-q1x8lc-3 tVfWq")
        title_inner=title_outer.find('h6', class_="typography__StyledTypography-sc-owin6q-0 VxEiN")
        title2=title_inner.a['href']
        title=title_inner.find('a').text.replace("\n","")
        description = article.find('span', class_ = "content-text").text.replace('  ','')
        date = article.find('span', class_ ="typography__StyledTypography-sc-owin6q-0 iOUkmj").text.split("at")[0]
        image_url = article.select_one('picture source[type="image/webp"]')['srcset'].split("339w")[0]
        source = "https://www.coindesk.com/"
        post_url = f"{source}{title2}"
        website_url = "https://www.coindesk.com/pf/resources/images/logos/Coindesk_logo_396x75.svg?d=357"

        document = {
            "Title": title,
            "Description": description,
            "Date": date,
            "image_url": image_url,
            "source": source,
            "post_url": post_url,
            "logo_url": website_url
        }
        
        if collection.count_documents(document, limit=1) == 0:
            data_list.append(document)

    for document in data_list:
        collection.insert_one(document)

    client.close()
    return True

def blockworks(url):
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0'
    headers = {'User-Agent': user_agent}
    html_text = requests.get(url, headers=headers).text

    load_dotenv()
    mongo_url = os.getenv("MONGODB_URL")
    client = MongoClient(mongo_url)
    db = client['Scrapped_Data']
    collection = db['coindesk']

    soup = BeautifulSoup(html_text, 'lxml')
    articles = list(soup.find_all('div', class_="grid grid-cols-1 grid-rows-[168px_minmax(168px,_1fr)] h-full"))
    data_list=[]
    count=0
    for article in articles:
        link = f'https://blockworks.co/{article.a['href']}'
        title = article.find('a', class_="font-headline flex-grow text-[18px] lg:text-[24px] font-semibold leading-snug hover:text-primary").text
        description = article.find("p" ,class_="flex-grow text-base text-left text-[#6a6a6a] text-light-gray").text
        date = article.find("time").text
        source = "https://blockworks.co/"
        logo_url="https://seekvectorlogo.net/wp-content/uploads/2023/04/blockworks-inc-vector-logo.png"
        image_url=f"https://blockworks.co{article.find("img",class_="object-cover w-full h-full")['src']}"
        document = {
            "Title": title,
            "Description": description,
            "Date": date,
            "image_url": image_url,
            "source": source,
            "post_url": link,
            "logo_url": logo_url
        }
        
        if collection.count_documents(document, limit=1) == 0:
            data_list.append(document)

    for document in data_list:
        collection.insert_one(document)
    client.close()
    return True

def main():
    url_coindesk= ["https://www.coindesk.com/newsletters/the-node/","https://www.coindesk.com/newsletters/first-mover/","https://www.coindesk.com/newsletters/first-mover/","https://www.coindesk.com/newsletters/crypto-long-short/","https://www.coindesk.com/newsletters/the-protocol/","https://www.coindesk.com/newsletters/crypto-for-advisors/"]
    for urls in url_coindesk:
        coindesk(urls)
    
    url_blockworks = "https://blockworks.co/news"
    blockworks(url_blockworks)

if __name__ == "__main__":
    main()
