# Context manager for connect to SQLite database
import sqlite3

class SQLiteConnect:
    def __init__(self, db_path):
        self.db_path = db_path
    
    def __enter__(self):
        self.db_connection = sqlite3.connect(self.db_path)
        return self.db_connection
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.db_connection:
            self.db_connection.close()
