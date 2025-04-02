from playwright.sync_api import Page

from controller.button import Button


class Filter:
    """Фильтр на странице списка digital кампаний"""

    def __init__(self, page: Page) -> None:
        self.page = page

        self.filters = Button(page, locator='form button', name='form button')
        self.dropdown = Button(
            page, locator='.css-19bb58m', name='.css-19bb58m'
        )
        self.dropdown_list = Button(
            page,
            locator='#react-select-2-option-0',
            name='#react-select-2-option-0',
        )
        self.accept_btn = Button(page, locator='button', name='Применить')

    def filter_click(self):
        self.filters.should_be_visible()
        self.filters.click()

    def dropdown_filter(self):
        self.dropdown.should_be_visible()
        self.dropdown.click()

    def dropdown_lists(self):
        self.dropdown_list.should_be_visible()
        self.dropdown_list.click()

    def filter_campaing(self):
        self.filter_click()
        self.dropdown_filter()
        self.dropdown_lists()
