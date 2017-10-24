# Datasets
In this section you can find the datasets used in the neo4j GraphGist and the demo app. I will
briefly describe each dataset.

## Countries
Simple csv file with every country and it's ISO alpha-2 (2 letters) code. Some minor changes
were made so the name of the country in the airports and airlines files matched the 'official'
country name. Some of the changes are:
  - Brunei Darussalam --> Brunei
  - Viet Nam --> Vietnam
  - Hong Kong SAR China --> Hong Kong
  - Korea, Republic of --> South Korea
  
## Airports
This file is a subset of the one obtained from the [open flights website](https://openflights.org/data.html).
This subset contains 30 of the most busiest airports by passenger traffic in the world. The following
information of each airport is used in the neo4j database:
  - Name: Name of the airport.
  - City: Main city served by airport.
  - IATA: 3-letter IATA code of the airport, defined by the [International Air Transport Association](http://www.iata.org/).
  - ICAO: 4-letter ICAO code of the airport.
  - Country: Country where the airport is located.
 
## Airlines
This file is also a subset of the airlines dataset you can find in [open flights](https://openflights.org/data.html).
The subset contains all the airlines that operate in the airports previously shown. The following information
is used in the database:
  - Name: Name of the airline.
  - Alias: Alias of the airline.
  - IATA: 2-letter IATA code, if available.
  - ICAO: 3-letter ICAO code, if available.
  - Country: Country where the airline is incorporated.
 
## Flights
The final file contains all the routes between the selected airports from the 6th to the 10th of November of 2017.
This routes where obtained using the [FlightStats API](https://developer.flightstats.com/). Each flight has
the following information:
  - Flight Number: Flight number returned by FlightStats. **It is not unique**.
  - Departure Airport: 3-letter IATA code of the airport where the flight departs.
  - Arrival Airport: 3-letter IATA code of the airport where the flight arrives.
  - Airline Code: 2-letter IATA code of the airline that provides the flight.
  - Departure Time
  - Departure Timestamp: Departure time described as Unix time, so calculations using times in the database
  can be done in a much easier way.
  - Arrival Time
  - Arrival Timestamp: Same as the departure timestamp.
