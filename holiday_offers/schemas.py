from typing import List
from datetime import datetime

from flask_restful import fields

from constants import DATETIME_FORMAT
from xml_service_client import Offer

# TODO consider using marshmallow


class DateTime(fields.Raw):
    def format(self, datetime_value: datetime):
        return datetime_value.strftime(DATETIME_FORMAT)


holiday_offer_schema = {
    'Sellprice': fields.String(attribute='sellprice'),
    'Starrating': fields.String(attribute='starrating'),
    'Hotelname': fields.String(attribute='hotelname'),
    'Inboundfltnum': fields.String(attribute='inboundfltnum'),
    'Outboundfltnum': fields.String(attribute='outboundfltnum'),
    'Inboundarr': DateTime(attribute='inboundarr'),
    'Inbounddep': DateTime(attribute='inbounddep'),
}


class SummaryField(fields.Raw):
    def format(self, offers: List[Offer]):
        offer_prices = [offer.sellprice for offer in offers]
        return {
            'most_expensive_price': max(offer_prices),
            'cheapest_price': min(offer_prices),
            'average_price': sum(offer_prices) / len(offers),
        }


holiday_offers_schema = {
    'offers': fields.List(fields.Nested(holiday_offer_schema)),
    'summary': SummaryField(attribute='offers'),
}
