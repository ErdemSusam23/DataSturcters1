import pandas as pd
import time

class DoubleCircularLinkedList:
    def __init__(self, nodes=None):
        self.head = None
        if nodes is not None:
            node = Node(data=nodes.pop(0))
            self.head = node
            prev_node = node
            for elem in nodes:
                node.next = Node(data=elem)
                node.next.prev = node
                node = node.next
            node.next = self.head
            self.head.prev = node

    def __iter__(self):
        node = self.head
        while True:
            yield node
            node = node.next
            if node == self.head:
                break
    def add_first(self, new_node):
        if self.head is None:
            self.head = new_node
            new_node.next = new_node
            new_node.prev = new_node
        else:
            last_node = self.head.prev
            new_node.next = self.head
            new_node.prev = last_node
            self.head.prev = new_node
            self.head = new_node

    def add_after(self, target_node_data, new_node):
        if self.head is None:
            raise Exception("List is empty")

        for node in self:
            if node.data == target_node_data:
                new_node.prev = node
                new_node.next = node.next
                node.next.prev = new_node
                node.next = new_node
                return

        raise Exception("Node with data '%s' not found" % target_node_data)
    
    def add_last(self, new_node):
        if self.head is None:
            self.head = new_node
            new_node.next = new_node
            new_node.prev = new_node
        else:
            last_node = self.head.prev
            last_node.next = new_node
            new_node.prev = last_node
            new_node.next = self.head
            self.head.prev = new_node

    def remove_node(self, target_node_data):
        if self.head is None:
            raise Exception("List is empty")

        for node in self:
            if node.data == target_node_data:
                node.prev.next = node.next
                node.next.prev = node.prev
                if node is self.head:
                    self.head = node.next
                node.prev = None
                node.next = None
                return

        raise Exception("Node with data '%s' not found" % target_node_data)
    
    def get(self, index):
        if self.head is None:
            raise Exception("List is empty")

        if index < 0:
            length = 0
            node = self.head
            while node.next != self.head:
                node = node.next
                length += 1
            index = length + index

        node = self.head
        for i in range(index):
            if node.next == self.head:
                raise Exception("Index out of range")
            node = node.next

        if node.next == self.head:
            raise Exception("Index out of range")

        return node.data

    def __getitem__(self, index):
        return self.get(index)
    
    def reverse(self):
        if self.head is None:
            return

        prev_node = None
        curr_node = self.head
        next_node = curr_node.next
        while next_node != self.head:
            curr_node.next = prev_node
            curr_node.prev = next_node
            prev_node = curr_node
            curr_node = next_node
            next_node = next_node.next

        curr_node.next = prev_node
        curr_node.prev = self.head
        self.head = curr_node
    
class Node:
    def __init__(self, data=None):
        self.data = data
        self.next = None
        self.prev = None
        
start_time = time.time()
df = pd.read_csv(r"C:\Users\livev\OneDrive\Masaüstü\orginaldata.csv")


data = df.values.tolist()


linked_list = DoubleCircularLinkedList()

for row in data:
    linked_list.add_last(Node(row))
end_time = time.time()
elapsed_time = end_time - start_time
print("Geçen zaman:", elapsed_time, "saniye")