"""Helper functions that may be used throughout the application"""

from datetime import datetime

FITBIT_DATETIME_FORMAT = "%Y-%m-%d"

def validate_date_range(begin_date, end_date):
    """begin_date and end_date should both be dates (not datetimes)"""
    if begin_date is None:
        begin_date = datetime.today().date()
    if end_date is None:
        end_date = datetime.today().date()
    if end_date < begin_date:
        msg = ("begin_date={} must be less than or equal to end_date={}"
                    .format(begin_date, end_date))
        raise ValueError(msg)
    return (begin_date, end_date)

def fitbit_datetime_to_date(str_date):
    """Convert a string of the form YYYY-MM-DD to a date"""
    return datetime.strptime(str_date, FITBIT_DATETIME_FORMAT).date()