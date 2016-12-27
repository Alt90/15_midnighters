import requests


API_URL = 'https://devman.org/api/challenges/solution_attempts/'


def get_json_by_page_number(page):
    api_page = requests.get(API_URL, params={'page': page})
    if api_page.status_code == 200 :
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

def get_midnighters():
    pass

if __name__ == '__main__':
    task_attempts_datas = load_attempts()
