import time
import csv
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
        node.previous = self.last_node
        self.last_node = node

    def add_after(self, target_node_data, new_node):
        if self.head is None:
            raise Exception("List is empty")

        for node in self:
            if node.data == target_node_data:
                new_node.next = node.next
                node.next = new_node
                new_node.previous = node
                if new_node.next:
                    new_node.next.previous = new_node
                if node == self.last_node:
                    self.last_node = new_node
                return

        raise Exception("Node with data '%s' not found" % target_node_data)

    def remove_node(self, target_node_data):
        if self.head is None:
            raise Exception("List is empty")

        if self.head.data == target_node_data:
            self.head = self.head.next
            if self.head:
                self.head.previous = None
            return

        current_node = self.head
        while current_node:
            if current_node.data == target_node_data:
                if current_node.next:
                    current_node.next.previous = current_node.previous
                if current_node.previous:
                    current_node.previous.next = current_node.next
                if current_node == self.last_node:
                    self.last_node = current_node.previous
                return
            current_node = current_node.next

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
            current_node.previous = next_node
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

def calculate_cumulative_totals_linked_list(linked_list):
    if linked_list.head is None:
        return None
    current = linked_list.head
    cumulative_total = current.data
    current.cumulative_total = cumulative_total
    while current.next:
        current = current.next
        cumulative_total += current.data
        current.cumulative_total = cumulative_total
    return cumulative_total

# Step 1: originaldata.csv dosyasındaki verileri çift yönlü bağlı listeye ekleyerek kümülatif toplamı hesaplayalım
linked_list = LinkedList()
for row in read_csv_rows(r"C:\Users\livev\OneDrive\Masaüstü\orginaldata.csv"):
    data = float(row[0])
    linked_list.add_last(Node(data))

cumulative_total = calculate_cumulative_totals_linked_list(linked_list)
print("Kümülatif Toplam Linked List:", cumulative_total)

# Step 2: originaldata.csv dosyasındaki verileri sıralayalım
sorted_data = sorted([node.data for node in linked_list])

# Step 3: inserteddata.csv dosyasından alınan yeni veriyi uygun yere ekleyelim
new_data = pd.read_csv("inserteddata.csv")
new_value = float(new_data.iloc[0, 0])

for i, value in enumerate(sorted_data):
    if new_value < value:
        sorted_data.insert(i, new_value)
        break
else:
    sorted_data.append(new_value)

# Step 4: deleteindex.csv dosyasındaki indeks numarasına sahip veriyi listeden çıkaralım
delete_index_data = pd.read_csv("deleteindex.csv")
delete_index = int(delete_index_data.iloc[0, 0])
del sorted_data[delete_index]

print("Sıralı Veri Listesi:", sorted_data)
