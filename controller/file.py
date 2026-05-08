from controller.factory import AssertableMixin, ClickableMixin, FillableMixin, GettableMixin, Factory


class File(AssertableMixin, ClickableMixin, FillableMixin, GettableMixin, Factory):
    """Компонент для работы с полями загрузки файлов (file input)."""

    @property
    def type_of(self) -> str:
        """Тип компонента для логирования."""
        return 'file_input'
