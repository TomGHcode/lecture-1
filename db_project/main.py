
import logging
from database import get_db_connection

logging.basicConfig(level=logging.INFO, filename='app.log',
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Funkcija, kas nolasa datus no datubāzes un atgriež tos kā sarakstu
def fetch_tasks():
    conn = get_db_connection() # Savienojums ar datubāzi
    cursor = conn.cursor() # Izveido kursoru SQL vaicājumiem
    
    # Izvēlas uzdevuma nosaukumu un izpildes statusu no tabulas
    cursor.execute("SELECT name, completed FROM tasks")
    tasks = cursor.fetchall()   # Iegūst visus rezultātus
    conn.close()     #aizver savienojumu
    
    logging.debug("Fetched tasks from database.")
    return tasks

def display_tasks(tasks):   # Noformē un izvada uzdevumus uz ekrāna.
    if not tasks:
        logging.info("No tasks to display.")
        return

    for idx, task in enumerate(tasks, start=1):
        name, completed = task['name'], "Pabeigts" if task['completed'] else "Nepabeigts"
        print(f"{idx}. {name} - {completed}")
        logging.debug(f"Task displayed: {name} - {completed}")

def main():         # Galvenā funkcija, kas nolasa uzdevumus no datubāzes un izvada tos uz ekrāna.
    tasks = fetch_tasks()   # Pārbauda, vai ir kādi uzdevumi
    display_tasks(tasks)    # Izvada uzdevumus uz ekrāna

if __name__ == '__main__':
    main()
