import requests
from bs4 import BeautifulSoup
import csv


def get_data(url):
    # for exemple this url adress
    #
    # url = 'https://github.com/trending'

    requests = requests.get(url)
    src = requests.text

    with open('index_.html', 'w', encoding="utf-8") as file:
        file.write(src)


    with open('index_.html') as file:
        html_site = file.read()

    soup = BeautifulSoup(html_site, 'lxml')


    repos = soup.find_all('article', class_='Box-row')
    for i in repos:
        repos_name = i.find('h2', class_='h3').find('a').get('href').strip('/')
        repos_link = 'https://github.com/trending/' + repos_name

        repos_stars = i.find('a', class_="Link Link--muted d-inline-block mr-3").text.strip()
        repos_dev = i.find('img', class_='avatar mb-1 avatar-user').get('alt')



        # Repos_Name = 'Repos Name'
        # Repos_Link = 'Repos Link'
        # Devoloper = 'Developer'
        # Number = 'Number of Starars'
        # with open('git_hub_respos.csv', 'w',newline='') as file:
        #     writer = csv.writer(file)
        #     writer.writerow(
        #     [Repos_Name, Repos_Link, Devoloper, Number]
        # )


        with open('git_hub_respos.csv', 'a') as file:
            writer = csv.writer(file)
            writer.writerow(
            (
                repos_name,
                repos_link,
                repos_dev,
                repos_stars
            )
        )

def main():
    get_data(url='https://github.com/trending')


if __name__ == '__scrapping_github_tranding_repos__':
    main()