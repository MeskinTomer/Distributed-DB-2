from DataBaseSync import DataBaseSync
import sys

if __name__ == '__main__':
    db = DataBaseSync()
    func = sys.argv[1]

    if func == 'Set':
        key = sys.argv[2]
        value = sys.argv[3]
        db.set_value(key, value)
    elif func == 'Get':
        key = sys.argv[2]
        db.get_value(key)
    elif func == 'Delete':
        key = sys.argv[2]
        db.delete_value(key)