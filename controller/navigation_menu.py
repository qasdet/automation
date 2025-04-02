from controller.factory import Factory

# Навигационное меню в Admin-office


class NavigationMenu(Factory):
    @property
    def type_of(self) -> str:
        return 'navigation menu'

    def goto(self, name_item: str) -> None:
        """Переход на указанную страницу
        Args:
            name_item название пункта меню
        """
        self.should_be_visible(name_item=name_item)
        self.click(name_item=name_item)
