import pickle
import os
from DataBaseDict import DataBaseDict

FILE_PATH = 'data.pkl'


class DataBaseFile(DataBaseDict):
    def __init__(self, dictionary=None):
        # Initialize with the provided dictionary or an empty one
        super().__init__(dictionary or {})
        # Save initial dictionary to file
        self._save_to_file()

    def _save_to_file(self):
        with open(FILE_PATH, 'wb') as file:
            pickle.dump(self.dict, file)

    def _load_from_file(self):
        if os.path.exists(FILE_PATH):
            with open(FILE_PATH, 'rb') as file:
                self.dict = pickle.load(file)
        else:
            self.dict = {}

    def set_value(self, key, val):
        self._load_from_file()  # Load current data
        super().set_value(key, val)  # Use the parent class method
        self._save_to_file()  # Save updated data

    def get_value(self, key):
        self._load_from_file()
        return super().get_value(key)  # Use the parent class method

    def delete_value(self, key):
        self._load_from_file()
        super().delete_value(key)  # Use the parent class method
        self._save_to_file()


if __name__ == '__main__':
    # Ensure no leftover data file before tests
    if os.path.exists(FILE_PATH):
        os.remove(FILE_PATH)

    # Initialize with some data
    db_file = DataBaseFile({"x": 100})

    # Test set_value and persistence
    db_file.set_value("y", 200)
    assert db_file.get_value("y") == 200, "set_value or get_value failed."

    # Test get_value for a non-existent key
    assert db_file.get_value("non_existent") is None, "get_value failed for non-existent key."

    # Test delete_value and persistence
    db_file.delete_value("y")
    assert db_file.get_value("y") is None, "delete_value failed."

    # Ensure deletion was saved by reloading from file
    db_file_new_instance = DataBaseFile()
    assert db_file_new_instance.get_value("y") is None, "Deletion was not persisted to file."

    print("All tests passed.")

    # Clean up after test
    if os.path.exists(FILE_PATH):
        os.remove(FILE_PATH)
