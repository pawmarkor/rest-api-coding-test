from datetime import date

from flask import abort
from flask_restful import Resource, marshal_with

from schemas import holiday_offers_schema
from filters import filter_offers
from xml_service_client import (
    ServiceClient,
    ServiceClientError,
    SearchContext,
)


class HolidayOffers(Resource):
    @marshal_with(holiday_offers_schema)
    def get(self):
        search_context = SearchContext(
            departure_codes=['LGW', 'STN', 'LHR', 'LCY', 'SEN', 'LTN'],
            country_id=1,
            region_id=4,
            area_id=9,
            resort_id=0,
            departure_date=date(year=2018, month=8, day=15),
            flex=False,
            number_of_adults=2,
            number_of_children=0,
            duration=7,
        )
        try:
            return {
                'offers': filter_offers(
                    ServiceClient.get_holiday_offers(search_context)
                )
            }
        except ServiceClientError:
            # TODO add test for this
            abort(503)
