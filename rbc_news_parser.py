import requests
import pprint
from bs4 import BeautifulSoup
import re

print('Данный парсер выводит статьи из раздела Газеты сайта rbc.ru')


url = 'https://rbc.ru'

response = requests.get(url)

# print(response.status_code)
#
url_soup = BeautifulSoup(response.text, 'html.parser')

# print(response.status_code)

# print(response.text)



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
# pprint.pprint(newspapers_dict)

text_data_dict = {}

for each_url in newspapers_dict.values():
    text_data_dict[each_url] = {
        'title': '',
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
        text_data_dict[each_url]['data'] = ' '.join(re.findall(r'\w+', element.get_text()))[:-6]

    for element in each_url_soup.find_all('span', class_='js-slide-title'):
        text_data_dict[each_url]['title'] = ' '.join(re.findall(r'\w+', element.get_text()))

    text_data_dict[each_url]['text'] = text_data_dict[each_url]['text'].replace('\xa0', ' ')

data_list = []
print('Сейчас в разделе Газеты сайта rb.cru {} статей'.format(len(text_data_dict.keys())))
for each_key in text_data_dict.keys():
    if text_data_dict[each_key]['data'] not in data_list:
        data_list.append(text_data_dict[each_key]['data'])

unique_data_list = set(data_list)

print('Статьи публиковались: ')
for element in sorted(unique_data_list):
    print(f'{sorted(unique_data_list).index(element) + 1}. ', element)

data_choice = int(input('За какую дату вы хотели бы просмотреть список статей (введите номер)? '))

data_for_read = list(unique_data_list)[data_choice - 1]

print(f'Список статей за {data_for_read}:')

article_list = []

for each_key in text_data_dict.keys():
    if text_data_dict[each_key]['data'] == data_for_read:
        article_list.append(each_key)
        list_number = article_list.index(each_key)
        print (f'{list_number + 1}. ', text_data_dict[each_key]['title'], f'.')

article_for_read = int(input(f'Какую статью за {data_for_read} Вы хотели бы прочитать? '))

url_for_read = article_list[article_for_read - 1]

print('Ссылка на статью на сайте: ')
print(url_for_read)
print('Текст статьи: ')
pprint.pprint(text_data_dict[url_for_read]['text'])




