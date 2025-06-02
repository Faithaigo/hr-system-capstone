import datetime


def calculate_difference(start_date, end_date):
    """
    Calculate the difference between two dates
    :param start_date:
    :param end_date:
    :return:
    """
    begin_date = datetime.datetime.strptime(str(start_date), '%Y-%m-%d')
    end_date = datetime.datetime.strptime(str(end_date), '%Y-%m-%d')

    difference = end_date - begin_date
    return difference.days + 1