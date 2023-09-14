import logging
import datetime
import requests
from bs4 import BeautifulSoup
from parser import find_all_races_of_year
from features import time_execution


# year = 2023
#
# All_race = find_all_races_of_year(year)


@time_execution
def current_race(race, year):
    url = find_all_races_of_year(year)[race]

    response = requests.get(url=url)
    decoded_content = response.content.decode('utf-8')
    page = BeautifulSoup(decoded_content, 'lxml')

    # Find all events which were at this race and returns name to
    resultsarchive_side_nav = page.select_one('.resultsarchive-side-nav').find_all('a')
    buttons = dict()
    for event in resultsarchive_side_nav:
        buttons[event.text] = 'https://www.formula1.com' + event.attrs['href']

    return buttons


@time_execution
def event_results(race, year, event='Race result'):
    # Try in one function
    url = find_all_races_of_year(year)[race]

    t_start = datetime.datetime.now()
    response = requests.get(url=url)
    decoded_content = response.content.decode('utf-8')
    page = BeautifulSoup(decoded_content, 'lxml')
    t_finish = datetime.datetime.now()
    t_delta1 = t_finish - t_start
    print(f"Time of load page: {t_delta1.microseconds / 1000} ms")


    # Find all events which were at this race and returns name to
    resultsarchive_side_nav = page.select_one('.resultsarchive-side-nav').find_all('a')
    buttons = dict()
    for ev in resultsarchive_side_nav:
        buttons[ev.text] = 'https://www.formula1.com' + ev.attrs['href']

    all_events = buttons
    if event != 'Race result':
        t_start = datetime.datetime.now()
        url_to_event_results = all_events[event]
        response = requests.get(url_to_event_results)
        decoded_content = response.content.decode('utf-8')
        page = BeautifulSoup(decoded_content, 'lxml')
        t_finish = datetime.datetime.now()
        t_delta2 = t_finish - t_start
        print(f"Time of load 2 page: {t_delta2.microseconds / 1000} ms")
        print(f"Summary time to load {(t_delta1.microseconds + t_delta2.microseconds)/1000} ms")



    #############

    # all_events = current_race(race, year)
    # url_to_event_results = all_events[event]

    # response = requests.get(url_to_event_results)
    # decoded_content = response.content.decode('utf-8')
    # page = BeautifulSoup(decoded_content, 'lxml')

    resultsarchive_table = page.select_one('.resultsarchive-table').select('tr')

    # Parse title of page and make it more readable
    page_title = page.select_one('title')
    page_title_list = [el.strip() for el in page_title.text.strip().split('\n') if len(el) != 0 and not el.isspace()]
    page_title = ' '.join(page_title_list)

    results_dict = dict()
    position = 0
    title = []

    # find table head
    for r in resultsarchive_table:
        if r.find('th'):
            title.extend(r.text.strip('\n').split('\n'))

    dict_with_title_of_table = {key: '' for key in title}  # create dict with title

    for driver in resultsarchive_table:
        # Add Driver Name as list to dict driver_result_dict
        driver_result_list = []
        for data in driver:
            if data != '\n' and data.find('span', {'class': 'hide-for-tablet'}) and \
                    data.find('span', {'class': 'hide-for-mobile'}) and \
                    data.find('span', {'class': 'uppercase hide-for-desktop'}):
                driver_data_list = data.text.strip('\n').split('\n')
                if len(driver_data_list[0]) != 0:
                    driver_result_list.extend(driver_data_list)

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

        current_driver_results_dict = dict()
        for key, value in zip(dict_with_title_of_table.keys(), driver_td):
            current_driver_results_dict[key] = value

        if len(current_driver_results_dict) != 0:
            results_dict[position] = current_driver_results_dict

        position += 1

    return results_dict, dict_with_title_of_table, page_title, all_events


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    t_start = datetime.datetime.now()

    # all_races = find_all_races_of_year()
    # results = current_race('Bahrain', 2023)
    results2 = event_results('Bahrain', 2023, 'Fastest laps')
    # results2 = event_results('Bahrain', 2023, 'Race result')
    t_finish = datetime.datetime.now()
    t_delta = t_finish - t_start
    print(f"Summary time: {t_delta.microseconds / 1000} ms")
    # for race in all_races:
    #     print(race, all_races.get(race))
    # print(results2)
