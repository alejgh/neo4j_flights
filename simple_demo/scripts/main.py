import getpass
import sys

import colorama as clr
import neo4j.exceptions
from neo4j.v1 import GraphDatabase, basic_auth

# WORK IN PROGRESS


if __name__ == '__main__':
    clr.init()

    username = input("Introduce your neo4j user name: ")
    password = getpass.getpass("Introduce your password: ")
    try:
        driver = GraphDatabase.driver("bolt://localhost:7687",
                                      auth=basic_auth(username, password))
        session = driver.session()
    except neo4j.exceptions.AuthError:
        print(clr.Fore.RED)
        print("Invalid username/password. Authentication failure.")
        sys.exit(-1)
    result = session.run("MATCH (airport:Airport)<-"
                         "[departs:DEPARTS_AT]-(f:Flight)"
                         "RETURN airport.name as airport, "
                         "split(departs.date, ' ')[0] as day, "
                         "count(f) as departures "
                         "ORDER BY airport.name, day")

    print(clr.Fore.LIGHTMAGENTA_EX)
    for record in result:
        print("Airport: {0} - Day: {1} - Departures: {2}".format(
                                    record['airport'], record['day'],
                                    record['departures']))
