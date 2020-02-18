import time

from faker import Faker
import pytest
import random
from test_data import Movie, Service, RentalDate
import api

fake = Faker()
fake_movies = ['The Green Mile', 'Inception', 'Forrest Gump', 'Scarface']
fake_genres = ['drama', 'comedy', 'melodrama']


@pytest.fixture(scope="session")
def services():
    device_list = ["tv", "mobile", "stb", ["tv", "mobile", "stb"]]
    services_id = {}
    for device in device_list:
        if type(device) is list:
            devices = ', '.join(device)
            response = Service().create('subscription', f"full_subscription", random.randint(1, 10), devices)
            services_id['full_sub'] = (response.json()["id"])
        else:
            response = Service().create('subscription', f"{device}_subscription", random.randint(1, 10), device)
            services_id[device] = (response.json()["id"])
        time.sleep(3)

    return services_id


@pytest.fixture(scope="session")
def movies(services):
    for device, service_id in services.items():
        if api.check_service_creation(service_id) is False:
            raise AssertionError(f'Service for {device} does not created')
    movies_id = []
    for device, service_id in services.items():
        start_date, end_date = random.choice([RentalDate().get_past_rental(), RentalDate().get_current_rental(),
                                              RentalDate().get_future_rental()])
        response = Movie().create(random.choice(fake_movies), random.choice(fake_genres), start_date, end_date,
                                  service_id)
        if api.check_movie_creation(response.json()['id']) is not None:
            movies_id.append(response.json()["id"])

    return movies_id


# @pytest.fixture(scope="module", autouse=True)
# def clean_test_data(movies, services):
#     yield movies
#     Movie().delete(movies)
#     Service().delete(services)


@pytest.fixture(scope="session")
def tokens():
    token_list = []
    response = api.get_token_for_device(random.choice(['tv', 'mobile', 'stb']))
    token_list.append(response.json()["token"])

    return token_list
