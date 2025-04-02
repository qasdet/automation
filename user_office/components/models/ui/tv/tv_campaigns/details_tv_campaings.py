from user_office.components.models.ui.tv.tv_campaigns.create_tv_campaings import (
    CreateTVCampaign,
)


class DetailsTVCampaign(CreateTVCampaign):
    """Модель страницы Детали кампании

    Примечание: модель имеет теже самые элементы, что и старница создания,
    поэтому отнаследована от нее и расширина необходимыми методами проверки
    Страница отображается после нажатия кнопки Сохранить Черновик
    или Подробнее о кампании
    """

    def check_campaign_info_in_planning_status(
        self, full_fields: bool = True, **kwargs: str
    ) -> None:
        """Проверяем, что информация о кампании в статусе
        Пларирование совпадает с указанной
        Args:
            full_fields: True заполнить все поля,
                        False заполнить обязательные поля
            **kwargs: ожидаеммая информация
        """
        # self.status.should_have_text(PLANNING_STATUS)
        self.check_campaign_information(full_fields=full_fields, **kwargs)

    def check_campaign_info_in_draft_status(
        self, full_fields: bool = True, **kwargs: str
    ) -> None:
        """Проверяем, что информация о кампании в статусе
        Черновик совпадает с указанной
        Args:
            full_fields: True заполнить все поля,
                         False заполнить обязательные поля
            **kwargs: ожидаеммая информация
        """
        # self.status.should_have_text(DRAFT_STATUS)
        self.check_campaign_information(full_fields=full_fields, **kwargs)

    def check_campaign_information(
        self, full_fields: bool = True, **kwargs: str
    ) -> None:
        """Проверяем, что информация о кампании совпадает с указанной
        Args:
            full_fields: True заполнить все поля,
                         False заполнить обязательные поля
            **kwargs: ожидаеммая информация
        """
        # self.title.should_have_text(kwargs.get('name'))
        self.date_start.should_have_value(kwargs.get('date_start'))
        self.date_end.should_have_value(kwargs.get('date_end'))
        self.client.should_have_text(
            f"{kwargs.get('client')} {kwargs.get('code_client')}"
        )
        self.brand.should_have_text(
            f"{kwargs.get('brand')} {kwargs.get('code_brand')}"
        )
        self.product.should_have_text(
            f"{kwargs.get('product')} {kwargs.get('code_product')}"
        )
        if full_fields:
            # TODO Расскоментировать повле исправления MDP-3607
            # self.market_targets_description.should_have_text(
            #     kwargs.get("market_targets", "")
            # )
            self.target_audience_description.should_have_text(
                kwargs.get('target_audience', '')
            )
            self.conditions_description.should_have_text(
                kwargs.get('conditions', '')
            )
