from playwright.sync_api import Page
from controller.title import Title
from controller.button import Button


class AnalitycsPage:
    def __init__(self, page: Page) -> None:
        self.page = page
        self.landing = Title(
            page=page,
            locator="[data-testid='analytic_data_landing']",
            name="Лендинг"
        )
        self.data_conversion = Title(
            page=page,
            locator="[data-testid='analytic_data_mplan_conversion_name_0']",
            name="Конверсионная метрика"
        )
        self.analytic_data_info_about_download = Title(
            page=page,
            locator="[data-testid='analytic_data_info_about_download']",
            name='Download'
        )
        self.analytic_data_info_about_count_conversions = Title(
            page=page,
            locator="[data-testid='analytic_data_info_about_count_conversions']",
            name='About'
        )
        self.save_button = Button(
            page=page,
            locator='text="Сохранить изменения"',
            name='Сохранить изменения'
        )
        self.toastify = Title(
            page=page,
            locator='text="Изменения успешно сохранены"',
            name='Изменения успешно сохранены'
        )

    def checking_is_visibility_of_data_on_the_form(self):
        self.landing.has_texts(text='https://yandex.ru')
        self.data_conversion.should_be_visible(text="YANDEX_METRIC_IN_POST_CLICK_DONT_DELETE")
        self.analytic_data_info_about_download.has_texts(text='Яндекс Метрика 219235111')
        self.analytic_data_info_about_count_conversions.has_texts(text='1 конверсия') #Фикс бага MDP-6168
        self.page.get_by_test_id('analytic_data_mplan_instrument_name_0').click()
        self.page.get_by_role("option", name="Установки YM").click()
        text = self.page.get_by_test_id('analytic_data_mplan_instrument_name_0').inner_text()
        assert text == 'option Установки, selected.\nУстановки YM', "Не вижу выпадашки постклика"
        self.analytic_data_info_about_download.should_be_visible()
        self.analytic_data_info_about_count_conversions.should_be_visible()
        self.save_button.click()
        assert self.page.get_by_role(role='alert').all_inner_texts() != "['']"
        self.toastify.has_texts(text='Изменения успешно сохранены')

    def checking_is_not_visibility_of_data_on_the_form(self):
        self.analytic_data_info_about_download.should_be_not_visible()
        self.analytic_data_info_about_count_conversions.should_be_not_visible()
        self.page.get_by_text(
            text="В размещении отсутствуют конверсии. Чтобы сопоставить фактические конверсии, необходимо указать хотя бы одну плановую конверсию.")
