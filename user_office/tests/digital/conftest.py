import pytest

from random import randint
from user_office import constants
from db_stuff.db_interactions.clients_db_interactions import get_client_id_by_naming
from db_stuff.db_interactions.brands_db_interactions import get_brand_id_by_naming
from db_stuff.db_interactions.products_db_interactions import get_product_id_by_naming
from db_stuff.db_interactions.agencies_db_interactions import get_agency_id_by_naming
from db_stuff.db_interactions.departments_db_interactions import get_department_id_by_naming
from db_stuff.db_interactions.goals_db_interactions import get_goal_id_by_code
from db_stuff.db_interactions.ad_formats_db_interactions import get_ad_format_id_by_naming
from db_stuff.db_interactions.ad_sizes_db_interactions import get_ad_size_id_by_naming
from db_stuff.db_interactions.buy_types_db_interactions import get_buy_type_id_by_naming
from db_stuff.db_interactions.sellers_db_interactions import get_seller_id_by_naming
from db_stuff.db_interactions.sources_db_interactions import get_source_id_by_naming
from db_stuff.db_interactions.product_categories_db_interactions import get_product_category_id_by_code
from db_stuff.db_interactions.product_types_db_interactions import get_product_type_id_by_code
from db_stuff.db_interactions.integration_tools_db_interactions import get_tool_id_by_code
from helper.names_generator.advertising_campaign_names_generator import (
    advertising_campaign_name_generator,
    advertising_campaign_code_generator,
)
from user_office.api_interactions.placement_templates.placement_templates_api_interactions import (PlacementTemplatesQueriesAPI,
                                                                                                   PlacementTemplatesMutationsAPI)
from admin_office.api_interactions.clients.clients_api_interactions import create_client_user_office
from admin_office.api_interactions.brands.brands_api_interactions import brand_creation
from admin_office.api_interactions.products.products_api_interactions import create_product_user_office
from user_office.api_interactions.organization_links.organization_links_api_interactions import OrganizationLinksMutationsAPI


def random_letter():
    return str(chr(randint(ord('a'), ord('z'))) + str(randint(0, 99)) + chr(randint(ord('a'), ord('z')))
               + str(randint(0, 99)) + chr(randint(ord('a'), ord('z'))) + str(randint(0, 99)))


@pytest.fixture(scope="session", autouse=True)
def digital_data_from_database():
    return {
        # данные из бд для кампании
        'client_id': str(get_client_id_by_naming(constants.DIGITAL_CLIENT_NAMING)),
        'brand_id': str(get_brand_id_by_naming(constants.DIGITAL_BRAND_NAMING)),
        'product_id': str(get_product_id_by_naming(constants.DIGITAL_PRODUCT_NAMING)),
        'agency_id': str(get_agency_id_by_naming(constants.DIGITAL_AGENCY_NAMING)),
        'co_brand_id': str(get_brand_id_by_naming(constants.DIGITAL_CO_BRAND_NAMING)),
        'second_co_brand_id': str(get_brand_id_by_naming(constants.DIGITAL_CO_BRAND_NAMING2)),
        'department_id': str(get_department_id_by_naming(constants.DIGITAL_DEPARTMENT_NAMING)),
        # данные для создания сущностей кампании
        'product_category_id': str(get_product_category_id_by_code(constants.DIGITAL_PRODUCT_CATEGORY_CODE)),
        'product_type_id': str(get_product_type_id_by_code(constants.DIGITAL_PRODUCT_TYPE_CODE)),
        # данные из бд для редактирования/повтора кампании
        'new_agency_id': str(get_agency_id_by_naming(constants.DIGITAL_AGENCY_NAMING2)),
        'new_client_id': str(get_client_id_by_naming(constants.DIGITAL_CLIENT_NAMING2)),
        'new_brand_id': str(get_brand_id_by_naming(constants.DIGITAL_BRAND_NAMING2)),
        'new_product_id': str(get_product_id_by_naming(constants.DIGITAL_PRODUCT_NAMING2)),
        # данные из бд для медиаплана
        'metric_code_imps': constants.DIGITAL_IMPS_METRIC_CODE,
        'metric_code_clicks': constants.DIGITAL_CLICKS_METRIC_CODE,
        'goal_id_brand': str(get_goal_id_by_code(constants.DIGITAL_GOAL_BRAND_CODE)),
        'goal_id_consd': str(get_goal_id_by_code(constants.DIGITAL_GOAL_CONSD_CODE)),
        # данные для размещения api
        'source_id_ym': str(get_source_id_by_naming(constants.DIGITAL_SOURCE_NAMING_YM)),
        'ad_format_id': str(get_ad_format_id_by_naming(constants.DIGITAL_AD_FORMAT_NAMING)),
        'ad_size_id': str(get_ad_size_id_by_naming(constants.DIGITAL_AD_SIZE_NAMING)),
        'buy_type_id': str(get_buy_type_id_by_naming(constants.DIGITAL_BUY_TYPE_NAMING_CPM)),
        'channel_naming': constants.DIGITAL_CHANNEL_NAMING,
        'seller_id_mts': str(get_seller_id_by_naming(constants.DIGITAL_SELLER_NAMING_MTS)),
        'source_id_mts_dsp': str(get_source_id_by_naming(constants.DIGITAL_SOURCE_NAMING_MTS_DSP)),
        'seller_id_ya': str(get_seller_id_by_naming(constants.DIGITAL_SELLER_NAMING_YA)),
        'source_id_yd': str(get_source_id_by_naming(constants.DIGITAL_SOURCE_NAMING_YD)),
        'source_id_af': str(get_source_id_by_naming(constants.DIFITAL_SOURCE_NAMING_APF)),
        'source_id_ad': str(get_source_id_by_naming(constants.DIFITAL_SOURCE_NAMING_ADRVR)),
        'itool_id_mts_dsp': str(get_tool_id_by_code(constants.DIGITAL_ITOOL_CODE_MTS_DSP)),
        'itool_id_ym': str(get_tool_id_by_code(constants.DIGITAL_ITOOL_CODE_YM)),
        # данные для размещения ui
        'client_name': constants.DIGITAL_CLIENT_NAME,
        'client_naming': constants.DIGITAL_CLIENT_NAMING,
        'site_mts_dsp_name': constants.DIGITAL_SOURCE_MTS_DSP_NAME,
        'site_mytarget_name': constants.DIGITAL_SOURCE_MY_TARGET_NAME,
        'site_yd_name': constants.DIGITAL_SITE_YD_NAME,
        'placement_type_din_name': constants.DIGITAL_PLACEMENT_TYPE_NAME,
        'buy_type_cpm_name': constants.DIGITAL_BUY_TYPE_CPM_NAME,
        'buy_type_vcpm_name': constants.DIGITAL_BUY_TYPE_VCPM_NAME,
        'placement_platform_desktop_name': constants.DIGITAL_PLACEMENT_PLATFORM_DESKTOP_NAME,
        'channel_olv_name': constants.DIGITAL_CHANNEL_OLV_NAME,
        'channel_display_name': constants.DIGITAL_CHANNEL_DISPLAY_NAME,
        'landing_url': constants.DIGITAL_LANDING_LINK,
        'ad_format_html5_name': constants.DIGITAL_FORMAT_HTML5_NAME,
        'ad_format_instream_bumper_ads_name': constants.DIGITAL_AD_FORMAT_INSTREAM_BUMPER_ADS_NAME,
        'ad_size_1000x120_name': constants.DIGITAL_AD_SIZE_1000X120_NAME,
        'ad_size_1160x150_name': constants.DIGITAL_AD_SIZE_1160X150_NAME,
        'base_targeting_text': constants.BASE_TARGETING_DESCRIPTION_TEXT,
        'geo_targeting_text': constants.GEO_TARGETING_DESCRIPTION_TEXT,
        # коды метрик
        'budget_metric_code': constants.DIGITAL_CLICKS_METRIC_CODE,
        'freq_metric_code': constants.DIGITAL_METRIC_CODE_FREQ,
        'ctr_metric_code': constants.DIGITAL_METRIC_CODE_CTR,
        'vtr_metric_code': constants.DIGITAL_METRIC_CODE_VTR,
        'views_metric_code': constants.DIGITAL_CLICKS_METRIC_VIEWS,
        # Названия метрик
        'ctr_metric_name': constants.DIGITAL_BENCHMARK_METRIC_CTR_NAME,
        'budget_metric_name': constants.DIGITAL_METRIC_BUDGET_NAME
    }


@pytest.fixture(scope="function", autouse=True)
def digital_test_data(digital_data_from_database, authorization_in_user_office_with_token):
    """Возвращает тестовые данные из базы данных и сгенерированные названия и нейминг"""
    # Генерируется название и нейминг кампании
    campaign_name = advertising_campaign_name_generator()
    campaign_naming = advertising_campaign_code_generator()
    # Генерируется название и нейминг кампании для редактирования и повтора
    new_campaign_name = 'Upd' + campaign_name
    new_campaign_naming = 'U' + campaign_naming
    # Генерируется название размещения
    placement_name = 'TestPlacement ' + random_letter()
    condition_triggered = False
    client_id = digital_data_from_database['client_id']
    client_name = constants.DIGITAL_CLIENT_NAME
    client_naming = constants.DIGITAL_CLIENT_NAMING
    if client_id == '':
        client_data = {
            'name': client_name,
            'naming': client_naming
        }
        client_id = create_client_user_office(client_data, authorization_in_user_office_with_token)
        condition_triggered = True
    brand_id = digital_data_from_database['brand_id']
    if brand_id == '':
        brand_data = {
            'name': constants.DIGITAL_BRAND_NAME,
            'naming': constants.DIGITAL_BRAND_NAMING
        }
        brand_id = brand_creation(brand_data, authorization_in_user_office_with_token)
        condition_triggered = True
    product_id = digital_data_from_database['product_id']
    if product_id == '':
        product_data = {
            'name': constants.DIGITAL_PRODUCT_NAME,
            'naming': constants.DIGITAL_PRODUCT_NAMING,
            'product_category_id': digital_data_from_database['product_category_id'],
            'product_type_id': digital_data_from_database['product_type_id']
        }
        product_id = create_product_user_office(product_data, authorization_in_user_office_with_token)
        condition_triggered = True
    organization_link_data = {
        'client_id': client_id,
        'brand_id': brand_id,
        'product_id': product_id
    }
    if condition_triggered:
        OrganizationLinksMutationsAPI(authorization_in_user_office_with_token).create_organization_link(
            organization_link_data
        )
    digital_data_from_database['client_id'] = client_id
    digital_data_from_database['brand_id'] = brand_id
    digital_data_from_database['product_id'] = product_id
    return {
        'campaign_name': campaign_name,
        'campaign_naming': campaign_naming,
        'new_campaign_name': new_campaign_name,
        'new_campaign_naming': new_campaign_naming,
        'placement_name': placement_name,
        **digital_data_from_database
    }


@pytest.fixture(autouse=False)
def delete_placement_template_by_id_in_organization(authorization_in_user_office_with_token):
    """Фикстура удаления всех шаблонов размещения"""
    queries_api = PlacementTemplatesQueriesAPI(authorization_in_user_office_with_token)
    mutations_api = PlacementTemplatesMutationsAPI(authorization_in_user_office_with_token)
    yield
    placement_templates = queries_api.get_all_placement_templates()
    placement_templates_ids = [template['id'] for template in placement_templates.get('data', {}).get('placementTemplates', [])]
    if placement_templates_ids:
        for placement_templates_id in placement_templates_ids:
            mutations_api.delete_placement_template(placement_templates_id)
