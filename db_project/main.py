import logging
import sqlite3
import json
import os
import logging
from migrate import apply_migrations

# konfigurē logging
logging.basicConfig(level=logging.INFO, filename='app.log',
                    format='%(asctime)s - %(levelname)s - %(message)s')



# ielādē konfigurāciju no config faila
with open('config.json', 'r') as config_file:
    config = json.load(config_file)
DB_PATH = config['database']    # Nolasa datubāzes faila ceļu no konfigurācijas faila
migrations_folder = config.get('migrations_folder', './migrations')


# Izveido savienojumu ar datubāzi
def get_db_connection():
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row    # Padara request rezultātus pieejamus kā dictionaries
    logging.debug("Database connection established.")
    return connection


# Startēšanas laikā Izveido datubāzi / Izpilda migrācijas, kas atrodas migrāciju mapē
apply_migrations(DB_PATH, migrations_folder)


# Nolasa datus no datubāzes un atgriež tos kā sarakstu
def fetch_tasks():
    conn = get_db_connection()  # Savienojums ar datubāzi
    cursor = conn.cursor()      # Izveido kursoru SQL vaicājumiem
    
    # Izvēlas uzdevuma nosaukumu un izpildes statusu no tabulas
    cursor.execute("SELECT name, completed FROM tasks")
    tasks = [{"name": row[0], "completed": row[1]} for row in cursor.fetchall()]
    conn.close()
    
    logging.debug("Fetched tasks from database, connection closed.")
    return tasks


# Noformē un izvada uzdevumus uz ekrāna, norāda vai uzdevums pabeigts vai nepabeigts.
def display_tasks(tasks):
    print("Esošie uzdevumi:")
    for task in tasks:
        print(task)
        logging.debug(f"Task displayed: {task}")


# Galvenā funkcija, kas nolasa uzdevumus no datubāzes un izvada tos uz ekrāna.
def main():
    print("Pievienoju uzdevumus...")         
    tasks = fetch_tasks()    # Nolasa uzdevumus no datubāzes
    display_tasks(tasks)     # Izvada uzdevumus uz ekrāna

if __name__ == '__main__':
    main()
