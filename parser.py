import requests
import logging
from bs4 import BeautifulSoup

logging.basicConfig(level=logging.DEBUG)

r = requests.get('https://www.formula1.com/en/results.html/2023/races/1141/bahrain/race-result.html')
soup = BeautifulSoup(r.text, 'lxml')
results = soup.find('div', {'class': 'resultsarchive-wrapper'}).prettify()

table_of_results = soup.find('table', {'class': 'resultsarchive-table'})

dict_of_res = dict()


for row in table_of_results.find_all('tr'):
    driver = []
    for data in row.find_all('td'):
        if not data.text.isspace() and not 'limiter' in data.attrs['class']:
            driver.append(data.text.strip())

    if driver:
        position, number, name, constructor, laps, time, points = [el.replace('\n', ' ') for el in driver]
        row_data = {
            'number': position,
            'name': name,
            'constructor': constructor,
            'laps': laps,
            'time': time,
            'points': points,
        }

        dict_of_res[position] = row_data


print(dict_of_res)
