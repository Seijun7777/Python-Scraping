import requests
from bs4 import BeautifulSoup
import csv

# from selenium import webdriver
# import time


def get_data(url):
    req = requests.get(url)
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
    # with open('index.html', 'w', encoding='utf-8') as file:
    #     file.write(req.text)

    with open('index.html', encoding='utf-8') as file:
        src = file.read()

    soup = BeautifulSoup(src, 'lxml')

    title_list = []
    title_rank = soup.find('div', class_='sort-header first').text.strip()
    title = soup.find_all('div', class_='list-header')
    title_list.append(title_rank)
    for i in title:
        title_list.append(i.text.strip())
    with open('forbes_global2000.csv', 'w', encoding='utf-8') as file:
        writer_ = csv.writer(file, delimiter=';')
        writer_.writerow(title_list)

    info_title = soup.find('div', class_='grid-wrapper').find_all('div', class_='table')

    info_list = [[],[],[],[],[],[],[]]

    for i in info_title:
        info_blocks = i.find('div', class_='table-row-group').find_all('a')
        for j in info_blocks:
            rank = j.find('div', class_='rank first table-cell rank')
            org_name = j.find('div', class_='organizationName second table-cell name')
            country = j.find('div',class_='country table-cell country')
            revenue = j.find('div', class_='revenue')
            profits = j.find('div', class_='profits')
            assets = j.find('div', class_='assets')
            market_value = j.find('div', class_='marketValue')

            if rank == None or org_name == None or country == None or revenue == None or profits == None or assets == None or market_value == None:
                pass
            else:
                info_list[0].append(rank.text)
                info_list[1].append(org_name.text)
                info_list[2].append(country.text)
                info_list[3].append(revenue.text)
                info_list[4].append(profits.text)
                info_list[5].append(assets.text)
                info_list[6].append(market_value.text)

    for i in info_list:
        c = len(i)

    for i in range(c):
        with open('forbes_global2000.csv', 'a', encoding='utf-8') as file:
            writer_ = csv.writer(file, delimiter=';')
            writer_.writerow([info_list[0][i], info_list[1][i], info_list[2][i],info_list[3][i], info_list[4][i], info_list[5][i], info_list[6][i]])

def main():
    get_data(url='https://www.forbes.com/lists/global2000/')

if __name__=='__main__':
    main()