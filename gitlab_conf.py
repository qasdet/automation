import os

from dotenv import load_dotenv

load_dotenv()

ENV_VARIABLES = {}  # глобальная переменная


def get_env_variables(stand: str):
    """Получаем словарь с переменными окружения согласно указанному стенду
    Args:
        stand: Тип стенда
    """
    ENV_VARIABLES.update(
        {
            # Доступы к user-office
            'graphql_url': os.environ.get(f'{stand}_GRAPHQL'),
            'user_office_url': os.environ.get(f'{stand}_OFFICE'),
            'landing_url': os.environ.get(f'{stand}_LANDING'),
            'user_office_login': os.environ.get('USER_OFFICE_LOGIN'),
            'user_office_password': os.environ.get('USER_OFFICE_PASSWORD'),
            'user_office_gateway_auth_url': os.environ.get(f'{stand}_USER_OFFICE_GATEWAY_AUTH_URL'),

            # Доступы к admin-office
            'admin_api_auth_url': os.environ.get(f'{stand}_ADMIN_API_AUTH'),
            'admin_office_url': os.environ.get(f'{stand}_ADMIN'),
            'admin_office_login': os.environ.get('ADMIN_OFFICE_LOGIN'),
            'admin_office_password': os.environ.get('ADMIN_OFFICE_PASSWORD'),

            # Тестовые данные
            'client_id': os.environ.get(f'{stand}_DIGITAL_CLIENT_ID'),
            'brand_id': os.environ.get(f'{stand}_DIGITAL_BRAND_ID'),
            'product_id': os.environ.get(f'{stand}_DIGITAL_PRODUCT_ID'),
            'agency_id': os.environ.get(f'{stand}_DIGITAL_AGENCY_ID'),
            'co_brand_id': os.environ.get(f'{stand}_DIGITAL_CO_BRAND_ID'),
            'department_id': os.environ.get(f'{stand}_DIGITAL_DEPARTMENT_ID'),

            # Доступы к сторонним сервисам (Yandex, VK и т.д)
            'yandex_metric_account': os.environ.get('POST_CLICK_TOOL_YM_ACCOUNT'),
            'yandex_direct_account': os.environ.get('SITE_YD_ACCOUNT'),
            'yandex_login': os.environ.get('YANDEX_LOGIN'),
            'yandex_password': os.environ.get('YANDEX_PASSWORD'),

            # Получение UUID интеграционного токена по имени пользователя
            'yandex_login_from_db': os.environ.get('YANDEX_LOGIN_FROM_DB'),

            # Доступы к основной бд приложения
            'db_host': os.environ.get(f'{stand}_DB_HOST'),
            'db_port': os.environ.get(f'{stand}_DB_PORT'),
            'db_name': os.environ.get(f'{stand}_DB_NAME'),
            'db_user': os.environ.get(f'{stand}_DB_USER'),
            'db_password': os.environ.get(f'{stand}_DB_PASSWORD'),
            'db_schema': os.environ.get(f'{stand}_DB_SCHEMA'),

            # Сервис заявок и доступы к бд сервиса заявок
            'candidate_api_url': os.environ.get(f'{stand}_CANDIDATE_API_URL'),
            'candidate_db_host': os.environ.get(f'{stand}_CANDIDATE_DB_HOST'),
            'candidate_db_port': os.environ.get(f'{stand}_CANDIDATE_DB_PORT'),
            'candidate_db_name': os.environ.get(f'{stand}_CANDIDATE_DB_NAME'),
            'candidate_db_user': os.environ.get(f'{stand}_CANDIDATE_DB_USER'),
            'candidate_db_password': os.environ.get(f'{stand}_CANDIDATE_DB_PASSWORD'),
            'candidate_db_schema': os.environ.get(f'{stand}_CANDIDATE_DB_SCHEMA'),

            # Доступы к бд сервиса отчета
            'reporting_db_host': os.environ.get(f'{stand}_REPORTING_DB_HOST'),
            'reporting_db_port': os.environ.get(f'{stand}_REPORTING_DB_PORT'),
            'reporting_db_name': os.environ.get(f'{stand}_REPORTING_DB_NAME'),
            'reporting_db_user': os.environ.get(f'{stand}_REPORTING_DB_USER'),
            'reporting_db_password': os.environ.get(f'{stand}_REPORTING_DB_PASSWORD'),
            'reporting_db_schema': os.environ.get(f'{stand}_REPORTING_DB_SCHEMA'),

            # Доступы к БД directory (таблица channels)
            'db_name_for_directory': os.environ.get(
                f'{stand}_NAME_FOR_DIRECTORY_DB'
            ),
            'db_host_for_directory': os.environ.get(
                f'{stand}_HOST_FOR_DIRECTORY_DB'
            ),
            'db_user_for_directory': os.environ.get(
                f'{stand}_USER_FOR_DIRECTORY_DB'
            ),
            'db_password_for_directory': os.environ.get(
                f'{stand}DEV_PASSWORD_FOR_DIRECTORY_DB'
            ),
            'db_schema_for_directory': os.environ.get(
                f'{stand}_SCHEMA_FOR_DIRECTORY_DB'
            ),
        }
    )
