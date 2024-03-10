import csv

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

# CSV dosyasını okuyarak verileri bir liste içine aktar
def read_csv(file_path):
    with open(file_path, newline='') as csvfile:
        reader = csv.reader(csvfile)
        # Verileri float türüne dönüştür
        data = [float(row[0]) for row in reader]
    return data

# Ana işlem
def main():
    csv_file_path = r"C:\Users\livev\OneDrive\Masaüstü\orginaldata.csv"
    data = read_csv(csv_file_path)

    # Verileri bağlı listeye ekle
    linked_list = LinkedList()
    for num in data:
        linked_list.append(num)

    # Bağlı listeyi dairesel hale getir
    linked_list.make_circular()

    # Kümülatif toplamları hesapla
    linked_list.calculate_cumulative_totals()

    # Kümülatif toplamları yazdır
    current = linked_list.head
    while current:
        print(current.cumulative_total)
        current = current.next
        if current == linked_list.head:
            break

if __name__ == "__main__":
    main()
