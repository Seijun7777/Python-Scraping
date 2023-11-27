import requests
from bs4 import BeautifulSoup
import json


def get_category_OLX(url):
    headers = {
        'cookie': 'deviceGUID=ea0866b2-fa45-4bdc-bb19-42bed5872d68; a_refresh_token=d31a95c51f76670320d4eaf22b2b7a8700f7b0a9; a_grant_type=device; observed_aui=5d1e83231b9147c0a3e81b1a507f6383; user_id=242404696; __user_id_P&S=242404696; user_uuid=; user_business_status=private; _gcl_au=1.1.2103742525.1699994017; tmr_lvid=86c34531356cc211e46c59fa2b2438c0; tmr_lvidTS=1699994019342; cookieBarSeenV2=true; cookieBarSeen=true; _ym_uid=1699994022601758214; _ym_d=1699994022; _hjSessionUser_2218932=eyJpZCI6IjRmNTBhODIxLWZhMTEtNTI1Yi05YjFkLTVmYmMyYjJhZGFiNCIsImNyZWF0ZWQiOjE2OTk5OTM5ODI2MjYsImV4aXN0aW5nIjp0cnVlfQ==; laquesisff=aut-1425#aut-388#buy-2279#decision-657#euonb-114#grw-124#oesx-1437#oesx-2630#oesx-2797#oesx-2798#oesx-2864#oesx-2926#oesx-645#oesx-867#srt-1289#srt-1346#srt-1434#srt-1593#srt-1758#srt-663; laquesissu=300@my_messages_sent|1#301@jobs_recommendations|1#303@jobs_preferences_click|0#303@jobs_save_preferred_position|0#303@jobs_select_preferred_time|0#303@jobs_select_preferred_contract|0#303@jobs_save_preferred_salary|0; __gsas=ID=04669bce3c078b31:T=1700741841:RT=1700741841:S=ALNI_MaxhefSB8eBjFik59Pg5lBQw8KKjw; cto_bundle=cWQCD19xNTR2V2hXZVVYYW0zZnVyMWo0SWRnJTJGWDBkJTJCMkxsbnNKcE1ZN0ZDQ2xyTEJHajVzZ1NtOEJFeGloV3FxNVRUVmpOeEswJTJGVWxoJTJGOUV3ME52bHU1UFZZQzZmJTJGRzFoOXFoUE02NGdMMm03Y2NDSHJxV2RuN1cydHl0TGhIZ0YydjElMkJRYiUyRjVZRUl5JTJGTThYdE0xbkk2ZXF3JTNEJTNE; session_start_date=1700856257562; _hjIncludedInSessionSample_2218932=0; _hjSession_2218932=eyJpZCI6ImYyODNiMWM5LWY4OWEtNDJhMi04YWMxLWM5MzEyZTM3MDYzMyIsImNyZWF0ZWQiOjE3MDA4NTQ0NTg2MjksImluU2FtcGxlIjpmYWxzZSwic2Vzc2lvbml6ZXJCZXRhRW5hYmxlZCI6ZmFsc2V9; _hjAbsoluteSessionInProgress=0; PHPSESSID=v8h1tc5v4qt1o5m8n76gfjt2l4; a_access_token=faea66819bc2e139bf3dc375e06d28c837422348; __gads=ID=9ccab57be6f737d4:T=1699994034:RT=1700854462:S=ALNI_Mb4nT_lotqJvFRMBrQkTr4HBBn8Og; __gpi=UID=00000cc3dc2357db:T=1699994034:RT=1700854462:S=ALNI_MZaLETshffo62UEyF3jVWq-SwFoUA; lqstatus=1700855798|18bfd4b9c4cx6f90e6bc|euads-4495||; laquesis=euads-4495@b#jobs-6294@a#jobs-6512@a#olxeu-41358@b#posting-1090@b; onap=18bcf892160x529213a8-7-18c02d3a8b2x5ae28eac-4-1700856278; _gid=GA1.2.1804211285.1700854478; _ga=GA1.1.248603824.1699994015; _ga_169GF37KZE=GS1.1.1700854482.7.0.1700854482.60.0.0; _ym_isad=2; _ym_visorc=w; tmr_detect=0%7C1700854487945',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'
    }

    request = requests.get(url, headers).text

    with open('index.html', 'w', encoding="utf8") as file:
        file.write(request)

    with open('index.html', encoding="utf8") as file:
        src = file.read()

    soup = BeautifulSoup(src, 'lxml')
    category_block = soup.find_all('a', class_='css-1gpccxq')

    category_dict = {}

    for i in category_block:
        category_name = i.find('span', class_='css-xu7uwr').text
        category_url = f"https://www.olx.uz{i.get('href')}"
        category_dict[category_name] = category_url

    with open('OLX_Category_URL.json', 'w', encoding='utf-8') as file:
        json.dump(category_dict, file, indent=4)


def get_info_OLX():

    with open('OLX_Category_URL.json') as file:
        category = json.load(file)

    for i, o in category.items():
        request = requests.get(o)

        soup = BeautifulSoup(request.text, 'lxml')

        page_num = soup.find_all('a', class_="css-1mi714g")[-1].text

        data_olx_list = []

        for n in range(1, int(page_num) + 1):
            req = requests.get(f'{o}?page={n}')

            soup_ = BeautifulSoup(req.text, 'lxml')

            blocks_ob = soup_.find_all('div', class_='css-1sw7q4x')[:-1]
            for b in blocks_ob:
                src_olx = f"{o[0:19]}{b.find('a', class_='css-rc5s2u').get('href')[1:]}"
                name_olx = b.find('h6', class_='css-16v5mdi er34gjf0').text
                price_olx = b.find('p', class_='css-10b0gli er34gjf0').text[:-3].strip('сумДоговор')
                data_olx = b.find('p', class_='css-veheph er34gjf0').text

                data_olx_list.append(
                    {
                        'Name': name_olx,
                        'Prie': price_olx.strip(),
                        'src': src_olx,
                        'Data': data_olx
                    }
                )

        with open(f'{i}_OLX.json', 'w', encoding='utf-8') as file:
            json.dump(data_olx_list, file, indent=4, ensure_ascii=False)

        print(f'>>> {i} - Finished!\n==========================')

    print('||||||||||||||||||||||\n>>> Process FINISHED!')

def main():
    get_category_OLX(url='https://www.olx.uz/')
    get_info_OLX()

if __name__ == '__main__':
    main()
