import pandas as pd
import time

class Node:
    def __init__(self, data):
        self.data = data
        self.next = None
        self.prev = None


class DoubleCircularLinkedList:
    def __init__(self):
        self.head = None

    def clear(self):
        self.head = None
    def append(self, data):
        new_node = Node(data)
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

    def add_first(self, data):
        new_node = Node(data)
        if not self.head:
            self.head = new_node
            self.head.next = self.head
            self.head.prev = self.head
        else:
            new_node.next = self.head
            new_node.prev = self.head.prev
            self.head.prev.next = new_node
            self.head.prev = new_node
            self.head = new_node

    def delete_node_at_index(self, index):
        if self.head is None:
            return

        cur = self.head
        for i in range(index):
            cur = cur.next
            if cur == self.head:
                return  # index out of range

        # remove the node
        cur.prev.next = cur.next
        cur.next.prev = cur.prev
        if self.head == cur:  # node to be removed is head
            self.head = cur.next

    def __iter__(self):
        cur = self.head
        while True:
            yield cur.data
            cur = cur.next
            if cur == self.head:
                break

    def get(self, index):
        if self.head is None:
            return None
        cur = self.head
        for _ in range(index):
            cur = cur.next
            if cur == self.head:
                return None  # index out of range
        return cur.data

    def __getitem__(self, index):
        if self.head is None:
            raise IndexError('List is empty')
        cur = self.head
        for _ in range(index):
            cur = cur.next
            if cur == self.head:
                raise IndexError('Index out of range')
        return cur.data

    def remove_node(self, node_data):
        if self.head is None:
            return
        cur = self.head
        while True:
            if cur.data == node_data:
                if cur.next == cur:  # only one node in the list
                    self.head = None
                else:
                    cur.prev.next = cur.next
                    cur.next.prev = cur.prev
                    if self.head == cur:  # node to be removed is head
                        self.head = cur.next
                return
            cur = cur.next
            if cur == self.head:
                break

    def remove_duplicates(self):
        if self.head is None:
            return
        seen = set()
        cur = self.head
        while True:
            if cur.data in seen:
                next_node = cur.next
                self.remove_node(cur.data)
                cur = next_node
            else:
                seen.add(cur.data)
                cur = cur.next
            if cur == self.head:
                break

    def save_to_csv(self, filename):
        data = [node for node in self]
        df = pd.DataFrame(data)
        df.to_csv(filename, index=False, header=False)

    def cumulative_sum(self):
        node = self.head
        total = 0
        cumulative_list = DoubleCircularLinkedList()  # Assuming LinkedList is your linked list class

        while True:
            node_data = node.data  # 'node_data' is a float
            total += node_data
            cumulative_list.append(total)  # Append the cumulative sum to the new list
            node = node.next
            if node == self.head:
                break

        return cumulative_list  # This linked list now contains the cumulative sums


#r'C:\Users\ersus\OneDrive\Masaüstü\Python\DataStructuresAndAlgorithms\orginaldata.csv'
#r'D:\GitHub\DataSturcters1\data\inserteddata.csv'

#READ DATA TO LINKED LIST
start_time = time.time()

df = pd.read_csv(r'D:\GitHub\DataSturcters1\data\orginaldata.csv', header=None)
data = df.values.tolist()
linked_list = DoubleCircularLinkedList()
for row in data:
    for item in row:
        linked_list.append(item)

end_time = time.time()
elapsed_time = end_time - start_time
print("Read:", elapsed_time, "saniye")

#SAVE LINKED LIST TO CSV FILE
start_time = time.time()

linked_list.save_to_csv("data.csv")

end_time = time.time()
elapsed_time = end_time - start_time
print("SAVE:", elapsed_time, "saniye")

#INSERT NEW DATA TO LINKED LIST
start_time = time.time()

df = pd.read_csv(r'D:\GitHub\DataSturcters1\data\inserteddata.csv', header=None)
data = df.values.tolist()
for row in data:
    for item in row:
        linked_list.append(item)

end_time = time.time()
elapsed_time = end_time - start_time
print("Insert:", elapsed_time, "saniye")

#SORT THE LIST
start_time = time.time()
data_list = []
node = linked_list.head
while True:
    data_list.append(node.data)
    node = node.next
    if node == linked_list.head:
        break

# Convert the list to a pandas Series
series = pd.Series(data_list)

# Sort the series
sorted_series = series.sort_values()

# Clear the linked list
linked_list.clear()  # Assuming 'clear' is a method in your linked list class

# Append the sorted values back to the linked list
for item in sorted_series:
    linked_list.append(item)
end_time = time.time()
elapsed_time = end_time - start_time
print("SORT:", elapsed_time, "saniye")

#REMOVE DATA BY INDEX
start_time = time.time()

df = pd.read_csv(r'D:\GitHub\DataSturcters1\data\deleteindex.csv')
indices = df.values.tolist()
indices = [item for sublist in indices for item in sublist]
for index in indices:
    linked_list.delete_node_at_index(index)

end_time = time.time()
elapsed_time = end_time - start_time
print("REMOVE DATA BY INDEX:", elapsed_time, "saniye")

#CUMULATIVE
start_time = time.time()
cumulative_list = linked_list.cumulative_sum()
cumulative_list.save_to_csv("cumulative.csv")
end_time = time.time()
elapsed_time = end_time-start_time
print("Cumulative" , elapsed_time, "saniye")






