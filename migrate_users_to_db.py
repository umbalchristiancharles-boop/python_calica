import json
import pymysql
from typing import Dict

DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'db': 'hotel_db',
    'charset': 'utf8mb4',
    'autocommit': True
}

USERS_FILE = 'users.json'


def load_local_users(path: str) -> Dict:
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return {u['username']: u for u in data.get('users', [])}


def migrate():
    users = load_local_users(USERS_FILE)
    conn = pymysql.connect(**DB_CONFIG)
    cursor = conn.cursor(pymysql.cursors.DictCursor)

    inserted = 0
    updated = 0
    for username, user in users.items():
        # Check existing by username or email
        cursor.execute("SELECT id, username, email FROM users WHERE username = %s OR email = %s", (username, user.get('email')))
        row = cursor.fetchone()
        if row:
            # update basic fields if needed
            cursor.execute(
                "UPDATE users SET name=%s, phone=%s, role=%s WHERE id=%s",
                (user.get('name'), user.get('phone'), user.get('role', 'customer'), row['id'])
            )
            updated += 1
            print(f"Updated DB user: {username} (id={row['id']})")
        else:
            cursor.execute(
                "INSERT INTO users (name, username, email, phone, password, role) VALUES (%s,%s,%s,%s,%s,%s)",
                (
                    user.get('name'),
                    user.get('username'),
                    user.get('email'),
                    user.get('phone'),
                    user.get('password'),
                    user.get('role', 'customer')
                )
            )
            cursor.execute("SELECT id FROM users WHERE username = %s", (username,))
            new = cursor.fetchone()
            print(f"Inserted DB user: {username} (id={new['id']})")
            inserted += 1

    conn.close()
    print(f"Migration complete. Inserted: {inserted}, Updated: {updated}")


if __name__ == '__main__':
    print('Starting users.json → DB migration')
    migrate()
