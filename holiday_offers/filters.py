from decimal import Decimal
from datetime import time
from typing import Optional, List

from xml_service_client import Offer


def filter_offers(
        offers: List[Offer],
        earliest_departure_time: Optional[time] = None,
        earliest_return_time: Optional[time] = None,
        max_price: Optional[Decimal] = None,
        min_price: Optional[Decimal] = None,
        star_rating: Optional[bool] = False,
):
    filters = []
    if max_price is not None:
        filters.append(lambda offer: offer.sellprice <= max_price)
    if min_price is not None:
        filters.append(lambda offer: offer.sellprice >= min_price)
    if star_rating:
        filters.append(lambda offer: offer.starrating >= 3)
    if earliest_departure_time:
        # TODO do I use correct field here?
        filters.append(
            lambda offer: offer.outbounddep.time() >= earliest_departure_time
        )
    if earliest_return_time:
        # TODO do I use correct field here?
        filters.append(
            lambda offer: offer.inbounddep.time() >= earliest_return_time
        )
    return [
        offer for offer in offers
        if all(map(lambda filter: filter(offer), filters))
    ]
