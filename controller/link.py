from controller.factory import Factory

"""Компонент для обработки ссылок"""


class Link(Factory):
    @property
    def type_of(self) -> str:
        return 'link'
