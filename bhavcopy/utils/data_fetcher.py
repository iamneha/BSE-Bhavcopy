#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import zipfile
import io
import csv
import logging
import time
from datetime import datetime, timedelta
from urllib.request import urlopen  # python3

logger = logging.getLogger(__name__)

base_url = "https://www.bseindia.com/download/BhavCopy/Equity/EQ{date}_CSV.ZIP"


def get_valid_date(input_date=None):
    _date_format = '%d%m%y'
    if input_date:
        try:
            input_date = datetime.strptime(input_date, _date_format)
        except ValueError:
            logger.error("input_date is not in right format 'DDMMYY'")
    else:
        # No data for current date so yesterday's data as latest input data
        input_date = datetime.today() - timedelta(1)

    if input_date.weekday() == 5:  # no data for SATURDAY so taking friday
        return get_valid_date(
            (input_date - timedelta(1)).strftime(_date_format)
        )

    if input_date.weekday() == 6:  # no data for SUNDAY so taking friday
        return get_valid_date(
            (input_date - timedelta(2)).strftime(_date_format)
        )
    return input_date.strftime(_date_format)


def extract_data(input_date=None):

    # can also pass date in perticular format 'DDMMYY' for equity report
    date = get_valid_date(input_date)

    csv_file = 'EQ{date}.CSV'.format(date=date)
    response = urlopen(base_url.format(date=date))
    _zip = zipfile.ZipFile(io.BytesIO(response.read()))
    csv_reader = csv.DictReader(io.TextIOWrapper(_zip.open(csv_file)))

    # processing csv file
    return csv_reader


def store_data(DBModel, input_date=None):
    while True:
        rows = extract_data(input_date)
        db_input = [{
            'name': row.get('SC_NAME'),
            'value': [
                row.get('SC_CODE'),
                row.get('OPEN'),
                row.get('HIGH'),
                row.get('LOW'),
                row.get('CLOSE')
            ]
        } for row in rows]
        DBModel(db_input)
        time.sleep(86400)
