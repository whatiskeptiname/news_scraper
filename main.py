import requests
import json


search_title = "राम"
try:
    with open(f"{search_title}.json") as f:
        data = json.load(f)
except:
    data = {"page": 1, "items": []}

for page in range(
    data["page"], 4
):  # each page contains 10 articles in general condition
    url = (
        "https://bg.annapurnapost.com/api/search?title="
        + search_title
        + "&page="
        + str(page)
    )
    response = requests.get(url)
    items = response.json()["data"]["items"]
    data["items"].extend(items)
    with open(f"{search_title}.json", "w") as f:
        json.dump(data, f)
    data["page"] += 1  # update the page index
