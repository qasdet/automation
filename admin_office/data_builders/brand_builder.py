import string
from typing import Any

from faker import Faker

from admin_office.constants import ORGANIZATION
from admin_office.data_builders.base_builder import BaseBuilder

fake = Faker()
BRAND_AWARENESS = 'Высокая'


class BrandBuilder(BaseBuilder):
    """Builder для данных бренда.

    Использование:
        # Создать с дефолтными значениями
        data = BrandBuilder().build()

        # Создать с кастомными значениями через fluent interface
        data = (
            BrandBuilder()
            .with_name("Test Brand")
            .with_naming("TEST")
            .with_organization("ООО Тест")
            .build()
        )

        # Создать со случайными данными
        data = BrandBuilder().with_random_data().build()
    """

    def __init__(self) -> None:
        self.reset()

    def reset(self) -> 'BrandBuilder':
        """Сброс к начальным значениям"""
        self._name = f"0 {fake.text(5).replace('.', '')}"
        self._naming = fake.lexify(text='?' * 4, letters=string.ascii_uppercase)
        self._organization = ORGANIZATION
        self._brand_awareness = BRAND_AWARENESS
        return self

    def with_name(self, name: str) -> 'BrandBuilder':
        """Установить название бренда"""
        self._name = name
        return self

    def with_naming(self, naming: str) -> 'BrandBuilder':
        """Установить нейминг бренда"""
        self._naming = naming
        return self

    def with_organization(self, organization: str) -> 'BrandBuilder':
        """Установить организацию"""
        self._organization = organization
        return self

    def with_brand_awareness(self, brand_awareness: str) -> 'BrandBuilder':
        """Установить известность бренда"""
        self._brand_awareness = brand_awareness
        return self

    def with_random_data(self) -> 'BrandBuilder':
        """Заполнить случайными данными"""
        self._name = f"0 {fake.text(5).replace('.', '')}"
        self._naming = fake.lexify(text='?' * 4, letters=string.ascii_uppercase)
        self._organization = ORGANIZATION
        self._brand_awareness = fake.random_element([
            'Высокая', 'Средняя', 'Низкая'
        ])
        return self

    def build(self) -> dict[str, Any]:
        """Создать словарь с данными бренда"""
        return {
            'name': self._name,
            'naming': self._naming,
            'organization': self._organization,
            'brand_awareness': self._brand_awareness,
        }


class BrandDataFactory:
    """Фабрика для удобного создания данных бренда.

    Использование:
        data = BrandDataFactory.create_default()
        data = BrandDataFactory.create_random()
        data = BrandDataFactory.create_with_name("Custom Brand")
    """

    @staticmethod
    def create_default() -> dict[str, Any]:
        """Создать данные бренда с дефолтными значениями"""
        return BrandBuilder().build()

    @staticmethod
    def create_random() -> dict[str, Any]:
        """Создать данные бренда со случайными значениями"""
        return BrandBuilder().with_random_data().build()

    @staticmethod
    def create_with_name(name: str) -> dict[str, Any]:
        """Создать данные бренда с указанным именем"""
        return BrandBuilder().with_name(name).build()

    @staticmethod
    def create_with_custom(
        name: str = None,
        naming: str = None,
        organization: str = None,
        brand_awareness: str = None,
    ) -> dict[str, Any]:
        """Создать данные бренда с указанными значениями"""
        builder = BrandBuilder()
        if name:
            builder.with_name(name)
        if naming:
            builder.with_naming(naming)
        if organization:
            builder.with_organization(organization)
        if brand_awareness:
            builder.with_brand_awareness(brand_awareness)
        return builder.build()
