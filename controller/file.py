from controller.factory import Factory

"""Компонент для обработки загрузки/выгрузки эксель файлов"""


class File(Factory):
    @property
    def type_of(self) -> str:
        return 'file_input'

    # def file_check_in_folder(folder: str, file_format: str, number: int):
    #     """Метод проверяющий наличие файлов в папке по формату
    #     number: принимает число, относительного пути для перехода по директории "вниз"
    #             например чтобы спустится на уровень ниже от папки automation/files в папку automation
    #             нужно передать в аргумнет цифру 1
    #     file_format: формат файла который нужен проверить в папке - например .xlsx
    #             file_format='.xlsx'
    #     folder: папка где нужно проверить искомый файл
    #             folder = './files'
    #     file_xlsx: путь до файла или абсолютно укзанный файл
    #     """
    #
    #     current_path = Path.cwd().parents[number] / folder
    #     for file in current_path.iterdir():
    #         if file.suffix == file_format and file.is_file():
    #             assert file.is_file() == True, 'Файл отсутствует'
    #             assert (
    #                     file.suffix == file_format
    #             ), 'Расширение файла не соответсвует'
    #     return folder, file_format, number, file
