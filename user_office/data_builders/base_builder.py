"""
Базовый класс для Builder паттерна в User Office.

Этот модуль предоставляет абстрактный базовый класс для создания builder'ов,
используемых для генерации тестовых данных.

Builder паттерн позволяет:
    - Создавать объекты с изменяющимися параметрами
    - Использовать fluent interface (цепочки вызовов)
    - Генерировать тестовые данные с осмысленными значениями

Использование:
    1. Создать конкретный builder:
       class ClientBuilder(BaseBuilder):
           def build(self) -> dict:
               return {...}

    2. Использовать fluent interface:
       data = ClientBuilder().with_name("Test").build()

Примеры:
    >>> builder = ClientBuilder()
    >>> data = builder.with_name("My Company").build()

    >>> # Или через Factory
    >>> data = ClientDataFactory.create_default()
"""

from abc import ABC, abstractmethod
from typing import Any


class BaseBuilder(ABC):
    """
    Базовый абстрактный класс для Builder паттерна.

    Этот класс определяет интерфейс для всех builder'ов в проекте.
    Конкретные builder'ы должны наследоваться от него и реализовать
    метод build().

    Builder паттерн используется для:
        - Создания объектов с изменяющимися параметрами
        - Fluent interface (method chaining)
        - Генерации тестовых данных

    Пример использования:
        >>> class ClientBuilder(BaseBuilder):
        ...     def __init__(self):
        ...         self._name = "Default Name"
        ...
        ...     def with_name(self, name: str) -> 'ClientBuilder':
        ...         self._name = name
        ...         return self
        ...
        ...     def build(self) -> dict:
        ...         return {'name': self._name}

        >>> # Использование
        >>> data = ClientBuilder().with_name("Test").build()

    Methods:
        build(): Создать и вернуть объект (абстрактный)
        reset(): Сбросить состояние к начальному (опционально)
    """

    @abstractmethod
    def build(self) -> dict[str, Any]:
        """
        Создать и вернуть объект.

        Этот метод должен быть реализован в каждом конкретном builder'е.
        Возвращает словарь/объект с тестовыми данными.

        Returns:
            dict[str, Any]: Словарь с тестовыми данными

        Raises:
            NotImplementedError: Если метод не переопределен в классе-наследнике

        Example:
            >>> class MyBuilder(BaseBuilder):
            ...     def build(self) -> dict:
            ...         return {'key': 'value'}
        """
        raise NotImplementedError

    def reset(self) -> 'BaseBuilder':
        """
        Сбросить состояние builder к начальному.

        Этот метод позволяет переиспользовать builder для создания
        новых объектов после сброса состояния.

        Returns:
            BaseBuilder: self для fluent interface

        Raises:
            NotImplementedError: Если метод не переопределен в классе-наследнике

        Example:
            >>> builder = ClientBuilder()
            >>> data1 = builder.with_name("First").build()
            >>> builder.reset()  # Сброс к начальному состоянию
            >>> data2 = builder.with_name("Second").build()
        """
        raise NotImplementedError
