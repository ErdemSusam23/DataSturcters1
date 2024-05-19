import csv
from collections import deque
import random
import time

class Node:
    def __init__(self, data):
        self.data = data
        self.next = None
        self.prev = None

class Queue:
    def __init__(self):
        self.front = self.rear = None
        self.size = 0

    def IsEmpty(self):
        return self.front is None

    def EnQueue(self, item):
        temp = Node(item)
        if self.rear is None:
            self.front = self.rear = temp
        else:
            self.rear.next = temp
            temp.prev = self.rear
            self.rear = temp
        self.size += 1

    def DeQueue(self):
        if self.IsEmpty():
            return
        temp = self.front
        if self.front.next is not None:
            self.front = self.front.next
            self.front.prev = None
        else:
            self.front = self.rear = None
        self.size -= 1
        return temp.data

    def peek(self):
        if self.IsEmpty():
            return None
        return self.front.data
    
    def size(self):
        return self.size

def read_csv(file_name):
    with open(file_name, mode='r') as file:
        reader = csv.reader(file)
        return [float(row[0]) for row in reader]

def main():
    arrival_times = read_csv('Arrival.csv')
    server_durations = read_csv('Servers.csv')
    # Initialize servers and queues
    server_count = 4
    total_jobs = len(arrival_times)
    servers = [deque(server_durations) for _ in range(server_count)]
    server_jobs = [0] * server_count
    output_data = []
    for i, arrival in enumerate(arrival_times):
        next_customer = i + 2 if i + 2 <= len(arrival_times) else ''
        # Randomly select a server for the next task
        selected_server = random.randint(0, server_count - 1)
        # Get the duration for the selected server
        server_times = [''] * server_count
        if servers[selected_server]:  # Check if the deque is not empty
            server_duration = servers[selected_server].popleft()
            server_times[selected_server] = server_duration
            server_jobs[selected_server] += 1  # Increment job count for the server
        output_row = [i + 1, next_customer, arrival] + server_times
        output_data.append(output_row)
    time.sleep(0.2)
    with open('Queue.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['customer(i)', 'customer(i+1)', 'Arrival', 'server1', 'server2', 'server3', 'server4'])
        writer.writerows(output_data)
    # Print job counts for each server
    for i, job_count in enumerate(server_jobs):
        print(f"Server {i + 1}: {job_count} jobs")

if __name__ == "__main__":
    start = time.time()
    main()
    end = time.time()
    print(f"Exited with {(end - start):3f} seconds")
