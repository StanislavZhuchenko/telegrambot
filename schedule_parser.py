import requests
import datetime
import calendar
import logging
from bs4 import BeautifulSoup
response = requests.get(f'https://www.formula1.com/en/racing/2023.html')
soup = BeautifulSoup(response.text, 'lxml')
events = soup.find_all('div', {'class': 'col-12 col-sm-6 col-lg-4 col-xl-3'})
for event in events:
    round_numb = event.select_one('[class="card-title f1-uppercase f1-color--warmRed"]')
    date_start = event.select_one('[class="start-date"]').text
    date_end = event.select_one('[class="end-date"]').text
    place = event.select_one('[class="event-place d-block"]')
    upcoming_event_month = event.select_one('[class="month-wrapper f1-wide--xxs f1-uppercase"]')
    if not upcoming_event_month:
        upcoming_event_month = event.select_one('[class="month-wrapper f1-wide--xxs"]')
    if not upcoming_event_month:
        upcoming_event_month = calendar.month_abbr[datetime.date.today().month]
    if not isinstance(upcoming_event_month, str):
        print(date_start, '-', date_end, upcoming_event_month.text)
    else:
        print(upcoming_event_month)
    # if 'TESTING' in event.text:
    #     continue
    # date = event.find('div', {'class': 'date-month f1-uppercase f1-wide--s'})
    # completed_event_month = event.find('div', {'class': 'event-completed'})
    # upcoming_event_month = event.find('span', {'class': 'month-wrapper f1-wide--xxs'})
    # upcoming_event_month = event.select_one('[class="month-wrapper f1-wide--xxs f1-uppercase"]')
    # print(upcoming_event_month if upcoming_event_month else event.select_one('[class="month-wrapper f1-wide--xxs"]'))
    # if completed_event_month:
    # #     month = completed_event_month.text
    # if upcoming_event_month:
    #     month = upcoming_event_month.text
    #     description = event.find('div', {'class': 'event-description'})
    #     print('Date-->>', date.text)
    #     if month:
    #         print('MONTH-->>', month)
    #     print(description.text)
