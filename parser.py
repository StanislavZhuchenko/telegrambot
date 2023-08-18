import requests
import logging
from bs4 import BeautifulSoup
import datetime


# logging.basicConfig(level=logging.DEBUG)


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
        string_of_data += data + ' ' + results[data]['name'] + ' ' + results[data]['abbr'] + ' ' + results[data][
            'constructor'] + '\n'
    return string_of_data


def current_race_results(race, year):
    full_link = find_all_races_of_year(year)[race]

    r = requests.get(full_link)
    soup = BeautifulSoup(r.text, 'lxml')

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

    def formatted_current_race_results(results):
        string_of_data = 'POS, NAME, CAR\n'
        for data in results:
            string_of_data += f"{results[data]['position']} {results[data]['name']} {results[data]['constructor']}\n"
        return string_of_data

    results = formatted_current_race_results(dict_of_res)

    def find_all_results_of_event(soup: BeautifulSoup):
        """
        Find all results of all events inside Grad Prix like Qualifying, Practice, Sprints, etc.
        :return: dict with key: event, value: link to results of this event
        """
        resultsarchive_side_nav = soup.select_one('.resultsarchive-side-nav').find_all('a')
        buttons = dict()
        for event in resultsarchive_side_nav:
            buttons[event.text] = 'https://www.formula1.com' + event.attrs['href']
        # buttons.pop('Race result')
        return buttons

    buttons = find_all_results_of_event(soup)

    return results, buttons


# print(formatted_current_race_results(current_race_results('Bahrain', 2023)))


def event_results(race, year, event='Race result'):
    print(current_race_results(race=race, year=year)[1])
    try:
        url_to_event_results = current_race_results(race=race, year=year)[1][event]
    except KeyError:
        return None

    # with open('1990_races_65_brazil_practice-2.html', 'r') as f:
    #     response = f.read()
    response = requests.get(url_to_event_results)
    page = BeautifulSoup(response.text, 'lxml')
    resultsarchive_table = page.select_one('.resultsarchive-table').select('tr')
    results_dict = dict()
    position = 0
    title = []

    # find table head
    for r in resultsarchive_table:
        if r.find('th'):
            title.extend(r.text.strip('\n').split('\n'))

    driver_result_dict = {key: '' for key in title}  # create dict with title

    for driver in resultsarchive_table:
        driver_result_dict
        # Add Driver Name as list to dict driver_result_dict
        driver_result_list = []
        for data in driver:
            # if data != '\n' and data.find('span') and not data.find('span', {'class': 'suffix seconds'}):
            if data != '\n' and data.find('span', {'class': 'hide-for-tablet'}) and \
                    data.find('span', {'class': 'hide-for-mobile'}) and \
                    data.find('span', {'class': 'uppercase hide-for-desktop'}):
                # print('Data-->>', data)
                driver_data_list = data.text.strip('\n').split('\n')
                if len(driver_data_list[0]) != 0:
                    driver_result_list.extend(driver_data_list)

        # print(driver_result_list)

        # data of driver
        driver_td = []
        for row in driver:
            if row != '\n' and not (row.find('span', {'class': 'hide-for-tablet'}) and
                                    row.find('span', {'class': 'hide-for-mobile'}) and
                                    row.find('span', {'class': 'uppercase hide-for-desktop'})) and row.name != 'th':
                if row.attrs and not 'limiter' in row.attrs['class']:
                    driver_td.append(row.text)

        if len(driver_td) != 0:
            driver_td.insert(2, driver_result_list)
        # print('driver_td', driver_td)

        current_driver_results_dict = dict()
        for key, value in zip(driver_result_dict.keys(), driver_td):

            current_driver_results_dict[key] = value

        if len(current_driver_results_dict) != 0:
            results_dict[position] = current_driver_results_dict

        position += 1

    return results_dict


def pretty_event_results(data: dict):
    # columns = ['Pos', 'Surname', 'Abbr', 'Constructor', 'Time']
    columns = ['Pos', 'No', 'Driver', 'Q1', 'Q2', 'Q3', 'Laps']
    data_list = []

    # from dict to list
    for i in data:
        data_row = [str(i)]
        for el in columns[1:]:
            if el == 'Driver':
                data_row.append(data[i][el][-1])
            data_row.append(data[i][el])
        data_list.append(data_row)

    max_columns = []  # list with max width of columns
    for col in zip(*data_list):
        len_el = []
        [len_el.append(len(el)) for el in col]
        max_columns.append(max(len_el))

    results = str()
    # add table header
    for n, column in enumerate(columns):
        results += f'{column:{max_columns[n] + 2}}'
    results += '\n'

    # separate '-'
    results += f'{"-" * len(results)}\n'

    # add table row
    for el in data_list:
        for n, col in enumerate(el):
            results += f'{col:{max_columns[n] + 2}}'
        results += '\n'

    return results


# print(event_results('Bahrain', 2023, 'Practice 3'))
print(pretty_event_results(event_results('Bahrain', 2023, 'Qualifying')))


# d = event_results('Bahrain', 2023, 'Qualifying')
# for key in d:
#     print(key, d.get(key))
