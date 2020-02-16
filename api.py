import requests
import random


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

