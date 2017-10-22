#!/usr/bin/env python3

import calendar
import dateutil.parser
import urllib.request

def write_json_flight_data(routes, dates, appId, appKey, output_path):
    with open(output_path, 'w', encoding='utf-8') as output_file:
        print('Sending queries to flight stats...')
        first = True
        output_file.write('[')
        for route in routes:
            print('Departure: {0} - Arrival: {1}'.format(route[0], route[1]))
            src = route[0]
            dest = route[1]
            for date in dates:
                day, month, year = date.split('/')
                url = ('https://api.flightstats.com/flex/schedules/rest/v1/json/from/' + src +
                '/to/' + dest + '/departing/' + year + '/' + month + '/' + day +
                '?appId=' + appId + '&appKey=' + appKey)
                with urllib.request.urlopen(url) as response:
                    if first:
                        output_file.write(str(response.read(), 'utf-8') + '\n')
                        first = False
                    else:
                        output_file.write(',' + str(response.read(), 'utf-8') + '\n')
        output_file.write(']')


def parse_flight_time(time):
    pair = time.replace('T','').split('.')
    if pair[1] != '000':
        return None
    return pair[0]


def get_flight_timestamp(time):
    dt = dateutil.parser.parse(time)
    return calendar.timegm(dt.timetuple())
