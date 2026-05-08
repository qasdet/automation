from abc import ABC, abstractmethod
from typing import Any


class BaseBuilder(ABC):
    """Базовый класс для Builder паттерна.

    Использование:
        class ProductBuilder(BaseBuilder):
            def build(self) -> dict:
                return {...}

            def with_name(self, name: str) -> 'ProductBuilder':
                self._name = name
                return self
    """

    @abstractmethod
    def build(self) -> dict[str, Any]:
        """Создать и вернуть объект"""
        raise NotImplementedError

    def reset(self) -> 'BaseBuilder':
        """Сбросить состояние builder к начальному"""
        raise NotImplementedError
