import time
import pandas as pd

class Node:
    def __init__(self, data):
        self.data = data
        self.next = None
        self.previous = None

    def __repr__(self):
        return str(self.data)

class LinkedList:
    def __init__(self):
        self.head = None
        self.last_node = None

    def add_last(self, node):
        if self.head is None:
            self.head = node
            self.last_node = node
            return
        self.last_node.next = node
        self.last_node = node

    def add_after(self, target_node_data, new_node):
        if self.head is None:
            raise Exception("List is empty")

        for node in self:
            if node.data == target_node_data:
                new_node.next = node.next
                node.next = new_node
                return

        raise Exception("Node with data '%s' not found" % target_node_data)

    def remove_node(self, target_node_data):
        if self.head is None:
            raise Exception("List is empty")

        if self.head.data == target_node_data:
            self.head = self.head.next
            return

        previous_node = self.head
        for node in self:
            if node.data == target_node_data:
                previous_node.next = node.next
                return
            previous_node = node

        raise Exception("Node with data '%s' not found" % target_node_data)

    def get(self, index):
        if self.head is None:
            raise Exception("List is empty")

        if index < 0:
            length = 0
            node = self.head
            while node is not None:
                node = node.next
                length += 1
            index = length + index

        node = self.head
        for i in range(index):
            if node is None:
                raise Exception("Index out of range")
            node = node.next

        if node is None:
            raise Exception("Index out of range")

        return node.data

    def __getitem__(self, index):
        return self.get(index)

    def reverse(self):
        prev_node = None
        current_node = self.head
        while current_node is not None:
            next_node = current_node.next
            current_node.next = prev_node
            prev_node = current_node
            current_node = next_node
        self.head = prev_node

    def __iter__(self):
        self.current_node = self.head
        return self

    def __next__(self):
        if self.current_node is None:
            raise StopIteration
        current_node = self.current_node
        self.current_node = self.current_node.next
        return current_node

def read_csv_rows(file_path):
    with open(file_path, 'r') as file:
        for line in file:
            yield line.strip().split(',')

start_time = time.time()
linked_list = LinkedList()
for row in read_csv_rows(r"C:\Users\livev\OneDrive\Masaüstü\orginaldata.csv"):
    linked_list.add_last(Node(row))
end_time = time.time()
elapsed_time = end_time - start_time
print("Geçen zaman:", elapsed_time, "saniye")