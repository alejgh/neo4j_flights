#!/usr/bin/env python3

import argparse
import getpass

import colorama as clr

import neo4j_queries
from neo4j_connection import FlightsConnection

exit = False

info_queries = """Available queries:
1.- Information about every airline and their country.
2.- Top 10 airlines that provide the biggest amount of flights.
3.- Flights from Madrid to London ordered by departure date.
4.- Number of flights that depart from every airport each day.
5.- Flights from Spain to the US ordered by departure date.
6.- Number of flights that depart from and arrive to every airport each day.
7.- Flights from New York to Los Angeles the 8th of November, as well as the
airline that provides each flight.
8.- Paths to go from Gatwick (London) to Incheon (Seoul) the 9th of November
doing 2 flights at most.
9.- Which of the paths from query '8' arrives earlier?
10.- Shortest path from Madrid to Seoul."""


def print_help():
    print("In order to make a query you have to introduce the number of the "
          "query that you want to make.\nIf you type 'queries' you can "
          "see every query available.\nYou can also type 'exit' to stop "
          "the application, and 'help' to show this message again.")


def print_queries():
    print(info_queries)


def process_user_input(user_input, conn):
    """
    This function checks if the user input is a int. If it is,
    it calls the corresponding function from neo4j_queries.
    If it isn't an int
    """
    try:
        int(user_input)
        method = getattr(neo4j_queries, 'query' + user_input)
        method(conn.session)
    except ValueError:
        if user_input == 'queries':
            print_queries()
        elif user_input == 'exit':
            global exit
            exit = True
        elif user_input == 'help':
            print_help()
        else:
            print("Unrecognized input.")
            print_help()
    except Exception:
        print("Invalid query number.")


def main():
    clr.init()
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', type=str,
                        help='port where bolt is enabled', default='7687')
    args = parser.parse_args()
    username = input("Introduce your neo4j username: ")
    password = getpass.getpass("Introduce your password: ")

    with FlightsConnection(args.port, username, password) as conn:
        print_queries()
        print_help()
        while not exit:
            user_input = input(">> ")
            process_user_input(user_input, conn)


if __name__ == '__main__':
    main()
