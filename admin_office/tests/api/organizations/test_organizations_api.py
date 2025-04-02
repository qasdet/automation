import allure
import pytest

from datetime import datetime
from helper.array_helper import compare_the_response_from_service_with_expected_response
from admin_office.api_interactions.organizations.organization_api_interactions import (
    activate_organization,
    blocked_organization,
    create_organization,
    edit_organization,
    formatted_date_without_timezone,
    get_specified_amount_of_organizations,
    get_specified_amount_of_organizations_from_db,
)
from admin_office.tests.api.organizations.data_generator_for_organization import (
    EMPTY_KPP_ERROR,
    ERRORS_ABOUT_UNIQUENESS,
    FILLED_KPP_ERROR,
    kpp_generator,
)
from admin_office.tests.api.organizations.data_make_for_organization import (
    make_data_all_individual_entrepreneur_fields,
    make_data_all_legal_entity_fields,
    make_data_for_required_individual_entrepreneur_fields,
    make_the_expected_response,
)
from admin_office.tests.api.organizations.parameters_for_tests_validate import (
    data_for_validate_tests,
)
from db_stuff.db_interactions.organizations_db_interactions import (
    delete_organization_by_id,
)
from helper.linkshort import AllureLink as case
from helper.linkshort import JiraLink as jira

actions = ['create', 'edit']


@pytest.fixture(params=actions)
def create_or_edit_organization_with_errors(
        request,
        authorization_in_admin_office_with_token
):
    """
    Фикстура позволяет создавать, либо редактировать организацию с ошибками, в зависимости от заданного параметра.
    """
    organization_data = make_data_all_legal_entity_fields()
    response_data = {}
    token = authorization_in_admin_office_with_token
    args = {
        'token': token,
        'data_organization': organization_data,
        'with_error': True,
    }
    if request.param == 'create':
        method = create_organization
    else:
        response_data = create_organization(token, organization_data)
        method = edit_organization
        args.update({'organization_id': response_data['id']})
    yield args, method
    if request.param == 'edit':
        delete_organization_by_id(response_data['id'])


@pytest.fixture
def life_cycle_of_the_organization_with_all_field_api(
    authorization_in_admin_office_with_token,
):
    """
    Фикстура заполняет все поля создаваемой организации
    """
    organization_data = (
        make_data_all_legal_entity_fields()
    )  # Данные для юр. лица (ИНН+КПП)
    response_data = create_organization(
        authorization_in_admin_office_with_token, organization_data
    )
    yield organization_data, response_data
    delete_organization_by_id(response_data['id'])


@pytest.fixture
def life_cycle_of_the_organization_with_required_field(
    authorization_in_admin_office_with_token,
):
    """
    Фикстура заполняет только необходимые поля при создании организации.
    """
    organization_data = (
        make_data_for_required_individual_entrepreneur_fields()
    )  # Данные для ИП (только ИНН)
    response_data = create_organization(
        authorization_in_admin_office_with_token, organization_data
    )
    yield organization_data, response_data
    delete_organization_by_id(response_data['id'])


@pytest.mark.usefixtures('authorization_in_admin_office_with_token')
class TestsOrganizationsAPI:
    @staticmethod
    @pytest.mark.regress()
    @allure.title(
        'Тест проверяет действия над организацией со всем заполненными полями через API'
    )
    @allure.story(jira.JIRA_LINK + 'MDP-1013')
    @allure.testcase(case.ALLURE_LINK + '124595?treeId=289')
    @allure.severity(allure.severity_level.NORMAL)
    def test_life_cycle_of_the_organization_with_all_field(
        life_cycle_of_the_organization_with_all_field_api,
        authorization_in_admin_office_with_token,
    ):
        """Тест проверяет действия над организацией со всем заполненными полями
        - создание (организация как юр. лидо, т.е. ИНН+КПП) через фикстуры
        - редактирование (изменение всех полей)
        - активация
        - блокировка
        - получение записи по id
        - удаление из БД (через фикстуру)
        """
        token = authorization_in_admin_office_with_token
        # Проверка после создания
        (
            organization_data,
            response_data,
        ) = life_cycle_of_the_organization_with_all_field_api
        expected_response = make_the_expected_response(
            response_data['id'], organization_data
        )
        response_data['registeredAt'] = formatted_date_without_timezone(
            response_data['registeredAt']
        )
        compare_the_response_from_service_with_expected_response(
            response_data, expected_response
        )

        # Редактирование
        organization_data_new = make_data_all_legal_entity_fields()
        expected_response = make_the_expected_response(
            response_data['id'],
            organization_data_new,
            expected_response['registeredAt'],
        )
        response_data = edit_organization(
            token, response_data['id'], organization_data_new
        )
        response_data['registeredAt'] = formatted_date_without_timezone(
            response_data['registeredAt']
        )
        compare_the_response_from_service_with_expected_response(
            response_data, expected_response
        )

        # Активация
        response_data = activate_organization(token, response_data['id'])
        expected_response['status'] = 'active'
        response_data['registeredAt'] = formatted_date_without_timezone(
            response_data['registeredAt']
        )
        compare_the_response_from_service_with_expected_response(
            response_data, expected_response
        )

        # Блокировка
        response_data = blocked_organization(token, response_data['id'])
        expected_response['status'] = 'blocked'
        expected_response['blockedAt'] = datetime.now().strftime(
            '%Y-%m-%dT%H:%M'
        )
        response_data['blockedAt'] = formatted_date_without_timezone(
            response_data['blockedAt']
        )
        response_data['registeredAt'] = formatted_date_without_timezone(
            response_data['registeredAt']
        )
        compare_the_response_from_service_with_expected_response(
            response_data, expected_response
        )

    @staticmethod
    @pytest.mark.regress()
    @allure.title(
        'Тест проверяет действия над организацией с обязательными полями через API'
    )
    @allure.story(jira.JIRA_LINK + 'MDP-1013')
    @allure.testcase(case.ALLURE_LINK + '125166?treeId=289')
    @allure.severity(allure.severity_level.NORMAL)
    def test_life_cycle_of_the_organization_with_required_field(
        life_cycle_of_the_organization_with_required_field,
        authorization_in_admin_office_with_token,
    ):
        """Тест проверяет действия над организацией с обязательными полями

        - создание (организация как ИП, т.е. только ИНН) через фикстуры
        - редактирование (изменение всех обязательных полей)
        - удаление из БД (через фикстуру)
        """
        # Проверка после создания
        (
            organization_data,
            response_data,
        ) = life_cycle_of_the_organization_with_required_field
        token = authorization_in_admin_office_with_token
        expected_response = make_the_expected_response(
            response_data['id'], organization_data
        )
        response_data['registeredAt'] = formatted_date_without_timezone(
            response_data['registeredAt']
        )
        compare_the_response_from_service_with_expected_response(
            response_data, expected_response
        )

        # Редактирование
        organization_data_new = (
            make_data_for_required_individual_entrepreneur_fields()
        )
        expected_response = make_the_expected_response(
            response_data['id'],
            organization_data_new,
            expected_response['registeredAt'],
        )
        response_data = edit_organization(
            token, response_data['id'], organization_data_new
        )
        response_data['registeredAt'] = formatted_date_without_timezone(
            response_data['registeredAt']
        )
        compare_the_response_from_service_with_expected_response(
            response_data, expected_response
        )

    @staticmethod
    @pytest.mark.regress()
    @allure.title(
        'Проверка метода получения указанного количества записей отсортированных по статусу'
    )
    @allure.story(jira.JIRA_LINK + 'MDP-1013')
    @allure.severity(allure.severity_level.NORMAL)
    def test_get_specified_amount_of_organizations(
        authorization_in_admin_office_with_token,
    ):
        """Проверка метода получения указанного количества записей отсортированных по статусу"""
        token = authorization_in_admin_office_with_token
        rows_from_service = get_specified_amount_of_organizations(token)
        rows_from_db = get_specified_amount_of_organizations_from_db()
        assert len(rows_from_service) == len(
            rows_from_db
        ), 'Количество записей от сервиса не равно количеству из БД'
        # Ожидаем, что сервис и БД вернет записи в одинаковом порядке
        assert (
                rows_from_service == rows_from_db
        ), 'Данные с сервиса не совпадают с данными из БД'

    @staticmethod
    @pytest.mark.regress()
    @allure.title(
        'Проверка уникальных значений полей (телефон, инн, кпп, e-mail, огрн)'
    )
    @allure.story(jira.JIRA_LINK + 'MDP-1013')
    @allure.severity(allure.severity_level.NORMAL)
    def test_validation_about_uniqueness(
        life_cycle_of_the_organization_with_all_field_api,
        authorization_in_admin_office_with_token,
    ):
        """Проверка уникальных значений полей (телефон, инн, кпп, e-mail, огрн)"""
        token = authorization_in_admin_office_with_token
        (
            organization_data,
            response_data,
        ) = life_cycle_of_the_organization_with_all_field_api
        # Полный дубль
        response_errors = create_organization(
            token, organization_data, with_error=True
        )
        print(response_errors)
        errors_messages = sorted([msg['message'] for msg in response_errors])
        assert ERRORS_ABOUT_UNIQUENESS == errors_messages

        organization_data = make_data_all_legal_entity_fields()
        organization_data.pop('kpp')
        response_errors = create_organization(
            token, organization_data, with_error=True
        )
        assert len(
            response_errors
        ) == 1 and EMPTY_KPP_ERROR in response_errors[0].get('message')

        response_errors = edit_organization(
            token, response_data['id'], organization_data, with_error=True
        )
        assert len(
            response_errors
        ) == 1 and EMPTY_KPP_ERROR in response_errors[0].get('message')

        organization_data = make_data_all_individual_entrepreneur_fields()
        organization_data['kpp'] = kpp_generator()
        response_errors = create_organization(
            token, organization_data, with_error=True
        )
        assert len(
            response_errors
        ) == 1 and FILLED_KPP_ERROR in response_errors[0].get('message')

        response_errors = edit_organization(
            token, response_data['id'], organization_data, with_error=True
        )
        assert len(
            response_errors
        ) == 1 and FILLED_KPP_ERROR in response_errors[0].get('message')

    @staticmethod
    @pytest.mark.regress()
    @allure.story(jira.JIRA_LINK + 'MDP-1013')
    @allure.testcase(case.ALLURE_LINK + '124600?treeId=289')
    @allure.story(jira.JIRA_LINK + 'MDP-4444')
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.parametrize('key, invalid_values', data_for_validate_tests)
    def test_validate_all_field(
        create_or_edit_organization_with_errors, key, invalid_values
    ):
        """Валидация всех полей (телефон, инн, кпп, огрн)"""
        args, method = create_or_edit_organization_with_errors
        for item in invalid_values:
            args['data_organization'][key] = item
            response = method(**args)
            assert invalid_values[item] in response[0]['message']

    @staticmethod
    @pytest.mark.parametrize(
        'key',
        [
            pytest.param('inn', id='different_inn_and_the_same_kpp'),
            pytest.param('kpp', id='different_kpp_and_the_same_inn'),
        ],
    )
    @pytest.mark.regress()
    @allure.title(
        'Создание двух организаций с одинаковым кпп и разным инн и наоборот через API'
    )
    @allure.story(jira.JIRA_LINK + 'MDP-1013')
    @allure.testcase(case.ALLURE_LINK + '129345?treeId=289')
    @allure.severity(allure.severity_level.NORMAL)
    def test_create_two_organization(
        key, authorization_in_admin_office_with_token
    ):
        """Проверка создания двух организаций с одинаковым КПП и разным ИНН
        Проверка создания двух организаций с одинаковым ИНН и разным КПП"""
        # Достаточно, что запрос не падает с ошибкой
        # Разное инн, одинаковое кпп
        ids = []
        token = authorization_in_admin_office_with_token
        organization_data = make_data_all_legal_entity_fields()
        response = create_organization(token, organization_data)
        ids.append(response['id'])
        organization_data_new = make_data_all_legal_entity_fields()
        organization_data_new[key] = organization_data[key]
        response = create_organization(token, organization_data_new)
        ids.append(response['id'])
        # Удаляем в конце теста созданные организации
        for id_organization in ids:
            delete_organization_by_id(id_organization)
