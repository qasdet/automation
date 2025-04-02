from datetime import datetime
from dateutil.relativedelta import relativedelta
from calendar import monthrange


def get_count_of_days_by_dates(start_date, end_date):
    """Функция возвращает количество дней по месяцам в зависимости от принимаемых дат
        Args:
            start_date: дата начала периода
            end_date: дата завершения периода
        Returns:
            Словарь, где в качестве ключей названия месяца и год, а в качестве значений кол-во дней"""
    month_names = {
        1: 'Январь',
        2: 'Февраль',
        3: 'Март',
        4: 'Апрель',
        5: 'Май',
        6: 'Июнь',
        7: 'Июль',
        8: 'Август',
        9: 'Сентябрь',
        10: 'Октябрь',
        11: 'Ноябрь',
        12: 'Декабрь'
    }
    start_date = datetime.strptime(start_date, "%d.%m.20%y").date()
    end_date = datetime.strptime(end_date, "%d.%m.20%y").date()
    days_in_months = {}
    month = start_date
    while month <= end_date:
        i, last_day = monthrange(month.year, month.month)
        first_day = start_date.day if month.month == start_date.month else 1
        last_day = end_date.day if month.month == end_date.month and month.year == end_date.year else last_day
        days_in_month = last_day - first_day + 1
        key = f"{month_names[month.month]} {str(month.year)[2:]}"
        days_in_months[key] = days_in_month
        month += relativedelta(months=1)
    return days_in_months
