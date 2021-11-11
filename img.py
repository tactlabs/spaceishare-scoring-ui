import requests
from bs4 import BeautifulSoup
import os
import re
import shutil
    

def scrape_url(url):

    r = requests.get(url)
    soup = BeautifulSoup(r.text,'html.parser')

    # print(soup)
    # div = soup.find_all('div', class_ = "search-box-bg")
    div = []
    url = 'https://spaceishare.com/listing/parking-space/ontario/north-york/88-sheppard-avenue-east-parking-396'
    res=requests.get(url)
    html_page=res.content
    soup=BeautifulSoup(html_page,'html.parser')
    for a in soup.find_all('a'):
        if a.img:
            print(a.img['src'])
            div.append(a)
    name = soup.select("body > div.upload_page.desktop-view.showlisting > div > div:nth-child(2) > div.col-md-6.float-left.position-relative.bg-white.pad-none.content-section > div.col-md-12 > h6")[0].text
    # div = soup.find_all('div', class_ = "carousel-item")
    save_img(name, div)
    # print(div)
    # print(div)
    # get_images(div)

def save_img(name, urls):

    for url in urls:
        if 'http' in url:
            r = requests.get(url, stream=True)
            if r.status_code == 200:
                if 'images' not in os.listdir():
                    os.makedirs('images')

                extension = url.split('.')[-1]
                path = f'images/{name}.{extension}'

                with open(path, 'wb') as f:
                    r.raw.decode_content = True
                    shutil.copyfileobj(r.raw, f)
                


if __name__ == '__main__':
    scrape_url('https://spaceishare.com/Listings')