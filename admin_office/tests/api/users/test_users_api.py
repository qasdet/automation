import allure
import humps
import pytest

from admin_office.api_interactions.users.users_api_interactions import (
    activate_user,
    block_user,
    create_user,
    get_user_by_id,
    get_users,
    get_users_attribute,
    get_persons_attribute,
    update_user,
    get_persons,
)
from data_make_for_users import make_data_all_user_fields
from db_stuff.db_interactions.organizations_db_interactions import get_organization_id_by_name
from db_stuff.db_interactions.persons_db_interactions import (get_persons_list_db,
                                                              get_person_by_name,
                                                              delete_person_by_id,
                                                              )
from db_stuff.db_interactions.users_db_interactions import (get_users_list_db,
                                                            delete_user_by_id
                                                            )
from helper.array_helper import (
    remove_keys_from_dict,
    compare_lists_of_dictionaries,
)
from helper.linkshort import AllureLink as case
from helper.linkshort import JiraLink as jira

user_data_dict = make_data_all_user_fields() # Генерация словаря тестовых данных
edited_sign = '_ED'  # Крепим этот кусок к имени и фамилии пользователя, чтобы было понятно, что он отредактирован


@pytest.mark.usefixtures('authorization_in_admin_office_with_token')
class TestsUsersAPI:
    @staticmethod
    @pytest.mark.order(1)
    @pytest.mark.regress()
    @allure.title(
        'Тест проверяет работу с пользователями через АПИ'
    )
    @allure.story(jira.JIRA_LINK + 'MDP-1312')
    @allure.testcase(case.ALLURE_LINK + '124595?treeId=289')
    @allure.severity(allure.severity_level.NORMAL)
    def test_get_users_list(
            authorization_in_admin_office_with_token,
    ):
        """Получить список от сервера и сравнить его с данными из БД"""
        token = authorization_in_admin_office_with_token
        # Подготовка данных (persons и users), полученных из БД и от сервера. Приведение их к единому виду.
        persons_list_from_server = humps.decamelize(get_persons(token))
        persons_list_from_db = get_persons_list_db()
        users_list_from_server = humps.decamelize(get_users(token))
        users_list_from_db = get_users_list_db()
        for each_record in persons_list_from_db:
            remove_keys_from_dict(each_record,
                                  ['created_at',
                                   'updated_at'])  # Убираем эти поля, потому что в словаре с сервера их нет
        assert len(persons_list_from_db) == len(persons_list_from_server), \
            "Количество записей для persons, полученное из базы не совпадает" \
            " с количеством записей, полученных от сервера"
        assert len(users_list_from_db) == len(users_list_from_server), \
            "Количество записей для users, полученное из базы не совпадает" \
            " с количеством записей, полученных от сервера"
        assert compare_lists_of_dictionaries(persons_list_from_db, persons_list_from_server) is True, \
            "Словарь persons, полученный из базы и словарь, полученный от сервера - отличаются"
        #  Здесь в обоих словарях убраны поля с датами, потому что есть большая путаница с часовыми поясами
        for each_record in users_list_from_db:
            remove_keys_from_dict(each_record,
                                  ['registered_at',
                                   'blocked_at'])
        for each_record in users_list_from_server:
            remove_keys_from_dict(each_record,
                                  ['registered_at',
                                   'blocked_at'])
        assert compare_lists_of_dictionaries(users_list_from_db, users_list_from_server) is True, \
            "Содержимое таблицы users, полученное из базы, не совпадает с содержимым, полученным от сервера "

    @staticmethod
    @pytest.mark.order(2)
    @pytest.mark.regress()
    @allure.title(
        'Тест проверяет создание пользователя через АПИ'
    )
    @allure.story(jira.JIRA_LINK + 'MDP-1312')
    @allure.testcase(case.ALLURE_LINK + '124595?treeId=289')
    @allure.severity(allure.severity_level.NORMAL)
    def test_create_user(
            authorization_in_admin_office_with_token,
    ):
        token = authorization_in_admin_office_with_token
        """Создаём пользователя и проверяем, что он действительно создался"""
        answer_after_creation = create_user(user_data_dict['name'],
                                            user_data_dict['surname'],
                                            get_organization_id_by_name('ООО АВТОТЕСТЫ'),
                                            user_data_dict['login'],
                                            user_data_dict['email'],
                                            user_data_dict['phone'],
                                            token,
                                            )
        created_user_id = answer_after_creation['data']['adminProfileCreate']['user']['id']
        new_users_list = get_users_attribute(get_users(token), 'id')
        new_persons_list = get_persons_attribute(get_persons(token), 'id')
        is_user_in_new_list = created_user_id in new_users_list
        is_person_in_new_list = created_user_id in new_persons_list
        assert is_user_in_new_list is True, 'Нового id пользователя нет в списке users'
        assert is_person_in_new_list is True, 'Нового id пользователя нет в списке persons'

    @staticmethod
    @pytest.mark.order(3)
    @pytest.mark.regress()
    @allure.title(
        'Тест проверяет уникальность пользователя'
    )
    @allure.story(jira.JIRA_LINK + 'MDP-1312')
    @allure.testcase(case.ALLURE_LINK + '124595?treeId=289')
    @allure.severity(allure.severity_level.NORMAL)
    def test_user_unique(
            authorization_in_admin_office_with_token,
    ):
        """Ещё раз отправляем запрос на создание пользователя с теми же данными,
         которые были использованы в предыдущем тесте"""
        token = authorization_in_admin_office_with_token
        try:
            create_user(user_data_dict['name'],
                        user_data_dict['surname'],
                        get_organization_id_by_name('ООО АВТОТЕСТЫ'),
                        user_data_dict['login'],
                        user_data_dict['email'],
                        user_data_dict['phone'],
                        token,
                        )
        except AssertionError:
            print('У меня не получилось создать дубликат. Всё нормально!')
        else:
            assert False, "Кажется, я смог создать дубликат записи. Разбирайся давай, как такое могло получиться"

    @staticmethod
    @pytest.mark.order(4)
    @pytest.mark.regress()
    @allure.title(
        'Тест проверяет редактирование пользователя'
    )
    @allure.story(jira.JIRA_LINK + 'MDP-1312')
    @allure.testcase(case.ALLURE_LINK + '124595?treeId=289')
    @allure.severity(allure.severity_level.NORMAL)
    def test_edit_user(
            authorization_in_admin_office_with_token
    ):
        """Создаём пользователя, затем вносим изменения и сравниваем по полю email,
        что изменения произошли
        """
        token = authorization_in_admin_office_with_token
        created_user_id = get_person_by_name(user_data_dict['name'])['id']
        print(created_user_id)
        updated_user_info = update_user(created_user_id,
                                        user_data_dict['name'] + edited_sign,
                                        user_data_dict['surname'] + edited_sign,
                                        user_data_dict['login'] + edited_sign,
                                        user_data_dict['email'],
                                        user_data_dict['phone'],
                                        get_organization_id_by_name('ООО АВТОТЕСТЫ'),
                                        token, )
        updated_user_info = updated_user_info['data']['adminProfileUpdate']['person']
        assert not user_data_dict['name'] == updated_user_info['name'], 'У имени не поменялось значение'
        assert not user_data_dict['surname'] == updated_user_info['surname'], 'У фамилии не поменялось значение'

    @staticmethod
    @pytest.mark.order(5)
    @pytest.mark.regress()
    @allure.title(
        'Тест проверяет возможность смены статуса пользователя'
    )
    @allure.story(jira.JIRA_LINK + 'MDP-1312')
    @allure.testcase(case.ALLURE_LINK + '124595?treeId=289')
    @allure.severity(allure.severity_level.NORMAL)
    def test_user_status(
            authorization_in_admin_office_with_token,
    ):
        token = authorization_in_admin_office_with_token
        created_user_id = get_person_by_name(user_data_dict['name'] + edited_sign)['id']  # Ищем по
        # отредактированному имени пользователя
        start_status = get_user_by_id(created_user_id, token)['data']['adminProfiles'][0]['user']['status']
        if start_status == 'BLOCKED':
            activate_user(created_user_id, token)
            block_user(created_user_id, token)
            new_status = get_user_by_id(created_user_id['data']['adminProfiles'][0]['user']['status'])
            assert new_status == 'BLOCKED', 'Пользователь имеет другой статус'
        else:
            block_user(created_user_id, token)
            new_status = get_user_by_id(created_user_id, token)['data']['adminProfiles'][0]['user']['status']
            assert new_status == 'BLOCKED', 'Пользователь имеет другой статус'
        # Заметаем следы
        delete_person_by_id(created_user_id)
        delete_user_by_id(created_user_id)
