import random
import string

from faker import Faker

fake = Faker('ru_RU')

ERRORS_ABOUT_UNIQUENESS = [
    'указанный Email уже используется',
    'указанный ИНН и КПП уже используется',
    'указанный ОГРН/ОГРНИП уже используется',
    'указанный номер телефона уже используется',
]

EMPTY_KPP_ERROR = 'КПП: отсутствует реквизит'
FILLED_KPP_ERROR = 'КПП: у ИП такого реквизита нет'
KPP_VALUE_ERROR = 'КПП: должен состоять из 9 символов. Содержит только буквенно-цифровые символы'
PHONE_VALUE_ERROR = 'номер телефона должен состоять из 11 символов. Содержит только цифровые символы'
INN_VALUE_ERROR = (
    'ИНН: должен состоять из 10 символов(для организации) '
    'или из 12 символов(для физического лица). Содержит только цифровые символы'
)
INN_CONTROL_SUM_ERROR = 'ИНН: контрольная сумма не совпала'

OGRN_VALUE_ERROR = 'должен состоять из 13/15 символов соответственно. Содержит только цифровые символы'
OGRN_CONTROL_SUM_ERROR = 'ОГРН/ОГРНИП: контрольная сумма не совпала'


def inn_control_type_sum(
    number_without_check_digit: str, type_coefficient: str
) -> int:
    """Подсчет контрольной суммы
    10-значный ИНН:
        - Вычислить сумму произведений цифр ИНН (с 1-й по 9-ю)
        на следующие коэффициенты — 2, 4, 10, 3, 5, 9, 4, 6, 8
        (т.е. 2 * ИНН[1] + 4 * ИНН[2] + ...).
        - Вычислить остаток от деления полученной суммы на 11 (проверочное число ИНН)
    12-значный ИНН
        1. Вычислить 1-ю контрольную цифру:
            - Вычислить сумму произведений цифр ИНН (с 1-й по 10-ю)
            на следующие коэффициенты — 7, 2, 4, 10, 3, 5, 9, 4, 6, 8
            (т.е. 7 * ИНН[1] + 2 * ИНН[2] + ...).
            - Вычислить младший разряд остатка от деления полученной суммы на 11
            (первое проверочное число ИНН)
        2. Вычислить 2-ю контрольную цифру:
            - Вычислить сумму произведений цифр ИНН (с 1-й по 11-ю)
            на следующие коэффициенты — 3, 7, 2, 4, 10, 3, 5, 9, 4, 6, 8
            (т.е. 3 * ИНН[1] + 7 * ИНН[2] + ...).
            - Вычислить младший разряд остатка от деления полученной суммы на 11
            (второе проверочное число ИНН)

    Args:
        number_without_check_digit: ИНН без контрольной цифры
        type_coefficient: Тип коэффициентов
    Returns:
        Возвращаем контрольную цифру
    """
    inn_control_types = {
        'coefficients_1_12': [3, 7, 2, 4, 10, 3, 5, 9, 4, 6, 8],
        'coefficients_2_12': [7, 2, 4, 10, 3, 5, 9, 4, 6, 8],
        'coefficients_10': [2, 4, 10, 3, 5, 9, 4, 6, 8],
    }
    n = 0
    inn_control_type = inn_control_types[type_coefficient]
    for i in range(0, len(inn_control_type)):
        n += int(number_without_check_digit[i]) * inn_control_type[i]
    return n % 11 % 10


def inn_generator(length: int = 10) -> str:
    """Генерация ИНН
    ИНН для юр. лиц (состоит из 10 символов):
        1-4-ый знаки:
            для российской организации — код налогового органа, который присвоил ИНН;
            для иностранной организации — индекс, определяемый Федеральной налоговой службой;
        5-9-й знаки:
            для российской организации — порядковый номер записи о лице в территориальном разделе
            Единого государственного реестра налогоплательщиков налогового органа,
            который присвоил ИНН;
            для иностранной организации — код иностранной организации (КИО) согласно Справочнику
            «Коды иностранных организаций»;
        10-й знак — контрольное число

    ИНН для индивидуального предпринимателя (состоит из 12 символов):

        1-4-й знак — код налогового органа, который присвоил ИНН;
        5-10-й знаки — порядковый номер записи о лице в территориальном разделе
        Единого государственного реестра налогоплательщиков налогового органа, который присвоил ИНН;
        11-12-знакиы — контрольное число.

    Args:
        length: Длина ИНН (10 - юр. лицо, 12 - ИП)
    Returns:
        Возвращаем ИНН в виде строки
    """
    number_without_check_digit = fake.lexify(
        text='?????????' if length == 10 else '??????????',
        letters=string.digits,
    )
    if length == 12:
        check_digit_2 = inn_control_type_sum(
            number_without_check_digit, 'coefficients_2_12'
        )
        number_without_check_digit = number_without_check_digit + str(
            check_digit_2
        )
        check_digit_1 = inn_control_type_sum(
            number_without_check_digit, 'coefficients_1_12'
        )
        return f'{number_without_check_digit}{check_digit_1}'
    else:
        check_digit_1 = inn_control_type_sum(
            number_without_check_digit, 'coefficients_10'
        )
        return f'{number_without_check_digit}{check_digit_1}'


def kpp_generator() -> str:
    """КПП для юр. лиц (для ИП нет этого параметра)

    1-й и 2-й знак — Код региона РФ
    3-й и 4-й знак — Номер ИФНС, поставившей организацию на учет
    3-й и 4-й знак — Код причины постановки на учет
    7-9-й знаки — Порядковый номер постановки на учет по конкретной причине

    Returns:
        Возвращаем ОГРН в виде строки
    """
    subject_of_the_rf = str(random.randint(1, 89)).zfill(2)
    tax_service_number = str(random.randint(1, 99)).zfill(2)
    # наиболее распространенные коды причины постановки на учет
    registration_reason_code = random.choice(['01', '43', '44', '45', '50'])
    serial_number = fake.lexify(text='???', letters=string.digits)
    return f'{subject_of_the_rf}{tax_service_number}{registration_reason_code}{serial_number}'


def ogrn_generator(length: int = 13) -> str:
    """ОГРН для юр. лиц (13 символов)
    1-й знак — признак отнесения государственного регистрационного номера записи:
        к основному государственному регистрационному номеру (ОГРН) — 1, 5;
    2-3-й знаки — две последние цифры года внесения записи;
    4-5-й знаки — код субъекта Российской Федерации;
    6-12-й знаки — номер записи, внесенной в государственный реестр;
    13-й знаки — проверочное число ОГРН
    Как вычислить проверочное число:
        - остаток от деления предыдущего 12-значного числа на 11
        - если остаток от деления равен 10, то контрольное число равно 0 (нулю)

    ОГРНИП для ИП (15 символов)
        1-й знак ОГРНИП всегда «3», это его отличительная черта
        2-й и 3-й — год, в котором присвоен статус ИП (последние 2 цифры)
        4-й и 5-й — субъект РФ по общепринятой кодировке согласно Конституции
        6-й и 7-й — номер налоговой службы, которая производила выдачу
        8-14-й — порядковый номер записи регистрационного органа
        15-й — проверочное число ОГРНИП
        Как вычислить проверочное число:
        - остаток от деления предыдущего 14-значного числа на 13
        - если остаток от деления равен 10, то контрольное число равно 0 (нулю)

    Args:
        length: Длина ОГРН (13 - юр. лицо, 15 - ИП)
    Returns:
        Возвращаем ОГРН в виде строки
    """
    first_number = random.choice([1, 5]) if length == 13 else 3
    year_of_registration = str(random.randint(0, 99)).zfill(2)
    subject_of_the_rf = str(random.randint(1, 89)).zfill(2)
    tax_service_number = (
        '' if length == 13 else str(random.randint(1, 99)).zfill(2)
    )
    serial_number = fake.lexify(text='???????', letters=string.digits)
    number_without_check_digit = int(
        f'{first_number}{year_of_registration}{subject_of_the_rf}{tax_service_number}{serial_number}'
    )
    denominator = 11 if length == 13 else 13
    check_digit = number_without_check_digit % denominator
    return f'{number_without_check_digit}{check_digit % 10 if check_digit >= 10 else check_digit}'


def name_organization() -> str:
    """Название организации

    Returns:
        Возвращаем название в виде строки
    """
    return fake.word().capitalize()


def address_organization() -> str:
    """Адрес организации

    Returns:
        Возвращаем адрес в виде строки
    """
    return fake.address()


def email_organization() -> str:
    """e-mail организации

    Returns:
        Возвращаем e-mail в виде строки
    """
    return fake.email()


def phone_organization() -> str:
    """Телефон организации

    Returns:
        Возвращаем телефон в виде строки
    """
    # fake.phone_number() вернуть, когда будет добавлена маска со стороны фронтенда
    return fake.lexify(text='9?????????', letters=string.digits)
