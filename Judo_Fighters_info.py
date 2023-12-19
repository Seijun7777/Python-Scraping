import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import time
import csv


headers = {
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}
def get_data(url):
    info_list = []

    # req = requests.get(url=url, headers=headers)
    # try:
    #     driver = webdriver.Chrome()
    #
    #     driver.get(url=url)
    #     time.sleep(3)
    #
    #     with open('index__.html', 'w', encoding='utf-8') as file:
    #         file.write(driver.page_source)
    #
    # except Exception:
    #     print(Exception)
    # finally:
    #     driver.close()
    #     driver.quit()
    with open('index__.html', encoding='utf-8') as file:
        src = file.read()
    soup = BeautifulSoup(src, 'lxml')

    nation = soup.find('div', class_='page-content').find('select').find_all('option')

    url_list = []
    for i in nation[1:]:
        nations = i.get('value')
        reqs = requests.get(f'{url}?name=&nation={nations}&gender=both&category=sen')
        soup = BeautifulSoup(reqs.text, 'lxml')
        url_persons = soup.find('div', class_='results container-narrow').find_all('a')
        for i in url_persons:
            urls = i.get('href')
            url_list.append('https://www.ijf.org' + urls)


    for i in url_list:
            reqss = requests.get(i, headers=headers).text
            soup2 = BeautifulSoup(reqss, 'lxml')

            try:
                mainly = soup2.find('div', class_='athlete-title-hero').text.split(' ')
                name_1 = soup2.find('div', class_='athlete-title-hero').text.split(' ')[24].strip()
                name_2 = soup2.find('div', class_='athlete-title-hero').text.split(' ')[25].strip('\n')

                country = soup2.find('div', class_='athlete-title-hero').text.split(' ')

                if country[77] == '':
                    country = country[78].strip()
                else:
                    country = country[77].strip()

                age = soup2.find('div', class_='age-info').text.split(' ')[29]
                if mainly[26] == '':
                    pass
                else:
                    name_3 = soup2.find('div', class_='athlete-title-hero').text.split(' ')[26].strip()
                    # print(name_3)
                kg = soup2.find('div', class_='kg').text.strip()

                if mainly[26] == '':
                    name = name_1 + ' ' + name_2
                else:
                    name = name_1 + ' ' + name_2 + ' ' + name_3

            except Exception:
                age = None
                kg = None
                country = None
                name = None

                print(Exception)
            info_list.append([country, name, age, kg])
    with open('data_judoka.csv', 'w', encoding='utf-8') as file:
                write = csv.writer(file, delimiter=';')
                write.writerow(['Country', 'Name', 'Age', 'Weight'])
    for i in info_list:
                with open('data_judoka.csv', 'a', encoding='utf-8') as file:
                    write = csv.writer(file, delimiter=';')
                    write.writerow(i)


def main():
    get_data(url='https://www.ijf.org/judoka')

if __name__=='__main__':
    main()