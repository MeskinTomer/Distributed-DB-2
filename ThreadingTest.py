import threading
from DataBaseSync import DataBaseSync


class ThreadingTest:
    def __init__(self):
        self.threads = []  # Threads list
        self.data_base = DataBaseSync('Threading')  # DataBase object - Threading mode

    def test_1(self):
        # Write Test
        self.data_base.set_value('test 1', 'complete')

    def test_2(self):
        # Read Test
        return self.data_base.get_value('test 2')

    def test_3(self):
        # Read then Write Test
        thread = threading.Thread(target=self.data_base.get_value, args=('test 3',))
        thread.start()
        self.threads.append(thread)

        thread = threading.Thread(target=self.data_base.set_value, args=('test 3', 'complete'))
        thread.start()
        self.threads.append(thread)

        for thread in self.threads:
            thread.join()

    def test_4(self):
        # Write then Read Test
        thread = threading.Thread(target=self.data_base.set_value, args=('test 4', 'complete'))
        thread.start()
        self.threads.append(thread)

        thread = threading.Thread(target=self.data_base.get_value, args=('test 4',))
        thread.start()
        self.threads.append(thread)

        for thread in self.threads:
            thread.join()

    def test_5(self):
        # Multiple Reads Test
        for num in range(1, 15):
            thread = threading.Thread(target=self.data_base.get_value, args=('test 5',))
            thread.start()
            self.threads.append(thread)

        for thread in self.threads:
            thread.join()

    def test_6(self):
        # Multiple Reads, then multiple Writes Test
        for num in range(1, 6):
            thread = threading.Thread(target=self.data_base.get_value, args=('test 6',))
            thread.start()
            self.threads.append(thread)

        thread = threading.Thread(target=self.data_base.set_value, args=('test 6', 'complete 1'))
        thread.start()
        self.threads.append(thread)

        thread = threading.Thread(target=self.data_base.set_value, args=('test 6', 'complete 2'))
        thread.start()
        self.threads.append(thread)

        for thread in self.threads:
            thread.join()

    def test_all(self):
        # Commence all Tests
        self.test_1()
        self.test_2()
        self.test_3()
        self.test_4()
        self.test_5()
        self.test_6()


if __name__ == '__main__':
    test = ThreadingTest()
    test.test_6()
