#!/usr/bin/env python3

import csv
import itertools
import pdb
from collections import defaultdict
import numpy as np


def remove_airports_without_iata(input_path, output_path):
    with open(input_path, 'r', encoding='utf-8') as airports_file:
        airports_data = csv.DictReader(airports_file)
        with open(output_path, 'w', encoding='utf-8') as airports_output_file:
            airports_writer = csv.DictWriter(airports_output_file, airports_data.fieldnames)
            airports_writer.writeheader()
            for line in airports_data:
                if line['iata'] != '\\N':
                    airports_writer.writerow(line)



def pick_random_airports(input_path, output_path, number_of_selections=100):
    total_airports = sum(1 for airport in open(input_path, 'r', encoding='utf-8'))
    with open(input_path, 'r', encoding='utf-8') as airports_file:
        airports_data = csv.DictReader(airports_file)
        airports_selected = np.random.randint(0, total_airports, number_of_selections)
        with open(output_path, 'w', encoding='utf-8') as airports_output_file:
            airports_writer = csv.DictWriter(airports_output_file, airports_data.fieldnames)
            airports_writer.writeheader()
            for i, line in enumerate(airports_data):
                if i in airports_selected:
                    airports_writer.writerow(line)


def get_routes_from_airports(airports_file_path, routes_file_path):
    airports = []
    with open(airports_file_path, 'r', encoding='utf-8') as airports_data:
        airports_reader = csv.DictReader(airports_data)
        for airport in airports_reader:
            airports.append(airport['iata'])

    routes = []
    with open(routes_file_path, 'r', encoding='utf-8') as routes_data:
        routes_reader = csv.DictReader(routes_data)
        # get all posible departure-arrival airport combinations
        airport_combinations = list(itertools.permutations(airports, 2))
        for route in routes_reader:
            for combination in airport_combinations:
                if (route['source_airport'] == combination[0] and
                    route['dest_airport'] == combination[1]):
                    routes.append((combination[0], combination[1]))
    return routes

def get_best_airports(routes_file_path, num_airports=50):
    airports = defaultdict(int)
    with open(routes_file_path, 'r', encoding='utf-8') as routes_data:
        routes_reader = csv.DictReader(routes_data)
        for route in routes_reader:
            src = route['source_airport']
            dest = route['dest_airport']
            airports[src] += 1
            airports[dest] += 1
    return sorted(airports.items(), key=lambda k_v: k_v[1], reverse=True)[:num_airports]