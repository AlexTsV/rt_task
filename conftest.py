from faker import Faker
import pytest
import random
from test_data import Movie, Service, RentalDate
import api
fake = Faker()
fake_movies = ['The Green Mile', 'Inception', 'Forrest Gump']
fake_genres = ['drama', 'comedy', 'melodrama']


def delete_created_movies_and_services(movies_id, services):
    for movie_id in movies_id:
        Movie().delete(movie_id)
    for service_id in services:
        Service().delete(service_id)


@pytest.fixture(scope="session")
def services():
    devices = random.choice(["tv", "mobile", "stb", ["tv", "mobile", "stb"]])
    services_id = {}
    if type(devices) is list:
        devices = ', '.join(devices)
        response = Service().create('subscription', f"full_subscription", random.randint(1, 10), devices)
        services_id['full_sub'] = (response.json()["id"])
    else:
        response = Service().create('subscription', f"{devices}_subscription", random.randint(1, 10), devices)
        services_id[devices] = (response.json()["id"])
    return services_id


@pytest.fixture(scope="session", autouse=True)
def movies(services):
    movies_id = []
    for device, service_id in services.items():
        start_date, end_date = random.choice([RentalDate().get_past_rental(), RentalDate().get_current_rental(),
                                              RentalDate().get_future_rental()])
        response = Movie().create(random.choice(fake_movies), random.choice(fake_genres), start_date, end_date,
                                  service_id)
        movies_id.append(response.json()["id"])
    yield movies
    delete_created_movies_and_services(movies_id, services)


@pytest.fixture(scope="session")
def tokens(services):
    token_list = []
    for device, service_id in services.items():
        if device == 'full_sub':
            response = api.get_token_for_device(random.choice(['tv', 'mobile', 'stb']))
            token_list.append(response.json()["token"])
            return token_list
        response = api.get_token_for_device(device)
        token_list.append(response.json()["token"])

    return token_list
