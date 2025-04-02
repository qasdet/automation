import logging
from abc import ABC, abstractmethod
from pathlib import Path

import allure
from playwright.sync_api import Locator, Page, expect

this_dir = Path(__file__).resolve().parent

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s',
    filename=f'{this_dir}/pytest.log',
    filemode='w',
)


class Factory(ABC):
    def __init__(self, page: Page, locator: str, name: str) -> None:
        self.page: Page = page
        self.name: str = name
        self.locator: str = locator

    @property
    @abstractmethod
    def type_of(self) -> str:
        """Функция type_of возвращает наименование компонента для отчетности в аллюр"""
        return 'component'

    def get_locator(self, **kwargs) -> Locator:
        """
        Метод get_locator получает на вход все локаторы и преобразует их в строку
        Args:
            На вход принимается любой локатор в том числе и динамический в виде - data_test_id{number}
            динамический локатор обрабатывается в **kwargs
        Return:
            На выходе мы получаем именованые аргументы в виде строки
        """
        locator: str = self.locator.format(**kwargs)
        logging.info(f'I see you: locator {locator}')
        return self.page.locator(locator)

    def click(self, **kwargs) -> None:
        """
        Метод click получает на вход локаторы из метода get_locator и кликает по локаторам
        Args:
            На вход принимается любой локатор в том числе и динамический в виде - data_test_id{number}
            динамический локатор обрабатывается в **kwargs
        Return:
            На выходе мы получаем клик по строке или динамическому локатору
        """
        with allure.step(
                title=f'Clicking {self.type_of} with name "{self.name}"'
        ):
            locator: Locator = self.get_locator(**kwargs)
            logging.info(f'Clicking {self.type_of} with name "{self.name}"')
            locator.highlight()
            locator.click()

    def should_be_visible(self, **kwargs) -> None:
        with allure.step(
                title=f'Checking that {self.type_of} "{self.name}" is visible'
        ):
            locator: Locator = self.get_locator(**kwargs)
            expect(actual=locator, message='Не вижу локатор').to_be_visible()
            logging.info(
                f'Checking that {self.type_of} "{self.name}" is visible'
            )
            try:
                expect(
                    actual=locator, message='Не вижу локатор'
                ).to_be_visible(timeout=10.0)
            except AssertionError as err:
                logging.debug(err)

    def should_be_not_visible(self, **kwargs) -> None:
        """Проверка видимости локатора"""
        with allure.step(
                title=f'Checking that {self.type_of} "{self.name}" is visible'
        ):
            locator: Locator = self.get_locator(**kwargs)
            logging.info(
                f'Checking that {self.type_of} "{self.name}" is visible'
            )
            expect(
                actual=locator, message='Не вижу локатор'
            ).not_to_be_visible()

    def should_have_text(self, text: str, **kwargs) -> None:
        """Проверка видимости теста на страницеы

        Args:
            text (str): _description_
        """
        with allure.step(
                title=f'Checking that {self.type_of} "{self.name}" has text "{text}"'
        ):
            locator: Locator = self.get_locator(**kwargs)
            logging.info(
                f'Checking that {self.type_of} "{self.name}" has text "{text}"'
            )
            expect(actual=locator).to_have_text(expected=text)
            assert locator.is_visible()

    def matching_by_text(self, **kwargs) -> None:
        """Матчинг текста на странице"""
        with allure.step(
                title=f'Matching by text {self.type_of} with name "{self.name}"'
        ):
            locator: Locator = self.get_locator(**kwargs)
            logging.info(
                f'Matching by text {self.type_of} with name "{self.name}"'
            )
            self.page.locator(selector=f'internal:text=("{locator}")')

    def inner_text(self, **kwargs) -> str:
        """Поиск текста внутри элементов страницы - классов/дата атрибутов/айдишников

        Returns:
            str: _description_
        """
        with allure.step(
                title=f'Inner text {self.type_of} with name "{self.name}"'
        ):
            locator: Locator = self.get_locator(**kwargs)
            logging.info(f'Inner text {self.type_of} with name "{self.name}"')
            return locator.inner_text()

    def hover(self, **kwargs) -> None:
        """Метод наведения курсора на объект/элемент страницы"""
        with allure.step(
                title=f'Hovering over {self.type_of} with name "{self.name}"'
        ):
            locator: Locator = self.get_locator(**kwargs)
            logging.info(
                f'Hovering over {self.type_of} with name "{self.name}"'
            )
            locator.highlight()
            locator.hover()

    @staticmethod
    def file_check_in_folder(folder: str, file_format: str, numbers: int):
        """Метод проверяющий наличие файлов в папке по формату
        numbers: принимает число, относительного пути для перехода по директории "вниз"
                например чтобы спустится на уровень ниже от папки automation/files в папку automation
                нужно передать в аргумнет цифру 1
        file_format: формат файла который нужен проверить в папке - например .xlsx
                file_format='.xlsx'
        folder: папка где нужно проверить искомый файл
                folder = './files'
        """
        current_path = Path.cwd().parents[numbers] / folder
        for file in current_path.iterdir():
            if file.suffix == file_format and file.is_file():
                assert file.is_file() == True, 'Файл отсутствует'
                assert (
                        file.suffix == file_format
                ), 'Расширение файла не соответствует'
