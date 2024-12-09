import unittest
from database import get_db_connection, apply_migrations
from main import fetch_tasks

class TestDatabaseFunctions(unittest.TestCase):
    def test_connection(self):
        """Test to verify that the database connection is established correctly."""
        conn = get_db_connection()
        self.assertIsNotNone(conn)  # Ensure the connection is not None

    def test_task_fetching(self):
        """Test to verify that tasks can be fetched correctly from the database."""
        tasks = fetch_tasks()
        self.assertIsInstance(tasks, list)  # Ensure that fetched tasks are stored in a list

if __name__ == '__main__':
    unittest.main()
