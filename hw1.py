from abc import ABC, abstractmethod

class DataHandler(ABC):
    """Abstract base class for data handling operations."""
    
    @abstractmethod
    def read(self):
        pass
    
    @abstractmethod
    def write(self, data):
        pass


class TextFile(DataHandler):
    """Class for handling text file operations."""
    
    def __init__(self, filename):
        self.filename = filename
    
    def read(self):
        with open(self.filename, 'r', encoding='utf-8') as file:
            return file.read()
    
    def write(self, data):
        with open(self.filename, 'w', encoding='utf-8') as file:
            file.write(data)


class Database(DataHandler):
    """Class for database operations."""

    def __init__(self, connection_string):
        self.connection_string = connection_string
        self._connected = False
        self._data_store = {} # Just for tesing

        self._connect() # Auto-connect

    def _connect(self):
        print(f"LOG: Connected to database: {self.connection_string}")
        self._connected = True

    def _check_connection(self):
        if not self._connected:
            raise ConnectionError("ERROR: Database connection is not active")
    
    def read(self):
        self._check_connection()
        print("LOG: Reading from database")
        return self._data_store.copy()
    
    def write(self, data):
        self._check_connection()
        print("LOG: Writing to database")
        self._data_store.update(data)

class NetworkResource(DataHandler):
    """Class for network operations."""
    
    def __init__(self, url):
        self.url = url
        self._connected = False
        self._data_store = "" # Just for tesing

        self._connect()  # Auto-connect
    
    def _connect(self):
        print(f"LOG: Connected to network resource: {self.url}")
        self._connected = True
    
    def _check_connection(self):
        if not self._connected:
            raise ConnectionError("ERROR: Network connection is not active")
    
    def read(self):
        self._check_connection()
        print(f"LOG: Read from {self.url}")
        return self._data_store
    
    def write(self, data):
        self._check_connection()
        print(f"LOG: Write to {self.url}")
        self._data_store = data


#DON'T TOUCH UNDER THE LINE
#______________________________________________________________
def process_data(data_source, data=None):
    if data:
        data_source.write(data)
    return data_source.read()

text_file = TextFile("document.txt")
database = Database("users.db")
network = NetworkResource("http://example.com/api")

print(process_data(text_file, "Новый текст"))
print(process_data(database, {"name": "Иван", "age": 25}))
print(process_data(network, "POST data"))