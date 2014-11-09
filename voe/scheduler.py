from datetime import datetime, timedelta

def daterange(start_date, end_date):
    for n in range(int ((end_date - start_date).days)):
        yield start_date + timedelta(n)


def gen_dates(days=270):
    start_date = datetime.now()
    end_date = start_date + timedelta(days=days)

    dates = []

    for single_date in daterange(start_date, end_date):
        dates.append(single_date)

    return dates

def iterate(dates, increment=1):
    for element in range(0, len(dates), increment):
        yield dates[element]
