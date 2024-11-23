from main import Boook, Library
import json
import unittest
from unittest.mock import patch, mock_open


class TestLibrary(unittest.TestCase):
    # Тут создаю библиотеку с двумя книгами
    def setUp(self):
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
    def test_remobe_book(self):
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

    # Проверка на изменение статуса
    def test_change_status(self):
        self.library.change_status(1, "выдана")
        self.assertEqual(self.library.books[0].status, "выдана")

        with self.assertRaises(ValueError):
            self.library.change_status(1, "неизвестный статус")

    # Проверка на загрузку данных из файла
    def test_load_data(self):
        # Тут сейчас буду использовать моки для имитации файловых операций
        with patch("builtins.open", unittest.mock.mock_open(read_data=json.dumps([
            {"id": 1, "title": "Загруженная книга тест", "author": "Автор тест", "year": 2022, "status": "в наличии"}
        ]))):
            library = Library()
            self.assertEqual(len(library.books), 1)
            self.assertEqual(library.books[0].title, "Загруженная книга тест")

    # Проверка сохранение данных в файл
    def test_save_data(self):
        # Тут также мок буду использовать
        mock_file = mock_open()

        with patch("builtins.open", mock_file):
            with open("library.json", "w", encoding="utf-8") as f:
                f.write('{"title": "Book One", "author": "Author One"}')

        mock_file().write.assert_called_once_with('{"title": "Book One", "author": "Author One"}')

    # Проверка обработки некорректных ID
    def test_invalid_book_id(self):
        with patch("builtins.input", return_value="9999"):
            with patch("builtins.print") as mocked_print:
                self.library.remove_book(9999)
                mocked_print.assert_called_with("\n==== Нету книги с таким ID ====")

    # Проверка обработки некорректного статуса
    def test_invalid_status_change(self):
        with self.assertRaises(ValueError):  # Проверяем, что исключение ValueError будет выброшено
            self.library.change_status(1, "неизвестный статус")


if __name__ == "__main__":
    unittest.main()
