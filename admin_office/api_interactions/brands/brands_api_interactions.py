"""
Модуль устаревших API функций для работы с брендами.

.. deprecated::
    Используйте :class:`admin_office.api_repositories.BrandRepository` вместо этого модуля.

Этот модуль сохранен для обратной совместительности со старым кодом.
Все новые тесты и компоненты должны использовать BrandRepository.

Текущие устаревшие функции:
    - delete_brand_by_id() -> Используйте BrandRepository.delete()
    - get_count_of_brands() -> Используйте BrandRepository.get_count()
    - brand_creation() -> Используйте BrandRepository.create()

Пример перехода на новый API:
    # Старый код (deprecated):
    >>> from admin_office.api_interactions.brands import delete_brand_by_id
    >>> delete_brand_by_id(123, token)

    # Новый код (рекомендуется):
    >>> from admin_office.api_repositories import BrandRepository
    >>> BrandRepository(token).delete("123")
"""
from admin_office.api_repositories import BrandRepository


def delete_brand_by_id(id_brand: int, token: str) -> None:
    """
    Удалить бренд по его ID.

    .. deprecated::
        Используйте :meth:`BrandRepository.delete()` вместо этого метода.

    Вызывает метод delete() репозитория BrandRepository для удаления
    бренда по строковому идентификатору.

    Args:
        id_brand (int): Числовой идентификатор бренда для удаления
        token (str): Токен авторизации для API запросов

    Raises:
        Исключения от BrandRepository.delete() при неудаче

    Example:
        >>> delete_brand_by_id(123, "your_token_here")
    """
    BrandRepository(token).delete(str(id_brand))


def get_count_of_brands(token: str) -> int:
    """
    Получить общее количество брендов в системе.

    .. deprecated::
        Используйте :meth:`BrandRepository.get_count()` вместо этого метода.

    Возвращает количество всех брендов, доступных для текущего пользователя.

    Args:
        token (str): Токен авторизации для API запросов

    Returns:
        int: Общее количество брендов

    Example:
        >>> count = get_count_of_brands("your_token_here")
        >>> print(f"Всего брендов: {count}")
    """
    return BrandRepository(token).get_count()


def brand_creation(brand_data: dict, user_office_token: str) -> str:
    """
    Создать новый бренд с указанными данными.

    .. deprecated::
        Используйте :meth:`BrandRepository.create()` вместо этого метода.

    Создает бренд через API и возвращает идентификатор созданного бренда.

    Args:
        brand_data (dict): Словарь с данными бренда.
                          Ожидаемые ключи зависят от модели BrandRepository.
        user_office_token (str): Токен авторизации пользователя UserOffice

    Returns:
        str: Идентификатор (ID) созданного бренда в виде строки

    Example:
        >>> data = {"naming": "Test Brand", "description": "Описание"}
        >>> brand_id = brand_creation(data, "user_token")
        >>> print(f"Создан бренд с ID: {brand_id}")
    """
    brand = BrandRepository(user_office_token).create(brand_data)
    return brand.id
