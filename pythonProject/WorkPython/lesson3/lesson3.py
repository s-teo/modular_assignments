import time
import json
import requests
from bs4 import BeautifulSoup
import lxml
import datetime
import csv

start_time = time.time()

def get_data():
    cur_time = datetime.datetime.now().strftime("%d_%m_%Y_%H_%M")

    with open(f"labirint_{cur_time}.csv", "w", encoding="utf-8") as file:
        writer = csv.writer(file)

        writer.writerow(
            (
                "Название книги",
                "Автор",
                "Издательство",
                "Цена со скидкой",
                "Цена без скидки",
                "Процент скидки",
                "Статус наличия"
            )
        )

    headers = {
        "accept": "image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36",
    }

    url = "https://www.labirint.ru/genres/2308/"

    response = requests.get(url=url, headers=headers)
    soup = BeautifulSoup(response.text, "lxml")

    pages_count = int(soup.find("div", class_="pagination-numbers").find_all("a")[-1].text)

    books_data = []
    for page in range(1, pages_count + 1):
        url = f"https://www.labirint.ru/genres/2308/?display=table&page={page}"

        response = requests.get(url=url, headers=headers)
        soup = BeautifulSoup(response.text, "lxml")

        books_items = soup.find("tbody", class_="products-table__body").find_all("tr")

        for bi in books_items:
            book_data = bi.find_all("td")

            try:
                book_title = book_data[0].find("a").text.strip()
            except:
                book_title = "Название не указано"

            try:
                book_author = book_data[1].text.strip()
            except:
                book_author = "Автор не указан"

            try:
                # book_publishing = book_data[2].text
                book_publishing = book_data[2].find_all("a")
                book_publishing = ":".join([bp.text for bp in book_publishing])
            except:
                book_publishing = "Издатель не указан"

            try:
                book_new_price = int(book_data[3].find("div", class_="price").find("span").find("span").text.strip().replace(" ", ""))
            except:
                book_new_price = "Цена со скидко не указана"

            try:
                book_old_price = int(book_data[3].find("span", class_="price-gray").text.strip().replace(" ", ""))
            except:
                book_old_price = "Цена без скидки не указана"

            try:
                book_sale = round(((book_old_price - book_new_price) / book_old_price) * 100)
            except:
                book_sale = "Нет скидки"

            try:
                book_status = book_data[-1].text.strip()
            except:
                book_status = "Статус не указан"

            # print(book_title)
            # print(book_author)
            # print(book_publishing)
            # print(book_new_price)
            # print(book_old_price)
            # print(book_sale)
            # print(book_status)
            # print("#" * 10)

            books_data.append(
                {
                    "Название": book_title,
                    "Автор": book_author,
                    "Издательство": book_publishing,
                    "Цена со скидкой": book_new_price,
                    "Цена без скидки": book_old_price,
                    "Процент скидки": book_sale,
                    "Статус": book_status
                }
            )

            with open(f"labirint_{cur_time}.csv", "a", encoding="utf-8") as file:
                writer = csv.writer(file)

                writer.writerow(
                    (
                        book_title,
                        book_author,
                        book_publishing,
                        book_new_price,
                        book_old_price,
                        book_sale,
                        book_status
                    )
                )

        print(f"Обработана {page}/{pages_count}")
        time.sleep(1)

    with open(f"labirint_{cur_time}.json", "w", encoding="utf-8") as file:
        json.dump(books_data, file, indent=4, ensure_ascii=False)

def main():
    get_data()
    finish_time = time.time() - start_time
    print(f"На работу кода ушло: {finish_time}")

if __name__ == '__main__':
    main()
