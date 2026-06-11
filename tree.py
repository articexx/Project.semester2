class TreeNode:
    """Узел бинарного дерева поиска"""
    def __init__(self, key, value):
        self.key = key        # название категории
        self.value = value    # сумма трат в категории
        self.left = None
        self.right = None


class CategoryBST:
    """
    Бинарное дерево поиска.
    Ключ это категория (строка).
    Значение это общая сумма трат по категории.
    """
    def __init__(self):
        self.root = None

    def insert(self, key, value):
        """Вставить категорию или добавить сумму, если категория уже есть"""
        self.root = self._insert(self.root, key, value)

    def _insert(self, node, key, value):
        if node is None:
            return TreeNode(key, value)
        if key < node.key:
            node.left = self._insert(node.left, key, value)
        elif key > node.key:
            node.right = self._insert(node.right, key, value)
        else:
            # Категория существует => увеличиваем сумму
            node.value += value
        return node

    def inorder(self):
        """Обход inorder возвращает категории в алфавитном порядке"""
        result = []
        self._inorder(self.root, result)
        return result

    def _inorder(self, node, result):
        if node is not None:
            self._inorder(node.left, result)
            result.append((node.key, node.value))
            self._inorder(node.right, result)

    def is_empty(self):
        return self.root is None