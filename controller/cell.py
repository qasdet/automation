from controller.factory import Factory


class Cell(Factory):
    @property
    def type_of(self) -> str:
        return 'input'

    def cells(self, cln: int, rnm: int, text: str) -> None:
        self.page.get_by_role(role='cell').nth(index=cln).filter(
            has_text=text
        ).is_visible()
        self.page.get_by_role(role='row').nth(index=rnm)
