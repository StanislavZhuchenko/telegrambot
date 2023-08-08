import requests
import logging
from bs4 import BeautifulSoup
import datetime

logging.basicConfig(level=logging.DEBUG)


def find_all_races_of_year(year=datetime.date.today().year):
    current_year = datetime.date.today().year
    if 1950 <= int(year) <= current_year:
        response = requests.get(f'https://www.formula1.com/en/results.html/{year}/races.html')  # Link to all races
        soup = BeautifulSoup(response.text, 'lxml')
        div_with_results = soup.select('div.resultsarchive-filter-wrap:nth-of-type(3)')
        all_races = dict()
        for element in div_with_results:
            a_with_results = element.select('a')
            for a_attrs in a_with_results:
                all_races[a_attrs.text.strip()] = 'https://www.formula1.com' + a_attrs.attrs['href']
        return all_races
    else:
        return None

# print('find_all_races_of_year', find_all_races_of_year())

def summary_results_of_year(year=datetime.date.today().year):

    response = requests.get(f'https://www.formula1.com/en/results.html/{year}/races.html')

    soup = BeautifulSoup(response.text, 'lxml')
    table_results = soup.select_one('.resultsarchive-table').select_one('tbody').find_all('tr')
    race_results = dict()
    for row in table_results:
        res = row.text.split('\n')
        res1 = [el for el in res if len(el) != 0 and not el.isspace()]
        race, date, name, surname, abbr, constructor, laps, full_time = [data.strip() for data in res1]
        row_res = {'date': date, 'name': name, 'surname': surname, 'abbr': abbr,
                   'constructor': constructor, 'laps': laps, 'full_time': full_time}
        race_results[race] = row_res
    return race_results


def formatted_summary_of_year(results):
    string_of_data = 'GRAND PRIX, WINNER, CAR\n'
    for data in results:
        string_of_data += data + ' ' + results[data]['name'] + ' ' + results[data]['abbr'] + ' ' + results[data]['constructor']+'\n'
    return string_of_data

# print('summary_results_of_year', summary_results_of_year(2012))
# print(formatted_summary_of_year(2023))

# FIND LINK TO SELECTED GP
# response = requests.get('https://www.formula1.com/en/results.html/2023/races.html')  # Link to all races
# soup = BeautifulSoup(response.text, 'lxml')
# div_with_results = soup.select('div.resultsarchive-filter-wrap:nth-of-type(3)')
# for element in div_with_results:
#     a_with_results = element.select('a')
#     for a_attrs in a_with_results:
#         print(a_with_results)
#         # print(row.text.strip()) # All Name of GP
#         if a_attrs.text.strip() == 'Qatar':  # remove all spaces
#             links_to_race_results = a_attrs.attrs['href']  # access to href attrs in a_with_results
#
# full_link = 'https://www.formula1.com' + links_to_race_results
#
# print(full_link)
#

def current_race_results(race, year):
    full_link = find_all_races_of_year(year)[race]

    r = requests.get(full_link)
    soup = BeautifulSoup(r.text, 'lxml')
    results = soup.find('div', {'class': 'resultsarchive-wrapper'}).prettify()

    table_of_results = soup.find('table', {'class': 'resultsarchive-table'})

    if not table_of_results:
        print('No results are currently available')


    dict_of_res = dict()

    count = 1
    for a_attrs in table_of_results.find_all('tr'):
        driver = []

        for data in a_attrs.find_all('td'):
            if not data.text.isspace() and not 'limiter' in data.attrs['class']:
                driver.append(data.text.strip())
        # print(driver)
        if driver:
            position, number, fullname, constructor, laps, time, points = [el for el in driver]
            abbr = fullname.split('\n')[-1]
            name = ' '.join(fullname.split('\n')[0:2])
            row_data = {
                'position': position,
                'number': number,
                'name': name,
                'abbr': abbr,
                'constructor': constructor,
                'laps': laps,
                'time': time,
                'points': points,
            }

            dict_of_res[count] = row_data
            count += 1
    return dict_of_res

def formatted_current_race_results(results):
    string_of_data = 'POS, NAME, CAR\n'
    for data in results:
        string_of_data += f"{results[data]['position']} {results[data]['name']} {results[data]['constructor']}\n"
    return string_of_data

# print(current_race_results('Bahrain', 2023))
# print(formatted_current_race_results(current_race_results('Bahrain', 2023)))

