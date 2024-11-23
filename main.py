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
    pass


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
