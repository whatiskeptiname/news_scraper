import requests
from requests.exceptions import HTTPError
import json
import re


def cleanhtml(raw_html):  # remove html tags from articles
    raw_html = raw_html
    cleanr = re.compile("<.*?>")
    cleantext = re.sub(cleanr, "", raw_html)
    return cleantext


search_title = "हाम्रो"  # title to search
cleaned_articles = []  # list of articles
try:
    # with open("pagination_counter.json","w+") as pf:
    #     pagination_i = int(pf.readline())
    # print("-------------------" + pagination_i)
    for page in range(
        5, 6
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

    with open(f"{search_title}.json", "w") as f:  # keeping search_title as file name
        json.dump(cleaned_articles, f)

except HTTPError as http_err:
    print(f"HTTP error occurred: {http_err}")
except Exception as err:
    print(f"Other error occurred: {err}")


print("Completed!!!")
