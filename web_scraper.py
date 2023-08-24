import requests
from bs4 import BeautifulSoup as bs
import datetime
import pandas as pd
import os
import time

def code():
    url = "https://www.reddit.com/?feed=home"
    req = requests.get(url)
    soup = bs(req.content,"html.parser")
    divs = soup.find_all("div", {"slot": "title"})
    data = []
    
    index = 0
    if os.path.exists("reddit_titles.csv"):
        file = pd.read_csv("reddit_titles.csv")
        index = file.shape[0]

    for div in divs:
        index += 1
        title = div.get_text(strip=True)
        timestamp = datetime.datetime.timestamp(datetime.datetime.utcnow())
        data.append([index, title, timestamp])
        
    try:
        existing_df = pd.read_csv("reddit_titles.csv")
    except FileNotFoundError:
        existing_df = pd.DataFrame(columns=["Index", "Title", "Timestamp"])
    new_df = pd.DataFrame(data, columns=["Index", "Title", "Timestamp"])
    combined_df = pd.concat([existing_df, new_df])
    combined_df.to_csv("reddit_titles.csv", index=False)

    return data

while True:
     print(datetime.datetime.now())
     code()
     time.sleep(25)