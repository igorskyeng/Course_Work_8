import requests
from django.conf import settings
from rest_framework import status


def convert_currencies(rub_price):
    usd_price = 0
    resource = requests.get(
        f'{settings.CUR_API_URL}v3/latest?apikey={settings.CUR_API_KEY}&currencies=RUB'
    )

    if resource.status_code == status.HTTP_200_OK:
        usd_rate = resource.json()['data']['RUB']['value']
        usd_price = rub_price * usd_rate

    return usd_price
