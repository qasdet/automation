import time

from controller.button import Button
from playwright.sync_api import Page
from controller.drop_down_list import DropDownList
from controller.input import Input
from controller.list_item import ListItem
from gitlab_conf import ENV_VARIABLES
from user_office import constants


class DigitalPlacementConnections:
    def __init__(self, page: Page) -> None:
        self.page: Page = page
        self.site_statistics_method = DropDownList(
            page=page,
            locator='[data-testid='
                    "'publication-form_site-gather-method-select']",
            name='Выпадающий список выбора метода статистики для площадки',
        )
        self.site_account = DropDownList(
            page=page,
            locator='[data-testid='
                    "'publication-form_site-integration-token-select']",
            name='Выпадающий список выбора аккаунта площадки',
        )
        self.site_publish_method = DropDownList(
            page=page,
            locator="[data-testid='publication-form_site-publish-select']",
            name='Выпадающий список выбора метода публикации для площадки',
        )
        self.creative_publish_method = DropDownList(
            page=page,
            locator="[data-testid='publication-form_creative-select']",
            name="Выпадающий список выбора метода публикации для креативов'",
        )
        self.post_click_tool = DropDownList(
            page=page,
            locator="[data-testid='postclick_tool']",
            name='Выпадающий список выбора post-click tool',
        )
        self.post_click_tool_statistics_method = DropDownList(
            page=page,
            locator="[data-testid='postclick_gatherMethod']",
            name='Метод сбора статистики post-click tool',
        )
        self.post_click_tool_counter_id = Input(
            page=page,
            locator="[data-testid='postclick_counterID']",
            name='Идентификатор счетчика',
        )
        self.post_click_tool_account = DropDownList(
            page=page,
            locator="[data-testid='postclick_integration-token-select']",
            name='Выбор аккаунта Post-click',
        )
        self.post_click_application = DropDownList(
            page=page,
            locator="[data-testid='postclick_app_selection_{app_num}']",
            name='Приложение post-click tool',
        )
        self.post_click_in_app_event = Input(
            page=page,
            locator="[data-testid='postclick_inapp_event_{event_num}']",
            name='In-App события',
        )
        self.application_item = ListItem(
            page, locator="text='com.goodok.mts'", name='МТС GOODOK'
        )
        self.tracker_tool = DropDownList(
            page=page,
            locator="[data-testid='tracker_tool']",
            name='Выпадающий список выбора tracker tool',
        )
        self.verification_tool = DropDownList(
            page=page,
            locator="[data-testid='verifier_tool']",
            name='Выпадающий список выбора verification tool',
        )
        self.add_third_party_account_button_for_publication = Button(
            page=page,
            locator="[data-testid='publication-form_site-integration-token-select-add-account-button']",
            name='Кнопка добавления аккаунта сторонних сервисов'
        )
        self.add_third_party_account_button_for_post_click_tool = Button(
            page=page,
            locator="[data-testid='postclick_integration-token-select-add-account-button']",
            name='Кнопка добавления аккаунта сторонних сервисов post-click'
        )

    def fill_all_fields_default(self) -> None:
        """Заполнение всех полей настроек подключений по дефолту"""
        self.site_statistics_method.select_item_by_text(constants.DIGITAL_CONNECTIONS_ITEM_METHOD_MANUAL)
        self.site_publish_method.select_item_by_text(constants.DIGITAL_CONNECTIONS_ITEM_METHOD_MANUAL)
        self.post_click_tool.select_item_by_text(constants.DIGITAL_CONNECTIONS_ITEM_NOT_USED)
        self.tracker_tool.select_item_by_text(constants.DIGITAL_CONNECTIONS_ITEM_NOT_USED)
        self.verification_tool.hover()
        self.verification_tool.select_item_by_text(constants.DIGITAL_CONNECTIONS_ITEM_NOT_USED)

    def fill_all_fields_yandex_direct(self) -> None:
        """Заполнение полей настроек подключения. Яндекс Директ, Post-click tool Яндекс Метрика"""
        self.site_statistics_method.select_item_by_text(constants.DIGITAL_CONNECTIONS_ITEM_METHOD_AUTO)
        self.site_account.select_item_by_text(ENV_VARIABLES['yandex_direct_account'])
        self.site_publish_method.select_item_by_text(constants.DIGITAL_CONNECTIONS_ITEM_METHOD_MANUAL)
        self.post_click_tool.select_item_by_text(constants.DIGITAL_SITE_YM_NAME)
        self.post_click_tool_statistics_method.select_item_by_text(
            constants.DIGITAL_CONNECTIONS_ITEM_METHOD_AUTO
        )
        self.post_click_tool_counter_id.fill(constants.DIGITAL_POST_CLICK_COUNTER_ID_1)
        self.post_click_tool_account.select_item_by_text(ENV_VARIABLES['yandex_metric_account'])
        self.tracker_tool.select_item_by_text(constants.DIGITAL_CONNECTIONS_ITEM_NOT_USED)
        self.verification_tool.hover()
        self.verification_tool.select_item_by_text(constants.DIGITAL_CONNECTIONS_ITEM_NOT_USED)

    def yandex_direct_stat_gathering_method_automatic(
            self, statistic_method=constants.DIGITAL_CONNECTIONS_ITEM_METHOD_AUTO
    ) -> str:
        """Заполнение полей настроек подключения. Подключение к Яндекс.Директ, разрешение доступа из Яндекс.Директ
        для нашего ЛК"""
        self.site_statistics_method.select_item_by_text(statistic_method)
        self.site_account.click()
        with self.site_account.page.expect_popup() as yandex_popup_window:
            self.add_third_party_account_button_for_publication.click()
        # TODO Создать отдельный класс для yandex_popup_window (MDP-5770)
        yandex_popup_window_url = yandex_popup_window.value
        yandex_popup_window_url.goto(yandex_popup_window_url.url)
        yandex_popup_window_url.get_by_label("Mobile phone number").fill(ENV_VARIABLES['yandex_login'])
        yandex_popup_window_url.get_by_role("button", name="Next").click()
        yandex_popup_window_url.get_by_placeholder("Enter your password").fill(ENV_VARIABLES['yandex_password'])
        yandex_popup_window_url.get_by_role("button", name="Next").click()
        # TODO Поискать замену time.sleep в методах playwright (MDP-5793)
        time.sleep(7)
        if yandex_popup_window_url.is_visible('h1'):
            yandex_popup_window_url.get_by_role("button", name="Not now").click()
            yandex_popup_window_url.get_by_role("button", name=f"Log in as {ENV_VARIABLES['yandex_login']}").click()
        else:
            yandex_popup_window_url.get_by_role("button", name=f"Log in as {ENV_VARIABLES['yandex_login']}").click()
        self.site_account.click()
        self.site_publish_method.select_item_by_text(constants.DIGITAL_CONNECTIONS_ITEM_METHOD_MANUAL)
        self.creative_publish_method.select_item_by_text(constants.DIGITAL_CONNECTIONS_ITEM_METHOD_MANUAL)
        self.post_click_tool.select_item_by_text(constants.DIGITAL_CONNECTIONS_ITEM_NOT_USED)
        self.tracker_tool.select_item_by_text(constants.DIGITAL_CONNECTIONS_ITEM_NOT_USED)
        self.verification_tool.select_item_by_text(constants.DIGITAL_CONNECTIONS_ITEM_NOT_USED)
        time.sleep(5)
        value_of_chosen_account = self.site_account.inner_text()
        return value_of_chosen_account

    def yandex_metric_stat_gathering_method_automatic(
            self, counter_id_value=constants.DIGITAL_POST_CLICK_COUNTER_ID_2
    ) -> str:
        """Заполнение полей настроек подключения. Подключение к Яндекс.Метрике, разрешение доступа из Яндекс.Метрики
        для нашего ЛК"""
        self.site_statistics_method.select_item_by_text(constants.DIGITAL_CONNECTIONS_ITEM_METHOD_MANUAL)
        self.site_publish_method.select_item_by_text(constants.DIGITAL_CONNECTIONS_ITEM_METHOD_MANUAL)
        self.creative_publish_method.select_item_by_text(constants.DIGITAL_CONNECTIONS_ITEM_METHOD_MANUAL)
        self.tracker_tool.select_item_by_text(constants.DIGITAL_CONNECTIONS_ITEM_NOT_USED)
        self.verification_tool.select_item_by_text(constants.DIGITAL_CONNECTIONS_ITEM_NOT_USED)
        self.post_click_tool.select_item_by_text(constants.DIGITAL_SITE_YM_NAME)
        self.post_click_tool_statistics_method.select_item_by_text(constants.DIGITAL_CONNECTIONS_ITEM_METHOD_AUTO)
        self.post_click_tool_account.click()
        with self.post_click_tool_account.page.expect_popup() as yandex_direct_popup_window:
            self.add_third_party_account_button_for_post_click_tool.click()
        yandex_popup_window_url = yandex_direct_popup_window.value
        yandex_popup_window_url.goto(yandex_popup_window_url.url)
        yandex_popup_window_url.get_by_label("Mobile phone number").fill(ENV_VARIABLES['yandex_login'])
        yandex_popup_window_url.get_by_role("button", name="Next").click()
        yandex_popup_window_url.get_by_placeholder("Enter your password").fill(ENV_VARIABLES['yandex_password'])
        yandex_popup_window_url.get_by_role("button", name="Next").click()
        # TODO Поискать замену time.sleep в методах playwright (MDP-5793)
        time.sleep(10)
        if yandex_popup_window_url.is_visible('h1'):
            yandex_popup_window_url.get_by_role("button", name="Not now").click()
            yandex_popup_window_url.get_by_role("button", name=f"Log in as {ENV_VARIABLES['yandex_login']}").click()
        else:
            yandex_popup_window_url.get_by_role("button", name=f"Log in as {ENV_VARIABLES['yandex_login']}").click()
        self.post_click_tool_account.click()
        self.post_click_tool_counter_id.fill(counter_id_value)
        time.sleep(5)
        value_of_chosen_post_click_account = self.post_click_tool_account.inner_text()
        return value_of_chosen_post_click_account

    def yandex_metric_gathering_method_automatic(self,
                                                 counter_id_value=constants.DIGITAL_POST_CLICK_COUNTER_ID_3) -> None:
        """Заполнение полей настроек подключения, выбор Яндекс акканута из выпадающего списка - автоматически"""
        self.site_statistics_method.select_item_by_text(constants.DIGITAL_CONNECTIONS_ITEM_METHOD_MANUAL)
        self.site_publish_method.select_item_by_text(constants.DIGITAL_CONNECTIONS_ITEM_METHOD_MANUAL)
        self.creative_publish_method.select_item_by_text(constants.DIGITAL_CONNECTIONS_ITEM_METHOD_MANUAL)
        self.tracker_tool.select_item_by_text(constants.DIGITAL_CONNECTIONS_ITEM_NOT_USED)
        self.verification_tool.select_item_by_text(constants.DIGITAL_CONNECTIONS_ITEM_NOT_USED)
        self.post_click_tool.select_item_by_text(constants.DIGITAL_SITE_YM_NAME)
        self.post_click_tool_statistics_method.select_item_by_text(constants.DIGITAL_CONNECTIONS_ITEM_METHOD_AUTO)
        self.post_click_tool_account.click()
        # self.page.get_by_role("option", name="ewan.dolvitch (1908728804)").click()
        # закомментил, т.к метод все равно не используется
        # TODO: https://jira.mts.ru/browse/MDP-6106
        self.post_click_tool_counter_id.fill(counter_id_value)

    def yandex_metric_gathering_method_manual(self) -> None:
        """Заполнение полей настроек подключения, выбор Яндекс акканута из выпадающего списка - В ручную"""
        self.site_statistics_method.select_item_by_text(constants.DIGITAL_CONNECTIONS_ITEM_METHOD_MANUAL)
        self.site_publish_method.select_item_by_text(constants.DIGITAL_CONNECTIONS_ITEM_METHOD_MANUAL)
        self.creative_publish_method.select_item_by_text(constants.DIGITAL_CONNECTIONS_ITEM_METHOD_MANUAL)
        self.tracker_tool.select_item_by_text(constants.DIGITAL_CONNECTIONS_ITEM_NOT_USED)
        self.verification_tool.select_item_by_text(constants.DIGITAL_CONNECTIONS_ITEM_NOT_USED)
        self.post_click_tool.select_item_by_text(constants.DIGITAL_SITE_YM_NAME)

    def check_all_fields_yandex_direct(self) -> None:
        """Проверка заполнения настроек подключений. Яндекс Директ"""
        self.site_statistics_method.should_have_text(constants.DIGITAL_CONNECTIONS_ITEM_METHOD_AUTO)
        self.site_account.should_have_text(ENV_VARIABLES['yandex_direct_account'])
        self.site_publish_method.should_have_text(constants.DIGITAL_CONNECTIONS_ITEM_METHOD_MANUAL)
        self.post_click_tool.should_have_text(constants.DIGITAL_SITE_YM_NAME)
        self.post_click_tool_statistics_method.should_have_text(
            constants.DIGITAL_CONNECTIONS_ITEM_METHOD_AUTO
        )
        self.post_click_tool_counter_id.should_have_value(constants.DIGITAL_POST_CLICK_COUNTER_ID_1)
        self.post_click_tool_account.should_have_text(ENV_VARIABLES['yandex_metric_account'])
        self.tracker_tool.should_have_text(constants.DIGITAL_CONNECTIONS_ITEM_NOT_USED)
        self.verification_tool.should_have_text(constants.DIGITAL_CONNECTIONS_ITEM_NOT_USED)

    def fill_all_fields_post_click_appsflyer(self) -> None:
        """Заполнение полей настроек подключения. Post-click tool AppsFlyer"""
        self.site_statistics_method.select_item_by_text(constants.DIGITAL_CONNECTIONS_ITEM_METHOD_MANUAL)
        self.site_publish_method.select_item_by_text(constants.DIGITAL_CONNECTIONS_ITEM_METHOD_MANUAL)
        self.post_click_tool.select_item_by_text(constants.DIGITAL_POST_CLICK_APPSFLYER_NAME)
        self.post_click_tool_statistics_method.select_item_by_text(
            constants.DIGITAL_CONNECTIONS_ITEM_METHOD_AUTO
        )
        self.post_click_tool_account.select_item_by_text(constants.DIGITAL_APPSFLYER_ACC)
        self.post_click_application.click(app_num=0)
        self.application_item.click()
        self.post_click_in_app_event.fill(constants.DIGITAL_IN_APP_EVENT, event_num=0)
        self.tracker_tool.select_item_by_text(constants.DIGITAL_CONNECTIONS_ITEM_NOT_USED)
        self.verification_tool.hover()
        self.verification_tool.select_item_by_text(constants.DIGITAL_CONNECTIONS_ITEM_NOT_USED)

    def check_all_fields_post_click_appsflyer(self) -> None:
        """Проверка заполнения настроек подключений. Яндекс Директ"""
        self.site_statistics_method.should_have_text(constants.DIGITAL_CONNECTIONS_ITEM_METHOD_MANUAL)
        self.site_publish_method.should_have_text(constants.DIGITAL_CONNECTIONS_ITEM_METHOD_MANUAL)
        self.post_click_tool.should_have_text(constants.DIGITAL_POST_CLICK_APPSFLYER_NAME)
        self.post_click_tool_statistics_method.should_have_text(
            constants.DIGITAL_CONNECTIONS_ITEM_METHOD_AUTO
        )
        self.post_click_tool_account.should_have_text(constants.DIGITAL_APPSFLYER_ACC)
        self.post_click_application.should_have_text(constants.DIGITAL_POST_CLICK_APP, app_num=0)
        self.post_click_in_app_event.should_have_value(
            constants.DIGITAL_IN_APP_EVENT, event_num=0
        )
        self.tracker_tool.should_have_text(constants.DIGITAL_CONNECTIONS_ITEM_NOT_USED)
        self.verification_tool.should_have_text(constants.DIGITAL_CONNECTIONS_ITEM_NOT_USED)
