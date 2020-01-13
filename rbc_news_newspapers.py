import re
import requests
from bs4 import BeautifulSoup
import pprint

url = 'https://www.rbc.ru/newspaper/?utm_source=topline'

response = requests.get(url)

# print(response.status_code)
#
url_soup = BeautifulSoup(response.text, 'html.parser')

# print(response.status_code)

# print(response.text)


newspapers_dict ={

}
#
for each_url in url_soup.find_all('a', class_ = 'newspaper-page__news'):
    if 'https' and 'newspaper' in str(each_url):
        newspapers_dict[' '.join(re.findall(r'\w+', each_url.get_text()))]  = each_url.get('href')
#
#pprint.pprint(newspapers_dict)

text_data_dict = {}

for each_url in newspapers_dict.values():
    text_data_dict[each_url] = {
        'text': '',
        'data': ''
                  }


for each_url in newspapers_dict.values():

    response_each_url = requests.get(each_url)

    each_url_soup = BeautifulSoup(response_each_url.text, 'html.parser')


    for element in each_url_soup.find_all('div', class_='article__text'):
        for text in element.find_all('p'):
            text_data_dict[each_url]['text'] += text.get_text()

    for element in each_url_soup.find_all('span', class_='article__header__date'):
        text_data_dict[each_url]['data'] = ' '.join(re.findall(r'\w+', element.get_text()))

    text_data_dict[each_url]['text'] = text_data_dict[each_url]['text'].replace('\xa0', ' ')

pprint.pprint(text_data_dict)