from controller.factory import AssertableMixin, ClickableMixin, GettableMixin, Factory


class ListItem(ClickableMixin, AssertableMixin, GettableMixin, Factory):
    """Компонент для работы с элементами списка (list item)."""

    @property
    def type_of(self) -> str:
        """Тип компонента для логирования."""
        return 'list item'
