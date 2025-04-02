from datetime import date, datetime

from dateutil.relativedelta import relativedelta


def get_default_campaign_begin_date_for_api():
    """Функция возвращает дефолтную дату начала кампании в формате yyyy-mm-dd"""
    default_campaign_start_date = (
        date.today() + relativedelta(months=+1)
    ).strftime('20%y-%m-01')
    return default_campaign_start_date


def get_default_campaign_end_date_for_api():
    """Функция возвращает дефолтную дату завершения кампании в формате yyyy-mm-dd"""
    default_campaign_end_date = (
        datetime.strptime(
            ((date.today() + relativedelta(months=+1)).strftime('20%y-%m-01')),
            '20%y-%m-%d',
        )
        + relativedelta(days=+59)
    ).strftime('20%y-%m-%d')
    return default_campaign_end_date


def get_default_campaign_begin_date_for_ui():
    """Функция возвращает дефолтную дату начала кампании для в формате dd.mm.yyyy"""
    default_campaign_start_date = (
        date.today() + relativedelta(months=+1)
    ).strftime('01.%m.20%y')
    return default_campaign_start_date


def get_default_campaign_end_date_for_ui():
    """Функция возвращает дефолтную дату завершения кампании в формате dd.mm.yyyy"""
    default_campaign_end_date = (
        datetime.strptime(
            ((date.today() + relativedelta(months=+1)).strftime('01.%m.20%y')),
            '%d.%m.20%y',
        )
        + relativedelta(days=+59)
    ).strftime('%d.%m.20%y')
    return default_campaign_end_date
