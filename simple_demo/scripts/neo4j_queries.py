#!/usr/bin/env python3

import colorama as clr

HEADER_DELIMITER = "=" * 60
HEADER_COLOR = clr.Fore.BLUE


def query1(session):
    """
    This query returns every airline in the database, as well
    as the country where it is incorporated.
    """
    result = session.run(
            "MATCH (a:Airline)-[:IS_INCORPORATED_IN]->(c:Country)"
            "RETURN a.name as Airline, a.iata as IATA,"
            " a.icao as ICAO, c.name as Country")
    print(HEADER_DELIMITER)
    print(HEADER_COLOR + "Information about every airline.")
    print(clr.Fore.RESET + HEADER_DELIMITER)
    for record in result:
        print('Name: {} - IATA: {} - ICAO: {} - Country: {}'.format(
              record['Airline'], record['IATA'],
              record['ICAO'], record['Country']))


def query2(session):
    """
    This query returns the 10 airlines that provide the biggest number
    of flights in the database.
    """
    result = session.run(
            "MATCH (airline:Airline)-[:PROVIDES]->(f:Flight)"
            "RETURN airline.name as airline, count(f) as flights_provided "
            "ORDER BY flights_provided DESC "
            "LIMIT 10")
    print(HEADER_DELIMITER)
    print(HEADER_COLOR + "TOP 10 airlines with the most flights")
    print(clr.Fore.RESET + HEADER_DELIMITER)
    for record in result:
        print("Name: {0} - Number of flights provided: {1}".format(
              record['airline'], record['flights_provided']))


def query3(session):
    """
    This query returns information about the available flights from
    Madrid to London, ordered by departure date.
    """
    result = session.run(
        "MATCH (dptAirp:Airport)<-[dptAt:DEPARTS_AT]-(:Flight)-"
        "[arrAt:ARRIVES_AT]->(arrAirp:Airport) "
        "WHERE dptAirp.city = 'Madrid' and arrAirp.city = 'London'"
        "RETURN DISTINCT dptAirp.name as departure_airport, "
        "dptAt.date as departure_date, arrAirp.name as arrival_airport, "
        "arrAt.date as arrival_date "
        "ORDER BY departure_date"
    )
    print(HEADER_DELIMITER)
    print(HEADER_COLOR + "Flights from Madrid to London ordered by date")
    print(clr.Fore.RESET + HEADER_DELIMITER)
    for record in result:
        print("From: {0} - Dpt. date: {1} - To: {2} - Arr. date: {3}"
              .format(record['departure_airport'], record['departure_date'],
                      record['arrival_airport'], record['arrival_date']))


def query4(session):
    """
    This query returns the number of flights departing
    from each airport every day.
    """
    result = session.run(
        "MATCH (airport:Airport)<-[departs:DEPARTS_AT]-(f:Flight)"
        "RETURN airport.name as airport, split(departs.date, ' ')[0] as day, "
        "count(f) as departures "
        "ORDER BY airport.name, day"
    )
    print(HEADER_DELIMITER)
    print(HEADER_COLOR +
          "Number of flights departing from each airport every day")
    print(clr.Fore.RESET + HEADER_DELIMITER)
    for record in result:
        print("Airport: {0} - Day: {1} - Number of departures: {2}".format(
              record['airport'], record['day'], record['departures']))


def query5(session):
    """
    This query returns every flight from Spain to the U.S.
    ordered by date.
    """
    result = session.run(
        "MATCH (dptAirp:Airport)<-[dptAt:DEPARTS_AT]-(:Flight)"
        "-[arrAt:ARRIVES_AT]->(arrAirp:Airport), "
        "(dptAirp)-[:IS_LOCATED_IN]->(spain:Country), "
        "(arrAirp)-[:IS_LOCATED_IN]->(us:Country) "
        "WHERE spain.code = 'ES' and us.code = 'US' "
        "RETURN DISTINCT dptAirp.name as departure_airport, "
        "dptAt.date as departure_date, arrAt.date as arrival_date, "
        "arrAirp.name as arrival_airport "
        "ORDER BY departure_date"
    )
    print(HEADER_DELIMITER)
    print(HEADER_COLOR + "Flights from Spain to the United States.")
    print(clr.Fore.RESET + HEADER_DELIMITER)
    for record in result:
        print("From: {0} - Dpt. date: {1} - To: {2} - Arr. date: {3}"
              .format(record['departure_airport'], record['departure_date'],
                      record['arrival_airport'], record['arrival_date']))


def query6(session):
    """
    This query returns the number of flights departing
    from and arriving to every airport.
    """
    result = session.run(
        "MATCH (airport:Airport)<-[:DEPARTS_AT]-(f:Flight) "
        "WITH airport, count(f) as departures "
        "MATCH (f2:Flight)-[:ARRIVES_AT]->(airport)"
        "RETURN airport.name as airport_name, departures, "
        "count(f2) as arrivals"
    )
    print(HEADER_DELIMITER)
    print(HEADER_COLOR + "Number of departures and arrivals for each airport.")
    print(clr.Fore.RESET + HEADER_DELIMITER)
    for record in result:
        print("Airport name: {0} - Departures: {1} - Arrivals: {2}".format(
              record['airport_name'], record['departures'], record['arrivals']
              ))


def query7(session):
    """
    This query returns flight information from every flight that
    goes from New York to Los Angeles the 8th of November, as well
    as the airline that provides the flight.
    """
    result = session.run(
        "MATCH (dpt_airp:Airport{city: 'New York'})<-[departure:DEPARTS_AT]-"
        "(f:Flight)-[:ARRIVES_AT]->(arr_airp:Airport{city: 'Los Angeles'}), "
        "(airline:Airline)-[:PROVIDES]->(f) "
        "WHERE departure.date > '2017-11-08 00:00:00' "
        "AND departure.date < '2017-11-09 00:00:00' "
        "RETURN airline.name as airline, dpt_airp.name as departure_airport, "
        "arr_airp.name as arrival_airport, departure.date as departure_date "
        "ORDER BY departure.date"
    )
    print(HEADER_DELIMITER)
    print(HEADER_COLOR + "Flights from New York to Los Angeles departing "
          "the 8th of November")
    print(clr.Fore.RESET + HEADER_DELIMITER)
    for record in result:
        print("Airline: {0} - From: {1} - To: {2} - Dpt. Date: {3}".format(
              record['airline'], record['departure_airport'],
              record['arrival_airport'], record['departure_date']))


def query8(session):
    """
    This query returns the possible paths to reach Seoul
    departing from London the 9th of November doing 2
    flights at most.
    """
    result = session.run(
        "MATCH p=((src:Airport{name: 'London Gatwick Airport'})-[*1..4]-"
        "(dest:Airport{name: 'Incheon International Airport'})) "
        "WHERE ALL (i in range(0, size(relationships(p))-2) "
        "WHERE (relationships(p)[i]).date < (relationships(p)[i+1]).date) "
        "AND (relationships(p)[0]).date > '2017-11-07 00:00:00' "
        "RETURN p"
    )
    print(HEADER_DELIMITER)
    print(HEADER_COLOR + "Paths from London to Seoul, departing on the "
                         "9th of November\nand doing 2 flights at most.")
    print(clr.Fore.RESET + HEADER_DELIMITER)
    for record in result:
        _print_path(record['p'])


def query9(session):
    """
    This query returns the path that arrives earlier to
    the destination from query number 8.
    """
    result = session.run(
        "MATCH p=((src:Airport{name: 'London Gatwick Airport'})-[*1..4]-"
        "(dest:Airport{name: 'Incheon International Airport'})) "
        "WHERE ALL (i in range(0, size(relationships(p))-2) "
        "WHERE (relationships(p)[i]).date < (relationships(p)[i+1]).date) "
        "AND (relationships(p)[0]).date > '2017-11-07 00:00:00' "
        "RETURN p "
        "ORDER BY (relationships(p)[size(relationships(p))-1]).date "
        "LIMIT 1"
    )
    print(HEADER_DELIMITER)
    print(HEADER_COLOR + "Path that arrives earlier from query number 8")
    print(clr.Fore.RESET + HEADER_DELIMITER)
    for record in result:
        _print_path(record['p'])


def query10(session):
    """
    This query returns the shortest path from Madrid to Seoul.
    """
    result = session.run(
        "MATCH p=shortestpath((src:Airport{city: 'Madrid'})-[*..15]"
        "-(dest:Airport{city: 'Seoul'})) "
        "WHERE ALL (i in range(0, size(relationships(p))-2) "
        "WHERE (relationships(p)[i]).date < (relationships(p)[i+1]).date) "
        "RETURN p"
    )
    print(HEADER_DELIMITER)
    print(HEADER_COLOR + "Shortest path from Madrid to Seoul"
                         " (least amount of flights).")
    print(clr.Fore.RESET + HEADER_DELIMITER)
    for record in result:
        _print_path(record['p'])


def _print_path(path):
    relationships = path.relationships
    nodes = path.nodes
    path_str = ""
    for i in range(len(relationships)):
        if i % 2 == 0:
            path_str += "({0})-[Departure time: {1}]->".format(
                nodes[i]['name'], relationships[i]['date'])
        else:
            path_str += "(Flight: {0})-[Arrival time: {1}]->".format(
                nodes[i]['number'], relationships[i]['date'])
    path_str += "({0})".format(nodes[-1]['name'])
    print(path_str)
