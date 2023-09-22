from datetime import datetime

import requests
from bs4 import BeautifulSoup
from parser import pretty_event_results


def constructor_standings(year=datetime.now().year):
    try:
        url = f"https://www.formula1.com/en/results.html/{year}/team.html"
        response = requests.get(url)
        decoded_content = response.content.decode('utf-8')
        page = BeautifulSoup(decoded_content, 'lxml')
        table_titles = page.select_one('.resultsarchive-table').select('tr')
    except:
        return 'Error'

    # Parse title of page and make it more readable
    page_title = page.select_one('title')
    page_title_list = [el.strip() for el in page_title.text.strip().split('\n') if len(el) != 0 and not el.isspace()]
    page_title = ' '.join(page_title_list)

    # find table head
    title = []
    for a in table_titles:
        if a.find('th'):
            title.extend(a.text.strip('\n').split('\n'))

    dict_with_title_of_table = {key: '' for key in title}  # create dict with title

    table_of_results = page.find('div', {'class': 'resultsarchive-content'}).find('tbody').find_all('tr')
    constructors_standing = dict()
    position = 1
    for row in table_of_results:
        res = row.text.split('\n')
        res1 = [el for el in res if len(el) != 0 and not el.isspace()]
        row_res = dict()
        for key, value in zip(dict_with_title_of_table.keys(), res1):
            row_res[key] = value

        constructors_standing[position] = row_res
        position += 1
    # titles for table result
    return constructors_standing, title, page_title


if __name__ == "__main__":
    r = constructor_standings(2003)
    print(pretty_event_results(r))
