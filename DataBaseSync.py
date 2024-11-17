"""
The Python Class that implements the synchronized database
"""
import time
import win32event
import win32con
from DataBaseFile import DataBaseFile
import logging
import sys
import socket

MAX_READERS_COUNT = 10

logging.basicConfig(filename='DataBase.log', level=logging.DEBUG)


class DataBaseSync(DataBaseFile):
    def __init__(self, mode='Threading'):
        super().__init__()

        # Threading Mode
        if mode == 'Threading':
            self.lock = win32event.CreateMutex(None, False, None)
            self.semaphore = win32event.CreateSemaphore(None, MAX_READERS_COUNT, MAX_READERS_COUNT, None)
        # MultiProcessing Mode
        elif mode == 'MultiProcessing':
            self.lock = win32event.CreateMutex(None, False, "Global\\ProcessDatabaseMutex")
            self.semaphore = win32event.CreateSemaphore(None, MAX_READERS_COUNT, MAX_READERS_COUNT, "Global\\ProcessDatabaseSemaphore")

    def set_value(self, key, val):
        # Step 1: Acquire the mutex
        wait_result = win32event.WaitForSingleObject(self.lock, win32event.INFINITE)
        if wait_result == win32con.WAIT_OBJECT_0:
            permits_acquired = 0
            try:
                # Step 2: Acquire all 10 semaphores
                while permits_acquired < MAX_READERS_COUNT:
                    sem_result = win32event.WaitForSingleObject(self.semaphore, win32event.INFINITE)
                    if sem_result == win32con.WAIT_OBJECT_0:
                        permits_acquired += 1
                    else:
                        print("Failed to acquire a semaphore.")
                        break

                if permits_acquired == MAX_READERS_COUNT:
                    # Step 3: Perform the set operation safely
                    super().set_value(key, val)
                    print(f"Set key {key} to value {val} successfully.")
                    time.sleep(3)
                else:
                    print("Failed to acquire all semaphores. Set operation aborted.")
            finally:
                # Step 4: Release all acquired semaphores
                while permits_acquired > 0:
                    win32event.ReleaseSemaphore(self.semaphore, 1)
                    permits_acquired -= 1

                # Step 5: Release the mutex
                win32event.ReleaseMutex(self.lock)
        else:
            print("Failed to acquire mutex.")

    def get_value(self, key):
        wait_result = win32event.WaitForSingleObject(self.semaphore, win32event.INFINITE)
        if wait_result == win32con.WAIT_OBJECT_0:
            try:
                # Safely get the value from the database
                value = super().get_value(key)
                print(f"Retrieved key {key}: value {value}")
                time.sleep(3)
                return value
            finally:
                # Release the semaphore, making a slot available
                win32event.ReleaseSemaphore(self.semaphore, 1)
        else:
            print("Failed to acquire synchronization object.")
            return None

    def delete_value(self, key):
        wait_result = win32event.WaitForSingleObject(self.lock, win32event.INFINITE)
        if wait_result == win32con.WAIT_OBJECT_0:
            try:
                # Safely set the value in the database
                super().delete_value(key)
                print(f"Deleted key {key} successfully.")
                time.sleep(3)
            finally:
                # Release the synchronization object
                win32event.ReleaseMutex(self.lock)
        else:
            print("Failed to acquire synchronization object.")

    def __str__(self):
        return str(self.dict)


if __name__ == "__main__":
    db = DataBaseSync()
    operation = sys.argv[1]  # Operation type (set/get/delete)
    key = sys.argv[2]  # Key
    value = sys.argv[3] if len(sys.argv) > 3 else None  # Value (if any)
    port = int(sys.argv[-1])  # Last argument is the port number

    if operation == 'Set':
        db.set_value(key, value)
        result = f"Set key {key} to value {value} successfully."
    elif operation == 'Get':
        value = db.get_value(key)
        result = f"Retrieved key {key}: value {value}" if value is not None else f"Key {key} not found."
    elif operation == 'Delete':
        db.delete_value(key)
        result = f"Deleted key {key} successfully."
    else:
        result = f"Invalid operation: {operation}"

    # Connect to the parent process's socket
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            client_socket.connect(('localhost', port))
            client_socket.sendall(result.encode('utf-8'))  # Send the result
    except Exception as e:
        print(f"Error communicating with parent process: {str(e)}")
