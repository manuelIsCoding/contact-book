import sqlite3


class SQLiteConnect:
    """A class that supports the `with` statement through context
    manager protocol (it contains the dunder methods`__enter__`
    and `__exit__`)."""
    def __init__(self, db_path):
        self.db_path = db_path
    
    def __enter__(self):
        self.db_connection = sqlite3.connect(self.db_path)
        return self.db_connection
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.db_connection:
            self.db_connection.close()
