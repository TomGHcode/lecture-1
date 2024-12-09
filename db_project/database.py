
import sqlite3
import json
import os
import logging

# konfigurē logging
logging.basicConfig(level=logging.INFO, filename='app.log',
                    format='%(asctime)s - %(levelname)s - %(message)s')

# ielādē configuration
with open('config.json', 'r') as config_file:
    config = json.load(config_file)
DB_PATH = config['database']

# Funkcija, kas savieno ar datubāzi
def get_db_connection():
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row    # Padara request rezultātus pieejamus kā dictionaries
    logging.debug("Database connection established.")
    return connection

def apply_migrations():
    migrations_folder = 'migrations' # norādam migrāciju mapi, kurā atrodās migrācijai nepieciešamie query
    conn = get_db_connection()
    cursor = conn.cursor()

    for filename in sorted(os.listdir(migrations_folder)):
        if filename.endswith('.sql'):
            with open(os.path.join(migrations_folder, filename), 'r') as f:
                sql = f.read()
                cursor.executescript(sql)
                logging.info(f"Migrācija '{filename}' izpildīta.")

    conn.commit()
    conn.close()
    logging.debug("All migrations applied and database connection closed.")
