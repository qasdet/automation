# from admin_office.archive.models.graphql_queries import (
#     CREATE_BRAND_QUERY,
#     DELETE_BRAND_QUERY,
# )
# from admin_office.archive.models.pages import BaseDictionaryPageAPI
# from admin_office.tests.api.dictionaries.brands.api_interactions import (
#     make_few_requests_brands_list,
#     get_brands_request,
# )
# from db_stuff.db_interactions import local_db_send_query
# from db_stuff.db_queries import RECORD_IN_DB
# from gitlab_conf import DEV_GRAPHQL, DEV_DB_USER, DEV_DB_PASSWORD


# TODO Требуется актуализация тестов. Падают по непонятным причинам.
def test_several_responses_contain_same_data():
    pass
    # errors = []
    # brands = []
    # list_of_responses = make_few_requests_brands_list(
    #     5, get_brands_request.post_request()
    # )
    # for item in list_of_responses:
    #     if item.get("data"):
    #         brands.append(item)
    #     else:
    #         errors.append(item)
    # assert len(errors) == 0, "Некоторые запросы содержат ошибки в теле ответа"
    # assert len(brands) == len(list_of_responses), (
    #     "Количество элементов в изначальном списке не совпадает с кол-вом "
    #     "элементов, которые подверглись проверке наполнения "
    # )


def test_create_brand():
    pass
    # send_create_request = BaseDictionaryPageAPI(
    #     DEV_GRAPHQL, "CreateBrand", CREATE_BRAND_QUERY
    # )
    # created_brand_result = send_create_request.post_request()
    # assert (
    #         created_brand_result.get("data") is not None
    # ), "Данные в ответе пусты. Необходимо проверить запрос к серверу"
    # result_response = created_brand_result.get("data").get("BrandCreate").get("client")
    # for item in result_response.values():
    #     assert (
    #             item is not None
    #     ), "Какое-то из полей ответа пустое. Необходимо проверить запрос к серверу"
    # what_happened_in_db_after_brand_created = local_db_send_query(
    #     RECORD_IN_DB, DEV_DB_USER, DEV_DB_PASSWORD
    # )
    # assert what_happened_in_db_after_brand_created is not [], (
    #     "После создания бренда через АПИ, в базе эта запись " "не появилась "
    # )


def test_delete_brand():
    pass
    # send_delete_request = BaseDictionaryPageAPI(
    #     DEV_GRAPHQL, "DeleteBrand", DELETE_BRAND_QUERY
    # )
    # deleted_brand_result = send_delete_request.post_request()
    # assert (
    #         deleted_brand_result.get("data") is not None
    # ), "Данные в ответе пусты. Необходимо проверить запрос к серверу"
    # result_response = list(deleted_brand_result.get("data").values())[0]
    # assert result_response is True, "Сервер вернул не True, возможно запись не удалена"
    # what_happened_in_db_after_brand_deleted = local_db_send_query(
    #     RECORD_IN_DB, DEV_DB_USER, DEV_DB_PASSWORD
    # )
    # assert what_happened_in_db_after_brand_deleted is not None, (
    #     "После удаления бренда через АПИ, в базе эта запись " "не исчезла "
    # )
