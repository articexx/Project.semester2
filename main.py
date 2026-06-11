from tracker import ExpenseTracker


def main():
    tracker = ExpenseTracker(days=30)

    while True:
        print("БЮДЖЕТНЫЙ ПОМОЩНИК")
        print("1. Добавить расход")
        print("2. Сумма расходов за период [A..B]")
        print("3. День с максимальным расходом")
        print("4. Категории по сумме (сортировка вставками)")
        print("5. Категории из дерева (алфавитный порядок)")
        print("6. Отменить последнее добавление (стек)")
        print("7. Показать все расходы")
        print("0. Выход")

        choice = input("Выберите действие: ")

        if choice == "1":
            try:
                day = int(input("День (1-30): "))
                amount = float(input("Сумма: "))
                category = input("Категория: ")
                msg = tracker.add_expense(day, amount, category)
                print(msg)
            except ValueError:
                print("Ошибка: введите корректные числа")

        elif choice == "2":
            try:
                a = int(input("Начальный день: "))
                b = int(input("Конечный день: "))
                s = tracker.get_range_sum(a, b)
                print(f"Сумма с {a} по {b} день: {s}")
            except ValueError:
                print("Ошибка: введите числа")

        elif choice == "3":
            day, amount = tracker.get_max_day()
            if day != -1:
                print(f"Максимальный расход: день {day}, сумма {amount}")
            else:
                print("Расходов пока нет")

        elif choice == "4":
            sorted_cats = tracker.get_sorted_by_amount()
            print("Категории по сумме трат (убывание):")
            for cat, total in sorted_cats:
                print(f"  {cat}: {total}")

        elif choice == "5":
            bst_cats = tracker.get_bst_sorted()
            print("Категории из дерева (алфавитный порядок):")
            for cat, total in bst_cats:
                print(f"  {cat}: {total}")

        elif choice == "6":
            msg = tracker.undo_last()
            print(msg)

        elif choice == "7":
            expenses = tracker.get_all_expenses()
            print("Расходы по дням:")
            for i, val in enumerate(expenses, start=1):
                if val > 0:
                    print(f"  День {i}: {val}")
            if all(v == 0 for v in expenses):
                print("  (пока пусто)")

        elif choice == "0":
            print("До свидания!")
            break

        else:
            print("Неверный выбор")


if __name__ == "__main__":
    main()