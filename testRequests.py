import requests
import json
from datetime import datetime, timedelta

url = 'https://be.wizzair.com/9.16.2/Api/search/timetable'
headers = {
    "Host": "be.wizzair.com",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:69.0) Gecko/20100101 Firefox/69.0",
    "Content-Type": "application/json;charset=utf-8",
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "pl,en-US;q=0.7,en;q=0.3",
    "Accept-Encoding": "gzip, deflate, br",
    "Referer": "https://wizzair.com/en-gb/flights/timetable/warsaw-chopin/vienna--",
    "Content-Length": "260",
    "Origin": "https://wizzair.com",
    "Connection": "keep-alive",
    "TE": "Trailers",
    "Pragma": "no-cache",
    "Cache-Control": "no-cache"

}


# function to look for flight for 1 adult male from Warsaw, both direction
# takes target location, from date and to Date because it can be maximally a month
def sendRequestGetFlights(IPfromDate="2019-09-07", IPtoDate="2019-10-07", TPfromDate="2019-09-30", TPtoDate="2019-11-03", targetLocation="VIE"):
    body = {
        "flightList": [
            {
                "departureStation": "WAW",
                "arrivalStation": targetLocation,
                "from": IPfromDate,
                "to": IPtoDate
            },
            {
                "departureStation": targetLocation,
                "arrivalStation": "WAW",
                "from": TPfromDate,
                "to": TPtoDate
            }
        ],
        "priceType": "regular",
        "adultCount": 1,
        "childCount": 0,
        "infantCount": 0
    }

    return requests.post(url, data=json.dumps(body), headers=headers)

# r = sendRequestGetFlights()
# test with long periods
r = sendRequestGetFlights(IPfromDate="2019-10-06", IPtoDate="2019-10-07", TPfromDate="2019-10-08", TPtoDate="2019-11-03")
aa = json.loads(r.content)
print(r.content)


def getFlights(location, currentDeparture):
    r = sendRequestGetFlights(currentDeparture.strftime("%Y-%m-%d"),(currentDeparture + timedelta(days=30)).strftime("%Y-%m-%d"),
                              (currentDeparture + timedelta(days=7)).strftime("%Y-%m-%d"), (currentDeparture + timedelta(days=37)).strftime("%Y-%m-%d"),
                              location)
    # min(data, key=lambda t: t[1])
    cenyWylotow = [(e['price']['amount'], e['departureDate']) for e in json.loads(r.content)['outboundFlights']]
    cenyPrzylotow = [(e['price']['amount'], e['departureDate']) for e in json.loads(r.content)['returnFlights']]
    if(len(cenyPrzylotow) == 0 or len(cenyWylotow) == 0):
        return ()
    najtanszyWylot = min(cenyWylotow, key=lambda t: t[0])
    najtanszyPrzylot = min(cenyPrzylotow, key=lambda t: t[0])
    return (najtanszyWylot, najtanszyPrzylot)


def getChepeastHolidayMax7Days():

    # possibleLocations = ['VIE', 'CRL']
    possibleLocations = ['VIE', 'CRL', 'BOJ', 'SPU', 'LCA', 'BLL', 'TKU', 'BOD', 'GNB', 'LYS', 'NCE', 'KUT', 'CFU',
                         'BUD', 'KEF', 'ETM', 'TLV', 'AHO', 'BRI', 'BLQ', 'CTA', 'SUF', 'BGY', 'NAP', 'FCO', 'TRN',
                         'VRN', 'MLA', 'TGD', 'RAK', 'EIN', 'BGO', 'TRF', 'LIS', 'OPO', 'OTP', 'ALC', 'BCN', 'MAD',
                         'TFS', 'GOT', 'MMX', 'NYO', 'BSL', 'IEV', 'KBP', 'BHX', 'DSA', 'EDI', 'LPL', 'LTN']

    currentDeparture = datetime.now()  # current date and time
    # currentGoingBack = currentDeparture + timedelta(days=5)


    lokacjeDictionary = {}

    for location in possibleLocations:
        lokacjeDictionary[location] = []
        for i in range(3):
            lokacjeDictionary[location].append(getFlights(location, currentDeparture))
    return lokacjeDictionary


tanieLoty = getChepeastHolidayMax7Days()
print("end of program")