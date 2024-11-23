import json


class Boook:
    _id = 1

    # Ниже - конструктор для инициализации книг с её названием, автором и т.д.
    def __init__(self, title, author, year):
        self.id = Boook._id
        Boook._id += 1
        self.title = title
        self.author = author
        self.year = year
        self.status = "в наличии"

    # Метод для строкового представления
    def __str__(self):
        return (f"ID: {self.id},"
                f"Название: {self.title},"
                f"Автор: {self.author},"
                f"Год: {self.year},"
                f"Статус: {self.status}")


class Library:
    # Также конструктор для инициализации
    def __init__(self):
        self.books = []
        self.load_data()

    # Функция для загрузки данных из JSON
    def load_data(self):
        try:
            with open(file="library.json", mode="r", encoding="utf-8") as f:
                data = json.load(f)

                for book_data in data:
                    book = Boook(book_data["title"],
                                 book_data["author"],
                                 book_data["year"])
                    book.id = book_data["id"]
                    book.status = book_data["status"]
                    Boook._id = max(Boook._id, book.id + 1)
                    self.books.append(book)
        except FileNotFoundError:
            # Тут если же файл не найден, то вызываю метод для сохранения
            self.save_data()

    # Это уже метод для сохранения данных JSON
    def save_data(self):
        with open(file="library.json", mode="w", encoding="utf-8") as f:
            data = [{"id": book.id,
                     "title": book.title,
                     "author": book.author,
                     "year": book.year,
                     "status": book.status
                     } for book in self.books]
            # Это как раз действие для сохранения значений в формате json
            # data - сами данные, f - это наш файл из "as f:", чуть выше
            # ensure_ascii=False это чобы русские буквы (или кириллица, как хотите)
            # не сохранялись, как "битые символы", типа вот так: "\u043d\u0430\u043b"
            # а indent=4 ответственнен за отступы при формировании файла (для лучшей читаемости)
            json.dump(data, f, ensure_ascii=False, indent=4)

    # Добавление книги в библиотеку
    def add_book(self, title, author, year):
        book = Boook(title, author, year)
        self.books.append(book)
        self.save_data()

    # Удаление книги по ID
    def remove_book(self, book_id):
        book_for_remove = None  # Поставил это значение в случае,
        # если не найдём книгу с нужным id
        for book in self.books:
            if book.id == book_id:
                book_for_remove = book
                break

        if book_for_remove:
            self.books.remove(book_for_remove)
            self.save_data()
        else:
            print("\n==== Нету книги с таким ID ====")

    # Поиск книги по названию, автору, году
    def find_book(self, search):
        search = search.lower()

        results = []
        for book in self.books:
            if (search in book.title.lower() or
                    search in book.author.lower() or
                    search in str(book.year)):
                results.append(book)

        return results

    # Отображение вообще всех книг, которые есть (в красивом/удобном формате!!!)
    def show_books(self):
        if not self.books:
            print("==== Книги отсутствуют ====")
            # Просто оставляем return без ничего и функция завершит своё выполнение
            return

        print("Список всех книг в библиотеке:\n")
        print("-" * 50)

        for book in self.books:
            print(f"ID: {book.id}\n"
                  f"Название: {book.title}\n"
                  f"Автор: {book.author}\n"
                  f"Год: {book.year}\n"
                  f"Статус: {book.status}")
            print("-" * 50)

    # Изменение статуса книги
    def change_status(self, book_id, new_status):
        if new_status not in ["в наличии", "выдана"]:
            print("==== Некорректный статус ====")
            raise ValueError("Некорректный статус")

        book_to_change = None
        for book in self.books:
            if book.id == book_id:
                book_to_change = book
                break

        book_to_change.status = new_status
        self.save_data()
        print(f"Статус книги {book_to_change.title} изменен на '{new_status}'")


# Это, собственно, и есть главная функция для запуска программы
def main():
    library = Library()

    # Ниже стандартный интерфейс для взаимодействием с пользователем, а также
    # свои значения для ввода при выборе определенного choice
    while True:
        choice = int(input(f"\n1. Добавить книгу,\n"
                           f"2. Удалить книгу,\n"
                           f"3. Найти книгу,\n"
                           f"4. Показать все книги,\n"
                           f"5. Изменить статус книги,\n"
                           f"0. Выход.\n"
                           f"\nВаш выбор: "))

        # Добавление книги
        if choice == 1:
            title = input("\nВведите название книги: ")
            author = input("Введите автора книги: ")
            year = int(input("Введите год выпуска книги: "))
            library.add_book(title, author, year)

            print("\n==== Книга добавлена в библиотеку ====\n")

        # Удаление книги
        elif choice == 2:
            while True:
                try:
                    book_id = int(input("Введите ID книги для удаления: "))
                    library.remove_book(book_id)
                    break
                except ValueError:
                    print("\n==== Введено некорректное значение ====\n")

        # Нахождение книги
        elif choice == 3:
            search_term = input("Введите поисковый запрос (название, автор или год): ")
            results = library.find_book(search_term)
            if results:
                print("Найденные книги:")
                for book in results:
                    print(book)
            else:
                print("\n==== Книги не найдены по запросу ====")

        # Вывод всех книг
        elif choice == 4:
            library.show_books()

        # Изменение статуса книги
        elif choice == 5:
            while True:
                try:
                    book_id = int(input("Введите ID книги, статус которой хотите изменить: "))
                    break
                except ValueError:
                    print("\n==== Введено некорректное значение ====\n")

            book_to_change = None
            for book in library.books:
                if book.id == book_id:
                    book_to_change = book
                    break

            if book_to_change:
                new_status = input("Введите новый статус ('в наличии' или 'выдана'): ").lower()
                library.change_status(book_id, new_status)
            else:
                print("\n==== Книга с таким ID не найдена ====")

        # Просто выход из программы
        elif choice == 0:
            print("\n==== Выход из программы ====")
            break

        # Доколе некорректно введено значение
        else:
            print("\n==== Некорректный выбор ====")


if __name__ == "__main__":
    main()
