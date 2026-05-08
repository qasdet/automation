"""
Builder для данных бренда в User Office.

Используется для генерации тестовых данных бренда
с гибкими настройками (fluent interface).

Примеры использования:
    # Создать с client_id
    >>> data = BrandBuilder('client-uuid-123').build()

    # Создать с кастомным именем
    >>> data = BrandBuilder('client-uuid').with_name("My Brand").build()

    # Использовать фабрику
    >>> data = BrandDataFactory.create_default('client-uuid')
    >>> data = BrandDataFactory.create_random('client-uuid')

Структура данных:
    - name: Название бренда (генерируется Faker)
    - naming: Код бренда (формат: PREFIX-NUMBER)
    - client_id: ID клиента (обязательный параметр)

Note:
    client_id является обязательным для создания бренда,
    так как бренд должен быть привязан к клиенту.
"""

from typing import Any

from faker import Faker

from user_office.data_builders.base_builder import BaseBuilder

# Faker instance для генерации данных
fake = Faker()


class BrandBuilder(BaseBuilder):
    """
    Builder для создания данных бренда.

    Позволяет создавать объекты с настраиваемыми параметрами через fluent interface.
    Используется для генерации тестовых данных при создании брендов в системе.

    Примеры:
        >>> builder = BrandBuilder('client-id-123')
        >>> data = builder.build()

        >>> data = BrandBuilder('client-id').with_name("Test Brand").build()

        >>> data = BrandBuilder('client-id').with_random_data().build()

    Attributes:
        _client_id: ID клиента, к которому привязывается бренд
        _name: Название бренда
        _naming: Код/нейминг бренда (формат: PREFIX-NUMBER)
    """

    def __init__(self, client_id: str | None = None) -> None:
        """
        Инициализировать BrandBuilder.

        Args:
            client_id: ID клиента для привязки бренда. Если передан,
                      будет сохранен и использован при build().
        """
        self._client_id = client_id
        self.reset()

    def reset(self) -> 'BrandBuilder':
        """
        Сбросить состояние builder к начальному.

        Возвращает все атрибуты к значениям по умолчанию:
        - name: случайное название бренда
        - naming: случайный код формата PREFIX-NUMBER

        Returns:
            BrandBuilder: self для fluent interface

        Example:
            >>> builder = BrandBuilder('client-id').with_name("Custom")
            >>> builder.reset()
            >>> builder.build()  # Снова дефолтные данные
        """
        self._name = f"{fake.word('noun').capitalize()}-brand"
        self._naming = f"{fake.word('noun')[:6]}-{fake.random.randint(1, 200)}"
        return self

    def with_client_id(self, client_id: str) -> 'BrandBuilder':
        """
        Установить ID клиента.

        Args:
            client_id: ID клиента для привязки бренда

        Returns:
            BrandBuilder: self для fluent interface

        Example:
            >>> builder = BrandBuilder().with_client_id('client-123')
        """
        self._client_id = client_id
        return self

    def with_name(self, name: str) -> 'BrandBuilder':
        """
        Установить название бренда.

        Args:
            name: Название бренда

        Returns:
            BrandBuilder: self для fluent interface

        Example:
            >>> builder = BrandBuilder('client-id').with_name("My Brand")
        """
        self._name = name
        return self

    def with_naming(self, naming: str) -> 'BrandBuilder':
        """
        Установить нейминг/код бренда.

        Args:
            naming: Код бренда (например, 'BRAND-1')

        Returns:
            BrandBuilder: self для fluent interface

        Example:
            >>> builder = BrandBuilder('client-id').with_naming("MYBRAND-1")
        """
        self._naming = naming
        return self

    def with_random_data(self) -> 'BrandBuilder':
        """
        Заполнить все поля случайными данными.

        Перегенерирует name и naming новыми случайными значениями.

        Returns:
            BrandBuilder: self для fluent interface

        Example:
            >>> builder = BrandBuilder('client-id').with_random_data()
        """
        self._name = f"{fake.word('noun').capitalize()}-brand"
        self._naming = f"{fake.word('noun')[:6]}-{fake.random.randint(1, 200)}"
        return self

    def build(self) -> dict[str, Any]:
        """
        Создать словарь с данными бренда.

        Returns:
            dict[str, Any]: Словарь с полями:
                - name: Название бренда
                - naming: Код бренда
                - client_id: ID клиента

        Raises:
            ValueError: Если client_id не установлен

        Example:
            >>> data = BrandBuilder('client-123').build()
            >>> print(data)
            {'name': 'Test-brand', 'naming': 'TEST-42', 'client_id': 'client-123'}
        """
        if not self._client_id:
            raise ValueError("client_id is required for BrandBuilder")
        return {
            'name': self._name,
            'naming': self._naming,
            'client_id': self._client_id,
        }


class BrandDataFactory:
    """
    Фабрика для удобного создания данных бренда.

    Предоставляет статические методы для часто используемых сценариев
    создания тестовых данных бренда.

    Примеры:
        >>> data = BrandDataFactory.create_default('client-uuid')
        >>> data = BrandDataFactory.create_random('client-uuid')
        >>> data = BrandDataFactory.create_with_name('client-uuid', "My Brand")

    Methods:
        create_default(client_id): Создать с дефолтными значениями
        create_random(client_id): Создать со случайными значениями
        create_with_name(client_id, name): Создать с указанным именем
    """

    @staticmethod
    def create_default(client_id: str) -> dict[str, Any]:
        """
        Создать данные бренда с дефолтными значениями.

        Args:
            client_id: ID клиента для привязки бренда

        Returns:
            dict[str, Any]: Словарь с данными бренда

        Example:
            >>> data = BrandDataFactory.create_default('client-123')
        """
        return BrandBuilder(client_id).build()

    @staticmethod
    def create_random(client_id: str) -> dict[str, Any]:
        """
        Создать данные бренда со случайными значениями.

        Args:
            client_id: ID клиента для привязки бренда

        Returns:
            dict[str, Any]: Словарь со случайными данными бренда

        Example:
            >>> data = BrandDataFactory.create_random('client-123')
        """
        return BrandBuilder(client_id).with_random_data().build()

    @staticmethod
    def create_with_name(client_id: str, name: str) -> dict[str, Any]:
        """
        Создать данные бренда с указанным названием.

        Args:
            client_id: ID клиента для привязки бренда
            name: Название бренда

        Returns:
            dict[str, Any]: Словарь с данными бренда

        Example:
            >>> data = BrandDataFactory.create_with_name('client-123', "Test Brand")
        """
        return BrandBuilder(client_id).with_name(name).build()
