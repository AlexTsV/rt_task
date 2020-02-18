import requests
import random
import time
from test_data import Movie


def get_list_of_available_movies(token):
    headers = {
        'Accept': 'application/json',
        'X-TOKEN': f'{token}'
    }
    url = 'http://restream-recom1.herokuapp.com/api/movies'
    response = requests.get(url=url, headers=headers)

    return response


def get_token_for_device(device):
    headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}
    url = 'http://restream-recom1.herokuapp.com/api/token'
    if type(device) is list:
        data = '{"device_type": "%s"}' % random.choice(device)
        response = requests.post(url=url, headers=headers, data=data)
        return response
    data = '{"device_type": "%s"}' % device
    response = requests.post(url=url, headers=headers, data=data)

    return response


def check_movie_creation(movie_id):
    for i in range(4):
        result = Movie().get_info(movie_id)
        if result.status_code == 500:
            time.sleep(1)
        else:
            return result.json()
    else:
        return None


def check_status_code(token):
    for i in range(4):
        result = get_list_of_available_movies(token)
        if result.status_code != 200:
            time.sleep(1)
        else:
            return result.status_code
    else:
        return False


def check_service_creation(service_id):
    headers = {'Accept': 'application/json'}
    url = f'http://restream-recom1.herokuapp.com/qa/services/{service_id}'
    for i in range(4):
        response = requests.get(headers=headers, url=url)
        if response.status_code == 200:
            return True
        if response.status_code == 404:
            time.sleep(1)
    else:
        return False
