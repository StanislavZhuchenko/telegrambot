import requests
import datetime
from bs4 import BeautifulSoup
from parser import pretty_event_results


def driverstandings(year=datetime.date.today().year):
    try:
        url = f'https://www.formula1.com/en/results.html/{year}/drivers.html'
    except Exception as e:
        print(e)
    response = requests.get(url)
    decoded_content = response.content.decode('utf-8')
    soup = BeautifulSoup(decoded_content, 'lxml')

    # table_titles = soup.find('div', {'class': 'resultsarchive-content'}).find('thead').find_all('th')
    # titles = []
    # for title in table_titles:
    #     if len(title.text) != 0 and not title.text.isspace():
    #         titles.append(title.text)
    # print(titles)

    table_of_results = soup.find('div', {'class': 'resultsarchive-content'}).find('tbody').find_all('tr')
    driver_standing = dict()
    for row in table_of_results:
        res = row.text.split('\n')
        res1 = [el for el in res if len(el) != 0 and not el.isspace()]
        pos, name, surname, abbr, nationality, constructor, points = [el for el in res1]
        driver = name + ' ' + surname
        row_res = {'Pos': pos, 'driver': driver, 'nationality': nationality, 'constructor': constructor, 'points': points}
        driver_standing[int(pos)] = row_res
    # titles = {'Pos': '', 'driver': '', 'nation': '', 'constructor': '', 'points': ''}
    titles = ('Pos', 'driver', 'nationality', 'constructor', 'points')
    return driver_standing, titles


if __name__ == '__main__':
    d = driverstandings(2023)
    print(d)

    print(pretty_event_results(d))
