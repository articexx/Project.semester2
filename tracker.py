from tree import CategoryBST


class Stack:
    """Стек для хранения истории операций"""
    def __init__(self):
        self.items = []

    def push(self, item):
        self.items.append(item)

    def pop(self):
        if not self.is_empty():
            return self.items.pop()
        return None

    def is_empty(self):
        return len(self.items) == 0


class PrefixSum:
    """
    Массив расходов по дням и префиксные суммы.
    Обеспечивает O(1) для запроса суммы за период.
    """
    def __init__(self, days=30):
        self.days = days
        self.expenses = [0] * (days + 1)   # 1-индексация
        self.prefix = [0] * (days + 1)

    def add(self, day, amount):
        """Добавить расход в день и пересчитать префиксные суммы"""
        if 1 <= day <= self.days:
            self.expenses[day] += amount
            self._rebuild()

    def remove(self, day, amount):
        """Убрать расход (отмена операции)"""
        if 1 <= day <= self.days:
            self.expenses[day] -= amount
            if self.expenses[day] < 0:
                self.expenses[day] = 0
            self._rebuild()

    def _rebuild(self):
        """Перестроить массив префиксных сумм"""
        self.prefix[0] = 0
        for i in range(1, self.days + 1):
            self.prefix[i] = self.prefix[i - 1] + self.expenses[i]

    def range_sum(self, a, b):
        """Сумма расходов с дня a по день b. O(1)."""
        if 1 <= a <= b <= self.days:
            return self.prefix[b] - self.prefix[a - 1]
        return 0

    def max_day(self):
        """
        Линейный поиск дня с максимальным расходом.
        Возвращает (день, сумма).
        """
        max_val = -1
        max_d = -1
        for day in range(1, self.days + 1):
            if self.expenses[day] > max_val:
                max_val = self.expenses[day]
                max_d = day
        return max_d, max_val

    def get_all(self):
        """Вернуть массив расходов"""
        return self.expenses[1:]


class ExpenseTracker:
    """
    Основной класс бюджетного помощника.
    Управляет всеми операциями.
    """
    def __init__(self, days=30):
        self.prefix = PrefixSum(days)
        self.stack = Stack()                #стек для отмены
        self.category_bst = CategoryBST()   #дерево категорий
        self.category_dict = {}             #словарь для быстрого доступа

    def add_expense(self, day, amount, category):
        """Добавить расход"""
        if not (1 <= day <= 30):
            return "Ошибка: день должен быть от 1 до 30"

        # Обновляем префиксные суммы
        self.prefix.add(day, amount)

        # Сохраняем в стек для отмены
        self.stack.push((day, amount, category))

        # Обновляем дерево
        self.category_bst.insert(category, amount)

        # Параллельный словарь (для сортировки вставками)
        self.category_dict[category] = self.category_dict.get(category, 0) + amount

        return f"Добавлено: день {day}, сумма {amount}, категория '{category}'"

    def undo_last(self):
        """Отменить последнюю операцию (стек)"""
        if self.stack.is_empty():
            return "Нечего отменять"

        day, amount, category = self.stack.pop()

        # Откатываем префиксные суммы
        self.prefix.remove(day, amount)

        # Откатываем категории
        self.category_dict[category] -= amount
        if self.category_dict[category] <= 0:
            del self.category_dict[category]

        # Перестраиваем дерево
        self._rebuild_bst()

        return f"Отменено: день {day}, сумма {amount}, категория '{category}'"

    def _rebuild_bst(self):
        """Пересоздать дерево на основе словаря"""
        self.category_bst = CategoryBST()
        for cat, total in self.category_dict.items():
            self.category_bst.insert(cat, total)

    def get_range_sum(self, a, b):
        """Запрос суммы за период (префиксные суммы, O(1))."""
        return self.prefix.range_sum(a, b)

    def get_max_day(self):
        """День с максимальным расходом (линейный поиск)"""
        day, amount = self.prefix.max_day()
        return day, amount

    def get_sorted_by_amount(self):
        """
        Категории, отсортированные по сумме трат.
        Сортировка вставками.
        """
        items = list(self.category_dict.items())
        # Сортировка вставками по убыванию суммы
        for i in range(1, len(items)):
            key_item = items[i]
            j = i - 1
            while j >= 0 and items[j][1] < key_item[1]:
                items[j + 1] = items[j]
                j -= 1
            items[j + 1] = key_item
        return items

    def get_bst_sorted(self):
        """Категории в алфавитном порядке"""
        return self.category_bst.inorder()

    def get_all_expenses(self):
        """Все расходы по дням"""
        return self.prefix.get_all()