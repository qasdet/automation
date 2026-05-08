from controller.factory import AssertableMixin, Factory


class Cell(AssertableMixin, Factory):
    """Компонент для работы с ячейками таблицы."""

    @property
    def type_of(self) -> str:
        """Тип компонента для логирования."""
        return 'cell'

    def cells(self, cln: int, rnm: int, text: str) -> bool:
        """
        Проверить наличие ячейки с указанным текстом.

        Args:
            cln: Индекс колонки (0-based)
            rnm: Индекс строки (0-based)
            text: Текст, который должна содержать ячейка

        Returns:
            True если ячейка существует и видна
        """
        return (
            self.page.get_by_role(role='cell')
            .nth(index=cln)
            .filter(has_text=text)
            .is_visible()
        )
