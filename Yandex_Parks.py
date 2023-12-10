import requests
from bs4 import BeautifulSoup
import json
import csv
# from selenium import webdriver
# import time
# from selenium.webdriver.common.by import By



headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
    }

def get_page_html(url):

    req = requests.get(url=url, headers=headers)
    with open('indexx.html', 'w', encoding='utf-8') as file:
        file.write(req.text)


    # If you wanna use << Selenium >>:
        # try:
        #     driver = webdriver.Chrome()
        #
        #     driver.get(url=url)
        #     time.sleep(3)
        #
        #     with open('indexx.html', 'w', encoding='utf-8') as file:
        #         file.write(driver.page_source)
        #
        # except Exception:
        #     print(Exception)
        # finally:
        #     driver.close()
        #     driver.quit()


def get_data():
    with open('indexx.html', encoding='utf-8') as file:
        src = file.read()

    soup = BeautifulSoup(src, 'lxml')

    card_blocks = soup.find_all('div', class_='accordion_accordion__7KkXQ')

    info_dict = {
        'name' : [],
        'location': [],
        'phone': []
    }

    for i in card_blocks:
        name_park = i.find('d', class_='body2').text
        location_park = i.find('p', class_="caption1 accordion_captionClass__2ul6r").text

        info_dict['name'].append(name_park)
        info_dict['location'].append(location_park)

    json_info = soup.find('script', {'type':"application/json"}).text.split('"phone":')

    for i in json_info[1:]:
        num = i.split('"')
        info_dict['phone'].append(num[1])

    for l in info_dict.values():
        n = len(l)

    info_matrix_list = []
    for k in info_dict.values():
        info_matrix_list.append(k)

    info_list = []
    for i in range(n):
        info_list.append(
            {
                'name': info_matrix_list[0][i],
                'location': info_matrix_list[1][i],
                'phone': info_matrix_list[2][i]
            }
        )

    with open('Yandex_Parks_Info.json', 'w', encoding='utf-8') as file:
        json.dump(info_list, file, indent=4, ensure_ascii=False)

    with open('Yandex_Parks_info.csv', 'w', encoding='utf-8', newline='') as file:
        writer_ = csv.writer(file, delimiter=';')
        writer_.writerow(['Name', 'Location', 'Phone'])

    for i in range(n):
        with open('Yandex_Parks_info.csv', 'a', encoding='cp1251', errors='replace', newline='') as file:
            writer = csv.writer(file, delimiter=';')
            writer.writerow([info_matrix_list[0][i], info_matrix_list[1][i], info_matrix_list[2][i]])

def main():
    get_page_html(url='https://pro.yandex.ru/ru-ru/sankt-peterburg/knowledge-base/taxi/common/parks')
    get_data()

if __name__ == '__main__':
    main()
