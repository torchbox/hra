from django.utils.datetime_safe import date


def range_month(start_date, end_date):
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
