import json
import os
import re
from typing import Dict, List, Optional, Tuple

USERS_FILE = 'users.json'
BAD_WORDS = {'bad', 'inappropriate', 'spam'}  # Extend as needed

class AuthHandler:
    def __init__(self, users_file: str = USERS_FILE):
        self.users_file = users_file
        self.users: List[Dict] = self.load_users()
    
    def load_users(self) -> List[Dict]:
        if not os.path.exists(self.users_file):
            # Create default admin
            default_users = {
                'users': [
                    {
                        'username': 'admin',
                        'email': 'admin@hotel.com',
                        'password': 'Admin@123',  # Same as DB for consistency
                        'role': 'admin',
                        'name': 'Hotel Admin',
                        'phone': '09000000000'
                    }
                ]
            }
            self.save_users(default_users['users'])
            return default_users['users']
        try:
            with open(self.users_file, 'r') as f:
                data = json.load(f)
                return data.get('users', [])
        except:
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
        return True, phone  # Returns cleaned phone
    
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
        
        # Save as customer
        user = {
            'username': username,
            'email': email,
            'password': password,  # TODO: hash in prod
            'role': 'customer',
            'name': name,
            'phone': cleaned_phone
        }
        self.users.append(user)
        self.save_users(self.users)
        return True, 'Registered! Logged in as customer.'
    
    def login(self, username: str, password: str) -> Optional[Dict]:
        for user in self.users:
            if user['username'] == username and user['password'] == password:
                return user
        return None

