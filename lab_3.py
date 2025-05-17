class Node:
    def __init__(self, data):
        self.data = data
        self.next = None


class LinkedList:
    def __init__(self):
        self.head = None

    def append(self, data):
        new_node = Node(data)
        if not self.head:
            self.head = new_node
            return
        last_node = self.head
        while last_node.next:
            last_node = last_node.next
        last_node.next = new_node

    def to_list(self):
        result = []
        current = self.head
        while current:
            result.append(current.data)
            current = current.next
        return result

    def insert_at_beginning(self, data):
        new_node = Node(data)
        new_node.next = self.head
        self.head = new_node


def create_stack(line):
    stack = [None] * len(line)
    indices = list(range(len(line)))
    for i in range(len(line)):
        if (i % 2) == 0:
            idx = indices.pop(0)
            stack[idx] = line[i]
        else:
            idx = indices.pop()
            stack[idx] = line[i]
    return stack

from collections import deque

def arrange_cards(colors, implementation="array"):

    n = len(colors)
    line = [None] * len(colors) # Для всех реализаций используется список для "линии"

    # Заполнение линии в нужном порядке (общий код для всех реализаций)
    indices = list(range(len(colors)))
    for color in colors:
        line[indices.pop(0)] = color

    if implementation == "array":
        stack = create_stack(line)  # Используем create_stack для массивов/списков
        return stack

    elif implementation == "linked_list":
        linked_list = LinkedList()
        for item in line:
            linked_list.append(item)
        stack = create_stack(line)

        return stack


    elif implementation == "deque":
        stack = create_stack(line)  # Используем create_stack для массивов/списков
        return stack

    else:
        raise ValueError("Неверно указана реализация: array, linked_list, deque")


# --- Примеры использования ---
print("Москат Татьяна Михайловна, группа 090304-РПИа-о24")
target_colors = ['W', 'B', 'W', 'B']

# Array
initial_stack_array = arrange_cards(target_colors, implementation="array")
print(f"Array: Для целевой линии {target_colors}, исходная стопка должна быть: {initial_stack_array}")

# LinkedList
initial_stack_linked_list = arrange_cards(target_colors, implementation="linked_list")
print(f"LinkedList: Для целевой линии {target_colors}, исходная стопка должна быть: {initial_stack_linked_list}")

# Deque
initial_stack_deque = arrange_cards(target_colors, implementation="deque")
print(f"Deque: Для целевой линии {target_colors}, исходная стопка должна быть: {initial_stack_deque}")
