import requests
import json
import re


def cleanhtml(raw_html):
    # remove html tags from articles
    raw_html = raw_html
    cleanr = re.compile("<.*?>")
    cleantext = re.sub(cleanr, "", raw_html)
    return cleantext


def count_article(search_title):
    # return the number of articles in the file
    try:
        with open(f"{search_title}.json", "r+") as f:
            data = json.load(f)
            if (
                data == None
            ):  # if file contains no list, create one to prevent None error
                print("some error occured")
                data = []
                json.dump(data, f)
        return len(data)
    except FileNotFoundError:
        # create file if it doesnt exists and return the no. of articles as 0
        with open(f"{search_title}.json", "w") as f:
            f.write("[]")
            return 0


def load_article(search_title):
    # loads the articles on the file based on search tile
    cleaned_articles = []  # list of articles
    article_count = count_article(
        search_title
    )  # gives the no. of articles in the json file
    page_no = (
        article_count // 10 + 1
    )  # get the page on which the last fetch was done from
    for (
        page
    ) in range(  # starting from page_no (last fetched page) to next remaning pages
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
        for _ in items:  # loop over the articles
            content = items[i]["content"]
            cleaned_article = cleanhtml(content)  # remove html tags
            cleaned_articles.append(
                cleaned_article
            )  # append individual articles in a list
            i = i + 1
    return cleaned_articles


def append_article(search_title):
    # append previously loaded articles in the json file with new articles
    article_count = count_article(search_title)
    page_count = (
        article_count // 10
    )  # each page contaions 10 articles so integer division to get the lastly fetched page
    with open(f"{search_title}.json", "r+") as f:
        previous_articles = json.load(f, strict=False)
        previous_articles = previous_articles[
            0 : (page_count) * 10
        ]  # takes only articles from whole pages, ignores if the no. of articles loaded is less then total article in the page
        new_articles = load_article(search_title)
        if new_articles == None:
            print("some error occured")
            new_articles = []
        previous_articles.extend(
            new_articles
        )  # append previously loaded articles with newly fetched articles
    with open(f"{search_title}.json", "w") as f:
        # clear the file and dump total articles
        json.dump(previous_articles, f)


search_title = "हाम्"
append_article(search_title)
# print(count_article(search_title))

print("---------completed----------")
