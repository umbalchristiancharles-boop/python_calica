import json
import os
import re
from typing import Dict, List, Optional, Tuple
import pymysql
import pymysql.cursors
from migrate_users_to_db import DB_CONFIG

USERS_FILE = 'users.json'
BAD_WORDS = {'bad', 'inappropriate', 'spam'}  

class AuthHandler:
    def __init__(self, users_file: str = USERS_FILE):
        self.users_file = users_file
        self.users: List[Dict] = self.load_users()
    
    def load_users(self) -> List[Dict]:
        
        try:
            conn = pymysql.connect(**DB_CONFIG)
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            cursor.execute("SELECT id, username, email, password, role, name, phone FROM users")
            rows = cursor.fetchall()
            conn.close()
            users = []
            for r in rows:
                users.append({
                    'id': r.get('id'),
                    'username': r.get('username'),
                    'email': r.get('email'),
                    'password': r.get('password'),
                    'role': r.get('role') or 'customer',
                    'name': r.get('name') or '',
                    'phone': r.get('phone') or ''
                })
           
            has_admin = any((u.get('role') or '').lower() == 'admin' or (u.get('username') or '').lower() == 'admin' for u in users)
            if not has_admin:
                default_admin = {
                    'username': 'admin',
                    'email': 'admin@hotel.com',
                    'password': 'Admin@123',
                    'role': 'admin',
                    'name': 'Hotel Admin',
                    'phone': '09000000000'
                }
                users.insert(0, default_admin)
                try:
                    conn2 = pymysql.connect(**DB_CONFIG)
                    cur2 = conn2.cursor(pymysql.cursors.DictCursor)
                    cur2.execute("SELECT id FROM users WHERE username = %s OR email = %s", (default_admin['username'], default_admin['email']))
                    if not cur2.fetchone():
                        try:
                            cur2.execute("INSERT INTO users (name, username, email, phone, password, role) VALUES (%s,%s,%s,%s,%s,%s)",
                                         (default_admin['name'], default_admin['username'], default_admin['email'], default_admin['phone'], default_admin['password'], default_admin['role']))
                            conn2.commit()
                        except Exception:
                            pass
                    conn2.close()
                except Exception:
                    pass

            if users:
                try:
                    self.save_users(users)
                except Exception:
                    pass
                return users
        except Exception:
            pass

        if not os.path.exists(self.users_file):
            default_users = {
                'users': [
                    {
                        'username': 'admin',
                        'email': 'admin@hotel.com',
                        'password': 'Admin@123',  
                        'role': 'admin',
                        'name': 'Hotel Admin',
                        'phone': '09000000000'
                    }
                ]
            }
            self.save_users(default_users['users'])
            return default_users['users']
        try:
            with open(self.users_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data.get('users', [])
        except Exception:
            return []
    
    def save_users(self, users: List[Dict]):
        data = {'users': users}
        with open(self.users_file, 'w') as f:
            json.dump(data, f, indent=2)
    
    def validate_name(self, name: str) -> Tuple[bool, str]:
        name = name.strip()
        if len(name) < 2:
            return False, 'Name too short'
        if not re.match(r'^[a-zA-Z\s]+$', name):
            return False, 'Name must contain letters only'
        if any(word in name.lower() for word in BAD_WORDS):
            return False, 'Inappropriate name'
        return True, ''
    
    def validate_email(self, email: str) -> Tuple[bool, str]:
        email = email.strip().lower()
        if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
            return False, 'Invalid email format'
        if any(u['email'] == email for u in self.users):
            return False, 'Email already registered'
        return True, ''
    
    def validate_username(self, username: str) -> Tuple[bool, str]:
        username = username.strip()
        if len(username) < 3:
            return False, 'Username too short'
        if any(u['username'] == username for u in self.users):
            return False, 'Username taken'
        return True, ''
    
    def validate_phone(self, phone: str) -> Tuple[bool, str]:
        phone = re.sub(r'[^\d]', '', phone)
        if len(phone) > 11 or not phone:
            return False, 'Phone: 1-11 digits only'
        return True, phone  
    
    def validate_password(self, password: str) -> Tuple[bool, str]:
        if len(password) < 6:
            return False, 'Password at least 6 chars'
        return True, ''
    
    def register(self, name: str, username: str, email: str, phone: str, password: str) -> Tuple[bool, str]:
        ok_name, err = self.validate_name(name)
        if not ok_name: return False, err
        
        ok_user, err = self.validate_username(username)
        if not ok_user: return False, err
        
        ok_email, err = self.validate_email(email)
        if not ok_email: return False, err
        
        ok_phone, cleaned_phone = self.validate_phone(phone)
        if not ok_phone: return False, err
        
        ok_pw, err = self.validate_password(password)
        if not ok_pw: return False, err
        
        user = {
            'username': username,
            'email': email,
            'password': password,  # TODO: 
            'role': 'customer',
            'name': name,
            'phone': cleaned_phone
        }
        self.users.append(user)
        self.save_users(self.users)
        try:
            conn = pymysql.connect(**DB_CONFIG)
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            cursor.execute("SELECT id FROM users WHERE username = %s OR email = %s", (username, email))
            row = cursor.fetchone()
            if row:
                cursor.execute(
                    "UPDATE users SET name=%s, phone=%s, role=%s, password=%s WHERE id=%s",
                    (name, cleaned_phone, user.get('role', 'customer'), password, row['id'])
                )
            else:
                cursor.execute(
                    "INSERT INTO users (name, username, email, phone, password, role) VALUES (%s,%s,%s,%s,%s,%s)",
                    (name, username, email, cleaned_phone, password, user.get('role', 'customer'))
                )
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"DB insert failed (registration): {e}")
        return True, 'Registered! Logged in as customer.'
    
    def login(self, username: str, password: str) -> Optional[Dict]:
        username_norm = (username or '').strip().lower()
        for user in self.users:
            user_username = (user.get('username') or '').strip().lower()
            user_email = (user.get('email') or '').strip().lower()
            user_password = user.get('password') or ''
            if (username_norm == user_username or username_norm == user_email) and password == user_password:
                return user
        return None

    def delete_user(self, identifier: str) -> Tuple[bool, str]:
        """Delete a user by username or email from the local users file.

        `identifier` may be a username or an email. Returns (True, msg) when
        deleted, (False, msg) when not found or error. Attempts to also
        remove the DB record; DB errors are logged but do not stop the local
        deletion.
        """
        identifier = (identifier or '').strip()
        if not identifier:
            return False, 'Empty identifier'

        if identifier.lower() == 'admin' or identifier.lower() == 'admin@hotel.com':
            return False, 'Refusing to delete built-in admin'

        try:
            conn = pymysql.connect(**DB_CONFIG)
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            cursor.execute("SELECT id, username, email FROM users WHERE username = %s OR email = %s", (identifier, identifier))
            row = cursor.fetchone()
            if row:
                try:
                    cursor.execute("DELETE FROM users WHERE id = %s", (row.get('id'),))
                    conn.commit()
                except Exception as e:
                    print(f"DB delete failed (delete_user): {e}")
                finally:
                    conn.close()
                try:
                    self.users = self.load_users()
                except Exception:
                    pass
                return True, f"User {row.get('username')} deleted (DB)"
            conn.close()
        except Exception:
            pass

        found = None
        for u in list(self.users):
            if u.get('username') == identifier or u.get('email') == identifier:
                found = u
                break

        if not found:
            return False, 'User not found'

        try:
            self.users.remove(found)
            self.save_users(self.users)
            return True, f"User {found.get('username')} deleted (local)"
        except Exception as e:
            return False, f'Local delete failed: {e}'

