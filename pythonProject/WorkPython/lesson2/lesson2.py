import requests
from bs4 import BeautifulSoup
import lxml
import json

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',

}
count = 1

fests_urls_list = []

for i in range(0, 241, 24):
    url1 = f'https://www.skiddle.com/festivals/search/?ajaxing=1&sort=0&fest_name=&from_date=&to_date=&maxprice=500&o={i}&bannertitle=May'

    req = requests.get(url=url1, headers=headers)
    json_data = json.loads(req.text)
    html_response = json_data['html']

    with open(f"data/index_{i}.html", 'w', encoding='utf-8') as file:
        file.write(html_response)

    with open(f"data/index_{i}.html", encoding='utf-8') as file:
        src = file.read()

    soup = BeautifulSoup(src, 'lxml')

    cards = soup.find_all('a', class_='card-details-link')

    for item in cards:
        fest_url = 'https://www.skiddle.com' + item.get('href')
        fests_urls_list.append(fest_url)

fest_result_list =[]

for url in fests_urls_list:
    req = requests.get(url=url, headers=headers)

    soup = BeautifulSoup(req.text, "lxml")

    print("__________________________________________________")
    print(count)
    print(url)
    try:
        # контейнер с не всеми нужными
        fest_info_block = soup.find("div", class_="MuiGrid-root MuiGrid-container MuiGrid-spacing-xs-2 css-1ik2gjq")
        fest_info_list = fest_info_block.find_all(class_="MuiGrid-root MuiGrid-item MuiGrid-grid-xs-12 css-2re0kq")

        # название ивента
        fest_name_block = soup.find("div", class_="MuiContainer-root MuiContainer-maxWidthFalse css-1krljt2")
        fest_name = fest_name_block.find("h1").text

        # дата ивента
        fest_data = fest_info_list[0].find(class_="MuiGrid-root MuiGrid-container css-f3i3nk").find(class_="MuiGrid-root MuiGrid-item MuiGrid-grid-xs-11 css-twt0ol").find_all("span")
        fest_data[0].append(fest_data[1])
        # адрес ивента
        fest_location = fest_info_list[1].find(class_="MuiGrid-root MuiGrid-item MuiGrid-grid-xs-11 css-twt0ol").find("span").text

            # цена Ивента
        if len(fest_info_list) == 3:

            fest_price = fest_info_list[2].find(class_="MuiGrid-root MuiGrid-item MuiGrid-grid-xs-11 css-twt0ol").find("span").text
        elif len(fest_info_list) < 3:
            fest_price = "No information"


        fest_result_list.append(
            {
                "Count": count,
                "Link": url,
                "Fest name": fest_name,
                "Fest date": fest_data[0].text,
                "Fest location": fest_location,
                "Fest price": fest_price,
            }
        )
    except AttributeError:
        fest_result_list.append({
            "Count": count,
            "!": "Error"
        })
    count += 1

with open("fest_result_list.json", "a", encoding="utf-8") as file:
    json.dump(fest_result_list, file, indent=4, ensure_ascii=False)

