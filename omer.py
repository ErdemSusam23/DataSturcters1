import csv
import time
import pandas as pd

class Node:
    def __init__(self, data):
        self.data = data
        self.cumulative_total = None
        self.next = None

class LinkedList:
    def __init__(self):
        self.head = None
        self.tail = None

    def append(self, data):
        new_node = Node(data)
        if not self.head:
            self.head = new_node
        else:
            self.tail.next = new_node
        self.tail = new_node

    def make_circular(self):
        if self.head:
            self.tail.next = self.head

    def calculate_cumulative_totals(self):
        if not self.head:
            return None
        current = self.head
        cumulative_total = 0
        while current:
            cumulative_total += current.data
            current.cumulative_total = cumulative_total
            current = current.next
            if current == self.head:
                break
        return cumulative_total

    def insert_sorted(self, data):
        new_node = Node(data)
        if not self.head:
            self.head = new_node
            self.tail = new_node
            new_node.next = self.head
        elif data <= self.head.data:
            new_node.next = self.head
            self.head = new_node
            self.tail.next = new_node
        elif data >= self.tail.data:
            new_node.next = self.head
            self.tail.next = new_node
            self.tail = new_node
        else:
            current = self.head
            while current.next.data < data:
                current = current.next
            new_node.next = current.next
            current.next = new_node

    def delete_index(self, index):
        if not self.head:
            return
        current = self.head
        prev = None
        for _ in range(index):
            prev = current
            current = current.next
        if current == self.head:
            self.head = current.next
            self.tail.next = self.head
        else:
            prev.next = current.next

def read_csv(file_path):
    with open(file_path, newline='') as csvfile:
        reader = csv.reader(csvfile)
        data = [float(row[0]) for row in reader]
    return data

def main():
    # Step 1: Verileri dairesel bağlantılı liste olarak oluşturma
    csv_file_path = r"C:\Users\livev\OneDrive\Masaüstü\orginaldata.csv"
    data = read_csv(csv_file_path)
    linked_list = LinkedList()
    for num in data:
        linked_list.append(num)
    linked_list.make_circular()

    # Step 2: Kümülatif toplamı hesaplama
    cumulative_total = linked_list.calculate_cumulative_totals()
    print("Kümülatif Toplam:", cumulative_total)

    # Step 3: Verileri sıralama süresini ölçme
    start_time = time.time()
    sorted_data = sorted(data)
    elapsed_time = time.time() - start_time
    print("Sıralama süresi:", elapsed_time, "saniye")

    # Step 4: Yeni veriyi ekleme
    new_data = pd.read_csv("orginaldata.csv")
    new_value = new_data.iloc[0, 0]  # Örnek olarak ilk satırın ilk sütununu alalım
    linked_list.insert_sorted(new_value)

    # Step 5: Belirtilen indeksteki veriyi silme
    delete_index_data = pd.read_csv("deleteindex.csv")
    delete_index = delete_index_data.iloc[4, 0]  # Örnek olarak ilk satırın ilk sütununu alalım
    linked_list.delete_index(delete_index)

    # Bağlı liste oluşturma süresini ölçme
    start_time = time.time()
    for row in data:
        linked_list.append(Node(row))
    elapsed_time = time.time() - start_time
    print("Bağlı Liste Oluşturma süresi:", elapsed_time, "saniye")

if __name__ == "__main__":
    main()
