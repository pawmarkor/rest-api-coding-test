from decimal import Decimal
from datetime import datetime

from xml_service_client import ServiceClient, Offer


def test_parse_service_data():
    raw_service_data = '''
        <Container xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="HolidaysSearchRequest1.6.xsd">
            <Faults/>
            <Results count="226" searchtime="00:00.234">
                <Offer Type="DP" Hotelsupplier="You+Travel" Flightsuppler="Norwegian+Fly+%2F+Easyjet" Depaptcode="LGW" Depaptname="London%2C+Gatwick" Arraptcode="TFS" Arraptname="Tenerife%2C+Sur+Int.(Reina+Sofia" Outbounddep="15/08/2018 20:05" Outboundarr="16/08/2018 00:25" Outboundfltnum="D86405" Inbounddep="22/08/2018 12:45" Inboundarr="22/08/2018 16:55" Inboundfltnum="EZY8704" Duration="7" Hotelname="Estrella+Del+Norte" Resortname="Icod+De+Los+Vinos" Roomtype="Double+Without+Kitchen+Non+Refundable" Boardbasis="RO" Starrating="3" Ourhtlid="34854" Brochurecode="YOUT-20559" Hotelnetprice="83.00" Flightnetprice="360.00" Sellprice="443.14"/>
                <Offer Type="DP" Hotelsupplier="Hotel+Beds" Flightsuppler="Norwegian+Fly+%2F+Easyjet" Depaptcode="LGW" Depaptname="London%2C+Gatwick" Arraptcode="TFS" Arraptname="Tenerife%2C+Sur+Int.(Reina+Sofia" Outbounddep="15/08/2018 20:05" Outboundarr="16/08/2018 00:25" Outboundfltnum="D86405" Inbounddep="22/08/2018 12:45" Inboundarr="22/08/2018 16:55" Inboundfltnum="EZY8704" Duration="7" Hotelname="Globales+Acuario" Resortname="Puerto+De+La+Cruz" Roomtype="Enquire" Boardbasis="RO" Starrating="2" Ourhtlid="2882" Brochurecode="HBED-119" Hotelnetprice="83.00" Flightnetprice="360.00" Sellprice="443.24"/>
            </Results>
        </Container>
        '''  # noqa
    assert ServiceClient._parse_offers(raw_service_data) == [
        Offer(
            type="DP",
            hotelsupplier="You Travel",
            flightsuppler="Norwegian Fly / Easyjet",
            depaptcode="LGW",
            depaptname="London, Gatwick",
            arraptcode="TFS",
            arraptname="Tenerife, Sur Int.(Reina Sofia",
            outbounddep=datetime(
                year=2018, month=8, day=15, hour=20, minute=5
            ),
            outboundarr=datetime(
                year=2018, month=8, day=16, hour=0, minute=25
            ),
            outboundfltnum="D86405",
            inbounddep=datetime(
                year=2018, month=8, day=22, hour=12, minute=45
            ),
            inboundarr=datetime(
                year=2018, month=8, day=22, hour=16, minute=55
            ),
            inboundfltnum="EZY8704",
            duration=7,
            hotelname="Estrella Del Norte",
            resortname="Icod De Los Vinos",
            roomtype="Double Without Kitchen Non Refundable",
            boardbasis="RO",
            starrating=3,
            ourhtlid=34854,
            brochurecode="YOUT-20559",
            hotelnetprice=Decimal("83.00"),
            flightnetprice=Decimal("360.00"),
            sellprice=Decimal("443.14")
        ),
        Offer(
            type="DP",
            hotelsupplier="Hotel Beds",
            flightsuppler="Norwegian Fly / Easyjet",
            depaptcode="LGW",
            depaptname="London, Gatwick",
            arraptcode="TFS",
            arraptname="Tenerife, Sur Int.(Reina Sofia",
            outbounddep=datetime(
                year=2018, month=8, day=15, hour=20, minute=5
            ),
            outboundarr=datetime(
                year=2018, month=8, day=16, hour=0, minute=25
            ),
            outboundfltnum="D86405",
            inbounddep=datetime(
                year=2018, month=8, day=22, hour=12, minute=45
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
            starrating=2,
            ourhtlid=2882,
            brochurecode="HBED-119",
            hotelnetprice=Decimal("83.00"),
            flightnetprice=Decimal("360.00"),
            sellprice=Decimal("443.24")
        ),
    ]
