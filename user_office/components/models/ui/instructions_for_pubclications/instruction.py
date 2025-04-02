from playwright.sync_api import Page
from controller.title import Title
from controller.button import Button
from controller.input import Input


class InstructionsForPublications:
    """Здесь описана вся страница инструкции по публикации"""

    def __init__(self, page: Page):
        self.page = page
        self.instruction_title = Title(
            page,
            locator='[data-testid="instruction_title"]',
            name='Инструкция по публикации',
        )
        self.instruction_geo_targeting = Title(
            page,
            locator='[data-testid="instruction_title_basetargeting"]',
            name='Гео таргетинг в инструкции по публикации'
        )
        self.instruction_value_geo_targeting = Title(
            page,
            locator='[data-testid="instruction_value_geotargeting"]',
            name='Описание гео таргетинга'

        )
        self.instruction_base_targeting = Title(
            page,
            locator='[data-testid="instruction_title_basetargeting"]',
            name='Базовый таргетинг в инструкции по публикации'
        )
        self.instruction_value_base_targeting = Title(
            page,
            locator='[data-testid="instruction_value_basetargeting"]',
            name='Описание базового таргетинга'
        )
        self.instruction_descriptions = Title(
            page,
            locator='data-testid="instruction_description"',
            name='Заведите '
                 'размещение '
                 'используя '
                 'настройки '
                 'описанные в'
                 'данном '
                 'разделе.',
        )
        self.instruction_campaign_name = Title(
            page,
            locator="[data-testid='instruction_title_name_campaign']",
            name='Название кампании',
        )

        self.instructions_campaign_name_value = Title(
            page,
            locator="[data-testid='instruction_value_name_campaign']",
            name="Название кампании значение"
        )

        self.instruction_ad_title_url = Title(
            page,
            locator="[data-testid='instruction_title_ad_url']",
            name='Значение/ссылка',
        )
        self.instructions_adset_name = Title(
            page,
            locator="[data-testid='instruction_title_adset_name']",
            name='Название группы объявлений',
        )
        self.instructions_adset_value = Title(
            page,
            locator="[data-testid='instruction_value_ad_url']",
            name='Ссылка на рекламную кампанию UTM',
        )
        self.instructions_butget = Title(
            page,
            locator="[data-testid='instruction_title_budget']",
            name='Бюджет',
        )
        self.instructions_value_budget = Title(
            page,
            locator="[data-testid='instruction_value_budget']",
            name='Сумма общего бюджета',
        )
        self.instructions_daily_title_budget = Title(
            page,
            locator="[data-testid='instruction_title_daily_budget']",
            name='Бюджет Суточный',
        )
        self.instructions_value_daily_budget = Title(
            page,
            locator="[data-testid='instruction_value_daily_budget']",
            name='Сумма суточного Бюджета',
        )
        self.instructions_start_date_title = Title(
            page,
            locator="[data-testid='instruction_title_start_date']",
            name='Дата начала размещения',
        )

        self.instructions_start_date_value = Title(
            page,
            locator="[data-testid='instruction_value_start_date']",
            name="Дата/Значение"
        )

        self.instructions_end_date_title = Title(
            page,
            locator="[data-testid='instruction_title_end_date']",
            name='Дата завершения размещения',
        )

        self.instructions_end_date_value = Title(
            page,
            locator="[data-testid='instruction_value_end_date']",
            name='Дата завершения размещения значение',
        )
        self.campaign_widget_view_btn = Button(
            page,
            # locator='data-testid="campaign_widget_view_button"',
            # locator='text="Посмотреть"',
            locator="internal:testid=[data-testid=\"campaign_widget_view_button\"s]",
            name='Посмотреть'
        )

        self.mp_view_menu_btn = Button(
            page,
            # locator='td:nth-child(10)', #TODO: требуется доработка контроллера factory - клики по дата атрибутам аффектят
            locator="internal:testid=[data-testid=\"mp-view-menu\"s]",
            name='Дропдаун меню размещения'
        )
        self.connection_settings = Button(
            page,
            locator='text="Настройки подключений"',
            name="Настройки подключений"
        )

        self.statistics_method_btn = Button(
            page,
            locator="internal:testid=[data-testid=\"publication-form_site-gather-method-select\"s]",
            name='Метод сбора статистики'
        )

        self.publish_method = Button(
            page,
            locator="internal:testid=[data-testid=\"publication-form_site-publish-select\"s]",
            name='Метод Публикации'
        )

        self.manual_status = Button(
            page,
            locator='internal:text="Ручное"',
            name='Ручное'
        )

        self.postclick = Button(
            page,
            locator="internal:testid=[data-testid=\"postclick_tool\"s]",
            name='Post-click tool'
        )
        self.appsflyer_post_click = Button(
            page,
            locator='text="appsFlyer"',
            name='appsFlyer'
        )

        self.tracker = Button(
            page,
            locator="internal:testid=[data-testid=\"tracker_tool\"s]",
            name='Post-click tool'
        )

        self.adriver_tracker_tool = Button(
            page,
            locator='internal:text="AdRiver Tracker"',
            name='AdRiver Tracker'
        )

        self.verifier_tool = Button(
            page,
            locator="internal:testid=[data-testid=\"verifier_tool\"s]",
            name='verifier_tool'
        )

        self.adriver_verify = Button(
            page,
            locator='internal:text="Не используется"',
            name="Статус"
        )

        self.save_publication = Button(
            page,
            locator="internal:testid=[data-testid=\"publication_settings_save_button\"s]",
            name="Сохранить"
        )

        self.publish_btn = Button(
            page,
            locator='internal:text="Публикация"',
            name="Публикация"
        )

        self.count_creatives = Input(
            page,
            locator="internal:testid=[data-testid=\"instructions_input_count_creatives\"s]",
            name="Количество креативов"
        )

        self.create_creatives_btn = Button(
            page,
            locator="internal:testid=[data-testid=\"instructions_create_creatives\"s]",
            name="Создать креативы"
        )

        self.instructions_publication_completed_btn = Button(
            page,
            locator="internal:testid=[data-testid=\"instructions_publication_completed\"s]",
            name="Публикация"
        )

        self.published_status = Title(
            page,
            locator="internal:text=ы'Опубликовано'",
            name="Опубликовано"
        )

    def check_instruction_title(self):
        """Проверка видимости заголовков слева от значений справа, на странице инструкции по публикации
        пример Бюджет общий  1 272 024
        тест проверяет видимости текста Инструкция по публикации
        """
        self.instruction_title.should_be_visible()
        self.instruction_descriptions.should_be_visible()

    def check_instruction_campaign_name(self):
        """Проверка видимости заголовков слева от значений справа, на странице инструкции по публикации
        пример Название кампании   anth_90369h_autotestc_autotestb_au
        тест проверяет видимости текста Название кампании
        """
        self.instruction_campaign_name.should_be_visible()

    def check_ad_title_url(self):
        """
        Проверка видимости ссылки в инструкции по публикации
        """
        self.instruction_ad_title_url.should_have_text()

    def check_instructions_adset_name(self):
        """
        Проверка видимости ссылкр РК UTM
        """
        self.instructions_adset_name.should_have_text(text='Основная ссылка РК или адсета')

    def check_instructions_adset_value(self):
        """
        Проверка видимости ссылки в инструкции по публикации
        """
        self.instructions_adset_value.should_be_visible()

    def check_instructions_budget(self):
        """
        Проверка видимости - Общий бюджет
        """
        self.instructions_butget.should_be_visible()

    def check_instructions_value_budget(self):
        self.instructions_value_budget.should_be_visible()

    def check_instructions_daily_budget(self):
        """
        Проверка видимости - Бюджет суточный
        """
        self.instructions_daily_title_budget.should_be_visible()

    def check_instructions_value_daily_budget(self):
        self.instructions_value_daily_budget.should_be_visible()

    def check_instructions_start_date_title(self):
        """
        Проверка видимости - Дата начала
        """
        self.instructions_start_date_title.should_have_text(text='Дата начала размещения')

    def check_instructions_end_date_title(self):
        """
        Проверка видимости - Дата завершения
        """
        self.instructions_end_date_title.should_have_text(text='Дата завершения размещения')

    def check_geo_targeting_in_instruction_page(self):
        self.instruction_geo_targeting.should_be_visible()
        self.instruction_value_geo_targeting.should_be_visible()

    def check_base_targeting_in_instruction_page(self):
        self.instruction_base_targeting.should_be_visible()
        self.instruction_value_base_targeting.should_be_visible()

    # TODO: Переработать валидацию инструкции по публикации
    def check_all_instructions_page(self):
        self.check_instruction_campaign_name()
        self.check_instructions_budget()
        self.check_instructions_daily_budget()
        self.check_instructions_start_date_title()
        self.check_instructions_end_date_title()
        self.check_geo_targeting_in_instruction_page()
        self.check_base_targeting_in_instruction_page()


    def click_publications_button(self):
        """
        весь этот гавно костыль исправлю в рамках доработки контроллера фактори
        """
        self.campaign_widget_view_btn.click()
        self.mp_view_menu_btn.click()
        self.connection_settings.click()
        self.statistics_method_btn.click()
        self.page.keyboard.press("Enter")
        # self.status_hand.click() - Поправить локатор
        self.publish_method.click()
        self.page.keyboard.press("Enter")
        self.postclick.click()
        self.appsflyer_post_click.click()
        self.tracker.click()
        self.adriver_tracker_tool.click()
        self.verifier_tool.click()
        self.adriver_verify.click()
        self.save_publication.click()
        # self.publish_btn.click()
        # #Креативы перенесли в другое место на UI
        # # self.count_creatives.fill('4')
        # # self.create_creatives_btn.click()
        # self.instructions_publication_completed_btn.click()
        # self.page.go_back()
        # self.published_status.has_texts(text='Опубликовано')
