import imp
import requests
from requests.exceptions import HTTPError
import json
import re

# import os
# from pathlib import Path


def cleanhtml(raw_html):  # remove html tags from articles
    raw_html = raw_html
    cleanr = re.compile("<.*?>")
    cleantext = re.sub(cleanr, "", raw_html)
    return cleantext


search_title = "हाम्रो"  # title to search
cleaned_articles = []  # list of articles
previous_articles = []  # list of articles already downloaded
page_count = 1
try:
    # existing_file = Path(f"{search_title}.json")
    # existing_file.touch(exist_ok=True)

    # with open(f"{search_title}.json", "r") as f:  # keeping search_title as file name
    #     article_count = (
    #         len(f.readlines()) - 2
    #     )  # -2 because of the last brackets "[]" in the list

    # page_count = (article_count // 10) + 1  # 10 articles per page
    # if page_count < 1:
    #     page_count = 1
    for page in range(  # starting from page_count (current page) next remaning pages
        1, 4
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
        for item in items:
            content = items[i]["content"]
            cleaned_article = cleanhtml(content)
            cleaned_articles.append(cleaned_article)
            i = i + 1

    # with open(f"{search_title}.json", "w+") as f:  # keeping search_title as file name
    #     if os.stat(f"{search_title}.json").st_size == 0:
    #         json.dump(cleaned_articles, f)
    #         print("new file -------------------")
    #     previous_articles = json.loads(f.read())
    #     final_articles = previous_articles + cleaned_articles
    #     json.dump(cleaned_articles, f)

    with open(f"{search_title}.json", "w+") as f:  # keeping search_title as file name
        json.dump(cleaned_articles, f)

except HTTPError as http_err:
    print(f"HTTP error occurred: {http_err}")
except Exception as err:
    print(f"Other error occurred: {err}")

print("Completed!!!")
