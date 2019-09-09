from datetime import datetime, timedelta
import json
import wizzairApiWrapper


def get_30_days_periods(departure_from_date, departure_to_date, returning_from_date, returning_to_date):

    departure_from_date = datetime.strptime(departure_from_date, '%Y-%m-%d')
    departure_to_date = datetime.strptime(departure_to_date, '%Y-%m-%d')
    returning_from_date = datetime.strptime(returning_from_date, '%Y-%m-%d')
    returning_to_date = datetime.strptime(returning_to_date, '%Y-%m-%d')

    departures_list = []
    while departure_from_date < departure_to_date:
        departures_list.append((departure_from_date.strftime("%Y-%m-%d"), (departure_from_date + timedelta(days=30)).strftime("%Y-%m-%d")))
        departure_from_date += timedelta(days=31)

    returns_list = []
    while returning_from_date < returning_to_date:
        returns_list.append((returning_from_date.strftime("%Y-%m-%d"), (returning_from_date + timedelta(days=30)).strftime("%Y-%m-%d")))
        returning_from_date += timedelta(days=31)

    # fuse them here and not before because one of them might be longer
    length = len(departures_list) if len(departures_list) > len(returns_list) else len(returns_list)

    dates_list = []
    i = 0
    j = 0
    for aa in range(length):
        dates_list.append((departures_list[i][0], departures_list[i][1], returns_list[j][0], returns_list[j][1]))
        if i < len(departures_list)-1:
            i += 1
        if j < len(departures_list)-1:
            j += 1

    return dates_list


# zwracac loty dla dowolnej dlugosci odcinka czasu i obsluguje blad ale tylko dla jednego miasta
def get_flights(departure_from_date, departure_to_date, target_from_date, target_to_date,
                source_location="WAW", target_location="VIE", adult_count=1):
    time_periods_table = get_30_days_periods(departure_from_date, departure_to_date, target_from_date, target_to_date)

    flights_table = {'outboundFlights':[], 'returnFlights':[]}
    for periods in time_periods_table:
        # dla kazdego takiego trzeba wykonac request i zaapendowac do tablicy
        # podczas wykonywania requestu trzeba sprawdzic czy exception nie poleci i wydrukowac
        while True:
            try:
                r = wizzairApiWrapper.flights_timetable(departureFromDate=periods[0],
                                                        departureToDate=periods[1],
                                                        targetFromDate=periods[2],
                                                        targetToDate=periods[3],
                                                        sourceLocation=source_location,
                                                        targetLocation=target_location,
                                                        adultCount=adult_count)
                flights_table['outboundFlights'] += json.loads(r.content)['outboundFlights']
                flights_table['returnFlights'] += json.loads(r.content)['returnFlights']
                break
            except Exception as e:
                print(r.content)
                continue
    return flights_table


def all_flights_for_given_city(all_possible_target_cities, departure_from_date,
                               departure_to_date, target_from_date, target_to_date,
                               from_city, adult_count):
    all_flights = {}
    for city in all_possible_target_cities:
        flights_table = get_flights(departure_from_date=departure_from_date, departure_to_date=departure_to_date,
                                    target_from_date=target_from_date, target_to_date=target_to_date,
                                    source_location=from_city, target_location=city, adult_count= adult_count)
        all_flights[city] = flights_table

    return all_flights


# filtrujej ze wszystkich lotow tylko te najtansze
def get_cheap_flights_for_given_city(departureFromDate="2019-09-06", departureToDate="2019-10-06", targetFromDate="2019-09-30", targetToDate="2019-11-03",
                      sourceLocation="WAW", adultCount = 1):
    possibleLocations = ['VIE', 'CRL', 'BOJ', 'SPU', 'LCA', 'BLL', 'TKU', 'BOD', 'GNB', 'LYS', 'NCE', 'KUT', 'CFU',
                         'BUD', 'KEF', 'ETM', 'TLV', 'AHO', 'BRI', 'BLQ', 'CTA', 'SUF', 'BGY', 'NAP', 'FCO', 'TRN',
                         'VRN', 'MLA', 'TGD', 'RAK', 'EIN', 'BGO', 'TRF', 'LIS', 'OPO', 'OTP', 'ALC', 'BCN', 'MAD',
                         'TFS', 'GOT', 'MMX', 'NYO', 'BSL', 'IEV', 'KBP', 'BHX', 'DSA', 'EDI', 'LPL', 'LTN']
    # possibleLocations = ['VIE']

    all_flights = all_flights_for_given_city(possibleLocations, departure_from_date="2019-09-09", departure_to_date="2019-12-30",
                                             target_from_date="2019-09-10", target_to_date="2020-01-07",
                                             from_city="WAW", adult_count=1)

    cheap_flights = {}
    for key, flights_to_city in all_flights.items():

        temp_cheapest_outbound = {'priceType': 'price', 'price': {'amount': 9000000}}
        temp_cheapest_return = {'priceType': 'price', 'price': {'amount': 9000000}}
        for flight in flights_to_city['outboundFlights']:
            if flight['priceType'] == 'checkPrice':
                continue
            elif flight['price']['amount'] < temp_cheapest_outbound['price']['amount']:
                temp_cheapest_outbound = flight

        for flight in flights_to_city['returnFlights']:
            if flight['priceType'] == 'checkPrice':
                continue
            elif flight['price']['amount'] < temp_cheapest_return['price']['amount']:
                temp_cheapest_return = flight

        cheap_flights[key] = (temp_cheapest_outbound, temp_cheapest_return)
    return cheap_flights


cheap_flights = get_cheap_flights_for_given_city()
cheap_flights_short = [(key, flight[0]['price']['amount'] + flight[1]['price']['amount']) for key, flight in cheap_flights.items()]
cheap_flights_short_sorted = sorted(cheap_flights_short, key=lambda x: x[1])
print("done")

