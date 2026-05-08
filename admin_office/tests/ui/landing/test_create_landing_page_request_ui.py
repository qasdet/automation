import time
import allure
import pytest

from helper.linkshort import JiraLink as jira
from admin_office.api_interactions.user_candidates.user_candidates_api_interactions import get_user_candidate_data
from admin_office.components.pages.user_candidates.user_candidates_page import (
    AdminOfficeUserCandidatesPage,
)
from db_stuff.db_interactions.user_candidates_db_interactions import (
    get_specific_user_candidate_id,
    get_date_if_record_was_deleted,
)
from admin_office.components.pages.landing.landing_page import LandingPage
from admin_office.tests.api.landing.data_make_for_user_candidates import (
    make_data_all_user_candidate_fields,
)


user_candidate_data = make_data_all_user_candidate_fields('Семён',
                                                          'Юайный',
                                                          'ООО Юай-Автотесты',
                                                          'Эта заявка создана автоматическим тестом через UI')


class TestLandingPageRequestCreate:
    """
    Набор тестов для проверки функциональности посадочных страниц и заявок.

    Тестирует основные сценарии:
    - Создание заявки через посадочную страницу
    - Проверка созданной заявки в AdminOffice
    - Удаление заявки
    """

    @staticmethod
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    @allure.title('Оставить заявку через посадочную страницу')
    @allure.description(
        "Заполняет поля, затем нажимает кнопку 'Оставить заявку'"
    )
    @allure.story(jira.JIRA_LINK + 'MDP-4967')
    def test_create_landing_page_request(
        landing_page: LandingPage,
        landing_base_url: str,
    ):
        """
        Тест создания заявки через посадочную страницу.

        Проверяет:
        - Переход на посадочную страницу
        - Открытие формы заявки
        - Заполнение всех полей формы
        - Отправку заявки
        """
        landing_page.visit_landing_page(landing_base_url)
        landing_page.landing_model.click_leave_a_first_request_button()
        landing_page.landing_model.input_all_landing_fields(
            **user_candidate_data
        )
        time.sleep(4)
        landing_page.landing_model.click_leave_a_second_request_button()

    @staticmethod
    @pytest.mark.smoke
    @allure.title('Справочник Заявки')
    @allure.story(jira.JIRA_LINK + 'MDP-4967')
    def test_check_user_candidate_ui_request_admin_office(
        admin_user_candidates_page: AdminOfficeUserCandidatesPage,
        authorization_in_admin_office_with_token,
    ):
        """
        Тест проверки заявки в справочнике AdminOffice.

        Проверяет:
        - Получение ID заявки из базы данных
        - Получение данных заявки с сервера
        - Переход в справочник Заявки через sidebar
        - Проверку отображения заявки в списке
        - Удаление заявки через контекстное меню
        - Подтверждение удаления в диалоге
        - Проверку что заявка больше не отображается
        - Проверку наличия даты удаления в базе данных
        """
        token = authorization_in_admin_office_with_token
        just_created_user_candidate_id_from_db = get_specific_user_candidate_id(user_candidate_data['surname'])
        user_candidate_dict_from_server = get_user_candidate_data(token, just_created_user_candidate_id_from_db)
        admin_user_candidates_page.side_bar.check_user_candidates_link()
        admin_user_candidates_page.user_candidates.check_new_user_candidate(user_candidate_dict_from_server)
        admin_user_candidates_page.user_candidates.table.open_menu_action_in_row_by_contains_text(
            user_candidate_dict_from_server['id'])
        admin_user_candidates_page.user_candidates.table.click_item_menu_action('Удалить')
        admin_user_candidates_page.confirmation_dialog.confirm()
        admin_user_candidates_page.user_candidates.table.row_by_contains_text(
            user_candidate_dict_from_server['id']).should_not_be_visible()
        assert get_date_if_record_was_deleted(user_candidate_data['surname']), "В базе нет даты удаления данной записи"
