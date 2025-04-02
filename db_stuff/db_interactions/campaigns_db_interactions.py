from sqlalchemy import cast, func, literal_column, String, and_
from sqlalchemy.sql.functions import coalesce
from sqlalchemy.orm import aliased
from collections import defaultdict
from db_stuff.sqlalchmy_interactions import establish_postgresql_connection
from db_stuff.models.db_models import Campaigns, Clients, Brands, Products, CampaignStatuses, CampaignCobrands


def get_campaigns_by_organization_id(organization_id: str) -> list:
    """Получить список кампаний из БД по organization_id
    Args:
        organization_id: id организации
    Returns:
        Список кампаний
    """
    session = establish_postgresql_connection()
    campaigns = (
        session.query(Campaigns)
        .filter(Campaigns.acl_organization_id == organization_id)
        .all()
    )
    result = []
    for campaign in campaigns:
        result.append(
            {
                'id': str(campaign.id),
                'name': campaign.name,
                'code': campaign.code,
            }
        )
    session.close()
    return sorted(result, key=lambda x: x['id'])


def get_campaigns_for_campaigns_list(organization_id: str) -> list:
    """Получить выборку кампаний для списка кампаний в UI
        Args:
            organization_id: id организации

        Returns:
            Массив данных для списка кампаний на UI"""
    session = establish_postgresql_connection()
    co_brands = aliased(Brands)
    co_brands_count_subquery = session.query(
        CampaignCobrands.campaign_id,
        func.count(CampaignCobrands.cobrand_id).label('co_brands_count')
    ).group_by(
        CampaignCobrands.campaign_id
    ).subquery()
    co_brands_count_subquery_alias = aliased(co_brands_count_subquery)
    subquery = session.query(
        CampaignCobrands.campaign_id,
        func.min(CampaignCobrands.created_at).label('min_created_at')
    ).group_by(
        CampaignCobrands.campaign_id
    ).subquery().alias()
    campaigns_list = (session.query(
        Campaigns.code,
        literal_column("''"),
        Campaigns.name,
        Clients.name,
        Products.name + ' - ' + Brands.name.concat(coalesce(cast(co_brands.name, String), '')),
        func.to_char(Campaigns.updated_at, 'DD.MM.YYYY HH24:MI'),
        CampaignStatuses.name,
        literal_column("''"),
        coalesce(co_brands_count_subquery_alias.c.co_brands_count - 1, 0)
    )
      .join(Clients, Clients.id == Campaigns.client_id)
      .join(Brands, Brands.id == Campaigns.brand_id)
      .join(Products, Products.id == Campaigns.product_id)
      .join(CampaignStatuses, CampaignStatuses.id == Campaigns.status_id)
      .outerjoin(
        co_brands_count_subquery,
        co_brands_count_subquery.c.campaign_id == Campaigns.id
      )
      .outerjoin(
        subquery,
        subquery.c.campaign_id == Campaigns.id
      )
      .outerjoin(CampaignCobrands, and_(
          CampaignCobrands.campaign_id == subquery.c.campaign_id,
          CampaignCobrands.created_at == subquery.c.min_created_at
          )
      )
      .outerjoin(
          co_brands,
          co_brands.id == CampaignCobrands.cobrand_id
      )
      .outerjoin(
          co_brands_count_subquery_alias,
          co_brands_count_subquery_alias.c.campaign_id == Campaigns.id
      ).filter(Campaigns.acl_organization_id == organization_id)
      .order_by(Campaigns.created_at.desc())
      .all())
    campaigns_dict = defaultdict(list)
    for campaign in campaigns_list:
        campaigns_dict[campaign[0]].append(campaign)

    result = []
    for campaign in campaigns_list:
        other_co_brands_count = f", +{campaign[8]}" if campaign[8] and int(campaign[8]) > 0 else ''
        data = campaign[:4] + (campaign[4] + other_co_brands_count,) + campaign[5:8]
        result.append(data)
    formatted_result = [result[i:i + 10] for i in range(0, len(result), 10)]
    return formatted_result
