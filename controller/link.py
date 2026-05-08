from controller.factory import AssertableMixin, ClickableMixin, GettableMixin, Factory


class Link(ClickableMixin, AssertableMixin, GettableMixin, Factory):
    """Компонент для работы с гиперссылками (link/anchor elements)."""

    @property
    def type_of(self) -> str:
        """Тип компонента для логирования."""
        return 'link'
