import re
import requests
from bs4 import BeautifulSoup
import pprint

# url = 'https://www.rbc.ru/newspaper/2019/12/26/5e035efb9a794779da6b5cc7'
url = 'https://www.rbc.ru/newspaper/2019/12/24/5dfca3dc9a7947a09a08fcd6'

response = requests.get(url)

# print(response.status_code)
#
url_soup = BeautifulSoup(response.text, 'html.parser')

# print(response.status_code)

# print(response.text)
text_data_dict = {
    url: {'text': '',
          'data': ''
          }
}

for element in url_soup.find_all('div', class_ = 'article__text'):
    for text in element.find_all('p'):
        # print(text)
        text_data_dict[url]['text'] += text.get_text()


for element in url_soup.find_all('span', class_ = 'article__header__date'):
    text_data_dict[url]['data'] = ' '.join(re.findall(r'\w+', element.get_text()))

text_data_dict[url]['text'] = text_data_dict[url]['text'].replace('\xa0', ' ')

pprint.pprint(text_data_dict)

# news_dict ={}
#
# for each_url in url_soup.find_all('a', class_ = 'item-realty_medium__link'):
#     if 'https' in str(each_url):
#         news_dict[' '.join(re.findall(r'\w+', each_url.get_text()))] = each_url.get('href')
# #
# pprint.pprint(news_dict)
#
