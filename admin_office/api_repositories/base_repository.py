from abc import ABC, abstractmethod
from typing import Any, Generic, TypeVar

from http_methods.post import post_request


T = TypeVar('T')


class BaseRepository(ABC):
    """Базовый репозиторий для API операций.

    Использование:
        class BrandRepository(BaseRepository):
            def create(self, data: dict) -> Brand:
                ...
    """

    def __init__(self, token: dict[str, str]) -> None:
        """Инициализация репозитория с токеном авторизации.

        Args:
            token: Headers с токеном, напр. {'admin-authorization': 'Bearer ...'}
        """
        self._token = token

    def _execute_query(self, query: dict) -> dict:
        """Выполнить GraphQL запрос.

        Args:
            query: GraphQL query/mutation

        Returns:
            Response JSON
        """
        return post_request(query, self._token)

    @abstractmethod
    def create(self, data: dict) -> Any:
        """Создать сущность"""
        raise NotImplementedError

    @abstractmethod
    def get_by_id(self, id: str) -> Any | None:
        """Получить сущность по ID"""
        raise NotImplementedError

    @abstractmethod
    def delete(self, id: str) -> bool:
        """Удалить сущность по ID"""
        raise NotImplementedError

    @abstractmethod
    def get_count(self) -> int:
        """Получить количество записей"""
        raise NotImplementedError
