import requests
from requests.exceptions import HTTPError
import json
import re
import os


def cleanhtml(raw_html):
    # remove html tags from articles
    raw_html = raw_html
    cleanr = re.compile("<.*?>")
    cleantext = re.sub(cleanr, "", raw_html)
    return cleantext


def article_count(search_title):
    # return the number of articles in the file
    if os.path.exists(f"{search_title}.json"):
        with open(f"{search_title}.json", "r+") as f:
            data = json.load(f)
            return len(data)
    else:
        # create file if it doesnt exists and return the no. of articles as 0
        with open(
            f"{search_title}.json", "w+"
        ) as f:
            return 0


def load_article(search_title, article_count):
    # loads the articles on the file based on search tile and article count
    page_no = article_count // 10 + 1 # totle pages from which article is already fetched
    article_no = article_count % 10 # number of articles in the last page already fetched
    cleaned_articles = []  # list of articles
    
    for page in range(  # starting from page_count (current page) next remaning pages
        page_no, 4
    ):  # each page contains 10 articles so taking 3 pages in loop for 30 articles
        url = (
            "https://bg.annapurnapost.com/api/search?title="
            + search_title
            + "&page="
            + str(page)
        )
        response = requests.get(url)
        json_response = response.json()
        items = json_response["data"]["items"]
        i = 0  # index for item list count
        for _ in items:
            content = items[i]["content"]
            cleaned_article = cleanhtml(content)
            cleaned_articles.append(cleaned_article)
            i = i + 1
        with open(
            f"{search_title}.json", "w+"
        ) as f:  # keeping search_title as file name
            json.dump(cleaned_articles, f)





search_title = "हम्रो"
# load_article("हाम्रो", 2)
print(article_count(search_title))

print("-------------------")
