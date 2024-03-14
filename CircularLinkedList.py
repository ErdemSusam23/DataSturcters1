class Node:
    def __init__(self, data=None):
        self.data = data
        self.next = None
        

class CircularLinkedList:
    def __init__(self, nodes=None):
        self.head = None
        if nodes is not None:
            node = Node(data=nodes.pop(0))
            self.head = node
            for elem in nodes:
                node.next = Node(data=elem)
                node = node.next
            node.next = self.head

    def __iter__(self):
        node = self.head
        while True:
            yield node
            node = node.next
            if node == self.head:
                break

    def add_first(self, new_node):
        new_node.next = self.head
        node = self.head
        while node.next != self.head:
            node = node.next
        node.next = new_node
        self.head = new_node

    def add_after(self, target_node_data, new_node):
        if self.head is None:
            raise Exception("List is empty")

        node = self.head
        while node.data != target_node_data:
            node = node.next
            if node == self.head:
                raise Exception("Node with data '%s' not found" % target_node_data)

        new_node.next = node.next
        node.next = new_node

    def add_last(self, new_node):
        if self.head is None:
            self.head = new_node
            new_node.next = new_node
        else:
            node = self.head
            while node.next != self.head:
                node = node.next
            node.next = new_node
            new_node.next = self.head

    def remove_node(self, target_node_data):
        if self.head is None:
            raise Exception("List is empty")

        if self.head.data == target_node_data:
            if self.head.next == self.head:
                self.head = None
            else:
                node = self.head
                while node.next != self.head:
                    node = node.next
                node.next = self.head.next
                self.head = self.head.next
        else:
            node = self.head
            while node.next != self.head and node.next.data != target_node_data:
                node = node.next
            if node.next == self.head:
                raise Exception("Node with data '%s' not found" % target_node_data)
            node.next = node.next.next

    def get(self, index):
        if self.head is None:
            raise Exception("List is empty")

        node = self.head
        for i in range(index):
            if node.next == self.head:
                raise Exception("Index out of range")
            node = node.next

        return node.data

    def __getitem__(self, index):
        return self.get(index)

    def reverse(self):
        prev = None
        curr = self.head
        while True:
            next = curr.next
            curr.next = prev
            prev = curr
            curr = next
            if curr == self.head:
                break
        self.head = prev
