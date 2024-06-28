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
        logo_url="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAUQAAABMCAYAAAAVzs4fAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAABimSURBVHhe7Z0J2BVj+8Cfojct2iwJfUIlsoQkW9mXZItCirJG1gjJkrXFTkTKLpR9LbsQkqIoRJElsvO2/jH/+U3PcJpm5rnnnPPmPd93/67ruZrnvDPnnObM3M+9TxXPxyiKoiimqv1XURTlfx4ViIqiKBYViIqiKBYViIqiKBYViIqiKBYViIqiKBYViIqiKBYViIqiKBYViIqiKBYViIqiKBYViIqiKBYViIqiKBYViIqiKJaCut00XaOz3XKzUtkS88Mvn9lZOrVXrWna7baluXDAWaZZs2b21WQWLFhgatWqZWfxbLfddmbChAl2puRSpUoVuxXPZpttZqZOnWpnyv8Su+22m3nppZfsLJ7vv//erL766nZW2lRKDbH89wVm3LhnTfPmzc1OO+1kysvL7V8URVEqjkpvMr/++uvB6vP444/bVxRFUSqGkvAhLl682Bx44IFmxIgR9hVFUZTiU1JBlRNOOMHMnDnTzhRFUYpLSQnEv/76y+y99952piiKUlxKSiDCrFmzzIMPPmhniqIoxaPkBCJccskldktRFKV4lKRAnDFjht1SFEUpHiUpEMklf+aZZ+xMURSlOJSkQIS3337bbimKohSHggRirZp1xaOKV8PUqbWaeNQoa+AfVydxzPhwlv0WiqIoxaEggVijSmPxqF+riVnJW1M8Vq2+oaluGieOjZtvYb+FoihKcSiouUPbJhfbLTdVqi003wubO8Aqtf8yc+d9bGfLM+bxW82uu+8QbFd0c4dvvvnGvPfee+ann34Kxq+//mrq1KljGjRoEAyaH/znP/+xe1csn332mZk+fXrwPX788cfg/05pI2Pdddc1bdu2tXvK0eYOK44pU6aYL7744u9riSqs8DpaY401gt+vZs2adu9/n8rc3IHz9+677wb359y5c021atX+vhe22GKL4H7ISskKxB/nf2C3KkYgInhGjRplnnzySfPOO+/YV5PZcsstzX777WeOOOKIoClFMUEA8l0effTRYDuN2rVrm1122cUcdNBB5vDDDzerrLKK/UsyxRSICOkbb7zRzpblq6++Mp9++qmdLaVFixZm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"
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
