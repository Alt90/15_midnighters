import requests
from datetime import datetime
import pytz
import collections


API_URL = 'https://devman.org/api/challenges/solution_attempts/'
TIME_LIMIT = [datetime.strptime('06:00:00', '%H:%M:%S').time(),
              datetime.strptime('00:00:00', '%H:%M:%S').time()]


def get_json_by_page_number(page):
    api_page = requests.get(API_URL, params={'page': page})
    if api_page.status_code == 200:
        return api_page.json()
    else:
        return {}


def get_records_by_page_number(page):
    return get_json_by_page_number(page).get('records', [])


def get_count_page():
    return int(get_json_by_page_number(1).get('number_of_pages', 1))


def load_attempts():
    for page in range(get_count_page()):
        for records in get_records_by_page_number(page):
            yield records


def get_midnighters_task(task_attempts_datas):
    for task_date in task_attempts_datas:
        if task_in_time_limit(task_date):
            yield task_date


def convert_timestamp_to_time(timestamp, timezone):
    time = datetime.utcfromtimestamp(timestamp)
    time_in_timezone = pytz.timezone(timezone).fromutc(time)
    return time_in_timezone.time()


def task_in_time_limit(task_date):
    timestamp = task_date.get('timestamp', None)
    timezone = task_date.get('timezone', 'Europe/Moscow')
    if (timestamp is None):
        return False
    time = convert_timestamp_to_time(timestamp, timezone)
    return (TIME_LIMIT[0] > time > TIME_LIMIT[1])


def get_midnighters(midnighters_task):
    midnighters = collections.Counter()
    for task in midnighters_task:
        midnighters[task['username']] += 1
    return dict(midnighters)


def show_midnighters(midnighters):
    print('Name   Count midnight tasks')
    for name in dict(midnighters):
        print('%s (%s)' % (name, midnighters[name]))


if __name__ == '__main__':
    task_attempts_datas = load_attempts()
    midnighters_task = get_midnighters_task(task_attempts_datas)
    midnighters = get_midnighters(midnighters_task)
    show_midnighters(midnighters)
