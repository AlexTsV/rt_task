import time
import pytest
import logging
import api
logging.basicConfig(format='%(asctime)s - %(levelname)s - %(filename)s - %(funcName)s - %(lineno)s - %(message)s',
                    level='INFO',
                    filename='pytest.log')
log = logging.getLogger(__name__)
request_log = logging.getLogger('urllib3').setLevel('CRITICAL')


@pytest.mark.parametrize('device', ['tv', 'mobile', 'stb'])
def test_user_can_get_token_for_device(device):
    response = api.get_token_for_device(device)
    try:
        assert response.status_code == 200
    except AssertionError:
        message = f"User can't get token for {device}, status code {response.status_code}"
        log.info('FAILED')
        log.exception(message)
        raise AssertionError(message)
    try:
        assert response.json()['token'] is not None
    except AssertionError:
        message = f'No token for {device}'
        log.info('FAILED')
        log.exception(message)
        raise AssertionError(message)


def test_user_can_get_available_movies(tokens):
    for token in tokens:
        result = api.get_list_of_available_movies(token)
        try:
            assert result.status_code == 200
        except AssertionError:
            message = f"User can't get list of available movies, status code {result.status_code}"
            log.info('FAILED')
            log.exception(message)
            raise AssertionError(message)
        try:
            if len(result.json()['items']) == 0:
                raise AssertionError('No available movies')
        except AssertionError:
            message = 'No available movies'
            log.info('FAILED')
            log.exception(message)
            raise AssertionError(message)


def test_movie_currently_available(tokens):
    for token in tokens:
        result = api.get_list_of_available_movies(token)
        try:
            if len(result.json()) == 0:
                raise AssertionError('No available movies')
        except AssertionError:
            message = 'No available movies'
            log.info('FAILED')
            log.exception(message)
            raise AssertionError(message)
        for movie in result.json()['items']:
            try:
                assert movie['start_date'] <= time.time() <= movie['end_date']
            except AssertionError:
                message = f"{movie['name']} should not be available"
                log.info('FAiLED')
                log.exception(message)
                raise AssertionError(message)


def test_is_movie_included_in_the_services(tokens):
    for token in tokens:
        result = api.get_list_of_available_movies(token)
        try:
            if len(result.json()) == 0:
                raise AssertionError('No movie included in services')
        except AssertionError:
            message = 'No movie included in services'
            log.info('FAILED')
            log.exception(message)
            raise AssertionError(message)
        for movie in result.json()['items']:
            try:
                assert len(movie['services']) >= 1
            except AssertionError:
                message = f"The {movie['name']} is not included in any service"
                log.info('FAILED')
                log.exception(message)
                raise AssertionError(message)


# @pytest.mark.C123
# def test_if_movie_meets_all_conditions_it_included_in_result(movie_id):
#     movie_info = Movie().get(movie_id)
#     print(movie_info)
