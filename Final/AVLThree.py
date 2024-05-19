import csv
import time


# AVL Node and Tree Classes
class AVLNode:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None
        self.height = 1


class AVLTree:
    def __init__(self):
        self.root = None

    def insert(self, root, key):
        if not root:
            return AVLNode(key)
        elif key < root.key:
            root.left = self.insert(root.left, key)
        else:
            root.right = self.insert(root.right, key)

        root.height = 1 + max(self.get_height(root.left), self.get_height(root.right))
        balance = self.get_balance(root)

        if balance > 1 and key < root.left.key:
            return self.right_rotate(root)
        if balance < -1 and key > root.right.key:
            return self.left_rotate(root)
        if balance > 1 and key > root.left.key:
            root.left = self.left_rotate(root.left)
            return self.right_rotate(root)
        if balance < -1 and key < root.right.key:
            root.right = self.right_rotate(root.right)
            return self.left_rotate(root)

        return root

    def delete(self, root, key):
        if not root:
            return root
        elif key < root.key:
            root.left = self.delete(root.left, key)
        elif key > root.key:
            root.right = self.delete(root.right, key)
        else:
            if root.left is None:
                return root.right
            elif root.right is None:
                return root.left

            temp = self.get_min_value_node(root.right)
            root.key = temp.key
            root.right = self.delete(root.right, temp.key)

        if not root:
            return root

        root.height = 1 + max(self.get_height(root.left), self.get_height(root.right))
        balance = self.get_balance(root)

        if balance > 1 and self.get_balance(root.left) >= 0:
            return self.right_rotate(root)
        if balance > 1 and self.get_balance(root.left) < 0:
            root.left = self.left_rotate(root.left)
            return self.right_rotate(root)
        if balance < -1 and self.get_balance(root.right) <= 0:
            return self.left_rotate(root)
        if balance < -1 and self.get_balance(root.right) > 0:
            root.right = self.right_rotate(root.right)
            return self.left_rotate(root)

        return root

    def left_rotate(self, z):
        y = z.right
        T2 = y.left
        y.left = z
        z.right = T2
        z.height = 1 + max(self.get_height(z.left), self.get_height(z.right))
        y.height = 1 + max(self.get_height(y.left), self.get_height(y.right))
        return y

    def right_rotate(self, z):
        y = z.left
        if y is None:
            return z
        T3 = y.right
        y.right = z
        z.left = T3
        z.height = 1 + max(self.get_height(z.left), self.get_height(z.right))
        y.height = 1 + max(self.get_height(y.left), self.get_height(y.right))
        return y

    def get_height(self, root):
        if not root:
            return 0
        return root.height

    def get_balance(self, root):
        if not root:
            return 0
        return self.get_height(root.left) - self.get_height(root.right)

    def get_depth(self, root):
        if not root:
            return 0
        left_depth = self.get_depth(root.left)
        right_depth = self.get_depth(root.right)
        return max(left_depth, right_depth) + 1

    def search(self, root, key):
        if root is None or root.key == key:
            return root
        if key < root.key:
            return self.search(root.left, key)
        return self.search(root.right, key)

    def pre_order(self, root):
        res = []
        if root:
            res.append(root.key)
            res = res + self.pre_order(root.left)
            res = res + self.pre_order(root.right)
        return res

    def get_min_value_node(self, root):
        if root is None or root.left is None:
            return root
        return self.get_min_value_node(root.left)


# Linked List Classes
class ListNode:
    def __init__(self, data):
        self.data = data
        self.next = None


class LinkedList:
    def __init__(self):
        self.head = None

    def append(self, data):
        if not self.head:
            self.head = ListNode(data)
            return
        last = self.head
        while last.next:
            last = last.next
        last.next = ListNode(data)

    def __iter__(self):
        node = self.head
        while node is not None:
            yield node.data
            node = node.next


# CSV Reading Functions
def read_csv_to_list(file_path, data_type=float):
    with open(file_path, mode='r') as file:
        csv_reader = csv.reader(file)
        return [data_type(row[0]) for row in csv_reader]



def read_csv_to_linked_list(file_path, data_type=float):
    linked_list = LinkedList()
    with open(file_path, mode='r', encoding='utf-8-sig') as file:  # utf-8-sig kullanarak BOM'u atlayalım
        csv_reader = csv.reader(file)
        for row in csv_reader:
            linked_list.append(data_type(row[0]))
    return linked_list


# Build AVL Tree from list of numbers
def build_avl_tree(numbers):
    avl_tree = AVLTree()
    root = None
    for number in numbers:
        root = avl_tree.insert(root, number)
    return avl_tree, root


# Process the linked lists to modify the AVL tree
def process_linked_lists(tree, root, decisions, arbitrary_numbers):
    decision_node = decisions.head
    arbitrary_node = arbitrary_numbers.head

    while decision_node and arbitrary_node:
        action = decision_node.data
        number = arbitrary_node.data

        if action == 1:
            if not tree.search(root, number):
                root = tree.insert(root, number)
                print(f"Added {number} to AVL Tree.")
            else:
                print(f"Number {number} already exists in AVL Tree.")
        elif action == -1:
            if tree.search(root, number):
                root = tree.delete(root, number)
                print(f"Deleted {number} from AVL Tree.")


        decision_node = decision_node.next
        arbitrary_node = arbitrary_node.next

    return root


def main():
    import math

    # Read numbers from CSV file for initial AVL Tree
    numbers = read_csv_to_list('BinaryTreeOriginalData.csv')

    # Build AVL Tree
    avl_tree, root = build_avl_tree(numbers)

    # Print initial depth of AVL Tree
    initial_depth = avl_tree.get_depth(root)
    print(f"Initial depth of the AVL Tree: {initial_depth}")

    # Read decision linked list from CSV file
    decisions = read_csv_to_linked_list('decision.csv', int)

    # Read arbitrary numbers linked list from CSV file
    arbitrary_numbers = read_csv_to_linked_list('arbitrary_numbers.csv', float)

    # Process linked lists to modify AVL Tree
    root = process_linked_lists(avl_tree, root, decisions, arbitrary_numbers)

    # Print final depth of AVL Tree
    final_depth = avl_tree.get_depth(root)
    print(f"Final depth of the AVL Tree: {final_depth}")

    # Check if depth meets the required conditions
    n = len(numbers)

    # Measure elapsed time
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"All operations completed in {elapsed_time:.2f} seconds.")


if __name__ == "__main__":
    start_time = time.time()  # Başlangıç zamanını kaydet

    main()
