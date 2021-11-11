'''
Created on 

Course work: 

@author: Harini

Source:
    
'''

# Import necessary modules
from bs4 import BeautifulSoup
import requests
import json



def startpy():

    info_dict = {}
    space_fea_list = []
    url = 'https://spaceishare.com/listing/parking-space/ontario/north-york/88-sheppard-avenue-east-parking-396'
    res=requests.get(url)
    html_page=res.content
    soup=BeautifulSoup(html_page,'html.parser')

    heading = soup.select("body > div.upload_page.desktop-view.showlisting > div > div:nth-child(2) > div.col-md-6.float-left.position-relative.bg-white.pad-none.content-section > div.col-md-12 > h6")[0].text
    price = soup.select("#post-sticky-section > div.bg-white.border-radius-single > div.custom-select-wrapper > div > div.custom-options > span.custom-option.selected > b")[0].text
    mydivs = soup.find("div", {"class": "row mr-30 row-pad"})
    feat = mydivs.find_all("p", {"class": "p-font-size"})
    for t in feat:
        a=t.text.strip()
        space_fea_list.append(a)
    # print(space_fea_list)
    description = space_fea_list[0]
    type_space = space_fea_list[1]
    detail_feat = space_fea_list[2:]
    # print(detail_feat)
    # print(price)
    host = soup.find("p", {"class": "text-name1"})
    # print(host.text.strip())
    # images = soup.find("div", {"class":"carousel-item active"})
    for a in soup.find_all('a'):
        if a.img:
            # print(a.img['src'])
            a.img['src']

    info_dict["name"] = heading
    info_dict["price"] = price
    info_dict["description"] = description
    info_dict["type of space"] = type_space
    info_dict["space details and features"] = detail_feat
    info_dict["hosted by"] = host.text.strip()
    info_dict["images"] = []
    # data = []

    # with open("info.json", "r") as file:
    #     data = json.load(file)

    # try:
    #     data['pages'].append(info_dict)
    # except:
    #     data = {
    #             "pages" : [info_dict]
    #             }
    return info_dict
    # with open("info.json", "w") as file:
    #     json.dump(info_dict, file, indent=4)

if __name__ == '__main__':

    final_dict = startpy()
    print(final_dict)