#!/usr/bin/env python3

import csv_utils
import flightstats
import csv


def main():
    selected_airports = csv_utils.get_busiest_airports('../original/routes.csv', num_airports=30)
    csv_utils.write_airports(selected_airports, '../original/airports.csv',
                            '../generated/airports_filtered.csv')
    routes = csv_utils.get_routes_from_airports('../generated/airports_filtered.csv',
                                                '../original/routes.csv')
    dates = ['6/11/2017','7/11/2017','8/11/2017','9/11/2017','10/11/2017']
    appID = input('Introduce your flightaware app ID: ')
    appKey = input('Introduce your flightaware app Key: ')
    flightstats.write_json_flight_data(routes, dates, appID, appKey, '../generated/flights.json')
    csv_utils.json_to_csv('../generated/flights.json', '../generated/flights.csv')
    airlines = csv_utils.get_airlines_in_flights('../generated/flights.csv')
    csv_utils.write_airlines(airlines, '../generated/airlines_filtered.csv')

if __name__ == '__main__':
    main()
