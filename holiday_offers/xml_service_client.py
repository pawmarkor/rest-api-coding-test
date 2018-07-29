import urllib
from collections import defaultdict
from datetime import datetime, date
from decimal import Decimal
from dataclasses import dataclass
from typing import List

import xmltodict
import requests


@dataclass
class Offer:
    type: str
    hotelsupplier: str
    flightsuppler: str
    depaptcode: str
    depaptname: str
    arraptcode: str
    arraptname: str
    outbounddep: datetime
    outboundarr: datetime
    outboundfltnum: str
    inbounddep: datetime
    inboundarr: datetime
    inboundfltnum: str
    duration: int
    hotelname: str
    resortname: str
    roomtype: str
    boardbasis: str
    starrating: int
    ourhtlid: int
    brochurecode: str
    hotelnetprice: Decimal
    flightnetprice: Decimal
    sellprice: Decimal


@dataclass
class SearchContext:
    departure_codes: List[str]
    country_id: int
    region_id: int
    area_id: int
    resort_id: int
    departure_date: date
    flex: bool
    number_of_adults: int
    number_of_children: int
    duration: int


class ServiceClientError(Exception):
    pass


class ServiceClient:
    DATE_FORMAT = '%d/%m/%Y'
    DATETIME_FORMAT = f'{DATE_FORMAT} %H:%M'
    API_URL = 'http://87.102.127.86:8100/search/searchoffers.dll'

    @classmethod
    def get_holiday_offers(cls, search_context: SearchContext):
        raw_data = cls._retrieve_service_offers(search_context)
        return cls._parse_service_offers(raw_data)

    @classmethod
    def _retrieve_service_offers(cls, search_context: SearchContext):
        response = requests.get(
            cls.API_URL,
            params={
                'page': 'SEARCH',
                'platform': 'WEB',
                'depart': '|'.join(search_context.departure_codes),
                'countryid': search_context.country_id,
                'regionid': search_context.region_id,
                'areaid': search_context.area_id,
                'resortid': search_context.resort_id,
                'depdate': search_context.departure_date.strftime(
                    cls.DATE_FORMAT
                ),
                'flex': 1 if search_context.flex else 0,
                'adults': search_context.number_of_adults,
                'children': search_context.number_of_children,
                'duration': search_context.duration,
            }
        )
        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError:
            raise ServiceClientError()
        return response.text

    @classmethod
    def _parse_service_offers(cls, data: dict):
        def parse_types(offer):
            typed_fields = defaultdict(list)
            for field, field_type in Offer.__annotations__.items():
                typed_fields[field_type].append(field)
            for datetime_field in typed_fields[datetime]:
                offer[datetime_field] = datetime.strptime(
                    offer[datetime_field],
                    cls.DATETIME_FORMAT,
                )
            for int_field in typed_fields[int]:
                offer[int_field] = int(offer[int_field])
            for decimal_field in typed_fields[Decimal]:
                offer[decimal_field] = Decimal(offer[decimal_field])
            return offer

        try:
            offers = xmltodict.parse(data)['Container']['Results']['Offer']
        # TODO narrow down except here or log the original error message
        except:  # noqa
            raise ServiceClientError()
        return [
            Offer(
                **parse_types(
                    {
                        k.lstrip('@').lower(): urllib.parse.unquote_plus(v)
                        for k, v in offer.items()
                    }
                )
            )
            for offer in offers
        ]
