from DataBaseSync import DataBaseSync
import win32process
from win32api import CloseHandle
import socket
from threading import Thread


class MultiProcessingTest:
    def __init__(self):
        self.threads = []  # threads list
        self.data_base = DataBaseSync('MultiProcessing')  # DataBase object - Threading mode

    def __create_process(self, operation, args):
        key = args[0]
        value = args[1] if len(args) > 1 else None

        if operation != 'Set':
            command = f'python DataBaseSync.py {operation} {key}'
        else:
            command = f'python DataBaseSync.py {operation} {key} {value}'

        # Create a socket for communication
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind(('localhost', 0))  # Bind to an available port
        server_address, server_port = server_socket.getsockname()  # Get the address and port
        server_socket.listen(1)

        # Update the command to include the server port as an argument
        command += f" {server_port}"

        # Set up the environment for CreateProcess
        startup_info = win32process.STARTUPINFO()

        # Command to execute
        process_info = win32process.CreateProcess(
            None,  # Application name
            command,  # Command line (script + args)
            None,  # Process security attributes
            None,  # Thread security attributes
            True,  # Inherit handles
            0,  # Creation flags
            None,  # Environment
            None,  # Current directory
            startup_info
        )

        # Wait for the process to connect
        print(f"Launched process with PID: {process_info[1]}")
        client_socket, _ = server_socket.accept()

        # Receive data from the process
        output = None
        try:
            data = client_socket.recv(4096)
            if data:
                output = data.decode('utf-8')
                print(f"Process output: {output}")
        except Exception as e:
            print(f"Error reading output: {str(e)}")
        finally:
            client_socket.close()
            server_socket.close()

        # Clean up process handles
        CloseHandle(process_info[0])  # Close process handle
        CloseHandle(process_info[1])  # Close thread handle

        return output

    def test_1(self):
        # Write Test
        self.data_base.set_value('test 1', 'complete')

    def test_2(self):
        # Read Test
        return self.data_base.get_value('test 2')

    def test_3(self):
        # Read then Write Test
        operation = 'Get'
        args = ('test3',)
        t = Thread(target=self.__create_process, args=(operation, args))
        t.start()
        self.threads.append(t)

        operation = 'Set'
        args = ('test3', 'complete')
        t = Thread(target=self.__create_process, args=(operation, args))
        t.start()
        self.threads.append(t)

        for thread in self.threads:
            thread.join()

    def test_4(self):
        # Write then Read Test
        operation = 'Set'
        args = ('test4', 'complete')
        t = Thread(target=self.__create_process, args=(operation, args))
        t.start()
        self.threads.append(t)

        operation = 'Get'
        args = ('test4',)
        t = Thread(target=self.__create_process, args=(operation, args))
        t.start()
        self.threads.append(t)

        for thread in self.threads:
            thread.join()

    def test_5(self):
        # Multiple Reads Test
        for num in range(1, 15):
            operation = 'Get'
            args = ('test5',)
            t = Thread(target=self.__create_process, args=(operation, args))
            t.start()
            self.threads.append(t)

        for thread in self.threads:
            thread.join()

    def test_6(self):
        # Multiple Reads, then multiple Writes Test
        for num in range(1, 6):
            operation = 'Get'
            args = ('test6',)
            t = Thread(target=self.__create_process, args=(operation, args))
            t.start()
            self.threads.append(t)

        operation = 'Set'
        args = ('test6', 'complete 1')
        t = Thread(target=self.__create_process, args=(operation, args))
        t.start()
        self.threads.append(t)

        operation = 'Set'
        args = ('test 6', 'complete 2')
        t = Thread(target=self.__create_process, args=(operation, args))
        t.start()
        self.threads.append(t)

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
    test = MultiProcessingTest()
    test.test_3()
