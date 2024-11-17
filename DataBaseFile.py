import win32file
import os
import json

FILE_NAME = "data_file.txt"


class DataBaseFile:
    def __init__(self, dictionary=None):
        self.dict = {}
        self.handle = win32file.CreateFile(
            FILE_NAME,
            win32file.GENERIC_WRITE | win32file.GENERIC_READ,
            win32file.FILE_SHARE_READ | win32file.FILE_SHARE_WRITE,
            None,
            win32file.OPEN_ALWAYS,  # Overwrite the file if it exists
            0,
            None
        )

        self._load_from_file()

    def _save_to_file(self):
        # Convert the dictionary to JSON format and write to file
        data = json.dumps(self.dict).encode('utf-8')  # Convert dict to bytes
        win32file.SetFilePointer(self.handle, 0, win32file.FILE_BEGIN)  # Move to the beginning of the file
        win32file.SetEndOfFile(self.handle)  # Ensure the file is truncated before writing new data
        win32file.WriteFile(self.handle, data)
        #print(f"Data saved to file: {data}")

    def _load_from_file(self):
        if os.path.exists(FILE_NAME):
            win32file.SetFilePointer(self.handle, 0, win32file.FILE_BEGIN)  # Start from the beginning of the file
            result, data = win32file.ReadFile(self.handle, 1024)  # Read up to 1024 bytes
            #print(f"Data read from file: {data}")
            if result != 0 or not data:  # If no data was read or data is empty
                self.dict = {}  # Initialize the dictionary as empty
            else:
                try:
                    self.dict = json.loads(data.decode('utf-8'))  # Convert bytes back to dict
                except json.JSONDecodeError:
                    #print("Error: Invalid JSON in file.")
                    self.dict = {}  # Initialize as empty if JSON is invalid
        else:
            self.dict = {}

    def set_value(self, key, val):
        # Load current data
        self._load_from_file()
        # Add the key and value to the dict
        self.dict[key] = val
        # Save updated data back to the file
        self._save_to_file()

    def get_value(self, key):
        # Load current data
        self._load_from_file()
        # Return the value for the key (default to None if not found)
        return self.dict.get(key)

    def delete_value(self, key):
        # Load current data
        self._load_from_file()
        # Remove the key if it exists
        if key in self.dict:
            del self.dict[key]
            # Save updated data back to the file
            self._save_to_file()


if __name__ == '__main__':
    db = DataBaseFile()
    db.set_value('1', '1.0')
    db.set_value('2', '2.0')
    db.delete_value('1')
    print(db.get_value('1'))  # Should output: None
    print(db.get_value('2'))  # Should output: 2.0
    print(db.dict)
