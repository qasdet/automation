"""
Builder для данных клиента в User Office.

Используется для генерации тестовых данных клиента
с гибкими настройками (fluent interface).

Примеры использования:
    # Создать с дефолтными значениями
    >>> data = ClientBuilder().build()
    {'name': 'Acme Corp', 'naming': 'ACME-42'}

    # Создать с кастомным именем
    >>> data = ClientBuilder().with_name("My Company").build()
    {'name': 'My Company', 'naming': 'ACME-42'}

    # Использовать фабрику
    >>> data = ClientDataFactory.create_default()
    >>> data = ClientDataFactory.create_random()

Структура данных:
    - name: Название компании (генерируется Faker)
    - naming: Код компании (генерируется как "PREFIX-NUMBER")
"""

from typing import Any

from faker import Faker

from user_office.data_builders.base_builder import BaseBuilder

# Faker instance для генерации данных
fake = Faker()


class ClientBuilder(BaseBuilder):
    """
    Builder для создания данных клиента.

    Позволяет создавать объекты с настраиваемыми параметрами через fluent interface.
    Используется для генерации тестовых данных при создании клиентов в системе.

    Примеры:
        >>> builder = ClientBuilder()
        >>> data = builder.build()  # Дефолтные данные

        >>> data = ClientBuilder().with_name("Test Corp").build()

        >>> data = ClientBuilder().with_random_data().build()

    Attributes:
        _name: Название компании
        _naming: Код/нейминг компании (формат: PREFIX-NUMBER)
    """

    def __init__(self) -> None:
        """Инициализировать ClientBuilder с значениями по умолчанию."""
        self.reset()

    def reset(self) -> 'ClientBuilder':
        """
        Сбросить состояние builder к начальному.

        Возвращает все атрибуты к значениям по умолчанию:
        - name: случайное название компании
        - naming: случайный код формата PREFIX-NUMBER

        Returns:
            ClientBuilder: self для fluent interface

        Example:
            >>> builder = ClientBuilder().with_name("Custom")
            >>> builder.reset()
            >>> builder.build()  # Снова дефолтные данные
        """
        self._name = fake.company()
        self._naming = f"{fake.company()[:6]}-{fake.random.randint(1, 200)}"
        return self

    def with_name(self, name: str) -> 'ClientBuilder':
        """
        Установить название клиента.

        Args:
            name: Название компании

        Returns:
            ClientBuilder: self для fluent interface

        Example:
            >>> builder = ClientBuilder().with_name("My Company")
        """
        self._name = name
        return self

    def with_naming(self, naming: str) -> 'ClientBuilder':
        """
        Установить нейминг/код клиента.

        Args:
            naming: Код клиента (например, 'MYCO-123')

        Returns:
            ClientBuilder: self для fluent interface

        Example:
            >>> builder = ClientBuilder().with_naming("TEST-1")
        """
        self._naming = naming
        return self

    def with_random_data(self) -> 'ClientBuilder':
        """
        Заполнить все поля случайными данными.

        Перегенерирует name и naming новыми случайными значениями.

        Returns:
            ClientBuilder: self для fluent interface

        Example:
            >>> builder = ClientBuilder().with_random_data()
        """
        self._name = fake.company()
        self._naming = f"{fake.company()[:6]}-{fake.random.randint(1, 200)}"
        return self

    def build(self) -> dict[str, Any]:
        """
        Создать словарь с данными клиента.

        Returns:
            dict[str, Any]: Словарь с полями:
                - name: Название компании
                - naming: Код клиента

        Example:
            >>> data = ClientBuilder().build()
            >>> print(data)
            {'name': 'Acme Corp', 'naming': 'ACME-42'}
        """
        return {
            'name': self._name,
            'naming': self._naming,
        }


class ClientDataFactory:
    """
    Фабрика для удобного создания данных клиента.

    Предоставляет статические методы для часто используемых сценариев
    создания тестовых данных клиента.

    Примеры:
        >>> data = ClientDataFactory.create_default()
        >>> data = ClientDataFactory.create_random()
        >>> data = ClientDataFactory.create_with_name("My Company")

    Methods:
        create_default(): Создать с дефолтными значениями
        create_random(): Создать со случайными значениями
        create_with_name(): Создать с указанным именем
    """

    @staticmethod
    def create_default() -> dict[str, Any]:
        """
        Создать данные клиента с дефолтными значениями.

        Returns:
            dict[str, Any]: Словарь с данными клиента

        Example:
            >>> data = ClientDataFactory.create_default()
        """
        return ClientBuilder().build()

    @staticmethod
    def create_random() -> dict[str, Any]:
        """
        Создать данные клиента со случайными значениями.

        Returns:
            dict[str, Any]: Словарь со случайными данными клиента

        Example:
            >>> data = ClientDataFactory.create_random()
        """
        return ClientBuilder().with_random_data().build()

    @staticmethod
    def create_with_name(name: str) -> dict[str, Any]:
        """
        Создать данные клиента с указанным названием.

        Args:
            name: Название компании для клиента

        Returns:
            dict[str, Any]: Словарь с данными клиента

        Example:
            >>> data = ClientDataFactory.create_with_name("Test Company")
        """
        return ClientBuilder().with_name(name).build()
