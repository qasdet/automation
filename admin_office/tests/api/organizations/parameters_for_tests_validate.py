import pytest

from admin_office.tests.api.organizations.data_generator_for_organization import (
    INN_CONTROL_SUM_ERROR,
    INN_VALUE_ERROR,
    KPP_VALUE_ERROR,
    OGRN_CONTROL_SUM_ERROR,
    OGRN_VALUE_ERROR,
    PHONE_VALUE_ERROR,
)

data_for_validate_tests = [
    pytest.param(
        'phone',
        {
            '9076547': PHONE_VALUE_ERROR,
            '900aaaaa': PHONE_VALUE_ERROR,
            '+7901110111': PHONE_VALUE_ERROR,
        },
        id='phone',
    ),
    pytest.param(
        'inn',
        {
            '918273645': INN_VALUE_ERROR,
            '91827364567': INN_VALUE_ERROR,
            '9182736456127': INN_VALUE_ERROR,
            '89aaaooo9752': INN_VALUE_ERROR,
            '1234567890': INN_CONTROL_SUM_ERROR,
            '123456789012': INN_CONTROL_SUM_ERROR,
        },
        id='inn',
    ),
    pytest.param(
        'ogrn',
        {
            '1234567890986': OGRN_CONTROL_SUM_ERROR,
            'oooooaaaaaaa': OGRN_VALUE_ERROR,
            '501149857326': OGRN_VALUE_ERROR,
            '7111726340216': OGRN_CONTROL_SUM_ERROR,
            '50114985732611': OGRN_VALUE_ERROR,
            '304500116000112': OGRN_CONTROL_SUM_ERROR,
            '3045001160001571232': OGRN_VALUE_ERROR,
        },
        id='ogrn',
    ),
    pytest.param(
        'kpp',
        {'AAAA56789': KPP_VALUE_ERROR, '1111111111': KPP_VALUE_ERROR},
        id='kpp',
    ),
]
