"""Helper functions that may be used throughout the application"""

from datetime import datetime, timedelta, date
from django.utils import timezone

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


def daterange(begin_date, end_date, inclusive=False):
    """
    Used to iterate through dates in the given range.  begin_date is always
    included.  end_date is only included if inclusive is set to True.
    """
    num_days = int((end_date - begin_date).days)
    if inclusive:
        num_days += 1
    for num in range(num_days):
        yield begin_date + timedelta(num)

def update_quest(quest):
    """
    Check if we have updated the quest from fitbit recently.  If not,
    update.
    """
    # update database at most once an hour
    now = timezone.now()
    mins_since_last_updated = (now - quest.users_last_updated).seconds / 60
    if mins_since_last_updated > 0:
        quest.update_from_fitbit()
        