# coding: utf-8
import logging

from datetime import datetime
import time

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from voe.util import get_day, get_price, get_date, parse_date

WAIT = 1

def run(airport_from, airport_to, departure_date, arrival_date,
        fixed_departure_month, fixed_arrival_month, next_clicks_departure,
        next_clicks_arrival):
    departure_day = get_day(departure_date)
    arrival_day = get_day(arrival_date)

    browser = webdriver.Firefox()
    browser.get('http://compre2.voegol.com.br/Search.aspx?culture=pt-BR')

    el = browser.find_element_by_id('ControlGroupSearchView_AvailabilitySearchInputSearchView_TextBoxMarketOrigin1')
    el.send_keys(airport_from)
    dest = browser.find_element_by_xpath('//div[@airportcode="{}"]'.format(airport_from))
    dest.click()

    el = browser.find_element_by_id('ControlGroupSearchView_AvailabilitySearchInputSearchView_TextBoxMarketDestination1')
    el.send_keys(airport_to)
    dest = browser.find_element_by_xpath('//div[@airportcode="{}"]'.format(airport_to))
    dest.click()

    for i in range(next_clicks_departure):
        el = browser.find_element_by_xpath('//span[@class="ui-icon ui-icon-circle-triangle-e"]')
        el.click()
        time.sleep(0.5)

    dt_ida = browser.find_elements_by_xpath('//td[@data-month="{}"]'.format(fixed_departure_month))
    for el in dt_ida:
        if el.text == departure_day:
            el.click()
            break

    time.sleep(0.5)

    #el = browser.find_element_by_xpath('//div[@class="formBox formCellDiv13"]')
    #cal = el.find_elements_by_xpath('//div[@class="inpTxt01"]')
    #cal.click()
    time.sleep(0.5)

    next_clicks_arrival = 2

    for i in range(next_clicks_arrival):
        el = browser.find_element_by_xpath('//span[@class="ui-icon ui-icon-circle-triangle-e"]')
        el.click()
        time.sleep(0.5)

    dt_volta = browser.find_elements_by_id('dt_volta')
    dt_volta = browser.find_elements_by_xpath('//td[@data-month="{}"]'.format(fixed_arrival_month))
    for el in dt_volta:
        if el.text == arrival_day:
            el.click()
            break

    time.sleep(WAIT)
    browser.execute_script('document.getElementById("ControlGroupSearchView_ButtonSubmit").click();')

    _from = browser.find_element_by_xpath('//div[@class="sliderDates sliderGoing"]')
    to = browser.find_element_by_xpath('//div[@class="sliderDates sliderReturn"]')

    els = browser.find_elements_by_xpath('//div[@class="sliderDates sliderGoing"]/ul[@class="listDates"]/li')

    departure_result = []
    for el in els:
        price = get_price(el.text)
        date = parse_date(get_date(el.text))
        logging.info(dict(price=price, date=date))
        departure_result.append(dict(price=price, date=date))

    els = browser.find_elements_by_xpath('//div[@class="sliderDates sliderReturn"]/ul[@class="listDates"]/li')
    arrival_result = []
    for el in els:
        price = get_price(el.text)
        date = parse_date(get_date(el.text))
        logging.info(dict(price=price, date=date))
        arrival_result.append(dict(price=price, date=date))

    browser.quit()
    return departure_result, arrival_result


if __name__ == "__main__":
    main()
