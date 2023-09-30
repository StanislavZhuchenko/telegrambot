import calendar

import requests
import datetime
from bs4 import BeautifulSoup


def schedule_calendar():
    next_event = ""
    today = datetime.datetime.today()
    results = f"F1 Schedule {today.year}:\n"
    response = requests.get(f'https://www.formula1.com/en/racing/{today.year}.html')
    soup = BeautifulSoup(response.text, 'lxml')
    events = soup.find_all('div', {'class': 'col-12 col-sm-6 col-lg-4 col-xl-3'})
    counter = 0
    current_event = ''
    for event in events:
        round_numb = event.select_one('[class="card-title f1-uppercase f1-color--warmRed"]')
        if round_numb.text == 'TESTING':
            continue
        event_place = event.select_one('[class="event-place d-block"]')
        date_start = event.select_one('[class="start-date"]').text
        date_end = event.select_one('[class="end-date"]').text
        place = event.select_one('[class="event-place d-block"]')
        upcoming_event_month = event.select_one('[class="month-wrapper f1-wide--xxs f1-uppercase"]')

        if not upcoming_event_month:
            upcoming_event_month = event.select_one('[class="month-wrapper f1-wide--xxs"]')

        try:
            upcoming_event_month_text = upcoming_event_month.text
        except AttributeError:
            upcoming_event_month = calendar.month_abbr[datetime.date.today().month]

        if '-' in upcoming_event_month_text:
            first_month = upcoming_event_month_text.split('-')[0]
            second_month = upcoming_event_month_text.split('-')[1]
            upcoming_event_month_text = '\-'.join(upcoming_event_month_text.split('-'))

        else:
            first_month = upcoming_event_month_text
            second_month = upcoming_event_month_text

        first_date = f"{date_start} {first_month} {today.year}"
        full_date_start = datetime.datetime.strptime(first_date, '%d %b %Y')

        second_date = f"{date_end} {second_month} {today.year}"
        full_date_end = datetime.datetime.strptime(second_date, '%d %b %Y')

        # Represent what is next GP and if we have GP today it can be represented as current event
        if full_date_start.date() > today.date() and counter == 0:
            counter += 1
            next_event = f"NEXT\\>\\>\\> {round_numb.text}: {event_place.text}{date_start}\\-{date_end} {upcoming_event_month_text}\n\n"
        elif full_date_start.date() <= today.date() <= full_date_end.date():
            current_event = f"CURRENT EVENT\\>\\>\\> {round_numb.text}: {event_place.text}{date_start}\\-{date_end} {upcoming_event_month_text}\n\n"

        results += f"{round_numb.text}: {event_place.text}{date_start}\\-{date_end} {upcoming_event_month_text}\n"
    if len(current_event) > 0:
        return current_event + next_event + results
    else:
        return next_event + results



# print(schedule_calendar())
