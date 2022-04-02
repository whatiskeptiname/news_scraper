import requests
import json
import re
from icecream import ic


def cleanhtml(raw_html):
    # remove html tags from articles
    raw_html = raw_html
    cleanr = re.compile("<.*?>")
    cleantext = re.sub(cleanr, "", raw_html)
    return cleantext


def delete_file_content(file_ptr):
    # delete the content of the file
    file_ptr.seek(0)
    file_ptr.truncate()


def add_page_index(file_p, search_title, page_no):
    # update the page index of the file to the last fetch page from the site
    file_p.seek(0)
    data = json.load(file_p)
    data[search_title] = page_no
    delete_file_content(file_p)
    json.dump(data, file_p)


def load_article(file_p, search_title, current_page):
    # loads the articles on the file based on search tile
    end_page_no = 6  # fetch articles till page (end_page_no -1)
    cleaned_articles = []  # list of articles
    for (
        page
    ) in range(  # starting from page_no (last fetched page) to next remaning pages
        current_page + 1, end_page_no
    ):  # each page contains 10 articles so taking 3 pages in loop for 30 articles
        url = (
            "https://bg.annapurnapost.com/api/search?title="
            + search_title
            + "&page="
            + str(page)
        )
        response = requests.get(url)
        json_response = response.json()
        try:
            items = json_response["data"]["items"]
            for i, _ in enumerate(items):  # loop over the articles
                content = items[i]["content"]
                cleaned_article = cleanhtml(content)  # remove html tags
                cleaned_articles.append(
                    cleaned_article
                )  # append individual articles in a list
            add_page_index(file_p, search_title, page)  # update the page index
            print(f"Page {page} loaded")
        except KeyError:
            print("No more data availabel!!!")
    return cleaned_articles


search_title = "गुर"

if __name__ == "__main__":

    with open("article_index.json", "r+") as index_f:
        index_data = json.load(index_f)
        try:
            current_page = index_data[search_title]
            with open(f"{search_title}.json", "r+") as article_f:
                previous_articles = json.load(article_f, strict=False)
                new_articles = load_article(index_f, search_title, current_page)
                if new_articles == None:
                    print("some error occured")
                    new_articles = []
                previous_articles.extend(
                    new_articles
                )  # append previously loaded articles with newly fetched articles
                delete_file_content(article_f)
                json.dump(previous_articles, article_f)

        except (KeyError, FileNotFoundError):
            index_data.update({search_title: 0})
            current_page = index_data[search_title]
            delete_file_content(index_f)
            json.dump(index_data, index_f)
            with open(f"{search_title}.json", "w") as article_f:
                new_articles = load_article(index_f, search_title, current_page)
                try:
                    json.dump(new_articles, article_f)
                except:
                    print("Error Fetching Articles!!!")

print("\n--completed--")
