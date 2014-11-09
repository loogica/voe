import logging
import time
import sys

from functools import partial
from datetime import datetime
from string import Template

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from voe.util import get_day, execute_js, get_date, parse_date, get_price

WAIT = 1

def run(airport_from, airport_to, departure_date, arrival_date,
        fixed_departure_month, fixed_arrival_month, next_clicks_departure,
        next_clicks_arrival):
    departure_day = get_day(departure_date)
    arrival_day = get_day(arrival_date)

    browser = webdriver.Firefox()
    browser.get('http://www.voeazul.com.br/')

    browser.close()
    return [], []

    executer = partial(execute_js, browser)

    executer("$('.origem a').click();")
    script = Template("""
        $$('.origem ul.aeroporto ul li').each(function(i, el) {
            var x = $$(el).attr('onclick');
            if (x.search('$airport') > 0) {
                el.click();
            }
        });
    """).substitute(airport=airport_from)
    executer(script)

    executer("$('.destino a').click();")

    script = Template("""
        $$('.destino ul.aeroporto ul li').each(function(i, el) {
            var x = $$(el).attr('onclick');
            if (x.search('$airport') > 0) {
                el.click();
            }
        });
    """).substitute(airport=airport_to)
    executer(script)

    for i in range(next_clicks_departure):
        executer("$('.ui-icon-circle-triangle-e').click()")

    script = Template("""
        $$($$('#ui-datepicker-div table tbody')[0]).find('td').each(
            function(i, el) {
                var num = $$(el).text();
                if (num == '$n') {
                    $$(el).click();
                }
            }
        );
    """).substitute(n=departure_day)

    executer(script)

    for i in range(next_clicks_arrival):
        executer("$('.ui-icon-circle-triangle-e').click()")

    script = Template("""
        $$($$('#ui-datepicker-div table tbody')[0]).find('td').each(
            function(i, el) {
                var num = $$(el).text();
                if (num == '$n') {
                    $$(el).click();
                }
            }
        );
    """).substitute(n=arrival_day)

    executer(script)

    executer('$("#btn-idaevolta").click();')

    script = """
        var prices = [];
        $('#GoingPrices ul.tabset li').each(function(i, el) {
            var date = $(el).find('span').text();
            var price = $(el).find('div').text();
            prices.push({'date': date, 'price': price});
        });
        return prices;
    """

    prices = executer(script)

    departure_result = []
    for price in prices:
        if price['date']:
            date = parse_date(get_date(price['date']))
            price = price['price']
            logging.info(dict(price=price, date=date))
            departure_result.append(dict(price=price, date=date))

    script = """
        var prices = [];
        $('#BackPrices ul.tabset li').each(function(i, el) {
            var date = $(el).find('span').text();
            var price = $(el).find('div').text();
            prices.push({'date': date, 'price': price});
        });
        return prices;
    """

    prices = executer(script)

    arrival_result = []
    for price in prices:
        if price['date']:
            date = parse_date(get_date(price['date']))
            price = price['price']
            logging.info(dict(price=price, date=date))
            arrival_result.append(dict(price=price, date=date))

    browser.quit()
    return departure_result, arrival_result

if __name__ == "__main__":
    main()

