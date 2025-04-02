from typing import Self

from playwright.sync_api import Page


class KeyBind:
    __instance = None

    def __new__(cls) -> Self:
        if cls.__instance is None:
            cls.__instance: Self = super().__new__(cls=cls)
        return cls.__instance

    @staticmethod
    def press_enter(page: Page) -> None:
        page.keyboard.press(key='Enter')
