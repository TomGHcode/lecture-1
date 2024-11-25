from database import get_db_connection

# Funkcija, kas nolasa datus no datubāzes un atgriež tos kā sarakstu
def fetch_tasks():
    """
    Nolasa visus uzdevumus no 'tasks' tabulas.

    Returns:
        list: Saraksts ar vārdnīcām, kur katrs ieraksts satur 'name' un 'completed'.
    """
    conn = get_db_connection()  # Savienojums ar datubāzi
    cursor = conn.cursor()  # Izveido kursoru SQL vaicājumiem
    
    # Izvēlas uzdevuma nosaukumu un izpildes statusu no tabulas
    cursor.execute("SELECT name, completed FROM tasks")
    tasks = cursor.fetchall()  # Iegūst visus rezultātus
    
    conn.close()  # Aizver savienojumu ar datubāzi
    return tasks

def display_tasks(tasks):
    """
    Noformē un izvada uzdevumus uz ekrāna.

    Args:
        tasks (list): Saraksts ar uzdevumiem no datubāzes.
    """
    print("\nUzdevumu saraksts:")
    print("-" * 30)
    
    # Pārbauda, vai ir kādi uzdevumi
    if not tasks:
        print("Nav uzdevumu, kas jārāda.")
        return
    
    # Iterē cauri uzdevumiem un izvada tos formatētā tabulā
    for idx, task in enumerate(tasks, start=1):
        name = task[0]
        completed = "Pabeigts" if task[1] else "Nepabeigts"
        print(f"{idx}. {name} - {completed}")

def main():
    """
    Galvenā funkcija, kas nolasa uzdevumus no datubāzes un izvada tos uz ekrāna.
    """
    # Iegūst uzdevumus no datubāzes
    tasks = fetch_tasks()
    
    # Izvada uzdevumus uz ekrāna
    display_tasks(tasks)

if __name__ == '__main__':
    main()
