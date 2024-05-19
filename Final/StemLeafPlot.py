import csv

# Node class for linked list
class Node:
    def __init__(self, number, value):
        self.number = number
        self.value = value
        self.next = None

# Linked list class
class LinkedList:
    def __init__(self):
        self.head = None

    def append(self, number, value):
        new_node = Node(number, value)
        if not self.head:
            self.head = new_node
        else:
            current = self.head
            while current.next:
                current = current.next
            current.next = new_node

    def delete(self, node):
        current = self.head
        if current == node:
            self.head = current.next
            return
        while current.next:
            if current.next == node:
                current.next = current.next.next
                return
            current = current.next

# Hash table class
class HashTable:
    def __init__(self, size):
        self.size = size
        self.table = [[] for _ in range(size)]

    def hash_func(self, number):
        return int(number * self.size)

    def add(self, number):
        index = self.hash_func(number)
        if number not in self.table[index]:
            self.table[index].append(number)

    def delete(self, number):
        index = self.hash_func(number)
        if number in self.table[index]:
            self.table[index].remove(number)

    def contains(self, number):
        index = self.hash_func(number)
        return number in self.table[index]

# Function to read CSV file and return a linked list
# Function to read CSV file and return a linked list
# Function to read CSV file and return a linked list
def read_csv_to_linked_list(filename):
    linked_list = LinkedList()
    with open(filename, 'r', encoding='utf-8-sig') as file:  # specifying encoding as utf-8-sig
        reader = csv.reader(file)
        for row in reader:
            if len(row) >= 2:  # Check if row has at least 2 elements
                try:
                    number, value = float(row[0]), int(row[1])
                    linked_list.append(number, value)
                except ValueError:
                    print(f"Skipping invalid row: {row}")
            else:
                print(f"Ignoring incomplete row: {row}")
    return linked_list



# Function to generate stem-and-leaf plot from hash table
# Function to generate stem-and-leaf plot from hash table
# Function to generate stem-and-leaf plot from hash table
# Function to generate stem-and-leaf plot from hash table
# Function to generate stem-and-leaf plot from hash table
def generate_stem_and_leaf_plot(hash_table):
    stem_leaf_plot = {}
    for bucket in hash_table.table:
        for number in bucket:
            stem = int(number * 100)
            interval_start = stem / 100
            interval_end = (stem + 1) / 100 - 0.00001  # Adjusted to match the specified format
            interval = f'{interval_start:.2f}-{interval_end:.5f}'
            if interval not in stem_leaf_plot:
                stem_leaf_plot[interval] = 0
            stem_leaf_plot[interval] += 1  # Incrementing the frequency for the interval
    return stem_leaf_plot



# Function to write stem-and-leaf plot to CSV file
def write_stem_and_leaf_plot_to_csv(stem_leaf_plot, filename):
    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Interval', 'Frequency'])
        for interval, frequency in sorted(stem_leaf_plot.items()):
            writer.writerow([interval, frequency])

# Main function
def main():    
    # Read data from inputstemandleaf.csv and create hash table
    hash_table = HashTable(100)
    with open('inputstemandleaf.csv', 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            number = float(row[0])
            hash_table.add(number)

    # Read decision.csv and arbitrary_numbers.csv and convert them into linked lists
    linked_list_decision = read_csv_to_linked_list( 'decision.csv')
    linked_list_arbitrary_numbers = read_csv_to_linked_list( 'arbitrary_numbers.csv')

    # Process linked lists
    current_decision = linked_list_decision.head
    current_arbitrary_numbers = linked_list_arbitrary_numbers.head
    while current_decision and current_arbitrary_numbers:
        if current_decision.value == -1:
            if hash_table.contains(current_decision.number):
                hash_table.delete(current_decision.number)
            else:
                print(f"Number {current_decision.number} does not exist in the hash table")
        elif current_decision.value == 1:
            hash_table.add(current_decision.number)
            if hash_table.contains(current_decision.number):
                print(f"Number {current_decision.number} exists in the hash table")
        linked_list_decision.delete(current_decision)
        linked_list_arbitrary_numbers.delete(current_arbitrary_numbers)
        current_decision = linked_list_decision.head
        current_arbitrary_numbers = linked_list_arbitrary_numbers.head

    # Generate stem-and-leaf plot from hash table
    stem_leaf_plot = generate_stem_and_leaf_plot(hash_table)

    # Write stem-and-leaf plot to hashtableoutput.csv
    write_stem_and_leaf_plot_to_csv(stem_leaf_plot, 'hashtableoutput.csv')

if __name__ == "__main__":
    main()
