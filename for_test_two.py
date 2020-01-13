import re
import requests
from bs4 import BeautifulSoup
import pprint

url = 'https://realty.rbc.ru/?utm_source=topline'

response = requests.get(url)

# print(response.status_code)
#
url_soup = BeautifulSoup(response.text, 'html.parser')

# print(response.status_code)

# print(response.text)


news_dict ={}
#
for each_url in url_soup.find_all('a', class_ = 'item-realty_medium__link'):
    if 'https' in str(each_url):
        news_dict[' '.join(re.findall(r'\w+', each_url.get_text()))] = each_url.get('href')
#
pprint.pprint(news_dict)


