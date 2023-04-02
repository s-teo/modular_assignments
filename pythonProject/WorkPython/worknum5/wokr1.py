import requests
from bs4 import BeautifulSoup
import csv
import json

headers = {
    "Accept": "image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36"
}
# url = "http://thrones-online.com/"
#
# req = requests.get(url=url, headers=headers)
# src = req.text
# soup = BeautifulSoup(src, "lxml")
#
# with open("index.html", "w", encoding="utf-8") as file:
#     file.write(src)

with open("index.html", encoding="utf-8") as file:
    src = file.read()

soup = BeautifulSoup(src, "lxml")

count_season = soup.find("div", class_="alltable").find_all("div", class_="cell")
cs = len(count_season)

all_season_block = soup.find("div", class_="alltable").find_all("div", class_="cell")
all_season_list = {}
for item in all_season_block:
    season_href = item.find("a")
    for i in season_href:
        season_name = season_href.find("img").get("alt")
        season_url = "http://thrones-online.com/" + season_href.get("href")
#         all_season_list[season_name] = season_url
#
# print(all_season_list)
# with open("all_season_list.json", "w", encoding="utf-8") as file:
#     json.dump(all_season_list, file, indent=4, ensure_ascii=False)

with open("all_season_list.json", encoding="utf-8") as file:
    all_season = json.load(file)
serial_info = []
iteration_count = int(len(all_season))
count = 1
for season_count, season_url in all_season.items():
    req = requests.get(url=season_url, headers=headers)
    src = req.text

    with open(f"data/{count}. {season_count}.html", "w", encoding="utf-8") as file:
        file.write(src)

    with open(f"data/{count}. {season_count}.html", encoding="utf-8") as file:
        src = file.read()

    soup = BeautifulSoup(src, 'lxml')

    all_series = soup.find_all("div", class_="anonse")

    for item in all_series:
        all_series_info = item.findNext("h2").text

        season = all_series_info[0:7]
        series = all_series_info[8:17]
        series_name = all_series_info[17:50]

        serial_info.append(
            {
                "Сезон": season,
                "Серия": series,
                "Название серии": series_name
            }
        )
print(serial_info)
with open("serial_info.json", "w", encoding="utf-8") as file:
    json.dump(serial_info, file, indent=4, ensure_ascii=False)







