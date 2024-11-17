"""
The Python Class that implements the synchronized database
"""
import time
import win32event
import win32con
import win32file
from DataBaseFile import DataBaseFile
import logging

MAX_READERS_COUNT = 10

logging.basicConfig(filename='DataBase.log', level=logging.DEBUG)


class DataBaseSync(DataBaseFile):
    def __init__(self, dictionary=None, mode='Threading'):
        if dictionary is None:
            dictionary = {}

        super().__init__(dictionary)

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
    pass
