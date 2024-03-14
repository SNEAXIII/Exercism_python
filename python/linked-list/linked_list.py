class Node:
    def __init__(self, value, left=None, right=None):
        self.left: Node = left
        self.value = value
        self.right: Node = right

    def __str__(self):
        left_val = None
        if self.left:
            left_val = self.left.value
        right_val = None
        if self.right:
            right_val = self.right.value

        return f"{left_val}<--{self.value}-->{right_val}"


class LinkedList:
    def __init__(self):
        self.reset()

    def reset(self):
        self.len = 0
        self.tail = self.head = None

    def is_empty(self):
        return self.len <= 0

    def is_not_empty(self):
        return not self.is_empty()

    def is_critical(self):
        return self.len < 0

    def push(self, param):
        if self.is_not_empty():
            new_head = Node(param)
            copy_head = self.head
            new_head.left = copy_head
            copy_head.right = new_head
            self.head = new_head
        else:
            self.head = self.tail = Node(param)
        self.len += 1

    def unshift(self, param):
        if self.is_not_empty():
            new_tail = Node(param)
            copy_tail = self.tail
            new_tail.right = copy_tail
            copy_tail.left = new_tail
            self.tail = new_tail
        else:
            self.head = self.tail = Node(param)
        self.len += 1

    def shift(self):
        self.len -= 1
        if self.is_critical():
            raise IndexError("List is empty")
        return_value = self.tail.value
        if self.is_not_empty():
            new_tail = self.tail.right
            new_tail.left = None
            self.tail = new_tail
        else:
            self.reset()
        return return_value

    def pop(self):
        self.len -= 1
        if self.is_critical():
            raise IndexError("List is empty")
        return_value = self.head.value
        if self.is_not_empty():
            new_head = self.head.left
            new_head.right = None
            self.head = new_head
        else:
            self.reset()
        return return_value

    def find_the_first_occurence(self, param):
        current = self.tail
        for _ in range(self.len):
            if current.value == param:
                return current
            current = current.right
        raise ValueError("Value not found")

    def delete(self, param):
        current = self.find_the_first_occurence(param)
        left, right = current.left, current.right
        if self.len == 1:
            self.reset()
            return
        elif self.len == 2:
            for node in (left, right):
                if node:
                    self.tail = self.head = Node(node.value)
            self.len -= 1
            return
        if current is self.head:
            self.head = left
        elif current is self.tail:
            self.tail = right
        if left: left.right = right
        if right: right.left = left
        self.len -= 1

    def __len__(self):
        return self.len

    def __str__(self):
        if self.is_not_empty():
            to_right = f"({self.len})/ "
            current = self.tail
            while bool(current.right):
                to_right += str(current.value) + " --> "
                current = current.right
            to_right += str(current.value) + "\n"
            to_left = ""
            current = self.head
            while bool(current.left):
                to_left = " <-- " + str(current.value) + to_left
                current = current.left
            to_left = " " * 5 + str(current.value) + to_left + "\n"
            return to_right + to_left
        return "List is empty"