import json
import importlib
import sys

from voe.util import process_date_input, process_airport_input

def main():
    (date_departure, date_arrival, fixed_departure_month, fixed_arrival_month,
     next_clicks_departure, next_clicks_arrival) = process_date_input(None, None)

    airport_from, airport_to = process_airport_input(None, None)

    module_name = "voe.backend.{}".format(sys.argv[1])
    backend_impl = importlib.import_module(module_name)

    results = backend_impl.run(airport_from,
                               airport_to,
                               date_departure,
                               date_arrival,
                               fixed_departure_month,
                               fixed_arrival_month,
                               next_clicks_departure,
                               next_clicks_arrival)

    _from = airport_from
    _to = airport_to
    route_id = "{}-{}".format(_from, _to)
    rev_route_id = "{}-{}".format(_to, _from)
    routes = {}
    for i in range(1, 13):
        routes[i] = {}
    departures = results[0]
    arrivals = results[1]
    for dep in departures:
        date = dep['date']
        dep['departure_date'] = date.strftime('%-d/%m')
        dep['departure_price'] = dep['price']
        dep['route'] = route_id
        del dep['date']
        routes[date.month][date.day] = dep
    for arr in arrivals:
        date = arr['date']
        arr['arrival_date'] = date.strftime('%-d/%m')
        arr['arrival_price'] = arr['price']
        arr['rev_route'] = rev_route_id
        del arr['date']

        previous = routes[date.month][date.day]
        arr.update(previous)
        routes[date.month][date.day] = arr

    print(json.dumps(routes, indent=4))

if __name__ == "__main__":
    main()
