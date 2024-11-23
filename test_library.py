import json
import unittest
from main import Boook, Library
from unittest.mock import patch, mock_open


class TestLibrary(unittest.TestCase):
    def setUp(self):
        with patch('main.Library.load_data'):
            self.library = Library()
            self.library.books = [
                Boook("Книга тест 1", "Автор тест 1", 2024),
                Boook("Книга тест 2", "Автор тест 2", 2023)
            ]
            self.library.books[0].id = 1
            self.library.books[1].id = 2
            Boook._id = 3

    # Проверка на добавление книги
    def test_add_book(self):
        self.library.add_book("Новая книга тест", "Новый автор тест", 2022)
        self.assertEqual(len(self.library.books), 3)
        self.assertEqual(self.library.books[-1].title, "Новая книга тест")
        self.assertEqual(self.library.books[-1].author, "Новый автор тест")
        self.assertEqual(self.library.books[-1].year, 2022)
        self.assertEqual(self.library.books[-1].status, "в наличии")

    # Проверка на удаление книги
    def test_remove_book(self):
        self.library.remove_book(1)
        self.assertEqual(len(self.library.books), 1)
        self.assertNotIn(1, [book.id for book in self.library.books])

    # Проверка на поиск книги
    def test_find_book(self):
        # Тут проверяю поиск по названию
        results = self.library.find_book("Книга тест 1")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].title, "Книга тест 1")

        # Тут проверяю на поиск по автору
        results = self.library.find_book("Автор тест 2")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].author, "Автор тест 2")

    # Проверка на изменение статуса книги
    def test_change_status(self):
        self.library.change_status(1, "выдана")
        self.assertEqual(self.library.books[0].status, "выдана")

        with self.assertRaises(ValueError):
            self.library.change_status(1, "неизвестный статус")

    # Проверка на загрузку данных из файла
    def test_load_data(self):
        # Тут сейчас буду использовать моки для имитации файловых операций
        mock_data = json.dumps([
            {"id": 1, "title": "Загруженная книга тест", "author": "Автор тест", "year": 2022, "status": "в наличии"}
        ])

        with patch("builtins.open", mock_open(read_data=mock_data)):
            library = Library()
            self.assertEqual(len(library.books), 1)
            self.assertEqual(library.books[0].title, "Загруженная книга тест")
            self.assertEqual(library.books[0].author, "Автор тест")

    # Проверка сохранения данных в файл
    def test_save_data(self):
        mock_file = mock_open()

        with patch("builtins.open", mock_file):
            self.library.save_data()

        written_data = ''.join(call.args[0] for call in mock_file().write.call_args_list)

        expected_data = json.dumps([{
            "id": 1,
            "title": "Книга тест 1",
            "author": "Автор тест 1",
            "year": 2024,
            "status": "в наличии"
        }, {
            "id": 2,
            "title": "Книга тест 2",
            "author": "Автор тест 2",
            "year": 2023,
            "status": "в наличии"
        }], ensure_ascii=False, indent=4)

        self.assertEqual(written_data, expected_data)

    # Проверка обработки некорректного ID
    def test_invalid_book_id(self):
        # Тут мокирую ввод и проверяю, что выводится корректное сообщение об ошибке
        with patch("builtins.input", return_value="9999"):
            with patch("builtins.print") as mocked_print:
                self.library.remove_book(9999)
                mocked_print.assert_called_with("\n==== Нету книги с таким ID ====")

    # Проверка обработки некорректного статуса
    def test_invalid_status_change(self):
        with self.assertRaises(ValueError):  # Проверяем, что исключение ValueError будет выброшено
            self.library.change_status(1, "неизвестный статус")


if __name__ == "__main__":
    # # Изолируем реальные операции с файлом (у меня до этого library.json файл весь потерся из-за ошибки)
    with patch("builtins.open", mock_open()):
        unittest.main()
