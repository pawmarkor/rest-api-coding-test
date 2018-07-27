# rest-api-coding-test

## Task

Create a REST API that allows us to retrieve `Holiday Offers` from a upstream `xml service` and filter them by a set of criteria.

For the purpose of this test your service should call below url to retrieve the `Holiday Offers`
http://87.102.127.86:8100/search/searchoffers.dll?page=SEARCH&platform=WEB&depart=LGW%7CSTN%7CLHR%7CLCY%7CSEN%7CLTN&countryid=1&regionid=4&areaid=9&resortid=0&depdate=15%2F08%2F2018&flex=0&adults=2&children=0&duration=7

Each `Holiday Offer` element should look like the below:
```xml
<Offer 
       Sellprice="471.42" Flightnetprice="389.00" Hotelnetprice="83.00" Brochurecode="YOUT-20559" Ourhtlid="34854" 
       Starrating="3" Boardbasis="RO" Roomtype="Double+Without+Kitchen+Non+Refundable" Resortname="Icod+De+Los+Vinos" 
       Hotelname="Estrella+Del+Norte" Duration="7" Inboundfltnum="EZY8704" Inboundarr="22/08/2018 16:55" Inbounddep="22/08/2018 12:45" 
       Outboundfltnum="D86405" Outboundarr="16/08/2018 00:25" Outbounddep="15/08/2018 20:05" Arraptname="Tenerife%2C+Sur+Int.(Reina+Sofia" 
       Arraptcode="TFS" Depaptname="London%2C+Gatwick" Depaptcode="LGW" Flightsuppler="Norwegian+Fly+%2F+Easyjet"
       Hotelsupplier="You+Travel" Type="DP"/>
````

#### Key attributes to filter the offers by:
- `Sellprice` - The price of the holiday
- `Starrating` - The star rating of the hotel
- `Outbounddep` - The outward bound flight DateTime
- `Inbounddep` - The inward bound flight DateTime


### Your REST API should have:
#### Query Parameters
  - *earliest_departure_time* - The earliest `Time` of departure flight (Note that this is Time rather than DateTime)
  - *earliest_return_time* - The latest `Time` of return flight
  - *max_price* - The maximum acceptable price for the `Holiday Offer`
  - *min_price* - The minimum acceptable price for the `Holiday Offer`
  - *star_rating* - The minimum star rating for the hotel in the `Holiday Offer`
  
#### Response 
Must be in JSON format
Must contain :
  - A summary field containing
    - The most expensive offer price
    - The cheapest offer price
    - The average offer price
    
  - A list of the offers that met the filter criteria  


Below is an example of how the response could look like:
```json
{
  "summary" : {
      "most_expensive_price" : 400.0,
      "cheapest_price" : 200.0,
      "average_price" : 300.0
  },
  "offers" : [{
              "Sellprice": "400.0", 
              "Starrating":"3",
              "Hotelname":"Hotel A", 
              "Inboundfltnum":"EZY8704", 
              "Outboundfltnum":"D86405",
              "Inboundarr":"22/08/2018 16:55",
              "Inbounddep":"22/08/2018 12:45"
           },
           {
              "Sellprice": "200.0", 
              "Starrating":"3",
              "Hotelname":"Hotel B", 
              "Inboundfltnum":"EZY8704", 
              "Outboundfltnum":"D86405",
              "Inboundarr":"22/08/2018 16:55",
              "Inbounddep":"22/08/2018 12:45"
           },
  ]  
}
```



