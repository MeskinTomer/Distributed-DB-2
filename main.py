"""
The Python Class that implements the testing of the database using MultiProcessing
"""

import multiprocessing
from DataBaseSync import DataBaseSync


class MultiProcessingTest:
    def __init__(self):
        self.processes = []  # Processes list
        self.data_base = DataBaseSync('test.db', {}, 'MultiProcessing')  # DataBase Object - MultiProcessing mode

    def test_1(self):
        # Write Test
        self.data_base.set_value('test 1', 'complete')

    def test_2(self):
        # Read Test
        return self.data_base.get_value('test 2')

    def test_3(self):
        # Read then Write Test
        process = multiprocessing.Process(target=self.data_base.get_value, args=('test 3',))
        process.start()
        self.processes.append(process)

        process = multiprocessing.Process(target=self.data_base.set_value, args=('test 3', 'complete'))
        process.start()
        self.processes.append(process)

        for process in self.processes:
            process.join()

    def test_4(self):
        # Write then Read Test
        process = multiprocessing.Process(target=self.data_base.set_value, args=('test 4', 'complete'))
        process.start()
        self.processes.append(process)

        process = multiprocessing.Process(target=self.data_base.get_value, args=('test 4',))
        process.start()
        self.processes.append(process)

        for process in self.processes:
            process.join()

    def test_5(self):
        # Multiple Reads Test
        for num in range(1, 6):
            process = multiprocessing.Process(target=self.data_base.get_value, args=('test 5',))
            process.start()
            self.processes.append(process)

        for process in self.processes:
            process.join()

    def test_6(self):
        # Multiple Reads, then multiple Writes Test
        for num in range(1, 6):
            process = multiprocessing.Process(target=self.data_base.get_value, args=('test 6',))
            process.start()
            self.processes.append(process)

        process = multiprocessing.Process(target=self.data_base.set_value, args=('test 6', 'complete 1'))
        process.start()
        self.processes.append(process)

        process = multiprocessing.Process(target=self.data_base.set_value, args=('test 6', 'complete 2'))
        process.start()
        self.processes.append(process)

        for process in self.processes:
            process.join()

    def test_all(self):
        # Commence all Tests
        self.test_1()
        self.test_2()
        self.test_3()
        self.test_4()
        self.test_5()
        self.test_6()


if __name__ == '__main__':
    test = MultiProcessingTest()
    test.test_3()