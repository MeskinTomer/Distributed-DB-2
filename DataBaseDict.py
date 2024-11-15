"""
The Python Class that implements the base database
"""


class DataBaseDict:
    def __init__(self, dictionary):
        self.dict = dictionary

    def set_value(self, key, val):
        self.dict[key] = val

    def get_value(self, key):
        return self.dict.get(key, None)

    def delete_value(self, key):
        self.dict.pop(key, None)


if __name__ == '__main__':
    # Creating an instance of DataBaseDict with an initial dictionary
    db = DataBaseDict({"a": 1, "b": 2})

    # Testing set_value method
    db.set_value("c", 3)
    assert db.get_value("c") == 3, "set_value or get_value method failed."

    # Testing get_value method for an existing key
    assert db.get_value("a") == 1, "get_value method failed for existing key."

    # Testing get_value method for a non-existent key (should return None)
    assert db.get_value("non_existent_key") is None, "get_value method failed for non-existent key."

    # Testing delete_value method for an existing key
    db.delete_value("b")
    assert db.get_value("b") is None, "delete_value method failed."

    # Testing delete_value method for a non-existent key (should not raise an error)
    try:
        db.delete_value("non_existent_key")
    except Exception as e:
        assert False, f"delete_value raised an exception for a non-existent key: {e}"

    print("All tests passed.")
