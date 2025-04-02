import datetime


def date_converter_russian_notation(source_date: str) -> str:
    """Переводит дату из формата 'YYYY-MM-DDTHH:MM:SSZ' в формат 'DD.MM.YYYY'
    Args:
        source_date: 'YYYY-MM-DDTHH:MM:SSZ' в таком формате отдаём дату
    Returns:
        На выходе получаем эту же дату, но в формате 'DD.MM.YYYY' и без времени
    """
    source_date_without_time = source_date.split('T')[0].replace('-', '.')
    correct_date = datetime.datetime.strptime(
        source_date_without_time, '%Y.%m.%d'
    ).strftime('%d.%m.%Y')
    return correct_date
