import json
import logging
import importlib
import os
import sys

from datetime import timedelta
from pyvirtualdisplay.smartdisplay import SmartDisplay

from voe.util import process_date_input, process_airport_input, create_today_dir
from voe.scheduler import gen_dates, iterate


logging.basicConfig(level=logging.INFO)


def main():
    backend = sys.argv[1]
    module_name = "voe.backend.{}".format(backend)
    backend_impl = importlib.import_module(module_name)

    path = "data/"
    #current_day_path = create_today_dir(path)
    #os.chdir(current_day_path)

    routes = {}
    _from = sys.argv[2]
    _to = sys.argv[3]
    route_id = "{}-{}".format(_from, _to)
    rev_route_id = "{}-{}".format(_to, _from)
    routes['id'] = route_id
    for i in range(1, 13):
        routes[i] = {}

    with SmartDisplay(visible=0, bgcolor='black') as disp:
        for date in iterate(gen_dates(), increment=10):
            departure_date_str = date.strftime("%-d/%m")
            arrival_date_str = date.strftime("%-d/%m")

            (date_departure, date_arrival, fixed_departure_month,
            fixed_arrival_month, next_clicks_departure,
            next_clicks_arrival) = process_date_input(departure_date_str,
                                                    arrival_date_str)

            airport_from, airport_to = process_airport_input(_from, _to)

            logging.info("{} {} {} {}".format(backend, route_id, departure_date_str,
                                            arrival_date_str))

            results = backend_impl.run(airport_from,
                                    airport_to,
                                    date_departure,
                                    date_arrival,
                                    fixed_departure_month,
                                    fixed_arrival_month,
                                    next_clicks_departure,
                                    next_clicks_arrival)

            departures = results[0]
            arrivals = results[1]
            for dep in departures:
                date = dep['date']
                if not dep['price']:
                    continue
                dep['departure_date'] = date.strftime('%-d/%m')
                dep['departure_price'] = dep['price']
                dep['route'] = route_id
                del dep['date']
                routes[date.month][date.day] = dep
            for arr in arrivals:
                date = arr['date']
                if not arr['price']:
                    continue
                arr['arrival_date'] = date.strftime('%-d/%m')
                arr['arrival_price'] = arr['price']
                arr['rev_route'] = rev_route_id
                del arr['date']
                previous = routes[date.month].get(date.day, None)
                if previous:
                    arr.update(previous)
                routes[date.month][date.day] = arr

            print(routes)

            #out = open('{}.{}.json'.format(backend, route_id), "wt")
            #out.write(json.dumps(routes, indent=4))
            #out.close()

if __name__ == "__main__":
    main()
