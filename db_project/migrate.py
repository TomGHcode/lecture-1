from database import apply_migrations
from main import fetch_tasks

if __name__ == '__main__':
    
    print("Migrāciju izpilde...")

    apply_migrations()

    print("Pievienoju uzdevumus...")

    print("Esošie uzdevumi:")

    tasks = fetch_tasks()

    for task in tasks:
        print(dict(task))
