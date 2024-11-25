import sqlite3
import os

DB_PATH = "database.sqlite" #norāda datubāzes atrašanos vietu

# Funkcija, kas savieno ar datubāzi
def get_db_connection():
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row  # Padara request rezultātus pieejamus kā dictionaries
    return connection

# Migrācijas izpilde no norādītās mapes
def apply_migrations():
    migrations_folder = 'migrations' #norādam migrāciju mapi, kurā atrodās migrācijai nepieciešamie query
    conn = get_db_connection()
    cursor = conn.cursor()

    # Izpilda katru SQL failu migrācijas mapē
    for filename in sorted(os.listdir(migrations_folder)):
        if filename.endswith('.sql'):
            with open(os.path.join(migrations_folder, filename), 'r') as f:
                sql = f.read()
                cursor.executescript(sql)
                print(f"Migrācija '{filename}' izpildīta.")

    conn.commit()
    conn.close()
