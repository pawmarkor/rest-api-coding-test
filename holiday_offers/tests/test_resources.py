from decimal import Decimal
from datetime import time
from unittest.mock import patch, Mock

from flask import url_for

from tests.test_filters import generate_offer


def test_holiday_offers_url(app):
    assert url_for('holiday-offers') == '/holiday_offers'


def test_holiday_offers_endpoint_get_only(client):
    assert client.post(url_for('holiday-offers')).status_code == 405
    assert client.put(url_for('holiday-offers')).status_code == 405
    assert client.patch(url_for('holiday-offers')).status_code == 405


@patch('resources.filter_offers', Mock(
    return_value=[
        generate_offer(
            departure_time=time(hour=12, minute=0),
            return_time=time(hour=13, minute=0),
            price='1',
            star_rating=4,
        ),
        generate_offer(
            departure_time=time(hour=14, minute=0),
            return_time=time(hour=15, minute=0),
            price='2',
            star_rating=5,
        ),
        generate_offer(
            departure_time=time(hour=16, minute=0),
            return_time=time(hour=17, minute=0),
            price='3',
            star_rating=6,
        ),
    ]
))
@patch('resources.ServiceClient.get_holiday_offers', Mock(return_value=[]))
def test_holiday_offers_response(client):
    response = client.get(url_for('holiday-offers'))
    assert response.status_code == 200
    assert response.json == {
        'summary': {
            'most_expensive_price': 3,
            'cheapest_price': 1,
            'average_price': 2
        },
        'offers': [
            {
                'Sellprice': '1',
                'Starrating': '4',
                'Hotelname': 'Globales Acuario',
                'Inboundfltnum': 'EZY8704',
                'Outboundfltnum': 'D86405',
                'Inboundarr': '22/08/2018 16:55',
                'Inbounddep': '22/08/2018 13:00'
            },
            {
                'Sellprice': '2',
                'Starrating': '5',
                'Hotelname': 'Globales Acuario',
                'Inboundfltnum': 'EZY8704',
                'Outboundfltnum': 'D86405',
                'Inboundarr': '22/08/2018 16:55',
                'Inbounddep': '22/08/2018 15:00'
            },
            {
                'Sellprice': '3',
                'Starrating': '6',
                'Hotelname': 'Globales Acuario',
                'Inboundfltnum': 'EZY8704',
                'Outboundfltnum': 'D86405',
                'Inboundarr': '22/08/2018 16:55',
                'Inbounddep': '22/08/2018 17:00'
            },
        ]
    }


@patch('resources.ServiceClient.get_holiday_offers', Mock(return_value=[]))
@patch('resources.filter_offers')
def test_holiday_offers_query_params(filter_offers, client):
    filter_offers.return_value = []
    response = client.get(
        url_for('holiday-offers') + '?star_rating=1&'
                                    'min_price=1.11&'
                                    'max_price=2.22&'
                                    'earliest_return_time=11:11&'
                                    'earliest_departure_time=22:22'
    )
    assert response.status_code == 200
    filter_offers.assert_called_once_with(
        [],
        earliest_return_time=time(hour=11, minute=11),
        earliest_departure_time=time(hour=22, minute=22),
        max_price=Decimal("2.22"),
        min_price=Decimal("1.11"),
        star_rating=True,
    )
