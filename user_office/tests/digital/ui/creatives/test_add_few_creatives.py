import time
import allure
import pytest

from helper.linkshort import JiraLink as jira
from helper.linkshort import AllureLink as case
from user_office.components.pages.mediaplan.create_mediaplan_page import (
    CreateMediaplanPage,
)
from user_office.components.pages.mediaplan.mediaplan_page import MediaplanPage
from user_office.components.pages.placement.placement_page import PlacementPage
from user_office.api_interactions.campaign.campaign_api_interactions import CampaignsMutationsAPI
from user_office.api_interactions.mediaplan.mediaplan_api_interactions import MplansMutationsAPI
from user_office.api_interactions.placement.placement_api_interactions import PlacementMutationsAPI
from user_office.api_interactions.creatives.creatives_api_interactions import CreativesMutationsAPI
from user_office.api_interactions.creatives.creatives_api_interactions import CreativesQueriesAPI
from user_office.api_interactions.targeting.targeting_api_interactions import TargetingMutationsAPI
from helper.names_generator.creative_frame_names_generator import (
    creative_frame_name_generator,
    creative_frame_naming_generator,
)
from helper.names_generator.creative_names_generator import (
    creative_name_generator,
    creative_naming_generator,
)

creative_frame_name = creative_frame_name_generator()
creative_frame_naming = creative_frame_naming_generator(creative_frame_name)
creative_frame_dictionary = {
    'name': creative_frame_name,
    'naming': creative_frame_naming,
}
creative_name = creative_name_generator()
creative_naming = creative_naming_generator(creative_name)
creatives_dictionary = {
    'name': creative_name,
    'naming': creative_naming,
}


@pytest.mark.usefixtures('authorization_in_user_office_with_token')
class TestFewCreatives:
    @staticmethod
    @pytest.mark.smoke
    @allure.title('Загрузка нескольких креативов в размещении')
    @allure.story(jira.JIRA_LINK + 'MDP-5982')
    @allure.testcase(case.ALLURE_LINK + '400854')
    @allure.severity(allure.severity_level.NORMAL)
    def test_add_few_creatives(
            create_mediaplan_page: CreateMediaplanPage,
            mediaplan_page: MediaplanPage,
            authorization_in_user_office_with_token,
            digital_test_data,
            office_base_url: str,
            placement_page: PlacementPage,

    ):
        token = authorization_in_user_office_with_token
        campaign_id = CampaignsMutationsAPI(token).create_campaign_part(digital_test_data)
        mediaplan_data = MplansMutationsAPI(token).create_mplan_part(campaign_id)
        mediaplan_id = mediaplan_data['data']['mplanPlanningCreate']['id']
        placement_id = PlacementMutationsAPI(token).create_placement_part_yandex_direct(
            mediaplan_id, digital_test_data)['data']['placementCreate']['id']
        TargetingMutationsAPI(token).add_targeting_descriptions(placement_id)
        PlacementMutationsAPI(token).add_placement_metric_budget(placement_id)
        PlacementMutationsAPI(token).setup_placement_completed_status(placement_id)
        PlacementMutationsAPI(token).approve_placement(
            mediaplan_id, placement_id
        )
        mediaplan_page.page.goto(office_base_url + "mediaplan/digital/" + mediaplan_id + "/placement/" +
                                 placement_id + "/creatives")
        CreativesMutationsAPI(token).create_creative_frame(campaign_id,
                                                           creative_frame_dictionary['name'],
                                                           creative_frame_dictionary['naming'])
        placement_page.digital_placement.creatives.click_add_creative_button()
        i = 1
        while i < 4:  # Кол-во креативов, которые мы хотим добавить в креативную рамку. В данном случае - три.
            placement_page.digital_placement.creatives.click_create_creative_button()
            placement_page.digital_placement.creatives.choose_creative_form_frame(creative_frame_dictionary['name'])
            placement_page.digital_placement.creatives.choose_creative_adsize('1170x200')
            placement_page.digital_placement.creatives.fill_creative_name(creatives_dictionary['name'] + '_' + str(i))
            placement_page.digital_placement.creatives.fill_creative_naming(creatives_dictionary['naming'] + '_' + str(i))
            with placement_page.digital_placement.creatives.page.expect_file_chooser() as fc:
                placement_page.digital_placement.creatives.page.get_by_role(
                    'button', name="Выберите файлы или переместите их сюда").click()
            file_chooser = fc.value
            # Строку ниже можно раскомментировать только при локальном тестировании
            # file_chooser.set_files("1170x200.jpg")
            # А это строку ниже, при локальном тестировании нужно закомментировать, соответственно
            file_chooser.set_files("user_office/tests/digital/ui/creatives/1170x200.jpg")
            placement_page.digital_placement.creatives.click_creative_form_submit()
            time.sleep(1)
            placement_page.digital_placement.creatives.page.get_by_role("checkbox").nth(0).check()
            placement_page.digital_placement.creatives.click_general_button_confirm()
            placement_page.digital_placement.creatives.page.get_by_text("Добавлен", exact=True).nth(0).click()
            i += 1
        placement_page.digital_placement.creatives.click_general_button_cancel()
        get_info_from_server = CreativesQueriesAPI(token).get_creatives_from_specific_placement(placement_id)
        list_of_creative_names_from_ui = []
        list_of_creative_names_from_server = []
        for item in range(3):
            input_field_check = placement_page.digital_placement.creatives.page.get_by_label(
                "Название креатива").nth(item).element_handle()
            final_result = input_field_check.evaluate("node => node.value")
            list_of_creative_names_from_ui.append(final_result)
        for item in get_info_from_server['data']['placementCreatives']:
            list_of_creative_names_from_server.append(item['name'])
        assert list_of_creative_names_from_ui == list_of_creative_names_from_server, "Список названий креативов, " \
                                                                                     "собранный на странице креативов " \
                                                                                     "не совпадает со списком, " \
                                                                                     "полученным от сервера."
