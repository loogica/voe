# coding: utf-8

import logging
import os
import re
import sys
import time

from datetime import date, datetime

from logging import log

DEFAULT_WAIT = 0.2

def execute_js(browser, script):
    logging.debug(script)
    result = browser.execute_script(script)
    time.sleep(DEFAULT_WAIT)
    return result

def get_day(date):
    return date.split("/")[0]

def process_airport_input(_from, to):
    airport_from, airport_to = None, None
    if _from and to:
        airport_from = _from
        airport_to = to
    elif len(sys.argv) < 6:
        airport_from = input("Partida: ")
        airport_to = input("Destino: ")
    else:
        airport_from = sys.argv[4]
        airport_to = sys.argv[5]
    return airport_from, airport_to

def check_command_line_dates():
    dep_date, arr_date = None, None
    if len(sys.argv) < 4:
        dep_date = input("Data de Ida (DD/MM): ")
        arr_date = input("Data de Volta (DD/MM): ")
    else:
        dep_date = sys.argv[2]
        arr_date = sys.argv[3]
    return dep_date, arr_date

def process_date_input_1(departure, arrival):
    if departure and arrival:
        date_departure = departure
        date_arrival = arrival
    else:
        date_departure, date_arrival = check_command_line_dates()

    dep_day = date_departure.split("/")[0]
    arr_day = date_arrival.split("/")[0]
    dep_mo = int(date_departure.split("/")[1])
    arr_mo = int(date_arrival.split("/")[1])
    today = date.today()

    fixed_dep_mo = dep_mo - today.month + 1
    fixed_arr_mo = arr_mo - today.month + 1

    next_clicks_dep = dep_mo - today.month
    next_clicks_arr = arr_mo - today.month - next_clicks_dep

    return (date_departure, date_arrival, fixed_dep_mo, fixed_arr_mo,
            next_clicks_dep, next_clicks_arr)


def process_date_input(departure, arrival):
    if departure and arrival:
        date_departure = departure
        date_arrival = arrival
    else:
        date_departure, date_arrival = check_command_line_dates()

    dep_day = date_departure.split("/")[0]
    arr_day = date_arrival.split("/")[0]
    dep_mo = int(date_departure.split("/")[1])
    arr_mo = int(date_arrival.split("/")[1])
    today = date.today()

    fixed_dep_mo = dep_mo - 1
    fixed_arr_mo = arr_mo - 1

    next_clicks_dep = dep_mo - today.month
    next_clicks_arr = arr_mo - today.month - next_clicks_dep

    return (date_departure, date_arrival, fixed_dep_mo, fixed_arr_mo,
            next_clicks_dep, next_clicks_arr)

PRICE_REGEX = re.compile('.*R\$ (\d+\.*\d+,\d{2})')

def get_price(price):
    regex = PRICE_REGEX.search(price)
    if regex:
        return regex.group(1)
    return None

DATE_REGEX_GOL = re.compile('\w*(\d{2}) (\w{3}).*')
DATE_REGEX_GOL2 = re.compile('\w*(\d{1}) (\w{3}).*')
DATE_REGEX_AZUL = re.compile('\w*(\d{2})/(\w{3}).*')

def get_date(date):
    regex = DATE_REGEX_GOL.search(date)
    regex2 = DATE_REGEX_GOL2.search(date)
    regex3 = DATE_REGEX_AZUL.search(date)
    if regex:
        return regex.group(1), regex.group(2)
    if regex2:
        return regex2.group(1), regex2.group(2)
    if regex3:
        return regex3.group(1), regex3.group(2)
    return None

MONTHS_PT = [
    'janeiro',
    'fevereiro',
    'março',
    'abril',
    'maio',
    'junho',
    'julho',
    'agosto',
    'setembro',
    'outubro',
    'novembro',
    'dezembro'
]

MONTHS_PT_3 = map(lambda x: x[0:3], MONTHS_PT)

def month_from_alias(alias):
    return MONTHS_PT_3.index(alias.lower()) + 1

def parse_date(_date):
    month = month_from_alias(_date[1])
    day = int(_date[0])

    now = date.today()
    current_year = now.year
    current_month = now.month

    if month < current_month:
        current_year += 1

    try:
        _date = date(current_year, month, day)
    except:
        print(locals())
        return None
    return _date

def create_today_dir(path):
    timestamp = datetime.now().strftime("%Y%m%d%H%M")
    new_path = os.path.join(path, timestamp)
    if not os.path.exists(new_path):
        os.mkdir(new_path)
    return new_path

