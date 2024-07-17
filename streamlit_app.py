import re
from datetime import datetime
import asyncio
import aiohttp
from bs4 import BeautifulSoup
import pandas as pd
import streamlit as st

from sravni import sravni_excel  # Убедитесь, что этот модуль существует и доступен

table_names = {'company_name':[],'main_rait':[],'position':[],'review':[],'answer':[],'positive_reviews':[],'negative_reviews':[],'fast_issuance':[],'good_employee':[],'transparent_conditions':[],'convenience_application':[],'date':[]}

current_datetime = datetime.now().strftime('%Y-%m-%d')

st.markdown('<h2>Рейтинг МФО на сайтах Banki.ru и Sravni.ru</h2>', unsafe_allow_html=True)
my_bar = st.progress(0)
progress_text = "Коллега, возможно тебе покажется, что сайт долго обновляется, но просто подожди! 😉"

def extract_digits(s):  # Функция, убирает из строки все кроме цифр и точки
    return re.sub(r'[^\d.]', '', s)

async def fetch(session, url):
    async with session.get(url) as response:
        site = await response.text()
        print(response.status)
        if response.status != 200:
            await asyncio.sleep(2)
            async with session.get(url) as response:  # Повторный запрос при ошибке статуса
                print(f'TWO ------ {response.status}')
                site = await response.text()
        
        site = BeautifulSoup(site, 'lxml')

        #Поиск всех div в class которых есть 'CompanyHeadstyled' 
        try:
            company_name = site.select('div[class*=CompanyHeadstyled]')[-1].text.replace('Отзывы клиентов МФО ', '')
        except:
            company_name = "Нет данных"

        #Поиск всех div в class которых есть 'RatingsBadgestyled' 
        try:
            main_rait = float(site.select('div[class*=RatingsBadgestyled]')[1].text)
        except:
            main_rait = "Нет данных"

        try:
            position = int(extract_digits(site.find_all(class_='Text__sc-vycpdy-0 jZylFz')[0].text))
        except:
            position = "Нет данных"

        try:
            review = int(extract_digits(site.find_all(class_='Text__sc-vycpdy-0 jZylFz')[1].text))
        except:
            review = "Нет данных"

        try:
            answer = int(extract_digits(site.find_all(class_='Text__sc-vycpdy-0 jZylFz')[2].text))
        except:
            answer = "Нет данных"

        try:
            positive_reviews = float(extract_digits(site.find_all(class_='Text__sc-vycpdy-0 gMyhnj')[0].text))
        except:
            positive_reviews = "Нет данных"

        try:
            negative_reviews = float(extract_digits(site.find_all(class_='Text__sc-vycpdy-0 eVmhAG')[0].text))
        except:
            negative_reviews = "Нет данных"

        try:
            fast_issuance = float(extract_digits(site.find_all(class_='Text__sc-vycpdy-0 ceYcWs')[0].text))
        except:
            fast_issuance = "Нет данных"

        try:
            good_employee = float(extract_digits(site.find_all(class_='Text__sc-vycpdy-0 ceYcWs')[1].text))
        except:
            good_employee = "Нет данных"

        try:
            transparent_conditions = float(extract_digits(site.find_all(class_='Text__sc-vycpdy-0 ceYcWs')[2].text))
        except:
            transparent_conditions = "Нет данных"

        try:
            convenience_application = float(extract_digits(site.find_all(class_='Text__sc-vycpdy-0 ceYcWs')[3].text))
        except:
            convenience_application = "Нет данных"

        date_n = datetime.now()

        return (company_name, main_rait, position, review, answer, positive_reviews, negative_reviews, fast_issuance, good_employee, transparent_conditions, convenience_application, date_n)

async def main():
    companies = ['ekapusta', 'moneyman', 'zaymer', 'webbankir', 'carmoney', 'bistrodengi', 
                 'lime_zaim', 'kvatro', 'boostra', 'revotekhnologii', 'medium_score', 
                 'zaymigo', 'dengi_srazu', 'cashdrive', 'turbozajm', 'joymoney', 
                 'privsosed', 'centrofinans', 'oneclickmoney', 'migkredit', 'maxcredit', 
                 'cash_u', 'sammit', 'pliskov', 'bystrozaym', 'moneza', 'umnye_nalichnye', 
                 'smsfinance', 'creditter', 'svoi_ludi', 'otlichnye_nalichnye', 'budgett', 
                 'krediska', 'paylate', 'kangaria', 'payps', 'microdengi', '495credit', 
                 'kredito24', 'ezaem', 'konga', 'mobicredit', 'belkacredit', 'beriberu', 
                 'strana_express', 'denga', 'fastmoney', 'vivus', 'caranga', 'otp_finance', 
                 'celfin', 'grinmani', 'dengi_na_dom', 'micro_klad', 'zaimy_rf', 
                 'creditstar', 'chestnoye_slovo', 'alizaim', 'rosdengi', 'uralsibfinance', 
                 'knopkadengi', 'erck', 'vsegdazaem', 'finterra', 'finmoll', 'vivadengi', 
                 'creditplus', 'webzaim', 'zaim_express', 'kupi_ne_kopi', 'air_loanse', 
                 'a_dengi', 'fin5', 'srochno_dengi', 'do_zarplati', 'ykky', 'moneyfaktura', 
                 'daem_zaem', 'credit_smile', 'ren_express', 'express_dengi', 
                 'buro_zaimov', 'sovazaem', 'platiza', 'express_zaimy', 'fast-finance', 
                 'galiciya']
    base_url = 'https://www.banki.ru/microloans/responses/companies/'

    timeout = aiohttp.ClientTimeout(total=60)  # Общий таймаут 60 секунд
    async with aiohttp.ClientSession(timeout=timeout) as session:
        tasks = [fetch(session, base_url + company) for company in companies]
        results = await asyncio.gather(*tasks)

        # Сохранение результатов в структуру данных
        for result in results:
            (company_name, main_rait, position, review, answer, positive_reviews, 
             negative_reviews, fast_issuance, good_employee, transparent_conditions, 
             convenience_application, date_n) = result

            table_names['company_name'].append(company_name)
            table_names['main_rait'].append(main_rait)
            table_names['position'].append(position)
            table_names['review'].append(review)
            table_names['answer'].append(answer)
            table_names['positive_reviews'].append(positive_reviews)
            table_names['negative_reviews'].append(negative_reviews)
            table_names['fast_issuance'].append(fast_issuance)
            table_names['good_employee'].append(good_employee)
            table_names['transparent_conditions'].append(transparent_conditions)
            table_names['convenience_application'].append(convenience_application)
            table_names['date'].append(date_n)

    df_result = pd.DataFrame(table_names)
    df_result.to_excel('banki_ru.xlsx', index=False)
    st.dataframe(df_result)
    with open("banki_ru.xlsx", "rb") as file:
        st.download_button(
            label="Download excel banki.ru",
            data=file,
            file_name="banki_ru.xlsx"
        )

if st.button('Banki.ru'):
    asyncio.run(main())

if st.button('Sravni.ru'):
    df2 = sravni_excel()
    st.dataframe(df2)
    with open("sravni_ru.xlsx", "rb") as file:
        st.download_button(
            label="Download excel sravni.ru",
            data=file,
            file_name="sravni_ru.xlsx"
        )
