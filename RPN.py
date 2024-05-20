import csv
import time
from pathlib import Path
import math
import ast

class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

class Stack:
    def __init__(self):
        self.top = None

    def push(self, data):
        new_node = Node(data)
        new_node.next = self.top
        self.top = new_node

    def pop(self):
        if self.top is None:
            raise IndexError("pop from empty stack")
        data = self.top.data
        self.top = self.top.next
        return data

    def is_empty(self):
        return self.top is None

    def peek(self):
        if self.top is None:
            raise IndexError("peek from empty stack")
        return self.top.data

def is_operator(token):
    return token in ['+', '-', '*', '/', 'log', '^']

def precedence(op):
    if op == 'log':
        return 4
    if op == '^':
        return 3
    if op in ('*', '/'):
        return 2
    if op in ('+', '-'):
        return 1
    return 0

def rpn_to_algebraic(rpn_expression):
    stack = Stack()
    for token in rpn_expression:
        if not is_operator(token):
            stack.push(token)
        else:
            if token == 'log':
                operand = stack.pop()
                expression = f'log({operand})'
            else:
                operand2 = stack.pop()
                operand1 = stack.pop()
                expression = f'({operand1} {token} {operand2})'
            stack.push(expression)
    return stack.pop()

def algebraic_to_rpn(expression):
    output = []
    operators = Stack()
    i = 0
    while i < len(expression):
        if expression[i].isdigit() or expression[i] == '.':
            num = []
            while i < len(expression) and (expression[i].isdigit() or expression[i] == '.'):
                num.append(expression[i])
                i += 1
            output.append(''.join(num))
        elif expression[i] == '(':
            operators.push(expression[i])
            i += 1
        elif expression[i] == ')':
            while not operators.is_empty() and operators.peek() != '(':
                output.append(operators.pop())
            operators.pop()  # Remove '('
            i += 1
        elif expression[i] in ['+', '-', '*', '/', '^']:
            while (not operators.is_empty() and precedence(operators.peek()) >= precedence(expression[i])):
                output.append(operators.pop())
            operators.push(expression[i])
            i += 1
        elif expression[i:i + 3] == 'log':
            while (not operators.is_empty() and precedence(operators.peek()) >= precedence('log')):
                output.append(operators.pop())
            operators.push('log')
            i += 3
        else:
            i += 1

    while not operators.is_empty():
        output.append(operators.pop())

    return output

def evaluate_rpn(rpn_expression):
    stack = Stack()
    for token in rpn_expression:
        if not is_operator(token):
            stack.push(float(token))
        else:
            if token == 'log':
                operand = stack.pop()
                result = math.log10(operand)
            else:
                operand2 = stack.pop()
                operand1 = stack.pop()
                if token == '+':
                    result = operand1 + operand2
                elif token == '-':
                    result = operand1 - operand2
                elif token == '*':
                    result = operand1 * operand2
                elif token == '/':
                    result = operand1 / operand2
                elif token == '^':
                    result = math.pow(operand1, operand2)
            stack.push(result)
    return stack.pop()

def evaluate_algebraic(algebraic_expression):
    algebraic_expression = algebraic_expression.replace("^", "**")
    result = eval(algebraic_expression, {"__builtins__": None}, {"log": math.log10})
    return result



def process_rpn_file(input_file, output_file):
    if not input_file.exists():
        print(f"Error: File {input_file} does not exist.")
        return

    with open(input_file, 'r') as f:
        rpn_expression = f.read().strip().replace(" ", "").split(',')
        algebraic_expression = rpn_to_algebraic(rpn_expression)
        rpn_result = evaluate_rpn(rpn_expression)
        result = evaluate_algebraic(algebraic_expression)

    with open(output_file, 'w', newline='') as output:
        writer = csv.writer(output)
        writer.writerow(["Operation:", algebraic_expression])
        writer.writerow(["Result:", ""])
        writer.writerow(["", f"{rpn_result:.6f}"])
        writer.writerow(["", f"{result:.6f}"])


def main():
    current_dir = Path.cwd()
    input_file_rpn = current_dir / "rpninput.csv"
    output_file_algebraic = current_dir / "result_algebraic.csv"

    process_rpn_file(input_file_rpn, output_file_algebraic)
    print("Conversion complete. Results written to result_algebraic.csv")

if __name__ == "__main__":
    start = time.time()
    main()
    end = time.time()
    print(str(end - start))