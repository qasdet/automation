from dataclasses import dataclass
from typing import Any

from admin_office.api_repositories.base_repository import BaseRepository


@dataclass
class Brand:
    """Модель бренда"""
    id: str
    name: str
    naming: str
    client_id: str | None = None

    @classmethod
    def from_dict(cls, data: dict) -> 'Brand':
        return cls(
            id=data.get('id', ''),
            name=data.get('name', ''),
            naming=data.get('naming', ''),
            client_id=data.get('clientID') or data.get('client_id'),
        )


class BrandRepository(BaseRepository):
    """Репозиторий для работы с брендами через GraphQL API.

    Использование:
        repo = BrandRepository(token)
        brand = repo.create({'name': 'Test', 'naming': 'TEST'})
        count = repo.get_count()
        repo.delete(brand.id)
    """

    def create(self, data: dict) -> Brand:
        """Создать новый бренд.

        Args:
            data: Словарь с полями name и naming

        Returns:
            Brand с заполненным id
        """
        query = {
            'operation_name': 'BrandCreate',
            'variables': {
                'data': {
                    'name': data['name'],
                    'naming': data['naming'],
                }
            },
            'query': """mutation BrandCreate($clientID: ID, $data: BrandData!) {
                         brandCreate(clientID: $clientID, data: $data) {id name naming}}""",
        }
        result = self._execute_query(query)
        return Brand.from_dict(result['data']['brandCreate'])

    def get_by_id(self, id: str) -> Brand | None:
        """Получить бренд по ID.

        Args:
            id: ID бренда

        Returns:
            Brand или None если не найден
        """
        query = {
            'operationName': 'adminBrand',
            'variables': {'id': id},
            'query': '''query adminBrand($id: ID!) {
                         adminBrand(id: $id) {id name naming clientID}}''',  # noqa: E501
        }
        result = self._execute_query(query)
        data = result.get('data', {}).get('adminBrand')
        return Brand.from_dict(data) if data else None

    def get_by_naming(self, naming: str) -> Brand | None:
        """Получить бренд по неймингу.

        Args:
            naming: Нейминг бренда

        Returns:
            Brand или None если не найден
        """
        query = {
            'operationName': 'adminBrands',
            'query': 'query adminBrands {adminBrands {id name naming}}',
        }
        result = self._execute_query(query)
        brands = result.get('data', {}).get('adminBrands', [])
        for brand_data in brands:
            if brand_data.get('naming') == naming:
                return Brand.from_dict(brand_data)
        return None

    def delete(self, id: str) -> bool:
        """Удалить бренд по ID.

        Args:
            id: ID бренда

        Returns:
            True если удалён успешно
        """
        query = {
            'operationName': 'adminBrandDelete',
            'variables': {'id': str(id)},
            'query': 'mutation adminBrandDelete($id: ID!) {adminBrandDelete(id: $id)}',
        }
        result = self._execute_query(query)
        return result == {'data': {'adminBrandDelete': True}}

    def get_count(self) -> int:
        """Получить количество брендов.

        Returns:
            Количество записей
        """
        query = {
            'operationName': 'adminBrands',
            'query': 'query adminBrands {adminBrands {id}}',
        }
        result = self._execute_query(query)
        return len(result.get('data', {}).get('adminBrands', []))

    def get_all(self) -> list[Brand]:
        """Получить все бренды.

        Returns:
            Список всех брендов
        """
        query = {
            'operationName': 'adminBrands',
            'query': 'query adminBrands {adminBrands {id name naming}}',
        }
        result = self._execute_query(query)
        brands = result.get('data', {}).get('adminBrands', [])
        return [Brand.from_dict(b) for b in brands]
