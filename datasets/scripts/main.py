#!/usr/bin/env python3

import csv_utils

def main():
    #csv_utils.remove_airports_without_iata('datasets/original/airports.csv',
    #                                        'datasets/generated/airports_with_iata.csv')

    routes = []

    while (len(routes) > 1000 or len(routes) < 500):
        csv_utils.pick_random_airports('datasets/generated/airports_with_iata.csv',
                                        'datasets/generated/airports_filtered.csv',
                                        number_of_selections=30)
        routes = csv_utils.get_routes_from_airports('datasets/generated/airports_filtered.csv',
                                                    'datasets/original/routes.csv')
    for route in routes:
        print(route)


if __name__ == '__main__':
    main()
