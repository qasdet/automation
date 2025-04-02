from controller.factory import Factory

"""Компонент принимает любой список значений"""


class ListItem(Factory):
    @property
    def type_of(self) -> str:
        return 'list item'
