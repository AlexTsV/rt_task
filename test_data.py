import requests
from faker import Faker
from datetime import datetime, timedelta

headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}


class RentalDate:
    fake = Faker()

    def get_past_rental(self):
        start_date = self.fake.unix_time(end_datetime=datetime.now() - timedelta(days=10))
        end_date = self.fake.unix_time(end_datetime=datetime.now() - timedelta(days=5))

        return start_date, end_date

    def get_current_rental(self):
        start_date = self.fake.unix_time(end_datetime=datetime.now() - timedelta(days=1))
        end_date = self.fake.unix_time(start_datetime=datetime.now())

        return start_date, end_date

    def get_future_rental(self):
        start_date = self.fake.unix_time(start_datetime=datetime.now()) + 86400
        end_date = self.fake.unix_time(start_datetime=datetime.now()) + 864000

        return start_date, end_date


class Service:
    url = 'http://restream-recom1.herokuapp.com/qa/services'

    headers = {'Accept': 'application/json'}

    def create(self, name, desc, price, device):
        data = '{"id": 0, "name": "%s", "description": "%s", "price": %s, "device_types": ["%s"]}' % \
               (name, desc, price, device)
        response = requests.post(url=self.url, headers=headers, data=data)

        return response

    def delete(self, services_id):
        for device, service_id in services_id.items():
            url = f'{self.url}/{service_id}'
            requests.delete(headers=self.headers, url=url)

    def get_info(self, service_id):
        url = f'{self.url}/{service_id}'
        response = requests.get(headers=self.headers, url=url)

        return response


class Movie:
    url = 'http://restream-recom1.herokuapp.com/qa/movies'

    headers = {'Accept': 'application/json'}

    def create(self, name, desc, start_date, end_date, service_id):
        data = '{"id": 0, "name": "%s", "description": "%s", "start_date": %s, "end_date": %s,' \
               ' "services": [%s]}' % (name, desc, start_date, end_date, service_id)
        response = requests.post(url=self.url, headers=headers, data=data)

        return response

    def delete(self, movies_id):
        for movie_id in movies_id:
            url = f'{self.url}/{movie_id}'
            requests.delete(headers=self.headers, url=url)

    def get_info(self, movie_id):
        url = f'{self.url}/{movie_id}'
        response = requests.get(headers=self.headers, url=url)

        return response
