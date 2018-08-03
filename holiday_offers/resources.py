from decimal import Decimal
from datetime import date, datetime

from flask import abort
from flask_restful import (
    Resource,
    marshal_with,
    reqparse,
)

from schemas import holiday_offers_schema
from filters import filter_offers
from xml_service_client import (
    ServiceClient,
    ServiceClientError,
    SearchContext,
)
from constants import TIME_FORMAT


def time_builder(time_string: str) -> datetime.time:
    return datetime.strptime(time_string, TIME_FORMAT).time()


class HolidayOffers(Resource):
    @marshal_with(holiday_offers_schema)
    def get(self):
        args = self.parse_qs_arguments()

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
                    ServiceClient.get_holiday_offers(search_context),
                    earliest_return_time=args.get('earliest_return_time'),
                    earliest_departure_time=args.get(
                        'earliest_departure_time'
                    ),
                    max_price=args.get('max_price'),
                    min_price=args.get('min_price'),
                    star_rating=args.get('star_rating'),
                )
            }
        except ServiceClientError:
            # TODO add test for this
            abort(503)

    def parse_qs_arguments(self):
        parser = reqparse.RequestParser()
        parser.add_argument('earliest_departure_time', type=time_builder)
        parser.add_argument('earliest_return_time', type=time_builder)
        parser.add_argument('max_price', type=Decimal)
        parser.add_argument('min_price', type=Decimal)
        parser.add_argument('star_rating', type=bool)
        args = parser.parse_args()
        return args
