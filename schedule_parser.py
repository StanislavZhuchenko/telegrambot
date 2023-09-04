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
        # if not upcoming_event_month:
        #     upcoming_event_month = calendar.month_abbr[datetime.date.today().month]

        if '-' in upcoming_event_month.text:
            first_month = upcoming_event_month.text.split('-')[0]
        else:
            first_month = upcoming_event_month.text
        first_date = f"{date_start} {first_month} {today.year}"
        full_date_start = datetime.datetime.strptime(first_date, '%d %b %Y')
        if full_date_start.date() > today.date() and counter == 0:
            counter += 1
            next_event = f"NEXT>>> {round_numb.text}: {event_place.text}{date_start}-{date_end} {upcoming_event_month.text}\n\n"

        results += f"{round_numb.text}: {event_place.text}{date_start}-{date_end} {upcoming_event_month.text}\n"
    return next_event + results

# print(schedule_calendar())

