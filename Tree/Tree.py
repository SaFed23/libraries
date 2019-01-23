import sys
from copy import deepcopy
import pandas as pd
import anytree as atr


class TreeForNumber:

    def __init__(self, data=0):
        self.data = data
        self.left = None
        self.right = None
        self.level = 0

    def __add_level(self, __height=0):
        """Добавляет уровень к существующим узлам в дереве"""
        self.level = __height
        if self.left is not None:
            self.left.__add_level(__height + 1)
        if self.right is not None:
            self.right.__add_level(__height + 1)

    def add_node(self, new_top, flag=0):
        """Создание листа"""
        # Добавление одинакового листа влево
        if flag == 1:
            if self.data >= new_top.data:
                if self.left is None:
                    self.left = new_top
                else:
                    self.left.add_node(new_top, flag=1)
            if self.data < new_top.data:
                if self.right is None:
                    self.right = new_top
                else:
                    self.right.add_node(new_top, flag=1)
        # Добавление одинакового листа вправо
        if flag == 2:
            if self.data > new_top.data:
                if self.left is None:
                    self.left = new_top
                else:
                    self.left.add_node(new_top, flag=2)
            if self.data <= new_top.data:
                if self.right is None:
                    self.right = new_top
                else:
                    self.right.add_node(new_top, flag=2)
        # Исключение при наличии
        if flag == 0:
            try:
                if self.data > new_top.data:
                    if self.left is None:
                        self.left = new_top
                    else:
                        return self.left.add_node(new_top)
                if self.data < new_top.data:
                    if self.right is None:
                        self.right = new_top
                    else:
                        return self.right.add_node(new_top)
                if self.data == new_top.data:
                    raise ValueError
            except ValueError:
                sys.exit("This value exist in tree: " + str(self.data))

    def add_value(self, data, flag=0):
        """Добавление листа со значением"""
        new_top = TreeForNumber(data)
        self.add_node(new_top, flag)
        self.__add_level()

    def search_link(self, data):
        """Поиск узла перед узлом с заданным значением"""
        try:
            if self.left is None and self.right is None:
                raise ValueError
            if self.left is not None:
                if self.left.data == data:
                    return self
            if self.right is not None:
                if self.right.data == data:
                    return self
            if self.data > data:
                if self.left:
                    return self.left.search_link(data)
                else:
                    raise ValueError
            if self.data < data:
                if self.right:
                    return self.right.search_link(data)
        except ValueError:
            sys.exit("This value don't exist in tree")

    def search(self, data):
        """Поиск данного значения в дереве"""
        try:
            if self.data > data:
                if self.left is not None:
                    return self.left.search(data)
                else:
                    raise ValueError
            if self.data < data:
                if self.right is not None:
                    return self.right.search(data)
                else:
                    raise ValueError
            if self.data == data:
                return self
        except ValueError:
            sys.exit("This value don't exist in tree")

    def end_left(self):
        """Поиск последнего элемента слева"""
        if self.left is not None:
            return self.left.end_left()
        else:
            return self

    def end_right(self):
        """Поиск последнего элемента справа"""
        if self.right is not None:
            return self.right.end_right()
        else:
            return self

    def delete(self, data, flag=0):
        """Удаление листа или вершины из дерева"""
        node_for_delete = self.search(data)
        # Удаление листа
        if node_for_delete.left is None and node_for_delete.right is None:
            node = self.search_link(data)
            if node.left == node_for_delete:
                node.left = None
                return
            else:
                node.right = None
                return
        # Удаление вершины и подтягивание левого листа,
        # если правого листа не существует
        elif node_for_delete.right is None and node_for_delete.left is not None:
            node = self.search_link(data)
            if node.left == node_for_delete:
                node.left = node_for_delete.left
                return
            else:
                node.right = node_for_delete.left
                return
        # Удаление вершины и подтягивание правого листа,
        # если левого листа не существует
        elif node_for_delete.left is None and node_for_delete.right is not None:
            node = self.search_link(data)
            if node.left == node_for_delete:
                node.left = node_for_delete.right
                return
            else:
                node.right = node_for_delete.right
                return
        # Удаление вершины, в которой существует
        # как правое поддерево, так и левое
        elif node_for_delete.left is not None and node_for_delete.right is not None:
            if flag == 0:
                new_node = node_for_delete.left
                new_node = new_node.end_right()
                self.delete(new_node.data)
                node_for_delete.data = new_node.data
                return
            else:
                new_node = node_for_delete.right
                new_node = new_node.end_left()
                self.delete(new_node.data)
                node_for_delete.data = new_node.data
                return

    def lrn(self):
        """Обратный обход"""
        if self.left is not None:
            self.left.lrn()
        if self.right is not None:
            self.right.lrn()
        print(self.data, end=' ')

    def nlr(self):
        """Прямой обход"""
        print(self.data, end=' ')
        if self.left is not None:
            self.left.nlr()
        if self.right is not None:
            self.right.nlr()

    def lnr(self):
        """Центрированный обход"""
        if self.left is not None:
            self.left.lnr()
        print(self.data, end=' ')
        if self.right is not None:
            self.right.lnr()

    def bfs(self):
        """Обход в ширину"""
        queue = []
        values = []
        queue.append(self)
        while len(queue) > 0:
            temp_node = queue.pop(0)
            values.append(temp_node)
            if temp_node.left is not None:
                queue.append(temp_node.left)
            if temp_node.right is not None:
                queue.append(temp_node.right)
        return values

    def tree_by_list(self, array, flag=0):
        """Создание дерева из списка"""
        for element in array:
            new_top = TreeForNumber(element)
            self.add_node(new_top, flag)
        self.__add_level()

    def list_by_tree(self):
        """Создание списка из дерева"""
        array_top = self.bfs()
        values = []
        for top in array_top:
            values.append(top.data)
        return values

    def print_in_level(self):
        """Вывод дерева по уровню"""
        list_array = self.bfs()
        level = list_array[0].level
        for top in list_array:
            if level == top.level:
                print(top.data, end=' ')
            else:
                print('\n' + str(top.data), end=' ')
            level = top.level
        print()

    def __search_level(self, level):
        """Поиск элементов на соответствующем уровне"""
        list_array = self.bfs()
        values = []
        for top in list_array:
            if level == top.level:
                values.append(top)
        return values

    def __height(self):
        """Определение высоты дерева"""
        return max(self.left.__height() if self.left is not None else 0,
                   self.right.__height() if self.right is not None else 0) + 1

    def list_of_link(self):
        """Создание списка связей"""
        array = self.bfs()
        array_link = []
        for top in array:
            if top.left is not None:
                array_link.append([top.data, top.left.data])
            if top.right is not None:
                array_link.append([top.data, top.right.data])
        return array_link

    def print_tree(self):
        """Вывод дерева"""
        array_link = self.list_of_link()
        array_index = list(map(lambda x: x[1], array_link))
        array_value = list(map(lambda x: x[0], array_link))
        df = pd.DataFrame([array_value, array_index])
        array_tree = [atr.Node(str(df.iloc[0, 0]))]
        for i in range(len(df.columns)):
            index = None
            for top in array_tree:
                if str(df.iloc[0, i]) == top.name:
                    index = array_tree.index(top)
            if index is not None:
                array_tree.append(atr.Node(str(df.iloc[1, i]), parent=array_tree[index]))
        for pre, fill, node in atr.RenderTree(array_tree[0]):
            print("%s%s" % (pre, node.name))

    @staticmethod
    def split(base_array, size):
        """Разбиение списка на части"""
        arrays = []
        while len(base_array) > size:
            part = base_array[:size]
            arrays.append(part)
            base_array = base_array[size:]
        arrays.append(base_array)
        return arrays

    @classmethod
    def balanced_tree_by_array(cls, base_array):
        """Создание сбалансированного дерева из списка"""
        arrays = list([sorted(base_array)])
        root = TreeForNumber(data=None)
        size = 2
        while len(arrays) > 0:
            new_array = []
            for array in arrays:
                size = len(array) // 2
                if len(arrays) == 1:
                    root.data = array.pop(size)
                else:
                    root.add_value(array.pop(size))
                if len(array) > 1:
                    new_array += cls.split(array, size)
                elif len(array) != 0:
                    root.add_value(array.pop())
            arrays = new_array
        return root

    def balanced_tree_by_tree(self):
        """Создание сбалансированного дерева из существующего"""
        array = self.list_by_tree()
        return TreeForNumber.balanced_tree_by_array(array)

    @classmethod
    def create_tree(cls, array, flag=0):
        """Создание дерева"""
        root = cls(array.pop(0))
        root.tree_by_list(array, flag)
        return root

    # Перегрузка операторов

    def __lt__(self, other):
        """Меньше"""
        return self.__height() < other.__height()

    def __le__(self, other):
        """Меньше или равно"""
        return self.__height() <= other.__height()

    def __eq__(self, other):
        """Равно"""
        return self.__height() == other.__height()

    def __ne__(self, other):
        """Не равно"""
        return self.__height() != other.__height()

    def __gt__(self, other):
        """Больше"""
        return self.__height() > other.__height()

    def __ge__(self, other):
        """Больше или равно"""
        return self.__height() >= other.__height()

    def __iter__(self):
        """Создание итератора"""
        return iter(self.bfs())

    def __len__(self):
        """Высота"""
        return self.__height() - 1

    def __getitem__(self, item):
        """Вызов"""
        values = self.__search_level(item)
        if len(values):
            return self.__search_level(item)
        else:
            sys.exit("Wrong index. Numbering starts with 0 and ends with the height of the tree")

    def __contains__(self, item):
        """Определение на пренадлежность"""
        return item in self.list_by_tree()

    def __add__(self, other):
        """Сложение двух деревьев"""
        root = deepcopy(self)
        new_top = deepcopy(other)
        root.add_node(new_top, flag=1)
        root.__add_level()
        return root

    def __str__(self):
        """Вывод"""
        self.print_tree()
        return ''
