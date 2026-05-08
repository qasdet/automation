"""
Repository для работы с кампаниями через GraphQL API.

Этот модуль реализует паттерн Repository для работы с кампаниями
через GraphQL API User Office.

Основные возможности:
    - Создание кампаний
    - Получение кампаний по ID
    - Получение всех кампаний
    - Обновление кампаний
    - Подсчет количества кампаний

Использование:
    # Инициализация
    repo = CampaignRepository(token)

    # Создать кампанию
    campaign_id = repo.create({'name': 'Test', ...})

    # Получить по ID
    campaign = repo.get_by_id('uuid-123')

    # Получить все
    campaigns = repo.get_all()

    # Количество
    count = repo.get_count()

Примеры данных:
    campaign_data = {
        'client_id': 'uuid-клиента',
        'brand_id': 'uuid-бренда',
        'product_id': 'uuid-продукта',
        'campaign_name': 'Название кампании',
        'campaign_naming': 'NAMING-1',
        'action': 'DRAFT'  # или 'PLANNING'
    }
"""

from dataclasses import dataclass
from typing import Any

from helper.subfield_selections import campaign_subfields
from http_methods.post import post_request

from user_office.api_repositories.base_repository import BaseRepository


@dataclass
class Campaign:
    """
    Модель кампании.

    Используется для типизации возвращаемых данных из API.

    Attributes:
        id: Уникальный идентификатор кампании
        name: Название кампании
        code: Код/нейминг кампании
        client_id: ID клиента (опционально)
        brand_id: ID бренда (опционально)
        product_id: ID продукта (опционально)

    Примеры:
        >>> campaign = Campaign(
        ...     id='uuid-123',
        ...     name='Test Campaign',
        ...     code='TEST-1'
        ... )
        >>> print(campaign.name)
        'Test Campaign'
    """

    id: str
    name: str
    code: str
    client_id: str | None = None
    brand_id: str | None = None
    product_id: str | None = None

    @classmethod
    def from_dict(cls, data: dict) -> 'Campaign':
        """
        Создать Campaign из словаря.

        Обрабатывает вложенные словари client, brand, product.

        Args:
            data: Словарь с данными кампании от API

        Returns:
            Campaign: Новый экземпляр с данными из словаря

        Example:
            >>> api_data = {
            ...     'id': '123',
            ...     'name': 'Test',
            ...     'code': 'TEST',
            ...     'client': {'id': 'client-1'}
            ... }
            >>> campaign = Campaign.from_dict(api_data)
        """
        client_id = None
        if isinstance(data.get('client'), dict):
            client_id = data['client'].get('id')

        brand_id = None
        if isinstance(data.get('brand'), dict):
            brand_id = data['brand'].get('id')

        product_id = None
        if isinstance(data.get('product'), dict):
            product_id = data['product'].get('id')

        return cls(
            id=data.get('id', ''),
            name=data.get('name', ''),
            code=data.get('code', ''),
            client_id=client_id,
            brand_id=brand_id,
            product_id=product_id,
        )


class CampaignRepository(BaseRepository):
    """
    Репозиторий для работы с кампаниями через GraphQL API.

    Инкапсулирует логику работы с кампаниями:
    создание, получение, обновление, подсчет.

    Использование:
        >>> repo = CampaignRepository({'authorization': 'Bearer xxx'})

        # Создать кампанию
        >>> campaign_id = repo.create({
        ...     'client_id': 'client-uuid',
        ...     'brand_id': 'brand-uuid',
        ...     'product_id': 'product-uuid',
        ...     'campaign_name': 'Test',
        ...     'campaign_naming': 'TEST-1',
        ...     'action': 'DRAFT'
        ... })

        # Получить по ID
        >>> campaign = repo.get_by_id('uuid-123')
        >>> if campaign:
        ...     print(campaign.name)

        # Получить все
        >>> campaigns = repo.get_all()

        # Количество
        >>> count = repo.get_count()

    Наследует:
        BaseRepository

    Methods:
        create: Создать кампанию
        get_by_id: Получить кампанию по ID
        get_all: Получить все кампании
        get_count: Получить количество кампаний
        update: Обновить кампанию
    """

    def create(self, data: dict) -> str:
        """
        Создать новую кампанию.

        Выполняет мутацию campaignCreate в GraphQL API.

        Args:
            data: Словарь с данными кампании:
                - client_id: ID клиента (обязательно)
                - brand_id: ID бренда (обязательно)
                - product_id: ID продукта (обязательно)
                - campaign_name: Название кампании
                - campaign_naming: Код/нейминг кампании
                - start_on: Дата начала (опционально)
                - finish_on: Дата окончания (опционально)
                - action: Тип создания ('DRAFT' или 'PLANNING')

        Returns:
            str: ID созданной кампании

        Example:
            >>> repo = CampaignRepository(token)
            >>> campaign_id = repo.create({
            ...     'client_id': 'client-uuid',
            ...     'brand_id': 'brand-uuid',
            ...     'product_id': 'product-uuid',
            ...     'campaign_name': 'Test Campaign',
            ...     'campaign_naming': 'TEST-1',
            ...     'action': 'DRAFT'
            ... })
        """
        mutation_query = {
            'variables': {
                'clientID': data['client_id'],
                'code': data['campaign_naming'],
                'name': data['campaign_name'],
                'brandID': data['brand_id'],
                'productID': data['product_id'],
                'startOn': data.get('start_on'),
                'finishOn': data.get('finish_on'),
                'action': data.get('action', 'DRAFT'),
            },
            'query': f"""mutation campaignCreate($name: String!, $code: String, $brandID: ID!,
                                             $productID: ID!, $clientID: ID!, $agencyID: ID, $startOn: Time,
                                             $finishOn: Time, $targetAudience: String, $conditions: String
                                             $action: CampaignCreateAction!) {{
        campaignCreate(
        data: {{name: $name, brandID: $brandID, productID: $productID, clientID: $clientID,
        agencyID: $agencyID, startOn: $startOn, finishOn: $finishOn, targetAudience: $targetAudience,
        conditions: $conditions, code: $code}}
        action: $action
        ) {campaign_subfields}
        """,
        }
        result = post_request(mutation_query, self._token)
        return result['data']['campaignCreate']['id']

    def get_by_id(self, campaign_id: str) -> Campaign | None:
        """
        Получить кампанию по ID.

        Args:
            campaign_id: ID кампании

        Returns:
            Campaign или None если кампания не найдена

        Example:
            >>> repo = CampaignRepository(token)
            >>> campaign = repo.get_by_id('uuid-123')
            >>> if campaign:
            ...     print(f"Кампания: {campaign.name}")
        """
        query = {
            'variables': {'id': campaign_id},
            'query': f"""query Campaigns($id: ID) {{
            campaigns(id: $id) {campaign_subfields}
            }}""",
        }
        result = post_request(query, self._token)
        data = result.get('data', {}).get('campaigns', [])
        if data:
            return Campaign.from_dict(data[0])
        return None

    def get_all(self) -> list[Campaign]:
        """
        Получить все кампании.

        Returns:
            list[Campaign]: Список всех кампаний

        Example:
            >>> repo = CampaignRepository(token)
            >>> campaigns = repo.get_all()
            >>> for campaign in campaigns:
            ...     print(campaign.name)
        """
        query = {
            'query': f"""query Campaigns {{
            campaigns {{ {campaign_subfields} }}
            }}""",
        }
        result = post_request(query, self._token)
        campaigns_data = result.get('data', {}).get('campaigns', [])
        return [Campaign.from_dict(c) for c in campaigns_data]

    def get_count(self) -> int:
        """
        Получить количество кампаний.

        Returns:
            int: Количество кампаний в системе

        Example:
            >>> repo = CampaignRepository(token)
            >>> count = repo.get_count()
            >>> print(f"Всего кампаний: {count}")
        """
        query = {
            'query': f"""query Campaigns {{
            campaigns {{ id }}
            }}""",
        }
        result = post_request(query, self._token)
        return len(result.get('data', {}).get('campaigns', []))

    def update(self, campaign_id: str, data: dict) -> Campaign | None:
        """
        Обновить кампанию.

        Выполняет мутацию campaignUpdate в GraphQL API.

        Args:
            campaign_id: ID кампании для обновления
            data: Словарь с обновленными данными:
                - new_campaign_name: Новое название (опционально)
                - new_campaign_naming: Новый код (опционально)
                - client_id: ID клиента
                - brand_id: ID бренда
                - product_id: ID продукта

        Returns:
            Campaign или None если кампания не найдена

        Example:
            >>> repo = CampaignRepository(token)
            >>> updated = repo.update('uuid-123', {
            ...     'new_campaign_name': 'Updated Name',
            ...     'client_id': 'client-uuid',
            ...     'brand_id': 'brand-uuid',
            ...     'product_id': 'product-uuid'
            ... })
        """
        mutation_query = {
            'variables': {
                "name": data.get("new_campaign_name"),
                "id": campaign_id,
                "code": data.get("new_campaign_naming"),
                "clientID": data.get("client_id"),
                "brandID": data.get("brand_id"),
                "productID": data.get("product_id"),
            },
            'query': f"""mutation campaignUpdate($name: String!, $code: String!, $id: ID!,
                                $startOn: Time, $finishOn: Time, $clientID: ID!, $brandID: ID!, $productID: ID!)
                                {{campaignUpdate(
                                data: {{name: $name, code: $code, startOn: $startOn, finishOn: $finishOn,
                                clientID: $clientID, brandID: $brandID, productID: $productID}} id: $id)
                                {campaign_subfields}
                                }}""",
        }
        result = post_request(mutation_query, self._token)
        data = result.get('data', {}).get('campaignUpdate')
        if data:
            return Campaign.from_dict(data)
        return None
