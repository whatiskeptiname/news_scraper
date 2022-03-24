import requests
import json
import re
import os


def cleanhtml(raw_html):
    # remove html tags from articles
    raw_html = raw_html
    cleanr = re.compile("<.*?>")
    cleantext = re.sub(cleanr, "", raw_html)
    return cleantext


def count_article(search_title):
    # return the number of articles in the file
    if os.path.exists(f"{search_title}.json"):
        with open(f"{search_title}.json", "r") as f:
            data = json.load(f)
            return len(data)
    else:
        # create file if it doesnt exists and return the no. of articles as 0
        with open(f"{search_title}.json", "w+") as f:
            f.write("[]")
            return 0


def load_article(search_title):
    # loads the articles on the file based on search tile and article count

    cleaned_articles = []  # list of articles
    article_count = count_article(search_title)
    page_no = article_count // 10 + 1
    print(page_no)
    print(article_count)
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

    return cleaned_articles


def append_article(search_title):
    # append previously loaded articles with new articles
    article_count = 0
    article_count = count_article(search_title)
    page_count = article_count // 10 + 1

    with open(f"{search_title}.json", "r+") as f:
        previous_articles = json.load(f, strict=False)
        previous_articles = previous_articles[
            0 : (page_count - 1) * 10
        ]  # takes only articles from whole pages, ignores half loaded articles from a page
        new_articles = load_article(search_title)
        if new_articles == None:
            print("some error occured")
            new_articles = []

        previous_articles.extend(new_articles)

    with open(f"{search_title}.json", "w") as f:
        # clear the file
        json.dump(previous_articles, f)


search_title = "हाम्रो"
append_article(search_title)

print("---------completed----------")
