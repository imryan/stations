# an example program utilizing the MTA-API library by mimouncadosch.
# more info here: https://github.com/mimouncadosch/MTA-API.

from terminaltables import AsciiTable
import urllib2
import json

STATIONS_URL   = "http://mtaapi.herokuapp.com/stations"
STATION_ID_URL = "http://mtaapi.herokuapp.com/stop?id=%s"
ARRIVAL_URL    = "http://mtaapi.herokuapp.com/api?id=%s"
TIMES_URL      = "http://mtaapi.herokuapp.com/times?hour=%s&minute=%s"

def main():
    print_table()

    # get_all_stations()
    # get_station_by_id("120S")
    # get_station_by_name("96 St")
    # get_arrival_times("120S")
    # get_latest_arrival("120S")
    # get_stations_for_arrival("10", "25")

def print_table():
    table_data = [
        ["Station", "Latest Arrival"],
    ]

    stations = get_all_stations()

    for station in stations:
        table_data.append([station["name"], get_latest_arrival(station["id"])])

    table = AsciiTable(table_data)
    print(table.table)
    print("> loaded %s stations." % int(len(table_data)-1))

def get_all_stations():
    response = urllib2.urlopen(STATIONS_URL).read()
    data = json.loads(response)

    count = 0
    stations = []

    for station in data["result"]:
        count += 1
        stations.append(station)

    return stations

def get_station_by_id(station_id):
    response = urllib2.urlopen(STATION_ID_URL % station_id).read()
    data = json.loads(response)

    if (data["result"] == "key not found"):
        raise Exception("Station with ID '%s' not found." % station_id)

    return data["result"]["name"]

def get_station_by_name(station_name):
    response = urllib2.urlopen(STATIONS_URL).read()
    data = json.loads(response)

    stations = []

    for station in data["result"]:
        stations.append(station["id"])

    if any(station_name in s for s in stations):
        return station_name
    else:
        raise Exception("Station '%s' not found." % station_name)

def get_arrival_times(station_id):
    response = urllib2.urlopen(ARRIVAL_URL % station_id).read()
    data = json.loads(response)

    arrivals = []

    if (data["result"] == "key not found"):
        raise Exception("Station with ID '%s' not found." % station_id)

    for arrival in data["result"]["arrivals"]:
        arrivals.append(arrival)

    return arrivals

def get_latest_arrival(station_id):
    response = urllib2.urlopen(ARRIVAL_URL % station_id).read()
    data = json.loads(response)

    if (data["result"] == "key not found"):
        raise Exception("Station with ID '%s' not found." % station_id)

    return data["result"]["arrivals"][0]

def get_stations_for_arrival(arrival_hour, arrival_minute):
    response = urllib2.urlopen(TIMES_URL % (arrival_hour, arrival_minute)).read()
    data = json.loads(response)

    stations = []

    for station in data["result"]:
        stations.append(station)

    return stations

main()
