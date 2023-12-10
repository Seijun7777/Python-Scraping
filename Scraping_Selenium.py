from bs4 import BeautifulSoup
from selenium import webdriver
import time
import json


def get_data_UZUM(url):
    result_product_list = []
    try:
        for i in range(1, 209):

            driver = webdriver.Chrome()

            # If necessary, open the site tab in full screen:
            # driver.maximize_window()

            driver.get(url=f'{url}?currentPage={i}')
            time.sleep(1)
            soup = BeautifulSoup(driver.page_source, 'lxml')
            product_blocks = soup.find_all('div', class_='col-mbs-12 col-mbm-6 col-xs-4 col-md-3')

            for item in product_blocks:
                product_name = item.find('div', class_='subtitle slightly regular small-semi-bold').find('a').text.strip()
                product_link = 'https://uzum.uz/ru' + item.find('div', class_='subtitle slightly regular small-semi-bold').find('a').get('href').strip()

                try:
                    product_price = item.find('div', class_='product-card-main-info-wrapper').find('span', class_='currency product-card-old-price regular').text.strip()
                except Exception:
                    product_price = item.find('div', class_='product-card-main-info-wrapper').text.strip()

                product_png = item.find('div', class_='image-wrapper').find('img').get('src')
                try:
                    product_assessments = item.find('span', class_='hidden-mbs visible-mbl raiting-wrapper').text.strip()
                except Exception:
                    product_assessments = None
                result_product_list.append(
                    {
                        'Name': product_name,
                        'Price': product_price,
                        'PNG': product_png,
                        'url': product_link,
                        'Assessments': product_assessments
                    }
                )

    except Exception:
        print(Exception)

    finally:
        driver.close()
        driver.quit()

    with open(f'Uzum_Products_{url.split("/")[-1][:-6]}.json', 'w', encoding='utf-8') as file:
        json.dump(result_product_list, file, indent=4, ensure_ascii=False)

    print('-' * 20+'\n>>> Process Finished!')


def main():
    get_data_UZUM(url='https://uzum.uz/ru/category/elektronika-10020')

if __name__ == '__main__':
    main()
