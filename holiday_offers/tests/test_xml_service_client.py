from decimal import Decimal
from datetime import datetime, date

import pytest

from xml_service_client import (
    ServiceClient,
    Offer,
    SearchContext,
    ServiceClientError,
)


def test_parse_service_data():
    raw_service_data = '''<?xml version="1.0" encoding="UTF-8"?>
        <Container xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="HolidaysSearchRequest1.6.xsd">
            <Faults/>
            <Results count="226" searchtime="00:00.234">
                <Offer Type="DP" Hotelsupplier="You+Travel" Flightsuppler="Norwegian+Fly+%2F+Easyjet" Depaptcode="LGW" Depaptname="London%2C+Gatwick" Arraptcode="TFS" Arraptname="Tenerife%2C+Sur+Int.(Reina+Sofia" Outbounddep="15/08/2018 20:05" Outboundarr="16/08/2018 00:25" Outboundfltnum="D86405" Inbounddep="22/08/2018 12:45" Inboundarr="22/08/2018 16:55" Inboundfltnum="EZY8704" Duration="7" Hotelname="Estrella+Del+Norte" Resortname="Icod+De+Los+Vinos" Roomtype="Double+Without+Kitchen+Non+Refundable" Boardbasis="RO" Starrating="3" Ourhtlid="34854" Brochurecode="YOUT-20559" Hotelnetprice="83.00" Flightnetprice="360.00" Sellprice="443.14"/>
                <Offer Type="DP" Hotelsupplier="Hotel+Beds" Flightsuppler="Norwegian+Fly+%2F+Easyjet" Depaptcode="LGW" Depaptname="London%2C+Gatwick" Arraptcode="TFS" Arraptname="Tenerife%2C+Sur+Int.(Reina+Sofia" Outbounddep="15/08/2018 20:05" Outboundarr="16/08/2018 00:25" Outboundfltnum="D86405" Inbounddep="22/08/2018 12:45" Inboundarr="22/08/2018 16:55" Inboundfltnum="EZY8704" Duration="7" Hotelname="Globales+Acuario" Resortname="Puerto+De+La+Cruz" Roomtype="Enquire" Boardbasis="RO" Starrating="2" Ourhtlid="2882" Brochurecode="HBED-119" Hotelnetprice="83.00" Flightnetprice="360.00" Sellprice="443.24"/>
                <Offer Type="DP" Hotelsupplier="Hotel+Beds" Flightsuppler="Norwegian+Fly+%2F+Easyjet" Depaptcode="LGW" Depaptname="London%2C+Gatwick" Arraptcode="TFS" Arraptname="Tenerife%2C+Sur+Int.(Reina+Sofia" Outbounddep="15/08/2018 20:05" Outboundarr="16/08/2018 00:25" Outboundfltnum="D86405" Inbounddep="22/08/2018 12:45" Inboundarr="22/08/2018 16:55" Inboundfltnum="EZY8704" Duration="7" Hotelname="Globales+Acuario" Resortname="Puerto+De+La+Cruz" Roomtype="Enquire" Boardbasis="RO" Starrating="2" Ourhtlid="2882" Brochurecode="HBED-119" Hotelnetprice="83.00" Flightnetprice="360.00"/>
            </Results>
        </Container>'''  # noqa

    assert ServiceClient._parse_service_offers(raw_service_data) == [
        Offer(
            outbounddep=datetime(
                year=2018, month=8, day=15, hour=20, minute=5
            ),
            outboundfltnum="D86405",
            inbounddep=datetime(
                year=2018, month=8, day=22, hour=12, minute=45
            ),
            inboundarr=datetime(
                year=2018, month=8, day=22, hour=16, minute=55
            ),
            inboundfltnum="EZY8704",
            hotelname="Estrella Del Norte",
            starrating=3,
            sellprice=Decimal("443.14")
        ),
        Offer(
            outbounddep=datetime(
                year=2018, month=8, day=15, hour=20, minute=5
            ),
            outboundfltnum="D86405",
            inbounddep=datetime(
                year=2018, month=8, day=22, hour=12, minute=45
            ),
            inboundarr=datetime(
                year=2018, month=8, day=22, hour=16, minute=55
            ),
            inboundfltnum="EZY8704",
            hotelname="Globales Acuario",
            starrating=2,
            sellprice=Decimal("443.24")
        ),
    ]


def test_parse_service_data_failed():
    with pytest.raises(ServiceClientError):
        ServiceClient._parse_service_offers('<wrong<xml')


class TestRetrieveOffersFromService:
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

    def test_retrieve_holiday_from_service_successful(self, requests_mock):
        requests_mock.get(
            'http://87.102.127.86:8100/search/searchoffers.dll?page=SEARCH'
            '&platform=WEB&depart=LGW%7CSTN%7CLHR%7CLCY%7CSEN%7CLTN'
            '&countryid=1&regionid=4&areaid=9&resortid=0'
            '&depdate=15%2F08%2F2018&flex=0&adults=2&children=0&duration=7',
            text='test'
        )

        assert ServiceClient._retrieve_service_offers(
            self.search_context
        ) == 'test'

    def test_retrieve_holiday_from_service_failed(self, requests_mock):
        requests_mock.get(
            'http://87.102.127.86:8100/search/searchoffers.dll?page=SEARCH'
            '&platform=WEB&depart=LGW%7CSTN%7CLHR%7CLCY%7CSEN%7CLTN'
            '&countryid=1&regionid=4&areaid=9&resortid=0'
            '&depdate=15%2F08%2F2018&flex=0&adults=2&children=0&duration=7',
            status_code=500
        )

        with pytest.raises(ServiceClientError):
            ServiceClient._retrieve_service_offers(self.search_context)
