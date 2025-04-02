class DigitalUrl:
    @staticmethod
    def get_url_digital_campaigns_list_page(
            office_base_url: str
    ) -> str:
        """Функция возвращает URL для списка рекламных кампаний"""
        campaigns_list_page_url = (
                office_base_url + 'campaigns/digital'
        )
        return campaigns_list_page_url

    @staticmethod
    def get_url_digital_campaign_page(
            office_base_url: str, campaign_id: str
    ) -> str:
        """Функция собирает URL для рекламной кампании
                office_base_url: основной корневой url
                campaign_id: принимает на вход uuid кампании
        """
        campaign_page_url = (
                office_base_url + 'campaigns/digital/' + campaign_id
        )
        return campaign_page_url

    @staticmethod
    def get_url_digital_mplan_page(office_base_url: str, mplan_id: str) -> str:
        """Функция собирает URL для медиаплана
                office_base_url: основной корневой url
                mplan_id: принимает на вход uuid медиплана
        """
        mplan_page_url = (
                office_base_url + 'mediaplan/digital/' + mplan_id
        )
        return mplan_page_url

    @staticmethod
    def get_url_digital_create_mp_page(
            office_base_url: str, campaign_id: str
    ) -> str:
        """Функция собирает URL для создания медиплана
                campaign_id: принимает на вход uuid медиплана
        """
        create_mp_page_url = (
                office_base_url
                + 'campaigns/digital/'
                + campaign_id
                + '/createmediaplan'
        )
        return create_mp_page_url

    @staticmethod
    def get_url_digital_placement_page(
            office_base_url: str, mplan_id: str, placement_id: str
    ) -> str:
        """Функция собирает URL для создания медиплана
                mplan_id: принимает на вход uuid медиплана
                placement_id: принимает на вход uuid размещения
        """
        placement_page_url = (
                office_base_url
                + 'mediaplan/digital/'
                + mplan_id
                + '/placement/'
                + placement_id
                + '/composition'
        )
        return placement_page_url

    @staticmethod
    def get_url_digital_create_placement_page(
            office_base_url: str, mplan_id: str
    ) -> str:
        """Функция собирает URL для страницы размещения
                office_base_url: основной корневой url
                mplan_id: принимает на вход uuid медиплана
        """
        create_placement_page_url = (
                office_base_url
                + 'mediaplan/digital/'
                + mplan_id
                + '/placementcreate/general'
        )
        return create_placement_page_url

    @staticmethod
    def get_url_digital_create_instructions_for_publications(
            office_base_url: str, mplan_id: str, instructions_id: str
    ) -> str:
        """Функция собирает URL
                office_base_url: основной корневой url
                mplan_id: принимает на вход uuid медиплана
                instructions_id: принимает на вход uuid инструкции по публикации
        """
        create_instructions_for_publications_url = (
                office_base_url
                + 'mediaplan/digital/'
                + mplan_id
                + '/instructions/'
                + instructions_id
        )
        return create_instructions_for_publications_url

    @staticmethod
    def get_url_dictionaries_page(
            office_base_url: str, naming: str
    ) -> str:
        create_guide_url = (
                office_base_url
                + '/dictionaries/digital/'
                + naming
        )

        return create_guide_url

    @staticmethod
    def get_url_digital_reporting_page(
            office_base_url: str, campaign_id: str, default_begin_date: str, default_end_date: str
    ) -> str:
        """Функция собирает URL для страницы отчета План-факт
                office_base_url: основной корневой url
                campaign_id: id кампании
                default_begin_date: дефолтная дата начала кампании
                default_end_date: дефолтная дата завершения кампании
        """
        reporting_page_url = (
                office_base_url
                + 'campaigns/digital/'
                + campaign_id
                + f'/analytics/plan-fact?finishOn={default_end_date}&startOn={default_begin_date}'
        )
        return reporting_page_url

    def get_url_digital_data_analitycs_page(
            office_base_url: str, campaign_id: str
    ) -> str:
        """Функция собирает URL для страницы Аналитики
                office_base_url: основной корневой url
                campaign_id: id кампании
        """
        reporting_page_url = (
                office_base_url
                + 'campaigns/digital/'
                + campaign_id
                + f'/analytics/data'
        )
        return reporting_page_url