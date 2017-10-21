#!/usr/bin/env python3

import csv_utils

def main():
    selected_airports = csv_utils.get_busiest_airports('datasets/original/routes.csv', num_airports=30)
    csv_utils.write_airports(selected_airports, 'datasets/original/airports.csv',
                            'datasets/generated/airports_filtered.csv')

    routes = []
    routes = csv_utils.get_routes_from_airports('datasets/generated/airports_filtered.csv',
                                                'datasets/original/routes.csv')
    print(len(routes))
    for route in routes:
        print(route)



if __name__ == '__main__':
    main()
