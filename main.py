import json
from bs4 import BeautifulSoup
import requests
import pandas as pd
import DBConnector

req_headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'en-US,en;q=0.8',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/93.0.4577.82 Safari/537.36 '
}

# To do -- input of state
state = '/homes/knoxville_rb'

url = 'https://www.zillow.com' + state

page = requests.get(url, headers=req_headers)

soup = BeautifulSoup(page.content, 'html.parser')

next_page = soup.find_all('a',
                         class_="StyledButton-c11n-8-37-0__wpcbcc-0 cyhUbV PaginationButton-c11n-8-37-0__si2hz6-0 "
                                "eIcuqd")

new_url = url.replace(state, next_page[len(next_page) - 1]["href"])

# -- if there is a next page = next_page[len(nextPage) - 1]['disable tabindex']


lat = []
long = []
links = []
formatted_prices = []
formatted_address = []
formatted_links = []
house_info = []


def get_json_data():
    json_data = soup.find_all('script', type='application/ld+json')
    x = 0
    # used while loop because list needs to be indexed by an integer
    while x < len(json_data):
        try:
            lat.append(json.loads(json_data[x].text)['geo']['latitude'])
            long.append(json.loads(json_data[x].text)['geo']['longitude'])
            links.append(json.loads(json_data[x].text)['url'])
        except KeyError:
            print("Coordinates not found")
        x += 1


def get_html_data():
    prices = []
    addresses = []
    for _ in soup:
        prices = soup.find_all(class_="list-card-price")
        addresses = soup.find_all(class_="list-card-addr")

    for price in prices:
        formatted_prices.append(price.text)

    for address in addresses:
        formatted_address.append(address.text)


def format_house_info():
    i = 0
    while i < len(formatted_prices):
        house_info.append([formatted_address[i], formatted_prices[i], lat[i], long[i], links[i]])
        i += 1


def update_house_info_csv():
    columns_name = ['Addresses', 'Prices', 'Latitude', 'Longitude', 'Link']
    house_info_dataset = pd.DataFrame(columns=columns_name, data=house_info)
    house_info_dataset.to_csv('house_info_dataset.csv', index=False)


def data_to_db():
    i = 0
    while i < len(house_info):
        try:
            DBConnector.cur.execute("INSERT INTO public.\"House_Data\" (address, price, lat, long, "
                                    "link) values (%s,%s,%s,%s,%s);", (formatted_address[i], formatted_prices[i], lat[i],
                                                                       long[i], links[i]))
        except Exception:
            print("Already stored in database")
        i += 1

    DBConnector.conn.commit()
    DBConnector.cur.execute("SELECT * FROM public.\"House_Data\";")
    rows = DBConnector.cur.fetchall()
    for r in rows:
        print(r)
    DBConnector.cur.close()
    DBConnector.conn.close()


if __name__ == "__main__":
    print('Start of scraping')
    get_json_data()
    get_html_data()
    format_house_info()
    update_house_info_csv()
    print('Finished scraping')
    print('Data saved')
    data_to_db()
