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

    def is_not_empty(self):
        return self.len > 0

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

    def find_the_first_occurence(self,param):
        current = self.tail
        for _ in range(self.len):
            if current.value == param:
                return current
            current = current.right
        raise ValueError("Value not found")
    def delete(self, param):
        self.len -= 1
        if not self.is_not_empty():
            self.reset()
            return
        current = self.find_the_first_occurence(param)
        left,right = current.left,current.right
        if left:
            left.right = right
        if right:
            right.left = left
        if current is self.head and  current.left:
            self.head = current.left
        if current is self.tail and  current.right:
            self.tail = current.right

    def __len__(self):
        return self.len

    def __str__(self):
        result = f"({self.len})/ "
        current = self.tail
        if self.is_not_empty():
            print(bool(current.right))
            while bool(current.right):
                result += str(current.value) + " --> "
                current = current.right
            return result + str(current.value)
        return "List is empty"




linked_list = LinkedList()
linked_list.push(9)
linked_list.push(99)
linked_list.push(999)
linked_list.push(9999)
a = "test"
print(linked_list)
print("____________")
print(linked_list.pop())
print(linked_list.pop())
print(linked_list.pop())
print(linked_list.pop())
print("____________")
print(linked_list)
linked_list.unshift(8)
linked_list.unshift(88)
print("____________")
print(linked_list)
print("____________")
# dump(linked_list.tail)
