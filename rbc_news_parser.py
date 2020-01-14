import requests
import pprint
from bs4 import BeautifulSoup
import re

# выводим информационное сообщени о функционале программы
print('Данный парсер выводит статьи из раздела Газеты сайта rbc.ru')
print('Идет загрузка статей...')

# задаем путь к разделу Газеты сайта rbc.ru
url = 'https://www.rbc.ru/newspaper/?utm_source=topline'

# передаем в request путь и получаем в ответ содержимое сайта
response = requests.get(url)

# создаем экземпляр BeautifulSoup, передаем ему содержимое сайта
url_soup = BeautifulSoup(response.text, 'html.parser')

# создаем пустой словарь для хранения ссылок на статьи в разделе Газеты сайта rbc.ru
newspapers_dict ={

}

# заполняем словарь ссылками, ища все ссылки, которые содержат подстроку http и newspaper
for each_url in url_soup.find_all('a', class_ = 'newspaper-page__news'):
    if 'https' and 'newspaper' in str(each_url):
        newspapers_dict[' '.join(re.findall(r'\w+', each_url.get_text()))]  = each_url.get('href')

# создаем словарь для хранения ссылки на статью и вложенного словаря
#  для хранения заголовка статьи, текста статьи, даты публикации статьи
text_data_dict = {}

# заполняем словарь ссылками на статью
for each_url in newspapers_dict.values():
    text_data_dict[each_url] = {
        'title': '',
        'text': '',
        'data': ''
                  }

# в цикле
for each_url in newspapers_dict.values():

    # для каждой ссылки из словаря создаем экземпляр BeautifulSoup
    response_each_url = requests.get(each_url)
    each_url_soup = BeautifulSoup(response_each_url.text, 'html.parser')

    # для каждой ссылки заполняем словарь текстом статьи
    for element in each_url_soup.find_all('div', class_='article__content'):
        for text in element.find_all('p'):
            text_data_dict[each_url]['text'] += text.get_text()

    # для каждой ссылки заполняем словарь датой публикации статьи
    # [:-6] - в дате "отрезаем" часы и минуты
    for element in each_url_soup.find_all('span', class_='article__header__date'):
        text_data_dict[each_url]['data'] = ' '.join(re.findall(r'\w+', element.get_text()))[:-6]

    # для каждой ссылки заполняем словарь заголовком статьи
    for element in each_url_soup.find_all('span', class_='js-slide-title'):
        text_data_dict[each_url]['title'] = ' '.join(re.findall(r'\w+', element.get_text()))

    # из-за особенности rbc.ru (перед каждым символом "-" при парсинге) заменяем "\xa0" на пробел
    text_data_dict[each_url]['text'] = text_data_dict[each_url]['text'].replace('\xa0', ' ')

# создаем список для хранения дат публикаций всех статей
# список нужен исключительно для того, что позволяет обратиться к своим элементам по индексу
# в словаре такого функционала не нашел
data_list = []

# выводим информационное сообщение об общем кол-ве статье в разделе Газеты сайта rbc.ru
print('Сейчас в разделе Газеты сайта rb.cru {} статей'.format(len(text_data_dict.keys())))

# в цикле заполняем список датами публикации всех статей
for each_key in text_data_dict.keys():
    if text_data_dict[each_key]['data'] not in data_list:
        data_list.append(text_data_dict[each_key]['data'])

# создаем уникальный список из дат публикации статей
unique_data_list = set(data_list)

# выводим уникальный список дат публикации статей в терминал
print('Статьи публиковались: ')
for element in sorted(unique_data_list):
    print(f'{sorted(unique_data_list).index(element) + 1}. ', element)

# спрашиваем за какую дату, пользователь хотел бы прочитать статьи
data_choice = int(input('За какую дату вы хотели бы просмотреть список статей (введите номер)? '))

# формируем индекс (по дате публикации выбранной пользователем)
# для вывода списка статей по выбранной дате
data_for_read = sorted(list(unique_data_list))[data_choice-1]

# выводим в терминал список статей, опубликованных по выбранной дате
print(f'Список статей за {data_for_read}:')

# создаем список для хранения заголовков статей за выбранную дату
article_list = []

# заполняем список заголовками статей за выбранную дату
for each_key in text_data_dict.keys():
    if text_data_dict[each_key]['data'] == data_for_read:
        article_list.append(each_key)
        list_number = article_list.index(each_key)
        print (f'{list_number + 1}. ', text_data_dict[each_key]['title'], f'.')

# выводим в терминал сообщение о запросе статьи, которую пользователь хотел бы прочитать
# за выбранную дату
article_for_read = int(input(f'Какую статью за {data_for_read} Вы хотели бы прочитать? '))

# формируем индекс (по дате публикации выбранной пользователем)
# для вывода текста статьи по выбранной дате
url_for_read = article_list[article_for_read - 1]

# выводим в терминал ссылку на статью и ее текст
print('Ссылка на статью на сайте: ')
print(url_for_read)
print('Текст статьи: ')
pprint.pprint(text_data_dict[url_for_read]['text'])
