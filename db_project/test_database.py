import unittest
import sqlite3
import os
from migrate import apply_migrations


class TestDatabaseFunctions(unittest.TestCase):

    def setUp(self):
        # Create a connection to the in-memory database
        self.conn = sqlite3.connect(':memory:')
        self.cursor = self.conn.cursor()

        # Apply migrations directly using this connection
        self._apply_migrations()

        # Insert test data into the in-memory database
        self.cursor.execute("INSERT INTO tasks (name, completed) VALUES ('Task 1', 0);")
        self.cursor.execute("INSERT INTO tasks (name, completed) VALUES ('Task 2', 1);")
        self.conn.commit()

    def tearDown(self):
        # Close the in-memory database connection
        self.conn.close()

    def _apply_migrations(self):
        # Reimplement apply_migrations for this in-memory connection
        migrations_folder = './migrations'
        print("Applying migrations...")
        
        # Create schema_migrations table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS schema_migrations (
                id INTEGER PRIMARY KEY,
                migration_name TEXT UNIQUE
            )
        ''')
        
        # Fetch already applied migrations
        self.cursor.execute("SELECT migration_name FROM schema_migrations;")
        applied_migrations = {row[0] for row in self.cursor.fetchall()}

        # Apply pending migrations
        for migration in sorted(os.listdir(migrations_folder)):
            if migration not in applied_migrations:
                migration_path = os.path.join(migrations_folder, migration)
                with open(migration_path, 'r') as migration_file:
                    migration_sql = migration_file.read()
                self.cursor.executescript(migration_sql)
                self.cursor.execute("INSERT INTO schema_migrations (migration_name) VALUES (?);", (migration,))
        self.conn.commit()
        print("Migrations applied successfully.")

    def test_task_fetching(self):
        # Fetch tasks and verify their count and content
        self.cursor.execute("SELECT name, completed FROM tasks;")
        tasks = [{"name": row[0], "completed": bool(row[1])} for row in self.cursor.fetchall()]
        
        # Assertions
        self.assertEqual(len(tasks), 2)  # Ensure there are two tasks
        self.assertEqual(tasks[0]['name'], 'Task 1')
        self.assertFalse(tasks[0]['completed'])
        self.assertEqual(tasks[1]['name'], 'Task 2')
        self.assertTrue(tasks[1]['completed'])

if __name__ == '__main__':
    unittest.main()
