import allure
import pytest

from admin_office.api_repositories import BrandRepository
from admin_office.components.pages.brands.brands_page import (
    AdminOfficeBrandsPage,
)
from admin_office.constants import LIMIT_OF_ROWS_ON_ONE_PAGE_IN_BRANDS
from admin_office.data_builders import BrandDataFactory
from db_stuff.db_interactions.brands_db_interactions import get_brand_by_naming
from helper.linkshort import AllureLink as case
from helper.linkshort import JiraLink as jira


@pytest.fixture()
def brand_repository(authorization_in_admin_office_with_token) -> BrandRepository:
    """
    Фикстура для создания репозитория BrandRepository.

    Создает и возвращает объект BrandRepository с токеном авторизации
    для выполнения API запросов к разделу брендов.

    Args:
        authorization_in_admin_office_with_token: Токен авторизации в Admin Office

    Returns:
        BrandRepository: Объект репозитория для работы с брендами через API
    """
    return BrandRepository(authorization_in_admin_office_with_token)


@pytest.fixture()
def life_cycle_of_the_brand_with_all_field(
    authorization_in_admin_office_with_token,
):
    """
    Фикстура для создания и автоматической очистки бренда в тесте.

    Создает бренд с полными данными через BrandDataFactory в начале теста
    и автоматически удаляет его через BrandRepository в конце.

    Использование:
        >>> def test_something(life_cycle_of_the_brand_with_all_field):
        ...     data_brand = life_cycle_of_the_brand_with_all_field
        ...     # Тест использует созданный бренд
        ...     # После теста бренд автоматически удаляется

    Args:
        authorization_in_admin_office_with_token: Токен авторизации в Admin Office

    Yields:
        dict: Словарь с данными созданного бренда (naming, description и т.д.)
    """
    data_brand = BrandDataFactory.create_default()
    token = authorization_in_admin_office_with_token
    repo = BrandRepository(token)

    yield data_brand

    # Cleanup через Repository
    brand = repo.get_by_naming(data_brand['naming'])
    if brand:
        repo.delete(brand.id)


@pytest.mark.usefixtures('authorization_in_admin_office_with_token')
class TestsBrands:
    """
    Набор тестов для проверки функциональности справочника Бренды.

    Тестирует основные сценарии:
    - Просмотр списка брендов с пагинацией
    - Создание нового бренда с заполнением всех полей
    """

    @staticmethod
    @pytest.mark.smoke
    @allure.title('Справочник Бренды')
    @allure.severity(allure.severity_level.NORMAL)
    @allure.story(jira.JIRA_LINK + 'MDP-759')
    @allure.testcase(case.ALLURE_LINK + '175387')
    def test_view_brands(
        admin_base_url: str,
        admin_brands_page: AdminOfficeBrandsPage,
        brand_repository: BrandRepository,
    ):
        """
        Тест проверки отображения справочника брендов с пагинацией.

        Проверяет:
        - Общее количество брендов соответствует API
        - Пагинация корректно работает при переходе на вторую страницу
        - Количество строк на второй странице соответствует ожиданиям
        """
        admin_brands_page.go_to_brands()
        count_all_rows = brand_repository.get_count()
        admin_brands_page.brands.check_quantity_brands(count_all_rows)
        admin_brands_page.brands.check_transition_to_next_page(count_all_rows)
        count_rows_in_second_page = (
            count_all_rows
            if count_all_rows <= LIMIT_OF_ROWS_ON_ONE_PAGE_IN_BRANDS
            else count_all_rows - LIMIT_OF_ROWS_ON_ONE_PAGE_IN_BRANDS
        )
        admin_brands_page.brands.check_quantity_brands(
            count_rows_in_second_page
        )

    @staticmethod
    @pytest.mark.smoke
    @allure.title('Создание записи в справочнике Бренды')
    @allure.story(jira.JIRA_LINK + 'MDP-759')
    @allure.testcase(case.ALLURE_LINK + '159670')
    def test_create_brand(
        admin_brands_page: AdminOfficeBrandsPage,
        life_cycle_of_the_brand_with_all_field,
    ):
        """
        Тест создания нового бренда с заполнением всех полей.

        Проверяет полный цикл создания бренда:
        - Открытие формы создания
        - Заполнение всех полей данными из фикстуры
        - Сохранение бренда
        - Проверка отображения созданного бренда в списке
        """
        data_brand = life_cycle_of_the_brand_with_all_field
        admin_brands_page.go_to_brands()
        admin_brands_page.brands.open_the_brand_creation_form()
        admin_brands_page.card_brand.fill_all_fields(**data_brand)
        admin_brands_page.card_brand.save_brand()
        admin_brands_page.brands.check_new_brand(data_brand)
