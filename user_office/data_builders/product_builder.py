from typing import Any
from faker import Faker
from user_office.data_builders.base_builder import BaseBuilder

fake = Faker()

DEFAULT_CATEGORY_ID = 'bf5e67e6-5849-4e7f-84b5-21d3d175c4bb'
DEFAULT_TYPE_ID = '2a0f623a-f8a9-4af0-afdb-633956553e83'


class ProductBuilder(BaseBuilder):
    """Builder для данных продукта.

    Использование:
        data = ProductBuilder(client_id, brand_id).build()
        data = ProductBuilder(client_id, brand_id).with_name("My Product").build()
    """

    def __init__(
        self,
        client_id: str | None = None,
        brand_id: str | None = None,
        category_id: str = DEFAULT_CATEGORY_ID,
        type_id: str = DEFAULT_TYPE_ID,
    ) -> None:
        self._client_id = client_id
        self._brand_id = brand_id
        self._category_id = category_id
        self._type_id = type_id
        self.reset()

    def reset(self) -> 'ProductBuilder':
        """Сброс к начальным значениям"""
        self._name = f"{fake.word('noun').capitalize()}-prod"
        self._naming = f"{fake.company()[:6]}-{fake.random.randint(1, 200)}"
        return self

    def with_client_id(self, client_id: str) -> 'ProductBuilder':
        """Установить ID клиента"""
        self._client_id = client_id
        return self

    def with_brand_id(self, brand_id: str) -> 'ProductBuilder':
        """Установить ID бренда"""
        self._brand_id = brand_id
        return self

    def with_category_id(self, category_id: str) -> 'ProductBuilder':
        """Установить ID категории"""
        self._category_id = category_id
        return self

    def with_type_id(self, type_id: str) -> 'ProductBuilder':
        """Установить ID типа"""
        self._type_id = type_id
        return self

    def with_name(self, name: str) -> 'ProductBuilder':
        """Установить название продукта"""
        self._name = name
        return self

    def with_naming(self, naming: str) -> 'ProductBuilder':
        """Установить нейминг продукта"""
        self._naming = naming
        return self

    def with_random_data(self) -> 'ProductBuilder':
        """Заполнить случайными данными"""
        self._name = f"{fake.word('noun').capitalize()}-prod"
        self._naming = f"{fake.company()[:6]}-{fake.random.randint(1, 200)}"
        return self

    def build(self) -> dict[str, Any]:
        """Создать словарь с данными продукта"""
        if not self._client_id:
            raise ValueError("client_id is required for ProductBuilder")
        if not self._brand_id:
            raise ValueError("brand_id is required for ProductBuilder")
        return {
            'name': self._name,
            'naming': self._naming,
            'client_id': self._client_id,
            'brand_id': self._brand_id,
            'category_id': self._category_id,
            'type_id': self._type_id,
        }


class ProductDataFactory:
    """Фабрика для удобного создания данных продукта.

    Использование:
        data = ProductDataFactory.create_default(client_id, brand_id)
        data = ProductDataFactory.create_random(client_id, brand_id)
    """

    @staticmethod
    def create_default(client_id: str, brand_id: str) -> dict[str, Any]:
        """Создать данные продукта с дефолтными значениями"""
        return ProductBuilder(client_id, brand_id).build()

    @staticmethod
    def create_random(client_id: str, brand_id: str) -> dict[str, Any]:
        """Создать данные продукта со случайными значениями"""
        return ProductBuilder(client_id, brand_id).with_random_data().build()

    @staticmethod
    def create_with_name(client_id: str, brand_id: str, name: str) -> dict[str, Any]:
        """Создать данные продукта с указанным именем"""
        return ProductBuilder(client_id, brand_id).with_name(name).build()
