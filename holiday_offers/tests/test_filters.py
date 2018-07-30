from datetime import datetime, time
from decimal import Decimal

import pytest

from xml_service_client import Offer
from filters import filter_offers


def generate_offer(
        departure_time,
        return_time,
        price,
        star_rating
):
    return Offer(
        type="DP",
        hotelsupplier="Hotel Beds",
        flightsuppler="Norwegian Fly / Easyjet",
        depaptcode="LGW",
        depaptname="London, Gatwick",
        arraptcode="TFS",
        arraptname="Tenerife, Sur Int.(Reina Sofia",
        outbounddep=datetime(
            year=2018, month=8, day=15,
            hour=departure_time.hour, minute=departure_time.minute
        ),
        outboundarr=datetime(
            year=2018, month=8, day=16, hour=0, minute=25
        ),
        outboundfltnum="D86405",
        inbounddep=datetime(
            year=2018, month=8, day=22,
            hour=return_time.hour, minute=return_time.minute
        ),
        inboundarr=datetime(
            year=2018, month=8, day=22, hour=16, minute=55
        ),
        inboundfltnum="EZY8704",
        duration=7,
        hotelname="Globales Acuario",
        resortname="Puerto De La Cruz",
        roomtype="Enquire",
        boardbasis="RO",
        starrating=star_rating,
        ourhtlid=2882,
        brochurecode="HBED-119",
        hotelnetprice=Decimal("83.00"),
        flightnetprice=Decimal("360.00"),
        sellprice=Decimal(price)
    )


@pytest.mark.parametrize(
    'earliest_departure_time,earliest_return_time,'
    'max_price,min_price,star_rating,expected_idx',
    [
        (None, None, None, None, None, (0, 1, 2, 3)),
        (time(hour=14, minute=0), None, None, None, None, (2, 3)),
        (None, time(hour=14, minute=0), None, None, None, (2, 3)),
        (None, None, 2, None, None, (0, 1)),
        (None, None, None, 2, None, (1, 2, 3)),
        (None, None, None, None, True, (2, 3)),
        (None, None, 3, 2, True, (2,))
    ]
)
def test_filter(
        earliest_departure_time,
        earliest_return_time,
        max_price,
        min_price,
        star_rating,
        expected_idx,
):
    offers = [
        generate_offer(
            departure_time=time(hour=12, minute=0),
            return_time=time(hour=12, minute=0),
            price=1,
            star_rating=1,
        ),
        generate_offer(
            departure_time=time(hour=13, minute=0),
            return_time=time(hour=13, minute=0),
            price=2,
            star_rating=2,
        ),
        generate_offer(
            departure_time=time(hour=14, minute=0),
            return_time=time(hour=14, minute=0),
            price=3,
            star_rating=3,
        ),
        generate_offer(
            departure_time=time(hour=15, minute=0),
            return_time=time(hour=15, minute=0),
            price=4,
            star_rating=4,
        ),
    ]
    filtered_offers_idx = set(
        offers.index(filtered_offer) for filtered_offer in filter_offers(
            offers,
            earliest_departure_time,
            earliest_return_time,
            max_price,
            min_price,
            star_rating
        )
    )

    assert filtered_offers_idx == set(expected_idx)
