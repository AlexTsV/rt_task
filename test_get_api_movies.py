import random
import time
import pytest
import logging
import api
from test_data import Movie, Service

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(filename)s - %(funcName)s - %(lineno)s - %(message)s',
                    level='INFO',
                    filename='pytest.log')
log = logging.getLogger(__name__)
request_log = logging.getLogger('urllib3').setLevel('CRITICAL')


@pytest.mark.parametrize('device', ['tv', 'mobile', 'stb'])
def test_user_can_get_token_for_device(device):
    response = api.get_token_for_device(device)
    if response.status_code != 200:
        message = f"User can't get token for {device}, status code {response.status_code}"
        log.info('FAILED')
        log.exception(message)
        raise AssertionError(message)
    try:
        assert response.json()['token'] is not None
        log.info('PASSED')
    except AssertionError:
        message = f'No token for {device}'
        log.info('FAILED')
        log.exception(message)
        raise AssertionError(message)


def test_user_can_get_available_movies(tokens):
    for token in tokens:
        response = api.get_list_of_available_movies(token)
        status_code = response.status_code
        if status_code != 200:
            message = f"User can't get list of available movies, status code {status_code}"
            log.info('FAILED')
            log.exception(message)
            raise AssertionError(message)
        if len(response.json()['items']) == 0:
            message = 'No available movies'
            log.info('FAILED')
            log.exception(message)
            raise AssertionError(message)
        else:
            log.info('PASSED')


def test_movie_currently_available(tokens):
    for token in tokens:
        movies = api.get_list_of_available_movies(token)
        for movie in movies.json()['items']:
            try:
                assert movie['start_date'] <= time.time() <= movie['end_date']
                log.info('PASSED')
            except AssertionError:
                message = f"{movie['name']} should not be available"
                log.info('FAiLED')
                log.exception(message)
                raise AssertionError(message)


def test_is_movie_included_in_the_services(movies):
    for movie_id in movies:
        try:
            movie_info = Movie().get_info(movie_id)
            assert len(movie_info.json()['services']) >= 1
            log.info('PASSED')
        except AssertionError:
            message = f"The movie with id={movie_id} is not included in any service"
            log.info('FAILED')
            log.exception(message)
            raise AssertionError(message)


def test_if_movie_meets_all_conditions_it_included_in_result(movies, services):
    token = api.get_token_for_device('tv').json()['token']
    user_movies = api.get_list_of_available_movies(token)
    for movie in movies:
        movie_info = Movie().get_info(movie)
        if movie_info.json()['start_date'] <= time.time() <= movie_info.json()['end_date']:
            for device, service_id in services.items():
                if service_id in movie_info.json()['services']:
                    for user_movie in user_movies.json()['items']:
                        try:
                            assert movie_info.json()['id'] == user_movie['id']
                            log.info('PASSED')
                        except AssertionError:
                            message = 'movie meets all conditions does not included in result'
                            log.info('FAILED')
                            log.exception(message)
                            raise AssertionError(message)


def test_film_meets_all_conditions_except_rental_dates_its_not_included_in_result():
    pass


def test_if_movie_meets_all_conditions_except_token_device_type():
    pass
