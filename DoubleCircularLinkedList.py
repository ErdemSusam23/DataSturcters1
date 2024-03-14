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

    def merge_sort(self):
        if self.head is None or self.head.next == self.head:
            return

        # Split the list into two halves
        list1, list2 = self.split()

        # Recursively sort the halves
        list1.merge_sort()
        list2.merge_sort()

        # Merge the sorted halves
        self.merge(list1, list2)

    def split(self):
        slow = self.head
        fast = self.head

        while fast.next != self.head and fast.next.next != self.head:
            slow = slow.next
            fast = fast.next.next

        list2 = DoubleCircularLinkedList()
        list2.head = slow.next
        slow.next = self.head

        return self, list2

    def merge(self, list1, list2):
        dummy = Node()
        tail = dummy

        while list1.head != list1.head.next and list2.head != list2.head.next:
            if list1.head.data < list2.head.data:
                tail.next = list1.head
                list1.head = list1.head.next
            else:
                tail.next = list2.head
                list2.head = list2.head.next
            tail = tail.next

        tail.next = list1.head if list1.head != list1.head.next else list2.head

        self.head = dummy.next

    def add_cumulative_sum(self):
        if self.head is None:
            raise Exception("List is empty")

        cumulative_sum = 0
        cumulative_sum_list = DoubleCircularLinkedList()

        node = self.head
        while True:
            cumulative_sum += node.data[0]  # assuming the first column contains numeric data
            cumulative_sum_list.add_last(Node(cumulative_sum))
            node = node.next
            if node == self.head:
                break

        return cumulative_sum_list


class Node:
    def __init__(self, data=None):
        self.data = data
        self.next = None
        self.prev = None


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

#READ DATA TO LINKED LIST FIRST OPTION USES PANDAS AND IT IS FASTER
start_time = time.time()

x = 1
if x == 1:
    df = pd.read_csv(r'C:\Users\ersus\OneDrive\Masaüstü\Python\DataStructuresAndAlgorithms\orginaldata.csv')
    data = df.values.tolist()
    linked_list = DoubleCircularLinkedList()
    for row in data:
        linked_list.add_last(Node(row))
else:
    linked_list = DoubleCircularLinkedList()
    for row in read_csv_rows(r'C:\Users\ersus\OneDrive\Masaüstü\Python\DataStructuresAndAlgorithms\orginaldata.csv'):
        data = float(row[0])
        linked_list.add_last(Node(data))

end_time = time.time()
elapsed_time = end_time - start_time
print("Geçen zaman:", elapsed_time, "saniye")

#FIND CUMULATIVE SUM AND WRITE IT IN ON CUMULATIVE_SUM
start_time = time.time()

cumulative_sum = linked_list.add_cumulative_sum()
print(cumulative_sum[-1])

end_time = time.time()
elapsed_time = end_time - start_time
print("Geçen zaman:", elapsed_time, "saniye")

#SORT THE ORIGINAL DATA AND WRITE IT IN ON SORTED_DATA
start_time = time.time()

sorted_data = sorted([node.data for node in linked_list])
print(sorted_data[-1])

end_time = time.time()
elapsed_time = end_time - start_time
print("Geçen zaman:", elapsed_time, "saniye")
