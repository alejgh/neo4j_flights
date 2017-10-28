#!/usr/bin/env python3

import sys

import neo4j.exceptions
from colorama import Fore
from neo4j.v1 import GraphDatabase, basic_auth


class FlightsConnection():
    def __init__(self, port, username, password):
        self.start_connection(port, username, password)

    def start_connection(self, port, username, password):
        """
        Starts the connection with the database, handling any
        error that may occur, and returning the session.

        Arguments:
        - Port: The port used to connect to the database.
        - Username: Neo4j username.
        - Password: Neo4j password.
        """
        try:
            self.driver = GraphDatabase.driver(
                                "bolt://localhost:" + str(port),
                                auth=basic_auth(username, password))
            self.session = self.driver.session()
        except neo4j.exceptions.ServiceUnavailable as e:
            print(Fore.RED)
            print(e)
            sys.exit(-2)
        except neo4j.exceptions.AuthError:
            print(Fore.RED)
            print("Invalid username/password. Authentication failure.")
            sys.exit(-1)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.session.close()
