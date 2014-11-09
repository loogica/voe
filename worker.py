import json
import logging
import importlib
import os
import sys

from datetime import timedelta

import zmq

from decouple import config
from easyprocess import EasyProcess
from pyvirtualdisplay.smartdisplay import SmartDisplay

from voe.util import process_date_input, process_airport_input, create_today_dir
from voe.scheduler import gen_dates, iterate

MASTER_IP = config('MASTER_IP')
SINK_IP = config('SINK_IP')

PULL_PORT = 1313
SYNC_PORT = 13131
PUSH_PORT = 13132

PULL_ADDR = "tcp://{}:{}".format(MASTER_IP, PULL_PORT)
SYNC_ADDR = "tcp://{}:{}".format(MASTER_IP, SYNC_PORT)
PUSH_ADDR = "tcp://{}:{}".format(SINK_IP, PUSH_PORT)

logging.basicConfig(level=logging.INFO)

def main():
    context = zmq.Context()

    sync = context.socket(zmq.DEALER)
    pull = context.socket(zmq.PULL)
    push = context.socket(zmq.PUSH)

    import time
    pull.connect(PULL_ADDR)
    sync.connect(SYNC_ADDR)
    push.connect(PUSH_ADDR)
    time.sleep(1)

    while True:
        sync.send("ready")
        task = pull.recv()

        logging.info("Received task {}".format(task))

        backend = task.split(" ")[0]
        _from = task.split(" ")[1]
        _to = task.split(" ")[2]

        module_name = "voe.backend.{}".format(backend)
        backend_impl = importlib.import_module(module_name)

        routes = {}
        route_id = "{}-{}".format(_from, _to)
        rev_route_id = "{}-{}".format(_to, _from)
        routes['id'] = route_id

        for i in range(1, 13):
            routes[i] = {}

        with SmartDisplay(visible=0, bgcolor='black') as disp:
            for date in iterate(gen_dates(days=10), increment=1):
                departure_date_str = date.strftime("%-d/%m")
                arrival_date_str = date.strftime("%-d/%m")

                logging.info("{} {} {}".format(task, departure_date_str,
                                            arrival_date_str))

                (date_departure, date_arrival, fixed_departure_month,
                fixed_arrival_month, next_clicks_departure,
                next_clicks_arrival) = process_date_input(departure_date_str,
                                                        arrival_date_str)

                airport_from, airport_to = process_airport_input(_from, _to)

                try:
                    results = backend_impl.run(airport_from,
                                            airport_to,
                                            date_departure,
                                            date_arrival,
                                            fixed_departure_month,
                                            fixed_arrival_month,
                                            next_clicks_departure,
                                            next_clicks_arrival)
                except Exception as e:
                    logging.error(e)
                    results = ((), ())

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

                push.send(json.dumps(routes, indent=4))

        disp.stop()


if __name__ == "__main__":
    main()
