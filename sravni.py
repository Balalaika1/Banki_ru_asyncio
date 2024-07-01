import requests
from datetime import datetime
import lxml

from bs4 import BeautifulSoup
import pandas as pd

current_datetime = datetime.now().strftime('%Y-%m-%d')
def sravni_excel():
    url = 'https://www.sravni.ru/zaimy/rating-mfo/?userRatingType=all'
    data = requests.get(url)
    data = data.text
    data

    soup = BeautifulSoup(data,'lxml')
    # Выгружаем только нужную нам таблицу
    base = soup.find('tbody')
    base

    # выгружаем компании с главной страницы
    companies = base.find_all('tr')


    table_names = {'position':[],'name':[],'main_rait':[],'review':[],'answer':[],'solved_problems':[]}
    for i in companies:
        # выгружаем позицию в рейтинге
        position = i.find('div', {'class':'_1h41p0x _1livb46'})
        table_names['position'].append(int(position.text))

        # выгружаем название компании
        name = i.find('span', {'class':'cell_name__jiGtV'})
        table_names['name'].append(name.text)

        # Рейтинг компании
        main_rait = i.find('span', {'class':'_e9qrci _1gyyr3m'})
        table_names['main_rait'].append(float(main_rait.text))

        # Отзывы
        review = i.find('td', {'class':'cell_cell--reviewsCount__4HQLJ'})
        table_names['review'].append(int(review.text))

        # Ответы
        answer = i.find('td', {'class':'cell_cell--responseCount__PcrpN'})
        table_names['answer'].append(int(answer.text))

        solved_problems = i.find('td', {'class':'cell_cell--solvedProblems__LUIt5'})
        table_names['solved_problems'].append(int(solved_problems.text))

    df = pd.DataFrame(table_names)
    df.to_excel(f'sravni_ru.xlsx')

    return df
