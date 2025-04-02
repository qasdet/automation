def value_handler(value: int) -> str:
    """Функция возвращает строковое число через пробелы. Например 5555 вернет 5 555
        Args:
            value: Число
        Returns:
            Cтроковое число формата 0 000
    """
    formatted_value = "{:,.0f}".format(value).replace(",", " ")
    return str(formatted_value)


def value_handler_decimal(value: float | int) -> str:
    """Функция возвращает строковое число через пробелы. 5555 вернет '5 555,00'
        Args:
            value: Число с плавающей точкой
        Returns:
            Строковое число формата '0 000,00'
    """
    formatted_value = format(value, ',.2f').replace(',', ' ').replace('.', ',')
    return formatted_value


def value_handler_decimal_dot(value: float | int) -> str:
    """Функция возвращает строковое число через пробелы. 5555 вернет '5 555.00'
        Args:
            value: Число с плавающей точкой
        Returns:
            Строковое число формата '0 000.00'
    """
    formatted_value = format(value, ',.2f').replace(',', ' ')
    return formatted_value


def value_handler_decimal_prc(value: float | int) -> str:
    """Функция возвращает строку, представляющую число без "0" в конце, если число является целым значением,
    точка заменяется на запятую
        Args:
            value: Число с плавающей точкой
        Returns:
            Строковое число
    """
    if value.is_integer():
        return str(int(value))
    else:
        return str(value).replace(".", ",")
