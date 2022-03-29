import requests
import json
import re


def cleanhtml(raw_html):
    # remove html tags from articles
    raw_html = raw_html
    cleanr = re.compile("<.*?>")
    cleantext = re.sub(cleanr, "", raw_html)
    return cleantext


def last_fetched_page(search_title):
    # return the last fetched page number
    try:
        with open(f"{search_title}.json", "r+") as _:  # check if file exists
            with open("article_index.json", "r+") as f:
                data = json.load(f)
                return data[search_title]  # return the page number of last fetch
    except FileNotFoundError:
        # update page index of deleted file to 0
        # add new search title with page index 0 to the index file if it doesnt exist
        with open(f"{search_title}.json", "w") as f:
            f.write("[]")
        with open("article_index.json", "r+") as f:
            data = json.load(f)
            data.update({search_title: 0})
        # clear the  file to dump
        with open("article_index.json", "w") as f:
            json.dump(data, f)
            return 0
    except KeyError:
        with open("article_index.json", "r+") as f:
            data = json.load(f)
            data.update({search_title: 0})
        # clear the  file to dump
        with open("article_index.json", "w") as f:
            json.dump(data, f)
        return 0


def add_page_index(search_title, page_no):
    # update the page index of the file to the last fetch page from the site
    with open("article_index.json", "r+") as f:
        data = json.load(f)
        # page_index = {search_title: page_no}
        data[search_title] = page_no
        # clear the  file to dump
    with open("article_index.json", "w") as f:
        json.dump(data, f)


def load_article(search_title):
    # loads the articles on the file based on search tile
    end_page_no = 4  # fetch articles till page (end_page_no -1)
    cleaned_articles = []  # list of articles
    page_no = last_fetched_page(
        search_title
    )  # get the page on which the last fetch was done from
    for (
        page
    ) in range(  # starting from page_no (last fetched page) to next remaning pages
        page_no + 1, end_page_no
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
        add_page_index(search_title, page)  # update the page index
        print(f"Page {page} loaded")
    return cleaned_articles


def append_article(search_title):
    # append previously loaded articles in the json file with new articles
    page_count = last_fetched_page(
        search_title
    )  # each page contaions 10 articles so integer division to get the lastly fetched page
    with open(f"{search_title}.json", "r+") as f:
        previous_articles = json.load(f, strict=False)
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


search_title = "हाम्रो"
append_article(search_title)

print("\n--completed--")
