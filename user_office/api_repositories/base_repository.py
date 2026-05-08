"""
Базовый репозиторий для API операций в User Office.

Этот модуль предоставляет абстрактный базовый класс для работы с API
через паттерн Repository.

Repository паттерн позволяет:
    - Инкапсулировать работу с API
    - Типизировать возвращаемые данные
    - Централизовать логику запросов

Использование:
    1. Создать наследника:
       class CampaignRepository(BaseRepository):
           def create(self, data):
               ...

    2. Использовать:
       repo = CampaignRepository(token)
       repo.create({'name': 'Test'})
"""

from abc import ABC, abstractmethod
from typing import Any


class BaseRepository(ABC):
    """
    Базовый абстрактный класс для Repository паттерна.

    Определяет интерфейс для всех репозиториев в проекте.
    Конкретные репозитории должны наследоваться от него
    и реализовать абстрактные методы.

    Repository паттерн используется для:
        - Унификации доступа к API
        - Типизации возвращаемых данных
        - Инкапсуляции логики работы с запросами

    Пример использования:
        >>> class CampaignRepository(BaseRepository):
        ...     def create(self, data: dict) -> str:
        ...         # Создать кампанию и вернуть ID
        ...         return campaign_id
        ...
        ...     def get_by_id(self, id: str):
        ...         # Получить кампанию по ID
        ...         return campaign

        >>> repo = CampaignRepository(token)
        >>> campaign_id = repo.create({'name': 'Test Campaign'})
        >>> campaign = repo.get_by_id(campaign_id)

    Attributes:
        _token: Headers с токеном авторизации для запросов к API

    Methods:
        create: Создать сущность (абстрактный)
        get_by_id: Получить сущность по ID (абстрактный)
        get_count: Получить количество записей (абстрактный)
    """

    def __init__(self, token: dict[str, str]) -> None:
        """
        Инициализировать репозиторий с токеном авторизации.

        Args:
            token: Headers с токеном авторизации.
                  Пример: {'authorization': 'Bearer xxx'} или {'admin-authorization': 'Bearer xxx'}
        """
        self._token = token

    @abstractmethod
    def create(self, data: dict) -> Any:
        """
        Создать новую сущность.

        Args:
            data: Словарь с данными для создания сущности.
                 Структура зависит от конкретного репозитория.

        Returns:
            Зависит от конкретной реализации:
            - ID созданной сущности (str)
            - Созданный объект (типизированный)
            - None в случае ошибки

        Raises:
            NotImplementedError: Если метод не переопределен в классе-наследнике

        Example:
            >>> repo = CampaignRepository(token)
            >>> campaign_id = repo.create({'name': 'Test', 'code': 'TEST'})
        """
        raise NotImplementedError

    @abstractmethod
    def get_by_id(self, id: str) -> Any | None:
        """
        Получить сущность по ID.

        Args:
            id: Уникальный идентификатор сущности

        Returns:
            Объект сущности или None если не найдена.
            Тип возвращаемого объекта зависит от конкретной реализации.

        Raises:
            NotImplementedError: Если метод не переопределен в классе-наследнике

        Example:
            >>> repo = CampaignRepository(token)
            >>> campaign = repo.get_by_id('uuid-123')
            >>> if campaign:
            ...     print(campaign.name)
        """
        raise NotImplementedError

    @abstractmethod
    def get_count(self) -> int:
        """
        Получить количество записей.

        Returns:
            int: Количество записей данного типа в системе

        Raises:
            NotImplementedError: Если метод не переопределен в классе-наследнике

        Example:
            >>> repo = CampaignRepository(token)
            >>> count = repo.get_count()
            >>> print(f"Всего кампаний: {count}")
        """
        raise NotImplementedError
