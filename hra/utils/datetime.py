from dateutil.relativedelta import relativedelta
from django.utils.datetime_safe import date


def range_month(start_date, end_date):
    """
    Generates range of a months from `start_date` to `end_date`.
    """

    current_year = start_date.year
    current_month = start_date.month

    yield date(current_year, current_month, 1)

    while current_year != end_date.year or current_month != end_date.month:
        if current_month % 12 == 0:
            current_year += 1
            current_month = 1
        else:
            current_month += 1

        yield date(current_year, current_month, 1)


def iter_between_dates(start_date, end_date, step_days):
    """
    Generates range of dates from `start_date` to `end_date`.
    Each step will be no longer than `step_days` days.
    """
    def increment_date():
        result = current_start_date + relativedelta(days=step_days)

        if result > end_date:
            result = end_date

        return result

    current_start_date = start_date
    current_end_date = increment_date()
    yield current_start_date, current_end_date

    while current_end_date < end_date:
        current_start_date = current_end_date + relativedelta(days=1)
        current_end_date = increment_date()
        yield current_start_date, current_end_date
