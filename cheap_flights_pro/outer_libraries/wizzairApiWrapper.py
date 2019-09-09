import requests
import json

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


def flights_timetable(departureFromDate="2019-09-06", departureToDate="2019-10-06", targetFromDate="2019-09-30", targetToDate="2019-11-03",
                      sourceLocation="WAW", targetLocation="VIE", adultCount = 1):
    body = {
        "flightList": [
            {
                "departureStation": sourceLocation,
                "arrivalStation": targetLocation,
                "from": departureFromDate,
                "to": departureToDate
            },
            {
                "departureStation": targetLocation,
                "arrivalStation": sourceLocation,
                "from": targetFromDate,
                "to": targetToDate
            }
        ],
        "priceType": "regular",
        "adultCount": adultCount,
        "childCount": 0,
        "infantCount": 0
    }

    return requests.post(url, data=json.dumps(body), headers=headers)