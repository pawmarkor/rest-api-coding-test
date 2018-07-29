import urllib
from collections import defaultdict
from datetime import datetime
from decimal import Decimal
from dataclasses import dataclass

import xmltodict


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


class ServiceClient:
    DATETIME_FORMAT = '%d/%m/%Y %H:%M'

    @classmethod
    def get_holiday_offers(cls):
        raw_data = cls._retrieve_holiday_from_service()
        return cls._parse_offers(raw_data)

    @staticmethod
    def _retrieve_holiday_from_service():
        raise NotImplementedError

    @classmethod
    def _parse_offers(cls, data: dict):
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

        offers = xmltodict.parse(data)['Container']['Results']['Offer']
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
