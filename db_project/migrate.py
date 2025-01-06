import sqlite3
import os
import logging

# Izpilda visas neizpildītās migrācijas no norādītās mapes.
def apply_migrations(db_path, migrations_folder):

    print("Migrāciju izpilde...")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()


    # Izveido tabulu migrāciju izsekošanai, ja tā neeksistē
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS schema_migrations (
            id INTEGER PRIMARY KEY,
            migration_name TEXT UNIQUE
        )
    ''')

    # Iegūt jau izpildītās migrācijas
    cursor.execute("SELECT migration_name FROM schema_migrations;")
    applied_migrations = {row[0] for row in cursor.fetchall()}


    # Izpilda migrācijas kas nav iepriekš izpildītas
    for migration in sorted(os.listdir(migrations_folder)):
        if migration not in applied_migrations:
            migration_path = os.path.join(migrations_folder, migration)
            with open(migration_path, 'r') as migration_file:
                migration_sql = migration_file.read()
            
            try:
                cursor.executescript(migration_sql)
                cursor.execute("INSERT INTO schema_migrations (migration_name) VALUES (?);", (migration,))
                conn.commit()
                print(f"Izpildīta migrācija: {migration}")
                logging.info(f"Izpildīta migrācija: {migration}")
            except sqlite3.Error as e:
                print(f"Kļūda izpildot migrāciju {migration}: {e}")
                logging.error(f"Kļūda izpildot migrāciju {migration}: {e}")
                conn.rollback()
    
    conn.close()
    print("Migrācijas izpildītas veiksmīgi.")
    logging.debug("All migrations completed, database connection closed.")
