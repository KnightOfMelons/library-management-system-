import json


class Boook:
    _id = 1

    def __init__(self, title, author, year):
        self.id = Boook._id
        Boook._id += 1
        self.title = title
        self.author = author
        self.year = year
        self.status = "в наличии"

    def __str__(self):
        return (f"ID: {self.id},"
                f"Название: {self.title},"
                f"Автор: {self.author},"
                f"Год: {self.year},"
                f"Статус: {self.status}")


class Library:
    def __init__(self):
        self.books = []
        self.load_data()

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
            self.save_data()

    def save_data(self):
        with open(file="library.json", mode="w", encoding="utf-8") as f:
            data = [{"id": book.id,
                     "title": book.title,
                     "author:": book.author,
                     "year": book.year,
                     "status": book.status
                     } for book in self.books]
            # Это как раз действие для сохранения значений в формате json
            # data - сами данные, f - это наш файл из "as f:", чуть выше
            # ensure_ascii=False это чобы русские буквы (или кириллица, как хотите)
            # не сохранялись, как "битые символы", типа вот так: "\u043d\u0430\u043b"
            # а indent=4 ответственнен за отступы при формировании файла (для лучшей читаемости)
            json.dump(data, f, ensure_ascii=False, indent=4)

    def add_book(self, title, author, year):
        book = Boook(title, author, year)
        self.books.append(book)
        self.save_data()

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
            print("==== Нету книги с таким ID ====")

    def find_book(self, search):
        search = search.lower()

        results = []
        for book in self.books:
            if (search in book.title.lower() or
                    search in book.author.lower() or
                    search in str(book.year)):
                results.append(book)

        return results

    def show_books(self):
        if not self.books:
            print("==== Книги отсутствуют ====")
            # Просто оставляем return без ничего и функция завершит своё выполнение
            return

        print("Список всех книг в библиотеке:\n"
              "-" * 50)

        for book in self.books:
            print(f"ID: {book.id}")
            print(f"Название: {book.title}")
            print(f"Автор: {book.author}")
            print(f"Год: {book.year}")
            print(f"Статус: {book.status}")
            print("-" * 50)

    def change_status(self, book_id, new_status):
        if new_status not in ["в наличии", "выдана"]:
            print("==== Некорректный статус ====")
            return

        book_to_change = None
        for book in self.books:
            if book.id == book_id:
                book_to_change = book
                break

        if book_to_change:
            book_to_change.status = new_status
            self.save_data()
            print(f"Статус книги {book_to_change.title} изменен на '{new_status}'")
        else:
            print("==== Книга с таким ID не найдена ====")


def main():
    library = Library()

    while True:
        choice = int(input(f"1. Добавить книгу,\n"
                           f"2. Удалить книгу,\n"
                           f"3. Найти книгу,\n"
                           f"4. Показать все книги,\n"
                           f"5. Изменить статус книги,\n"
                           f"0. Выход.\n"
                           f"Ваш выбор: "))

        if choice == 1:
            pass
        elif choice == 2:
            pass
        elif choice == 3:
            pass
        elif choice == 4:
            pass
        elif choice == 5:
            pass
        elif choice == 0:
            print("==== Выход из программы ====")
            break
        else:
            print("==== Некорректный выбор ====")


if __name__ == "__main__":
    main()
